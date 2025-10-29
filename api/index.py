from app import app

# Vercel expects the Flask app to be directly callable
# Flask apps are WSGI applications by default
app = app
