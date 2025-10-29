import json
import secrets
import string

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(request.body)
        client_name = data.get('client_name')
        redirect_uri = data.get('redirect_uri')
        
        if not client_name or not redirect_uri:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Client name and redirect URI required'})
            }
        
        # Generate client credentials
        client_id = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(24))
        client_secret = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(48))
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'client_id': client_id,
                'client_secret': client_secret
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }