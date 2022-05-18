import {Injectable} from '@angular/core';
import {FieldsModel} from '../models/fields.model';
import {Form, FormControl, FormGroup} from '@angular/forms';

@Injectable({
  providedIn: 'root'
})
export class FormCreationService {
  constructor() {
  }

  toFormGroup(fields: FieldsModel[]): FormGroup {
    const group: any = {};

    fields.forEach(field => {
      group[field.name] = new FormControl('');
    });

    return new FormGroup(group);
  }
}
