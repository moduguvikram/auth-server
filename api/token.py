import json
import secrets
import string
import base64

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Parse form data
        body = request.body
        if isinstance(body, bytes):
            body = body.decode('utf-8')
        
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
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Username and password required'})
                }
            
            # Generate access token
            access_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
            refresh_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600,
                    'refresh_token': refresh_token
                })
            }
            
        elif grant_type == 'client_credentials':
            # Generate access token for client credentials
            access_token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(40))
            
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({
                    'access_token': access_token,
                    'token_type': 'Bearer',
                    'expires_in': 3600,
                    'scope': 'profile'
                })
            }
        
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Unsupported grant type'})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }