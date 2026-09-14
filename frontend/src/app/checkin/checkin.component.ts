import { Component } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { CheckinService } from '../checkin.service'
import { Checkin } from '../checkin.service';

@Component({
  selector: 'app-check-in',
  templateUrl: './checkin.component.html',
  styleUrls: ['./checkin.component.css']
})
export class CheckInComponent {

  form = this.formBuilder.group({
    pid: '',
  });

  message: string = "";

  constructor(
    private checkinService: CheckinService,
    private formBuilder: FormBuilder,
  ) {}

  onSubmit(): void {
    let form = this.form.value;
    let pid = parseInt(form.pid ?? "");

    this.checkinService
      .checkinUser(pid)
      .subscribe({
        next: (checkin) => this.onSuccess(checkin),
        error: (err) => this.onError(err)
      });
  }

  private onSuccess(checkin: Checkin): void {
    this.message = `Thanks for checking in: ${checkin.user.first_name} ${checkin.user.last_name}`;
    this.form.reset();
  }

  private onError(err: Error) {
    if (err.message) {
      this.message = err.message;
    } else {
      this.message = "Unknown error: " + JSON.stringify(err);
    }
  }
}