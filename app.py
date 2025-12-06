# app.py - allow ?u= or ?username=
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

def check_with_roblox(name):
    url = "https://auth.roblox.com/v1/usernames/validate"
    params = {
        "request.username": name,
        "request.birthday": "2000-01-01"
    }
    r = requests.get(url, params=params, timeout=4)
    data = r.json()
    return data.get("code") == 0, data

@app.route("/check", methods=["GET","POST"])
def check():
    # Accept both ?u= and ?username= and JSON POST {"usernames": []} optionally
    name = request.args.get("u") or request.args.get("username")
    if request.method == "POST" and not name:
        body = request.get_json(silent=True) or {}
        names = body.get("usernames")
        if isinstance(names, list) and names:
            out = {}
            for n in names[:50]:
                ok, raw = check_with_roblox(n)
                out[n] = {"available": ok, "raw": raw}
            return jsonify(out)
        return jsonify({"error":"missing usernames"}), 400

    if not name:
        return jsonify({"error":"missing username parameter (use u or username)"}), 400

    ok, raw = check_with_roblox(name)
    return jsonify({"username": name, "available": ok, "raw": raw})
