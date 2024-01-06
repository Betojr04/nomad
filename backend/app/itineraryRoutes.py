from flask import Blueprint, jsonify, request
from app.models import db, User, Itinerary
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

itinerary = Blueprint('itinerary', __name__)

# ROUTE FOR CREATING AN ITINERARY
@itinerary.route('/create-itinerary', methods=['POST'])
@jwt_required()
def create_itinerary():
    """
    Endpoint to create a new itinerary. This route validates the input data,
    creates a new itinerary record, and saves it to the database.
    
    Validations include checking required fields and ensuring correct data formats.
    In case of database errors, the transaction is rolled back to maintain integrity.
    """
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
            # Validate and parse the date-time string
            time_of_event = datetime.strptime(time_of_event, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid time of event format'}), 400

    # Additional field validations omitted for brevity

    try:
        new_itinerary = Itinerary(
            user_id=current_user_id,
            itinerary_name=itinerary_name,
            time_of_event=time_of_event,
            # Other fields omitted for brevity
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

# ROUTE FOR GETTING AN ITINERARY
@itinerary.route('/itineraries', methods=['GET'])
@jwt_required()
def get_itinerary():
    """
    Endpoint for retrieving an itinerary. Supports fetching by ID or name.
    The query adjusts based on the provided parameter. If no itinerary is found,
    it responds with an error.
    """
    current_user = get_jwt_identity()
    itinerary_id = request.args.get('id')
    itinerary_name = request.args.get('name')

    query = Itinerary.query.filter_by(user_id=current_user)
    
    if itinerary_id:
        query = query.filter_by(id=itinerary_id)
    elif itinerary_name:
        query = query.filter(Itinerary.itinerary_name.ilike(f'%{itinerary_name}%'))

    itinerary = query.first()

    if itinerary is None:
        return jsonify({'error': 'Itinerary not found'}), 404

    return jsonify(itinerary.serialize()), 200
