import { Component, signal } from '@angular/core';
import { DatePipe } from '@angular/common';

export interface Appointment {
  id: string;
  customerName: string;
  request: string;
  scheduledAt: Date;
  status: 'pending' | 'confirmed' | 'cancelled';
}

@Component({
  selector: 'app-appointment-list',
  imports: [DatePipe],
  templateUrl: './appointment-list.html',
  styleUrl: './appointment-list.scss',
})
export class AppointmentList {
  // Placeholder data — replace with real API service
  appointments = signal<Appointment[]>([
    {
      id: '1',
      customerName: 'Alice Martin',
      request: 'Dentist appointment next Tuesday afternoon',
      scheduledAt: new Date('2026-05-27T14:00:00'),
      status: 'confirmed',
    },
    {
      id: '2',
      customerName: 'Bob Dupont',
      request: 'General check-up, any morning slot this week',
      scheduledAt: new Date('2026-05-26T09:30:00'),
      status: 'pending',
    },
    {
      id: '3',
      customerName: 'Claire Petit',
      request: 'Follow-up consultation for back pain',
      scheduledAt: new Date('2026-05-28T11:00:00'),
      status: 'cancelled',
    },
  ]);
}
