import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

# Heatmap import
from utils.heatmap import generate_heatmap

# AI Prediction import
from utils.predict import predict_disease

app = Flask(__name__)
CORS(app)

# =========================
# DATABASE INIT
# =========================

def init_db():

    conn = sqlite3.connect(
        "history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

        CREATE TABLE IF NOT EXISTS scans (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            image TEXT,

            disease TEXT,

            confidence INTEGER,

            date TEXT

        )

    """)

    conn.commit()

    conn.close()

# Initialize DB
init_db()

# =========================
# UPLOAD FOLDER
# =========================

UPLOAD_FOLDER = "uploads"

if not os.path.exists(
    UPLOAD_FOLDER
):
    os.makedirs(
        UPLOAD_FOLDER
    )

# =========================
# HOME
# =========================

@app.route("/")
def home():

    return (
        "Backend Running Successfully"
    )

# =========================
# PREDICT API
# =========================

@app.route(
    "/predict",
    methods=["POST"]
)

def predict():

    try:

        if "file" not in request.files:

            return jsonify({
                "error":
                "No file uploaded"
            })

        file = request.files["file"]

        # Save image
        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        file.save(filepath)

        # =========================
        # REAL AI PREDICTION
        # =========================

        disease, confidence = predict_disease(
            filepath
        )

        # =========================
        # GENERATE HEATMAP
        # =========================

        heatmap_path = generate_heatmap(
            filepath
        )

        # =========================
        # SAVE TO DATABASE
        # =========================

        conn = sqlite3.connect(
            "history.db"
        )

        cursor = conn.cursor()

        cursor.execute("""

            INSERT INTO scans (

                image,
                disease,
                confidence,
                date

            )

            VALUES (

                ?, ?, ?, datetime('now')

            )

        """, (

            file.filename,
            disease,
            round(confidence * 100)

        ))

        conn.commit()

        conn.close()

        # =========================
        # RETURN JSON
        # =========================

        return jsonify({

            "disease": disease,

            "confidence": confidence,

            "heatmap": heatmap_path

        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

# =========================
# HISTORY API
# =========================

@app.route("/history")
def history():

    conn = sqlite3.connect(
        "history.db"
    )

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        image,
        disease,
        confidence,
        date

        FROM scans

        ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({

            "image": row[0],

            "disease": row[1],

            "confidence": row[2],

            "date": row[3]

        })

    return jsonify(history)

# =========================
# SERVE UPLOADS
# =========================

@app.route(
    "/uploads/<path:filename>"
)

def uploaded_file(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )

# =========================
# RUN APP
# =========================

if __name__ == "__main__":

    app.run(debug=True)