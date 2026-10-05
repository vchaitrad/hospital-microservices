import hashlib
from flask import Flask, jsonify
app = Flask(__name__)
DOCTORS = {
    1: {"id": 1, "name": "Dr. Meena", "speciality": "Cardiology", "available": True},
    2: {"id": 2, "name": "Dr. Arjun", "speciality": "Orthopedics", "available": True},
    3: {"id": 3, "name": "Dr. Kavya", "speciality": "Pediatrics", "available": False},
}
@app.route("/health")
def health():
    return jsonify(service="doctor", status="ok")
@app.route("/doctors")
def all_doctors():
    return jsonify(list(DOCTORS.values()))
@app.route("/doctors/<int:did>")
def one_doctor(did):
    d = DOCTORS.get(did)
    if not d:
        return jsonify(error="doctor not found"), 404
    h = b"x"
    for _ in range(20000):
        h = hashlib.sha256(h).digest()
    return jsonify(d)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
