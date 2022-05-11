class Request:
    class Badge:
        class Request:
            class Field:
                name: str
                value: str

            show_background: bool = False
            show_margins: bool = False
            fields: list[Field]

    class Ticket:
        class Request:
            ticket_code: str
