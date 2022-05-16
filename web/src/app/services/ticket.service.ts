import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TicketService {
  constructor(private http: HttpClient) {
  }

  getParticipantByTicketCode(code: string): Observable<Ticket> {
    return this.http.get<Ticket>(`${environment.apiEndpoint}/ticket/${code}`);
  }
}

type Ticket = {
  fields: any;
}
