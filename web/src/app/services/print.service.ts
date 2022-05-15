import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {AppState} from '../state/app.state';

@Injectable({
  providedIn: 'root'
})
export class PrintService {

  constructor(private http: HttpClient, private state: AppState) {
  }

  print() {
    return this.http.post<PrintJob>(`${environment.apiEndpoint}/badge/print`, {
      'show_background': false,
      'show_margins': false,
      'fields': this.state.fields,
    });
  }

  printJobFinished(id: number) {
    return this.http.get<JobState>(`${environment.apiEndpoint}/printer/job/${id}`);
  }
}

type PrintJob = {
  jobid: number;
}

type JobState = {
  'jobid': number;
  'number_of_documents': number;
  'time_at_completed': number;
  'time_at_creation': number;
  'time_at_processing': number;
  'job_state': number;
  'job_state_reason': string;
  'job_printer_state_message': string;
  'job_printer_state_reasons': string[];
}
