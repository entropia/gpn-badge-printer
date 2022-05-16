import {Component, OnInit} from '@angular/core';
import {PrintService} from '../../services/print.service';
import {ConfirmationService} from 'primeng/api';
import {interval, mergeMap} from 'rxjs';
import {Router} from '@angular/router';

@Component({
  templateUrl: 'print.component.html',
  styleUrls: [],
})
export class PrintComponent implements OnInit {
  isSecondPrint: boolean = false;

  constructor(private confirmationService: ConfirmationService, private printService: PrintService, private router: Router) {
  }

  ngOnInit() {
    this.startPrint();
  }

  startPrint() {
    const pss = this.printService.print().subscribe((printJob) => {
      pss.unsubscribe();
      this.checkPrintProgress(printJob.jobid);
    });
  }

  checkPrintProgress(jobId: number) {
    const ob = interval(5 * 100).pipe(
      mergeMap(() => this.printService.printJobFinished(jobId))
    )
      .subscribe((jobState: any) => {
        if (jobState.time_at_completed > 0) {
          ob.unsubscribe();

          if (this.isSecondPrint) {
            this.goToStart();
          } else {
            this.confirmationService.confirm({
              message: 'You need to turn the paper.',
              header: 'Next step',
              acceptLabel: 'I turned the paper (Enter)',
              rejectLabel: 'Stop printing (Esc)',
              icon: 'pi pi-exclamation-triangle',
              accept: () => {
                this.isSecondPrint = true;
                this.startPrint();
              },
              reject: () => {
                this.goToStart();
              }
            });
          }
        }
        },
        () => {
          this.confirmationService.confirm({
            message: 'Printing did not work',
            header: 'Print failed',
            acceptLabel: 'Try again (Enter)',
            rejectLabel: 'Go back to start (Esc)',
            icon: 'pi pi-exclamation-triangle',
            accept: () => {
              this.startPrint();
            },
            reject: () => {
              this.goToStart();
            }
          });
        });
  }

  private goToStart() {
    this.router.navigate(['/']);
  }
}
