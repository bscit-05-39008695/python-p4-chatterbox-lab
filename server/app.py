from flask import Flask, request, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message
from flask import jsonify


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at.asc()).all()
    return make_response(
        jsonify([message.to_dict() for message in messages]),  # Add jsonify
        200
    )

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    
    new_message = Message(
        body=data.get('body'),
        username=data.get('username')
    )
    
    db.session.add(new_message)
    db.session.commit()
    
    return make_response(
        new_message.to_dict(),
        200
    )

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.filter_by(id=id).first()
    
    if not message:
        return make_response(
            {'error': 'Message not found'},
            400
        )
    
    data = request.get_json()
    for attr in data:
        setattr(message, attr, data[attr])
    
    db.session.commit()
    
    return make_response(
        message.to_dict(),
        200
    )

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.filter_by(id=id).first()
    
    if not message:
        return make_response(
            {'error': 'Message not found'},
            400
        )
    
    db.session.delete(message)
    db.session.commit()
    
    return make_response('', 200)

if __name__ == '__main__':
    app.run(port=5555, debug=True)