from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alerts.db"
db = SQLAlchemy(app)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    severity = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), default="open")

    def to_dict(self):
        return {"id": self.id, "title": self.title, "severity": self.severity, "status": self.status}

with app.app_context():
    db.create_all()

@app.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = Alert.query.all()
    return jsonify([a.to_dict() for a in alerts])

@app.route("/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()
    alert = Alert(title=data.get("title", "Untitled"), severity=data.get("severity", "low"))
    db.session.add(alert)
    db.session.commit()
    return jsonify(alert.to_dict()), 201

@app.route("/alerts/<int:alert_id>/acknowledge", methods=["PATCH"])
def acknowledge_alert(alert_id):
    alert = Alert.query.get(alert_id)
    if not alert:
        return jsonify({"error": "Alert not found"}), 404
    alert.status = "acknowledged"
    db.session.commit()
    return jsonify(alert.to_dict())

if __name__ == "__main__":
    app.run(debug=True)