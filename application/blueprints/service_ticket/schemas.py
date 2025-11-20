from application.extensions import ma
from application.models import ServiceTicket
from marshmallow import fields


class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket
        include_fk = True
        load_instance = False
        dump_only = ("customer", "mechanics")
        unknown = "exclude"

    customer = fields.Nested("CustomerSchema", exclude=("service_tickets",), dump_only=True)
    mechanics = fields.List(fields.Nested("MechanicSchema", exclude=("tickets",)), dump_only=True)

service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)
