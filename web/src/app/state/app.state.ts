import {Injectable} from '@angular/core';
import {SafeResourceUrl} from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class AppState {
  private _fields: any[] = [];
  private _imagePreview: SafeResourceUrl = '';
  private _formValues: {[p: string]: any} = [];

  get fields(): any[] {
    return this._fields;
  }

  set fields(value: any[]) {
    this._fields = value;
  }

  get imagePreview(): SafeResourceUrl {
    return this._imagePreview;
  }

  set imagePreview(value: SafeResourceUrl) {
    this._imagePreview = value;
  }

  get formValues(): {[p: string]: any} {
    return this._formValues;
  }

  set formValues(values: {[p: string]: any}) {
    this._formValues = values;
  }

  reset() {
    this._imagePreview = '';
    this._fields = [];
    this._formValues = [];
  }
}
