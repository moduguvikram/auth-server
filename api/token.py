from http.server import BaseHTTPRequestHandler
import json
import secrets
import string
import base64

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            body = post_data.decode('utf-8')
            
            # Parse form-encoded data
            params = {}
            for param in body.split('&'):
                if '=' in param:
                    key, value = param.split('=', 1)
                    params[key] = value
            
            grant_type = params.get('grant_type')
            
            if grant_type == 'password':
                username = params.get('username')
                password = params.get('password')
                
                if not username or not password:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Username and password required'}).encode())
                    return
                
                # Generate access token
                access_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
                refresh_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600,
                    'refresh_token': refresh_token
                }
                self.wfile.write(json.dumps(response).encode())
                
            elif grant_type == 'client_credentials':
                # Generate access token for client credentials
                access_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = {
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600,
                    'scope': 'profile'
                }
                self.wfile.write(json.dumps(response).encode())
            
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unsupported grant type'}).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())