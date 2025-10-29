import json
import pyotp
import hashlib
from http.server import BaseHTTPRequestHandler
from .storage import save_user, get_user

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Username and password required'}).encode())
                return
            
            # Check if user already exists
            if get_user(username):
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'User already exists'}).encode())
                return
            
            # Generate OTP secret and hash password
            otp_secret = pyotp.random_base32()
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            
            # Save user to storage
            save_user(username, password_hash, otp_secret)
            
            # Create OTP URI
            otp_uri = pyotp.TOTP(otp_secret).provisioning_uri(
                name=username, 
                issuer_name="ThisOAuthServer"
            )
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'message': 'User registered',
                'otp_uri': otp_uri
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())