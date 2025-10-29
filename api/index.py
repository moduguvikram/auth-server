from app import app

# For Vercel deployment
if __name__ == "__main__":
    app.run(debug=True)
else:
    # This is the WSGI application for Vercel
    application = app
