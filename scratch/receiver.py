from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/number', methods=['POST'])
def receive_number():
    data = request.get_json()
    number = data.get("number")
    print(f"Received: {number}")
    return jsonify({"status": "success"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

