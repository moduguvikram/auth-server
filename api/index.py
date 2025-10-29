from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register_user', methods=['POST'])
def register_user():
    return jsonify(message="User registration endpoint", status="working")

@app.route('/test')
def test():
    return jsonify(message="Test endpoint working")

if __name__ == '__main__':
    app.run(debug=True)