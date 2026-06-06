from flask import Flask, jsonify, request

app = Flask(__name__)

alerts = []

@app.route("/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts)

@app.route("/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()
    alert = {
        "id": len(alerts) + 1,
        "title": data.get("title", "Untitled"),
        "severity": data.get("severity", "low"),
        "status": "open"
    }
    alerts.append(alert)
    return jsonify(alert), 201

@app.route("/alerts/<int:alert_id>/acknowledge", methods=["PATCH"])
def acknowledge_alert(alert_id):
    for alert in alerts:
        if alert["id"] == alert_id:
            alert["status"] = "acknowledged"
            return jsonify(alert)
    return jsonify({"error": "Alert not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
