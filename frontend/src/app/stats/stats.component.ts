import { Component } from '@angular/core';
import { Observable } from 'rxjs';
import { RegistrationService } from '../registration.service';
import { User } from '../user';
import { CheckinService } from '../checkin.service';
import { DeleteUserService } from '../delete-user.service'

export interface Checkin {
  user: User;
  created_at: Date;
}

@Component({
  selector: 'app-stats',
  templateUrl: './stats.component.html',
  styleUrls: ['./stats.component.css']
})
export class StatsComponent {

  public users$: Observable<User[]>;
  public checkins$: Observable<Checkin[]>;

  constructor(private registrationService: RegistrationService, private checkinService: CheckinService, private deleteUserService: DeleteUserService ) {
    this.users$ = this.registrationService.getUsers();
    this.checkins$ = this.checkinService.getCheckins();
  }

  deleteUser(pid: number) {
    // Call the delete user service to initiate user deletion
    this.deleteUserService.deleteRegisteredUser(pid).subscribe(() => {
      // After deletion succeeds, reinitialize the observables
      this.users$ = this.registrationService.getUsers();
      this.checkins$ = this.checkinService.getCheckins();
    });
  }
}

