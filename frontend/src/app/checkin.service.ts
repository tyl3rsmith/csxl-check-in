import { Injectable } from '@angular/core';
import { Observable, throwError, of } from 'rxjs';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { User } from './user';
import { map, catchError } from 'rxjs/operators';

export interface CheckinRequest {
  pid: number;
}

export interface Checkin {
  user: User;
  created_at: Date;
}

@Injectable({
  providedIn: 'root'
}) 
export class CheckinService {

  checkIns: any[] = [];

  constructor(private http: HttpClient) { }
  getCheckins(): Observable<Checkin[]> {
    return this.http.get<Checkin[]>("/api/checkin").pipe(
      map((checkins: Checkin[]) => {
        return checkins.map(checkin => {
          checkin.created_at = new Date(checkin.created_at);
          return checkin;
      });
    })
    );
  }


  checkinUser(checkInPID: number): Observable<Checkin> {
    let checkin: CheckinRequest = {pid: checkInPID}

    let errors: string[] = []
    if (checkInPID.toString().length !== 9) {
      errors.push(`Invalid PID length: ${checkInPID}`)
    }

    if (errors.length > 0) {
      return throwError(() => { return new Error(errors.join("\n")) });
    }

    return this.http.post<Checkin>("/api/checkin", checkin).pipe(
      catchError((error: HttpErrorResponse) => {
        const errorMessage = error.error.detail;
        return throwError(() => new Error(errorMessage));
      })
    );
  }
}
