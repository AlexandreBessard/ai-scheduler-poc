import { Component, OnInit, signal, inject } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

interface ChatResponse {
  message: string;
  thread_id: string;
}

@Component({
  selector: 'app-scheduling-prompt',
  imports: [FormsModule],
  templateUrl: './scheduling-prompt.html',
  styleUrl: './scheduling-prompt.scss',
})
export class SchedulingPrompt implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000';

  readonly threadId = crypto.randomUUID();

  prompt = '';
  messages = signal<Message[]>([]);
  loading = signal(false);

  ngOnInit(): void {
    this.sendMessage('hello');
  }

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

  private sendMessage(text: string): void {
    this.messages.update(msgs => [...msgs, { role: 'user', text }]);
    this.loading.set(true);

    this.http.post<ChatResponse>(`${this.apiUrl}/chat`, { message: text, thread_id: this.threadId })
      .subscribe({
        next: (res) => {
          this.messages.update(msgs => [...msgs, { role: 'assistant', text: res.message }]);
          this.loading.set(false);
        },
        error: () => {
          this.messages.update(msgs => [...msgs, { role: 'assistant', text: 'Could not reach the server. Make sure the backend is running.' }]);
          this.loading.set(false);
        },
      });
  }
}
