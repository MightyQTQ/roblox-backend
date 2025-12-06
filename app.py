from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/code")
def get_code():
    return jsonify({"code": "12345"})  # Replace with anything you want

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
