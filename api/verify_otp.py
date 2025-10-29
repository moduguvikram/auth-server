import json
import pyotp

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        code = data.get('code')
        
        if not username or not code:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Username and code required'})
            }
        
        # For demo purposes, using a fixed secret
        # In production, retrieve from database
        otp_secret = "JBSWY3DPEHPK3PXP"  # Example secret
        
        totp = pyotp.TOTP(otp_secret)
        if totp.verify(code):
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'valid': True})
            }
        else:
            return {
                'statusCode': 401,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'valid': False})
            }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }