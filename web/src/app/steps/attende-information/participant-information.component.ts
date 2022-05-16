import {AfterViewInit, Component, OnInit} from '@angular/core';
import {InfoService} from '../../services/info.service';
import {PreviewService} from '../../services/preview.service';
import {FormCreationService} from '../../services/form-creation.service';
import {DomSanitizer} from '@angular/platform-browser';
import {FormGroup} from '@angular/forms';
import {AppState} from '../../state/app.state';
import {Router} from '@angular/router';
import {TicketService} from '../../services/ticket.service';
import {MessageService} from 'primeng/api';
import {Direction} from '../../components/shortcut/shortcut.component';
import {tick} from '@angular/core/testing';

@Component({
  templateUrl: 'participant-information.component.html',
  styleUrls: []
})
export class ParticipantInformationComponent implements OnInit, AfterViewInit {
  form!: FormGroup;
  fields: any[] = [];

  Direction = Direction;

  constructor(
    private infoService: InfoService,
    private previewService: PreviewService,
    private ticketService: TicketService,
    private formCreationService: FormCreationService,
    private sanitizer: DomSanitizer,
    private state: AppState,
    private router: Router,
    private messageService: MessageService,
  ) {
  }

  ngOnInit() {
    this.state.reset();
    this.getFields();
  }

  ngAfterViewInit() {
    document.getElementsByTagName('input')[0].focus();
  }

  getFields() {
    this.infoService.getFields().subscribe((fields) => {
      this.fields = fields;
      this.form = this.formCreationService.toFormGroup(fields);
    });
  }

  sendData() {
    this.previewService.getPreview(this.form.value).subscribe((preview) => {
      this.state.fields = preview.fields;
      this.state.imagePreview = this.sanitizer.bypassSecurityTrustResourceUrl(preview.image);

      this.router.navigate(['preview']);
    });
  }

  getTicketInformation(data: any) {
    const tss = this.ticketService.getParticipantByTicketCode(data.target?.value).subscribe(
      (ticket) => {
        tss.unsubscribe();
        Object.keys(this.form.controls).forEach((ctrl) => {
          if (ticket.fields.hasOwnProperty(ctrl)) {
            this.form.controls[ctrl].setValue(ticket.fields[ctrl]);
          }
        });

        document.getElementsByTagName('input')[1].focus();
      },
      () => {
        this.messageService.add({severity: 'error', summary: 'Ticket not found'})
      }
    );
  }
}
