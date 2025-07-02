Cafe API Web App
================

📖 Project Description:
-----------------------
Cafe API is a simple Flask-based web app that lets users manage a list of cafes. You can view all cafes, search by location, add new cafes using a form, update coffee prices, and delete cafes using an API key. It's a great starter project for learning REST APIs, Flask, and database integration with SQLAlchemy.

-----------------------------
🛠️ Features:
-----------------------------
- Get a random cafe
- Get all cafes
- Search cafes by location
- Add new cafes via form or POST request
- Update the coffee price
- Delete a cafe using API key

-----------------------------
📁 Project Structure:
-----------------------------
```
- main.py            --> Main Flask application
- templates/
  ├── index.html     --> Homepage listing API endpoints
  └── add_cafe.html  --> Form to add new cafes
- cafes.db           --> SQLite database (auto-created)
```
-----------------------------
📡 API Endpoints:
-----------------------------
```
GET     /random                     -> Get a random cafe
GET     /all                        -> Get all cafes
GET     /search?loc=<location>      -> Search for cafes by location
GET     /all/<int:id>               -> Get a cafe by its ID
POST    /add                        -> Add a new cafe (via form or POST data)
PATCH   /update-price/<id>?new_price=<price>    -> Update cafe price
DELETE  /report-closed/<id>?api-key=YOUR_API_KEY -> Delete a cafe (requires API key)
```
```
🔑 Default API key: mithildabhi_api_key
```
-----------------------------
🌐 Web Interface:
-----------------------------
- Home:
```
http://localhost:5000/
```
- Add Cafe:
```
http://localhost:5000/add
```
-----------------------------
▶️ Getting Started:
-----------------------------
1. Clone the repository
```
   git clone https://github.com/yourusername/cafe-api.git
   cd cafe-api
```
2. Install dependencies
```
   pip install flask flask_sqlalchemy
```
3. Run the server
```
   python main.py
```
4. Open your browser and go to http://localhost:5000/

-----------------------------
📌 Notes:
-----------------------------
- Database is created automatically if it doesn't exist.
- Can be tested using browser or tools like Postman/Insomnia.
- JSON responses follow consistent structure.

-----------------------------
👨‍💻 Author:
-----------------------------
Created by Mithil Dabhi
