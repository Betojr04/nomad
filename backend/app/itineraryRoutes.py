from flask import Blueprint, jsonify, request
from app.models import db, User, Itinerary
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token

itinerary = Blueprint('itinerary', __name__)

@itinerary.route('/create-itinerary', methods=['POST'])
@jwt_required()
def create_itinerary():
    current_user_id = get_jwt_identity()  # Assuming the JWT contains the user_id
    data = request.json

    new_itinerary = Itinerary(
        user_id=current_user_id,
        itinerary_name=data.get('itinerary_name'),
        # Add other fields as provided in the request
        # For events, you may need additional logic if they are complex
    )

    db.session.add(new_itinerary)
    try:
        db.session.commit()
        return jsonify({"message": "Itinerary created successfully", "itinerary": new_itinerary.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500