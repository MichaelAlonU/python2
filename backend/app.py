from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # מאפשר CORS לכל המקורות
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'  # קובץ SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# יצירת DB
db = SQLAlchemy(app)

# מודל של טבלה
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(200))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

# יצירת הטבלה בפועל אם היא לא קיימת
with app.app_context():
    db.create_all()

# נתיב להוספת רשומה
@app.route('/items', methods=['POST'])
def add_item():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Missing 'name' field"}), 400
    
    item = Item(name=data['name'], description=data.get('description', ''))
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201

# נתיב להצגת כל הרשומות
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([item.to_dict() for item in items])

@app.route('/')
def health():
    return {"status": "ok"}

if __name__ == '__main__':
    app.run(debug=True)
