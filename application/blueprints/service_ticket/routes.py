from flask import request, jsonify
from application.extensions import db
from application.models import ServiceTicket, Customer, Mechanic
from sqlalchemy import select
from marshmallow import ValidationError
from .schemas import service_ticket_schema, service_tickets_schema
from . import ticket_bp

# TICKET ROUTES
# Pass in all the required information to create the service_ticket
@ticket_bp.route("", methods=["POST"])
def create_service_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, ticket_data["customer_id"])
    if not customer:
        return jsonify({"error": "Customer not found."}), 404
    
    new_ticket = ServiceTicket(**ticket_data)
    
    db.session.add(new_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_ticket), 201

# Add a relationship between a service ticket and the mechanics.
@ticket_bp.route("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>", methods=["PUT"])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic in ticket.mechanics:
        return jsonify({"message": "Mechanic already assigned to this ticket."}), 200
    
    ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(ticket), 200

# Remove the relationship from the service ticket and the mechanic.
@ticket_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=["PUT"])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Service ticket not found."}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"error": "Mechanic not found."}), 404
    
    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic is not assigned to this ticket."}), 400
    
    ticket.mechanics.remove(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(ticket), 200

# Get all service tickets
@ticket_bp.route("", methods=["GET"])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(tickets), 200
