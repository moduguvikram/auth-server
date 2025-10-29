# OAuth2 Authentication Server

A Flask-based OAuth2 authentication server with TOTP (Time-based One-Time Password) support.

## Features

- User registration with TOTP setup
- OAuth2 authorization server with multiple grant types
- Password grant with OTP verification
- Client credentials grant
- Protected resource endpoints
- QR code generation for TOTP setup

## Prerequisites

- Python 3.12+
- Poetry package manager

## Installation

```bash
poetry install
```

## Running the Server

### Local Development
```bash
python api/app.py
```

### Vercel Deployment
The project is configured for Vercel deployment with `vercel.json`.

## API Workflows

### Password Grant Flow (User Authentication)

**1. Register User**
```bash
curl -X POST http://localhost:5000/register_user \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'
```
Response:
```json
{
  "message": "User registered",
  "otp_uri": "otpauth://totp/ThisOAuthServer:testuser?secret=..."
}
```
Scan the `otp_uri` QR code with Google Authenticator.

**2. Verify OTP**
```bash
curl -X POST http://localhost:5000/verify_otp \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","code":"123456"}'
```
Response:
```json
{"valid": true}
```

**3. Create OAuth2 Client**
```bash
curl -X POST http://localhost:5000/create_client \
  -H "Content-Type: application/json" \
  -d '{"client_name":"UserApp","redirect_uri":"http://localhost:3000/callback"}'
```
Response:
```json
{
  "client_id": "4R0o9atlUvUvAWhNNihPSsLN",
  "client_secret": "J3oq2uHDGdJQbz7zlwjOSnECYqplEXj34eH3SCOzK0liV4kO"
}
```

**4. Get Access Token (Password Grant)**
```bash
curl -X POST http://localhost:5000/token \
  -u "4R0o9atlUvUvAWhNNihPSsLN:J3oq2uHDGdJQbz7zlwjOSnECYqplEXj34eH3SCOzK0liV4kO" \
  -d "grant_type=password&username=testuser&password=password123"
```
Response:
```json
{
  "access_token": "MTV3IBXhMhrs6RnKAx6jJ0wgXZN1ooq5pbXHI7F2YE",
  "expires_in": 864000,
  "refresh_token": "g67yHraHSKeShhelY8VVjfcjEDwx9iAbAcBbdno1nDvsV5KU",
  "token_type": "Bearer"
}
```

**5. Access Protected Resource**
```bash
curl http://localhost:5000/profile \
  -H "Authorization: Bearer MTV3IBXhMhrs6RnKAx6jJ0wgXZN1ooq5pbXHI7F2YE"
```
Response:
```json
{
  "type": "user",
  "username": "testuser",
  "otp_verified": true
}
```

### Client Credentials Flow (Machine-to-Machine)

**1. Create OAuth2 Client**
```bash
curl -X POST http://localhost:5000/create_client \
  -H "Content-Type: application/json" \
  -d '{"client_name":"ServiceApp","redirect_uri":"https://localhost/callback"}'
```
Response:
```json
{
  "client_id": "fZ4AqsZFTgMNvfIzaCPutJuB",
  "client_secret": "F7N6SSm2ipEQOrfwEThDfbzW1R0kia5qy55ZR77ofsvJnEaC"
}
```

**2. Get Access Token (Client Credentials)**
```bash
curl -X POST http://localhost:5000/token \
  -u "fZ4AqsZFTgMNvfIzaCPutJuB:F7N6SSm2ipEQOrfwEThDfbzW1R0kia5qy55ZR77ofsvJnEaC" \
  -d "grant_type=client_credentials&scope=profile"
```
Response:
```json
{
  "access_token": "GPSlmILLMF3W1GMNyVqJN4GSnwmuiKr02zbT4iaZ1f",
  "expires_in": 864000,
  "scope": "profile",
  "token_type": "Bearer"
}
```

**3. Access Protected Resource**
```bash
curl http://localhost:5000/profile \
  -H "Authorization: Bearer GPSlmILLMF3W1GMNyVqJN4GSnwmuiKr02zbT4iaZ1f"
```
Response:
```json
{
  "type": "client",
  "client_id": "fZ4AqsZFTgMNvfIzaCPutJuB",
  "message": "Machine token access"
}
```

## Project Structure

```
auth-server/
├── api/
│   ├── app.py          # Main Flask application
│   ├── models.py       # Database models
│   └── index.py        # Vercel handler
├── static/qrcodes/     # Generated QR codes
├── pyproject.toml      # Project dependencies
└── vercel.json         # Vercel deployment config
```

## Database Models

- **User**: Username, password, OTP secret, verification status
- **OAuth2Client**: Client credentials and metadata
- **OAuth2Token**: Access and refresh tokens

## Security Features

- Password hashing with Werkzeug
- TOTP-based two-factor authentication
- OAuth2 token-based authorization
- Secure token validation

## Dependencies

- Flask: Web framework
- SQLAlchemy: Database ORM
- Authlib: OAuth2 implementation
- PyOTP: TOTP generation
- QRCode: QR code generation
- Mangum: ASGI adapter for serverless deployment