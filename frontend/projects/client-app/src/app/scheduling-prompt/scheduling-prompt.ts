import { Component, signal, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { MarkdownComponent } from 'ngx-markdown';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

interface PaymentRequest {
  appointment_id: string;
  amount: number;
}

interface ChatResponse {
  message: string;
  thread_id: string;
  payment_request?: PaymentRequest;
}

@Component({
  selector: 'app-scheduling-prompt',
  imports: [FormsModule, MarkdownComponent],
  templateUrl: './scheduling-prompt.html',
  styleUrl: './scheduling-prompt.scss',
})
export class SchedulingPrompt {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000';

  readonly threadId = crypto.randomUUID();

  prompt = '';
  messages = signal<Message[]>([
    { role: 'assistant', text: "Hello! Welcome to our hair salon. I can help you book a haircut, trim, color, highlights, or blowout. What would you like to schedule?" },
  ]);
  loading = signal(false);

  pendingPayment = signal<PaymentRequest | null>(null);
  paymentLoading = signal(false);
  card = { number: '', expiry: '', cvv: '', name: '' };

  send(): void {
    const text = this.prompt.trim();
    if (!text) return;
    this.prompt = '';
    this.sendMessage(text);
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }

  submitPayment(): void {
    const payment = this.pendingPayment();
    if (!payment) return;
    this.paymentLoading.set(true);

    this.http.post(`${this.apiUrl}/appointments/${payment.appointment_id}/pay`, {})
      .subscribe({
        next: () => {
          this.pendingPayment.set(null);
          this.paymentLoading.set(false);
          this.card = { number: '', expiry: '', cvv: '', name: '' };
          this.messages.update(msgs => [...msgs, {
            role: 'assistant',
            text: `Payment of €${payment.amount.toFixed(2)} confirmed! Your appointment is fully secured.`,
          }]);
        },
        error: () => {
          this.paymentLoading.set(false);
          this.messages.update(msgs => [...msgs, {
            role: 'assistant',
            text: 'Payment could not be processed. Please try again.',
          }]);
        },
      });
  }

  dismissPayment(): void {
    this.pendingPayment.set(null);
    this.card = { number: '', expiry: '', cvv: '', name: '' };
  }

  private sendMessage(text: string): void {
    this.messages.update(msgs => [...msgs, { role: 'user', text }]);
    this.loading.set(true);

    this.http.post<ChatResponse>(`${this.apiUrl}/chat`, { message: text, thread_id: this.threadId })
      .subscribe({
        next: (res) => {
          this.messages.update(msgs => [...msgs, { role: 'assistant', text: res.message }]);
          if (res.payment_request) {
            this.pendingPayment.set(res.payment_request);
          }
          this.loading.set(false);
        },
        error: () => {
          this.messages.update(msgs => [...msgs, { role: 'assistant', text: 'Could not reach the server. Make sure the backend is running.' }]);
          this.loading.set(false);
        },
      });
  }
}
