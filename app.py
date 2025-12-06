from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"status": "online"})

@app.route("/check")
def check_username():
    username = request.args.get("u")
    if not username:
        return jsonify({"error": "No username provided"}), 400

    url = f"https://auth.roblox.com/v1/usernames/validate?request.username={username}&request.birthday=2000-01-01"

    try:
        response = requests.get(url, timeout=3)
        data = response.json()

        return jsonify({
            "username": username,
            "available": (data.get("code") == 0),
            "roblox_response": data
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
