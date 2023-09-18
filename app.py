import pangea.exceptions as pe
from pangea.config import PangeaConfig
from pangea.services.authn.authn import AuthN
from pangea.services.authn.models import IDProvider
import psycopg2
from pprint import pprint
from flask import Flask, request, jsonify
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

token = "pts_2cn3xdz64qv54jyyzsoitf3pcylmwgww"
domain = "aws.us.pangea.cloud"
config = PangeaConfig(domain=domain)
authn = AuthN(token, config=config, logger_name="pangea")

conn = psycopg2.connect(database="pangea",
                        host="localhost",
                        user="hackathon",
                        password="password123",
                        port="5432")

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/register', methods=["POST"])
def register():
        data = request.json
        user_email = data["user_email"]
        user_password = data["user_password"]
        try:
            response = authn.user.create(
                email=user_email, authenticator=user_password, id_provider=IDProvider.PASSWORD,
            )
            return jsonify({"status": response.status})
        except pe.PangeaAPIException as e:
            return jsonify({"status": e.response.status})

@app.route('/login', methods=["POST"])
def login():
        data = request.json
        user_email = data["user_email"]
        user_password = data["user_password"]
        try:
            response = authn.user.login.password(email=user_email, password=user_password)
            print(response.status)
            # Save user token to change password
            user_token = response.result.active_token.token
            return jsonify({"status": response.status, "user_token": user_token})
        except pe.PangeaAPIException as e:
            return jsonify({"status": e.response.status})
        
@app.route('/medical', methods = ["POST"])
def medical():
     '''
     [
        {
            expense_name: "",
            expense_price: 0,
            expense_date: ""
        }
     ]
     '''
     data = request.json
     # put on ec2

