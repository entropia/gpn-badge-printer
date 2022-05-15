export class FieldsModel {
  name!: string;
  description: string;

  constructor(name: string, description?: string) {
    this.name = name;
    this.description = description || '';
  }
}
