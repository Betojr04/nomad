from flask import Blueprint, jsonify, request
from app.models import db, User, Itinerary
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime

itinerary = Blueprint('itinerary', __name__)

"""
ROUTE FOR CREATING AN ITINERARY
"""
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

    itinerary_name = data.get('itinerary_name')
    if not itinerary_name:
        return jsonify({'error': 'Itinerary name is required'}), 400

    time_of_event = data.get('time_of_event')
    if time_of_event:
        try:
            time_of_event = datetime.strptime(time_of_event, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid time of event format'}), 400


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

"""
ROUTE FOR GETTING AN ITINERARY BY ID OR NAME, OR LISTING ALL ITINERARIES
"""
@itinerary.route('/itineraries', methods=['GET'])
@jwt_required()
def get_or_list_itineraries():
    
    """
    Endpoint for retrieving an itinerary. Supports fetching by ID or name or listing all itineraries.
    The query adjusts based on the provided parameter. If no itinerary is found, it will list all of them.
    """
    
    current_user = get_jwt_identity()
    itinerary_id = request.args.get('id')
    itinerary_name = request.args.get('name')

    query = Itinerary.query.filter_by(user_id=current_user)

    # Apply filters if provided
    if itinerary_id:
        query = query.filter_by(id=itinerary_id)
    elif itinerary_name:
        query = query.filter(Itinerary.itinerary_name.ilike(f'%{itinerary_name}%'))

    itineraries = query.all()

    if not itineraries:
        return jsonify({'error': 'No itineraries found'}), 404

    return jsonify([itinerary.serialize() for itinerary in itineraries]), 200


"""
ENDPOINT FOR UPDATING AN ITINERARY
"""
@itinerary.route('/itineraries/update', methods=['PUT'])
@jwt_required()
def update_itinerary():
    current_user = get_jwt_identity()
    data = request.json
    itinerary_id = data.get('id')
    itinerary_name = data.get('name')

    query = Itinerary.query.filter_by(user_id=current_user)
    if itinerary_id:
        query = query.filter_by(id=itinerary_id)
    elif itinerary_name:
        query = query.filter(Itinerary.itinerary_name.ilike(f'%{itinerary_name}%'))

    itinerary = query.first()

    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404

    # Updating fields
    itinerary.itinerary_name = data.get('itinerary_name', itinerary.itinerary_name)

    # Update time of event
    time_of_event = data.get('time_of_event')
    if time_of_event:
        try:
            itinerary.time_of_event = datetime.strptime(time_of_event, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({'error': 'Invalid time of event format'}), 400

    # Update event details
    itinerary.event_name = data.get('event_name', itinerary.event_name)
    itinerary.event_description = data.get('event_description', itinerary.event_description)
    itinerary.event_location = data.get('event_location', itinerary.event_location)
    itinerary.event_address = data.get('event_address', itinerary.event_address)
    itinerary.event_city = data.get('event_city', itinerary.event_city)
    itinerary.event_state = data.get('event_state', itinerary.event_state)

    try:
        db.session.commit()
        return jsonify({'message': 'Itinerary updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500



"""
ENDPOINT FOR DELETING AN ITINERARY
"""
@itinerary.route('/itineraries/delete', methods=['DELETE'])
@jwt_required()
def delete_itinerary():
    current_user = get_jwt_identity()
    data = request.json
    itinerary_id = data.get('id')
    itinerary_name = data.get('name')

    query = Itinerary.query.filter_by(user_id=current_user)
    if itinerary_id:
        query = query.filter_by(id=itinerary_id)
    elif itinerary_name:
        query = query.filter(Itinerary.itinerary_name.ilike(f'%{itinerary_name}%'))

    itinerary = query.first()

    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404

    db.session.delete(itinerary)

    try:
        db.session.commit()
        return jsonify({'message': 'Itinerary deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


# ROUTE FOR SHARE ITINERARY WITHIN THE PLATFORM
@itinerary.route('/itineraries/<int:itinerary_id>/share', methods=['POST'])
@jwt_required()
def share_itinerary(itinerary_id):
    current_user = get_jwt_identity()
    data = request.json()
    recipient_username = data.get('recipient_username')
    
    itinerary = Itinerary.query.filter_by(id=itinerary_id)
    if not itinerary or itinerary_id != current_user:
        return jsonify({'error': 'Itinerary not found or access denied'}), 404   
    
    recipient_username = User.query.filter_by(username=recipient_username).first()
    if not recipient_username:
        return jsonify({'error': 'Recipient user not found'}), 404
    
    itinerary.shared_with.append(recipient_username)
    db.session.commit()
    
    
# ROUTE FOR GENERATING A SHAREABLE LINK FOR AN ITINERARY
@itinerary.route('/itineraries/<int:itinerary_id>/share', methods=['POST'])
@jwt_required()
def share_itinerary(itinerary_id):
    """
    Endpoint to share an itinerary. Supports sharing within the platform and generating a shareable link.
    """
    current_user = get_jwt_identity()
    itinerary = Itinerary.query.filter_by(id=itinerary_id, user_id=current_user).first()

    if itinerary is None:
        return jsonify({'error': 'Itinerary not found'}), 404

    data = request.get_json()
    share_type = data.get('share_type')

    if share_type not in ['platform', 'link']:
        return jsonify({'error': 'Invalid share type'}), 400

    if share_type == 'platform':
        # Logic for sharing within the platform
        # This could involve adding the itinerary to a shared feed, notifying other users, etc.
        pass
    elif share_type == 'link':
        # Generate a shareable link
        shareable_link = f"http://yourapp.com/itineraries/{itinerary_id}"
        return jsonify({'message': 'Itinerary share link generated successfully', 'link': shareable_link}), 200

    return jsonify({'message': 'Itinerary shared successfully'}), 200

    