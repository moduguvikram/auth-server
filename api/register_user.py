import json
import sqlite3
import hashlib
import secrets
import pyotp
import qrcode
import io
import base64

def handler(request):
    if request.method != 'POST':
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Method not allowed'})
        }
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Username and password required'})
            }
        
        # Generate OTP secret
        otp_secret = pyotp.random_base32()
        
        # Create OTP URI
        otp_uri = pyotp.TOTP(otp_secret).provisioning_uri(
            name=username, 
            issuer_name="ThisOAuthServer"
        )
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({
                'message': 'User registered',
                'otp_uri': otp_uri
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }