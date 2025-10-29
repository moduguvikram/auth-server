from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Get Authorization header
            auth_header = self.headers.get('Authorization', '')
            
            if not auth_header.startswith('Bearer '):
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing or invalid authorization header'}).encode())
                return
            
            access_token = auth_header[7:]  # Remove 'Bearer ' prefix
            
            if not access_token:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Missing access token'}).encode())
                return
            
            # For demo purposes, return mock profile data
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'type': 'user',
                'username': 'demo_user',
                'otp_verified': True,
                'message': 'Profile access successful'
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())