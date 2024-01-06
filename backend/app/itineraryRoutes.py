from flask import Blueprint, jsonify, request
from app.models import db, User, Itinerary
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

itinerary = Blueprint('itinerary', __name__)


# ROUTE FOR CREATING AN ITINERARY
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

@itinerary.route('/create-itinerary', methods=['POST'])
@jwt_required()
def create_itinerary():
    current_user_id = get_jwt_identity()
    data = request.json

    # Validate required fields
    itinerary_name = data.get('itinerary_name')
    if not itinerary_name:
        return jsonify({'error': 'Itinerary name is required'}), 400

    # Example validations for other fields
    time_of_event = data.get('time_of_event')
    if time_of_event:
        try:
            time_of_event = datetime.strptime(time_of_event, '%Y-%m-%d %H:%M:%S') # Adjust format as per your need
        except ValueError:
            return jsonify({'error': 'Invalid time of event format'}), 400

    event_name = data.get('event_name')
    if not event_name:
        return jsonify({'error': 'Event name is required'}), 400

    event_description = data.get('event_description', '') # Optional field, defaults to empty string
    event_location = data.get('event_location')
    if not event_location:
        return jsonify({'error': 'Event location is required'}), 400

    event_address = data.get('event_address', '') # Optional field, defaults to empty string
    event_city = data.get('event_city', '') # Optional field, defaults to empty string
    event_state = data.get('event_state', '') # Optional field, defaults to empty string

    try:
        new_itinerary = Itinerary(
            user_id=current_user_id,
            itinerary_name=itinerary_name,
            time_of_event=time_of_event,
            event_name=event_name,
            event_description=event_description,
            event_location=event_location,
            event_address=event_address,
            event_city=event_city,
            event_state=event_state
        )
        db.session.add(new_itinerary)
        db.session.commit()
        return jsonify({"message": "Itinerary created successfully", "itinerary": new_itinerary.id}), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': 'Database integrity error: Possibly duplicate or invalid data'}), 400

    except SQLAlchemyError as e:
        db.session.rollback()
        # Optionally log the exception e for debugging
        return jsonify({'error': 'Database error'}), 500

    except Exception as e:
        # Log this exception, as it's unexpected
        return jsonify({'error': 'An unexpected error occurred'}), 500

    """
    THIS IS THE DATA FIELDS NEEDED FOR TESTING THE ROUTE IN POSTMAN, ADJUST AS NEEDED
    
    {
    "itinerary_id": 1,
    "itinerary_name": "Chilangolandia",
    "time_of_event": "2023-03-15T09:00:00",
    "event_name": "Visiting Mexico City",
    "event_description": "Tour of the city",
    "event_location": "La cuidad de chilangos",
    "event_address": "La concha de tu madre ",
    "event_city": "Cuidad de Mex",
    "event_state": "La republica"
}
    """
