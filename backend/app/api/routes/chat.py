import json
from collections import defaultdict
from time import time

from fastapi import APIRouter, Depends, HTTPException, Request
from langchain_core.messages import HumanMessage, ToolMessage

from app.models.appointment import ChatRequest, ChatResponse, PaymentRequest

router = APIRouter()

# Sliding-window rate limiter: max 20 messages per 60 s per thread_id
_RATE_LIMIT = 20
_RATE_WINDOW = 60
_counters: dict[str, list[float]] = defaultdict(list)


def _check_rate_limit(body: ChatRequest) -> ChatRequest:
    now = time()
    cutoff = now - _RATE_WINDOW
    timestamps = _counters[body.thread_id]
    _counters[body.thread_id] = [t for t in timestamps if t > cutoff]
    if len(_counters[body.thread_id]) >= _RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many messages. Please wait before sending again.")
    _counters[body.thread_id].append(now)
    return body


@router.post("/chat", response_model=ChatResponse)
async def chat(body: ChatRequest = Depends(_check_rate_limit), *, request: Request) -> ChatResponse:
    graph = request.app.state.graph
    config = {"configurable": {"thread_id": body.thread_id}, "recursion_limit": 10}
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=body.message)], "thread_id": body.thread_id},
        config=config,
    )
    last = result["messages"][-1]

    payment_request = None
    for msg in result["messages"]:
        if isinstance(msg, ToolMessage) and msg.name == "request_payment":
            try:
                data = json.loads(msg.content)
                if data.get("__payment_request__"):
                    payment_request = PaymentRequest(
                        appointment_id=data["appointment_id"],
                        amount=data["amount"],
                    )
            except (json.JSONDecodeError, KeyError):
                pass

    return ChatResponse(message=last.content, thread_id=body.thread_id, payment_request=payment_request)
