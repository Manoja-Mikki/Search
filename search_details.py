from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    passport_number = db.Column(db.String(10), nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "passport_number": self.passport_number,
            "expiry_date": self.expiry_date.strftime('%Y-%m-%d'),
            "status": self.status
        }

def init_db():
    with app.app_context():
        db.create_all()
        if User.query.count() == 0:
            initial_users = [
                User(id=1, name="Krishna", passport_number="U1743456", expiry_date=datetime.strptime("2030-02-01", "%Y-%m-%d"), status="Active"),
                User(id=2, name="Manoja", passport_number="U1772386", expiry_date=datetime.strptime("2012-10-01", "%Y-%m-%d"), status="Expired"),
                User(id=3, name="Bablu", passport_number="I1743221", expiry_date=datetime.strptime("2024-12-12", "%Y-%m-%d"), status="Active"),
                User(id=4, name="Kim ji won", passport_number="K233548", expiry_date=datetime.strptime("2026-02-01", "%Y-%m-%d"), status="Active"),
                User(id=5, name="Kim soo hyun", passport_number="K389023", expiry_date=datetime.strptime("2024-02-01", "%Y-%m-%d"), status="Expired")
            ]
            db.session.add_all(initial_users)
            db.session.commit()
            print("Data loaded successfully")

@app.route('/users/search', methods=['GET'])
def search_user():
    id_query = request.args.get('id')
    if not id_query:
        return jsonify({"error": "Please provide an id parameter"}), 400

    user = User.query.filter_by(id=id_query).first()
    if user:
        return jsonify(user.to_dict())
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
