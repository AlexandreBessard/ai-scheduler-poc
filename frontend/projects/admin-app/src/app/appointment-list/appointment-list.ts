import { Component, signal, inject, OnInit } from '@angular/core';
import { DatePipe, TitleCasePipe } from '@angular/common';
import { HttpClient } from '@angular/common/http';

export interface Appointment {
  id: string;
  customer_name: string;
  service_type: string;
  stylist_name: string;
  request: string;
  scheduled_at: string;
  duration_minutes: number;
  price: number;
  status: 'pending' | 'confirmed' | 'cancelled';
  payment_status: 'unpaid' | 'paid';
}

@Component({
  selector: 'app-appointment-list',
  imports: [DatePipe, TitleCasePipe],
  templateUrl: './appointment-list.html',
  styleUrl: './appointment-list.scss',
})
export class AppointmentList implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = 'http://localhost:8000';

  appointments = signal<Appointment[]>([]);
  loading = signal(true);
  error = signal<string | null>(null);

  ngOnInit(): void {
    this.http.get<Appointment[]>(`${this.apiUrl}/appointments`).subscribe({
      next: (data) => {
        this.appointments.set(data);
        this.loading.set(false);
      },
      error: () => {
        this.error.set('Could not load appointments. Make sure the backend is running.');
        this.loading.set(false);
      },
    });
  }
}