import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CheckInComponent } from './checkin.component';

describe('CheckinComponent', () => {
  let component: CheckInComponent;
  let fixture: ComponentFixture<CheckInComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CheckInComponent]
    });
    fixture = TestBed.createComponent(CheckInComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});