import random
import os
from flask import Flask, jsonify, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Connect to Database
app.secret_key = 'mithildabhi_api_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)
    
    def to_dict(self):
        """Converts the Cafe object into a dictionary for JSON serialization."""
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
    
def to_boolean(value):
    return str(value).lower() in ['true', 'on', '1']
    
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/random")
def select_random_cafe():
    """Returns a random cafe from the database."""
    cafes = Cafe.query.all()
    if not cafes:
        return jsonify(error={"Not Found": "No cafes available in the database."}), 404
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())

@app.route("/all")
def get_all_cafes():
    all_cafes = db.session.query(Cafe).all()
    if not all_cafes:
        return jsonify(cafes=[]), 200 # Return empty list if no cafes, but still a 200 OK
    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def get_cafe_at_location():
    search_location = request.args.get('loc')
    if not search_location:
        return jsonify(error={"Bad Request": "Please provide a 'loc' parameter for searching."}), 400

    cafes_at_location = Cafe.query.filter(Cafe.location.ilike(f'%{search_location}%')).all()    
    if cafes_at_location:
        return jsonify(cafes=[cafe.to_dict() for cafe in cafes_at_location])
    else:
        return jsonify(error={"Not Found": "Sorry, no cafe found at that location."}), 404
    
    
@app.route("/add", methods=['GET', 'POST'])
def add_cafe():
    if request.method == 'POST':
        new_cafe = Cafe(
            name=request.form.get("name"),
            map_url=request.form.get("map_url"),
            img_url=request.form.get("img_url"),
            location=request.form.get("location"),
            seats=request.form.get("seats"),
            has_toilet=to_boolean(request.form.get("has_toilet", "False")),
            has_wifi=to_boolean(request.form.get("has_wifi", "False")),
            has_sockets=to_boolean(request.form.get("has_sockets", "False")),
            can_take_calls=to_boolean(request.form.get("can_take_calls", "False")),
            coffee_price=request.form.get("coffee_price")
        )
        try:
            db.session.add(new_cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully added the new cafe."}), 201 # 201 Created
        except Exception as e:
            db.session.rollback() # Rollback the session on any error
            if "UNIQUE constraint failed" in str(e):
                return jsonify(error={"message": f"Error adding cafe: A cafe with this name already exists."}), 409 # Conflict
            elif "NOT NULL constraint failed" in str(e):
                return jsonify(error={"message": f"Error adding cafe: A required field was missing or invalid. Details: {str(e)}."}), 400 # Bad Request
            else:
                return jsonify(error={"message": f"An unexpected error occurred: {str(e)}."}), 500 # Internal Server Error
    return render_template("add_cafe.html")

@app.route('/all/<int:post_id>')
def show_post(post_id):
    cafe = Cafe.query.get(post_id)
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={"Not Found": f"No cafe found with id {post_id}."}), 404

@app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
def patch_new_price(cafe_id):
    new_price = request.args.get("new_price")
    cafe = db.session.query(Cafe).get(cafe_id)
    if cafe:
        cafe.coffee_price = new_price
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})
    else:
        return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."})

@app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
def delete_cafe(cafe_id):   
    # Get the API key from the request arguments
    api_key = request.args.get("api-key")

    if api_key == "mithildabhi_api_key":
        cafe_to_delete = db.session.query(Cafe).get(cafe_id)

        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200
        else:
            return jsonify(error={"Not Found": "Sorry, a cafe with that ID was not found in the database."}), 404
    else:
        return jsonify(error={"Forbidden": "Sorry, you're not allowed to do that. Make sure you have the correct api_key."}), 403 # 403 Forbidden status code
@app.route("/api/v1/cafes")
def get_all_cafes_json():
    cafes = Cafe.query.all()
    user = db.get_or_404(user,1)
    
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

if __name__ == '__main__':
    with app.app_context():
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if not os.path.exists(db_path):
            print(f"Creating database file: {db_path}")
            db.create_all()
        else:
            print(f"Database file already exists: {db_path}. Ensuring tables are up-to-date (no changes if already exist).")
            db.create_all()
    app.run()