from flask import Flask, request, jsonify
from agent import run_agent

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    return jsonify({"response": run_agent(user_msg)})

if __name__ == "__main__":
    app.run(debug=True)
