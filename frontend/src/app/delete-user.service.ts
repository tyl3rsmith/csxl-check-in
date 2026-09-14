import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class DeleteUserService {

  constructor(private http: HttpClient) {} 

  deleteRegisteredUser(pid: number): Observable<void> {
    return this.http.delete<void>(`/api/registration/${pid}`);
  }
}
