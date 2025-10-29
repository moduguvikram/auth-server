import json
import os
from typing import Dict, List, Optional

# Simple file-based storage for Vercel
DATA_DIR = '/tmp'

def save_data(filename: str, data: dict):
    filepath = os.path.join(DATA_DIR, f"{filename}.json")
    with open(filepath, 'w') as f:
        json.dump(data, f)

def load_data(filename: str) -> dict:
    filepath = os.path.join(DATA_DIR, f"{filename}.json")
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return json.load(f)
    return {}

def save_user(username: str, password_hash: str, otp_secret: str, otp_verified: bool = False):
    users = load_data('users')
    users[username] = {
        'password_hash': password_hash,
        'otp_secret': otp_secret,
        'otp_verified': otp_verified
    }
    save_data('users', users)

def get_user(username: str) -> Optional[dict]:
    users = load_data('users')
    return users.get(username)

def update_user_otp_verified(username: str, verified: bool):
    users = load_data('users')
    if username in users:
        users[username]['otp_verified'] = verified
        save_data('users', users)

def save_client(client_id: str, client_secret: str, client_name: str, redirect_uri: str):
    clients = load_data('clients')
    clients[client_id] = {
        'client_secret': client_secret,
        'client_name': client_name,
        'redirect_uri': redirect_uri
    }
    save_data('clients', clients)

def get_client(client_id: str) -> Optional[dict]:
    clients = load_data('clients')
    return clients.get(client_id)

def save_token(access_token: str, client_id: str, username: str = None, expires_in: int = 3600):
    tokens = load_data('tokens')
    tokens[access_token] = {
        'client_id': client_id,
        'username': username,
        'expires_in': expires_in
    }
    save_data('tokens', tokens)

def get_token(access_token: str) -> Optional[dict]:
    tokens = load_data('tokens')
    return tokens.get(access_token)