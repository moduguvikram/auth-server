import json

def handler(request):
    if request.method != 'GET':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        # Get Authorization header
        auth_header = request.headers.get('Authorization', '')
        
        if not auth_header.startswith('Bearer '):
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Missing or invalid authorization header'})
            }
        
        access_token = auth_header[7:]  # Remove 'Bearer ' prefix
        
        if not access_token:
            return {
                'statusCode': 401,
                'body': json.dumps({'error': 'Missing access token'})
            }
        
        # For demo purposes, return mock profile data
        # In production, validate token and return actual user data
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'type': 'user',
                'username': 'demo_user',
                'otp_verified': True,
                'message': 'Profile access successful'
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }