import {Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';
import {environment} from '../../environments/environment';
import {map, Observable} from 'rxjs';
import {FieldsModel} from '../models/fields.model';

@Injectable({
  providedIn: 'root'
})
export class InfoService {

  constructor(private http: HttpClient) {
  }

  getFields(): Observable<FieldsModel[]> {
    return this.http.get(`${environment.apiEndpoint}/badge/info`)
      .pipe(
        map((res: any) => res['fields'])
      );
  }
}
