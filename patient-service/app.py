from flask import Flask, jsonify
app = Flask(__name__)
PATIENTS = {
    1: {"id": 1, "name": "Ravi Kumar", "age": 34},
    2: {"id": 2, "name": "Anita Rao", "age": 28},
    3: {"id": 3, "name": "Suresh Patil", "age": 52},
}
@app.route("/health")
def health():
    return jsonify(service="patient", status="ok")
@app.route("/patients")
def all_patients():
    return jsonify(list(PATIENTS.values()))
@app.route("/patients/<int:pid>")
def one_patient(pid):
    p = PATIENTS.get(pid)
    if p:
        return jsonify(p)
    return jsonify(error="patient not found"), 404
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
