from flask import Flask, request, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import os
from flask_cors import CORS
CORS(app)

app = Flask(__name__, static_folder="public")

@app.route("/")
def index():
    return send_from_directory("public", "index.html")

@app.route("/search")
def search():
    q = request.args.get("q")
    url = f"https://duckduckgo.com/html/?q={q}"

    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        results = []
        for a in soup.select(".result__a")[:20]:
            results.append({
                "title": a.get_text(),
                "link": a.get("href")
            })

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

