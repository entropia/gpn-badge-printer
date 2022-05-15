import {Injectable} from '@angular/core';
import {SafeResourceUrl} from '@angular/platform-browser';

@Injectable({
  providedIn: 'root'
})
export class AppState {
  private _fields: any[] = [];

  get fields(): any[] {
    return this._fields;
  }

  set fields(value: any[]) {
    this._fields = value;
  }

  private _imagePreview: SafeResourceUrl = '';

  get imagePreview(): SafeResourceUrl {
    return this._imagePreview;
  }

  set imagePreview(value: SafeResourceUrl) {
    this._imagePreview = value;
  }
}
