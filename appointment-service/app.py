import os
import requests
from flask import Flask, jsonify
app = Flask(__name__)
PATIENT_URL = os.getenv("PATIENT_URL", "http://localhost:5001")
DOCTOR_URL = os.getenv("DOCTOR_URL", "http://localhost:5002")
@app.route("/health")
def health():
    return jsonify(service="appointment", status="ok")
@app.route("/book/<int:patient_id>/<int:doctor_id>")
def book(patient_id, doctor_id):
    try:
        p = requests.get(f"{PATIENT_URL}/patients/{patient_id}", timeout=5)
        if p.status_code != 200:
            return jsonify(error="patient not found"), 404
        d = requests.get(f"{DOCTOR_URL}/doctors/{doctor_id}", timeout=5)
        if d.status_code != 200:
            return jsonify(error="doctor not found"), 404
        doctor = d.json()
        if not doctor["available"]:
            return jsonify(error="doctor not available"), 409
        return jsonify(status="appointment booked", patient=p.json(), doctor=doctor)
    except requests.RequestException as e:
        return jsonify(error=str(e)), 502
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
