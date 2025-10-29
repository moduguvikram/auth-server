import json
import secrets
import string
from http.server import BaseHTTPRequestHandler
from .storage import save_client

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            client_name = data.get('client_name')
            redirect_uri = data.get('redirect_uri')
            
            if not client_name or not redirect_uri:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Client name and redirect URI required'}).encode())
                return
            
            # Generate client credentials
            client_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))
            client_secret = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
            
            # Save client to storage
            save_client(client_id, client_secret, client_name, redirect_uri)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = {
                'client_id': client_id,
                'client_secret': client_secret
            }
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())