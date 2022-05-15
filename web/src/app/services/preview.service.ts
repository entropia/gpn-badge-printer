import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {Observable} from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PreviewService {

  constructor(private http: HttpClient) {
  }

  getPreview(value: any): Observable<any> {
    console.log(Object.keys(value));
    let fields: any[] = [];
    Object.keys(value).forEach((key) => {
      fields.push({
        name: key,
        value: value[key]
      });
    });

    return this.http.post(`${environment.apiEndpoint}/badge/preview`, {
      'show_background': true,
      'show_margins': false,
      'fields': fields,
    });
  }
}
