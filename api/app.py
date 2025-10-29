from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from authlib.integrations.flask_oauth2 import AuthorizationServer, ResourceProtector, current_token
from authlib.integrations.sqla_oauth2 import create_query_client_func, create_save_token_func
from werkzeug.security import gen_salt, generate_password_hash, check_password_hash
import pyotp
import qrcode
import os
from authlib.oauth2.rfc6749 import grants
from authlib.oauth2.rfc6750 import BearerTokenValidator

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/dev.db"
app.config["SECRET_KEY"] = "super-secret-change-me"
app.config["OAUTH2_REFRESH_TOKEN_GENERATOR"] = True

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    otp_secret = db.Column(db.String(32), nullable=True)
    otp_verified = db.Column(db.Boolean, default=False)
    
    def get_user_id(self):
        return self.id

class OAuth2Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(48), unique=True, nullable=False)
    client_secret = db.Column(db.String(120), nullable=False)
    client_name = db.Column(db.String(120), nullable=True)
    client_metadata = db.Column(db.Text)
    
    def set_client_metadata(self, metadata):
        import json
        self.client_metadata = json.dumps(metadata)
    
    def get_client_metadata(self):
        import json
        return json.loads(self.client_metadata) if self.client_metadata else {}

class OAuth2Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(48), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    access_token = db.Column(db.String(255), unique=True, nullable=False)
    refresh_token = db.Column(db.String(255))
    expires_in = db.Column(db.Integer, default=3600)
    scope = db.Column(db.Text)
    
    @property
    def user(self):
        return User.query.get(self.user_id) if self.user_id else None

class MyBearerTokenValidator(BearerTokenValidator):
    def authenticate_token(self, token_string):
        return OAuth2Token.query.filter_by(access_token=token_string).first()

    def request_invalid(self, request):
        return False

    def token_revoked(self, token):
        return False

with app.app_context():
    db.create_all()

query_client = create_query_client_func(db.session, OAuth2Client)
save_token = create_save_token_func(db.session, OAuth2Token)
authorization = AuthorizationServer(app, query_client=query_client, save_token=save_token)

require_oauth = ResourceProtector()
require_oauth.register_token_validator(MyBearerTokenValidator())

@app.route("/register_user", methods=["POST"])
def register_user():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if User.query.filter_by(username=username).first():
        return jsonify(error="User already exists"), 400

    otp_secret = pyotp.random_base32()
    user = User(
        username=username,
        password=generate_password_hash(password),
        otp_secret=otp_secret
    )
    db.session.add(user)
    db.session.commit()

    otp_uri = pyotp.TOTP(otp_secret).provisioning_uri(
        name=username, issuer_name="ThisOAuthServer"
    )
    return jsonify(message="User registered", otp_uri=otp_uri)

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    username = data.get("username")
    code = data.get("code")
    user = User.query.filter_by(username=username).first()
    
    if not user:
        return jsonify(error="User not found"), 404

    totp = pyotp.TOTP(user.otp_secret)
    if totp.verify(code):
        user.otp_verified = True
        db.session.commit()
        return jsonify(valid=True)
    return jsonify(valid=False), 401

@app.route("/create_client", methods=["POST"])
def create_client():
    data = request.json
    client_name = data.get("client_name")
    redirect_uri = data.get("redirect_uri")

    client_id = gen_salt(24)
    client_secret = gen_salt(48)
    client = OAuth2Client(
        client_id=client_id,
        client_secret=client_secret,
        client_name=client_name
    )
    client_metadata = {
        "client_name": client_name,
        "grant_types": ["client_credentials", "password"],
        "response_types": ["code"],
        "redirect_uris": [redirect_uri],
        "scope": "profile email",
    }
    client.set_client_metadata(client_metadata)
    db.session.add(client)
    db.session.commit()
    return jsonify(client_id=client_id, client_secret=client_secret)

class PasswordGrant(grants.ResourceOwnerPasswordCredentialsGrant):
    def authenticate_user(self, username, password):
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password) and user.otp_verified:
            return user

authorization.register_grant(PasswordGrant)
authorization.register_grant(grants.ClientCredentialsGrant)

@app.route("/token", methods=["POST"])
def issue_token():
    return authorization.create_token_response()

@app.route("/profile")
@require_oauth()
def profile():
    token = current_token
    if hasattr(token, "user") and token.user:
        return jsonify({
            "type": "user",
            "username": token.user.username,
            "otp_verified": token.user.otp_verified
        })
    return jsonify({"type": "client", "client_id": token.client_id, "message": "Machine token access"})

if __name__ == "__main__":
    app.run(debug=True)