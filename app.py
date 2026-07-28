from flask import Flask, request, jsonify, send_from_directory
import requests
import os
from flask_cors import CORS

app = Flask(__name__, static_folder="public")
CORS(app)

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/search")
def search():
    q = request.args.get("q")
    url = f"https://api.duckduckgo.com/?q={q}&format=json"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        data = r.json()

        results = []
        for topic in data.get("RelatedTopics", []):
            if "Text" in topic and "FirstURL" in topic:
                results.append({
                    "title": topic["Text"],
                    "link": topic["FirstURL"],
                    "snippet": topic["Text"]
                })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
