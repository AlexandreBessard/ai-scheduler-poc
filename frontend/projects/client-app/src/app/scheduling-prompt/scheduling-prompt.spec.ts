import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SchedulingPrompt } from './scheduling-prompt';

describe('SchedulingPrompt', () => {
  let component: SchedulingPrompt;
  let fixture: ComponentFixture<SchedulingPrompt>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SchedulingPrompt],
    }).compileComponents();

    fixture = TestBed.createComponent(SchedulingPrompt);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
