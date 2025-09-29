from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)    
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

# ---- routes come AFTER app is created ----
@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([m.to_dict() for m in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    new_msg = Message(body=data['body'], username=data['username'])
    db.session.add(new_msg)
    db.session.commit()
    return jsonify(new_msg.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    msg = db.session.get(Message, id)
    if msg is None:
        abort(404, description="Message not found")
    msg.body = data['body']
    db.session.commit()
    return jsonify(msg.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = db.session.get(Message, id)
    if message is None:
        abort(404, description="Message not found")
    db.session.delete(message)
    db.session.commit()
    return '', 204
