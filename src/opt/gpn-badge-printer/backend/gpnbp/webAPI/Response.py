class Response:
    class Badge:
        class PreviewResponse:
            class Field:
                name: str
                value: str

            image: str
            fields: list[Field]

        class DefinitionResponse:
            class Field:
                name: str
                value: str
                description: str

            width: int
            height: int
            fields: list[Field]
            ticket_code_enabled: bool

    class Printer:
        class Status:
            printer_name: str
            printer_state: int
            printer_state_message: str
            printer_state_reasons: list[str]

        class Job:
            jobid: int

        class JobStatus:
            jobid: int
            number_of_documents: int
            time_at_completed: int
            time_at_creation: int
            time_at_processing: int
            job_state: int
            job_state_reason: str
            job_printer_state_message: str
            job_printer_state_reasons: list[str]

    class Ticket:
        class Response:
            class Field:
                name: str
                value: str

            ticket_code: str
            fields: list[Field]

    class Error:
        code: int
        message: str
