import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';

interface Message {
  role: 'user' | 'assistant';
  text: string;
}

@Component({
  selector: 'app-scheduling-prompt',
  imports: [FormsModule],
  templateUrl: './scheduling-prompt.html',
  styleUrl: './scheduling-prompt.scss',
})
export class SchedulingPrompt {
  prompt = '';
  messages = signal<Message[]>([]);
  loading = signal(false);

  send(): void {
    const text = this.prompt.trim();
    if (!text) return;

    this.messages.update(msgs => [...msgs, { role: 'user', text }]);
    this.prompt = '';
    this.loading.set(true);

    // Placeholder: replace with real API call
    setTimeout(() => {
      this.messages.update(msgs => [
        ...msgs,
        { role: 'assistant', text: 'Your appointment request has been received. We will confirm shortly.' },
      ]);
      this.loading.set(false);
    }, 800);
  }

  onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.send();
    }
  }
}
