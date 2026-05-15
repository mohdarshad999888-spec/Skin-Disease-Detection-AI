import os
import json
import numpy as np

# =========================
# TRY IMPORTING TENSORFLOW
# =========================

try:

    from tensorflow.keras.models import load_model

    from tensorflow.keras.preprocessing import image

    TF_AVAILABLE = True

except Exception as e:

    TF_AVAILABLE = False

    print("TensorFlow Import Error:", e)

# =========================
# MODEL PATH
# =========================

BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model.h5"
)

CLASS_NAMES_PATH = os.path.join(
    BASE_DIR,
    "class_names.json"
)

# =========================
# LOAD MODEL
# =========================

model = None

if TF_AVAILABLE and os.path.exists(MODEL_PATH):

    try:

        model = load_model(
            MODEL_PATH
        )

        print(
            "✅ Model loaded successfully"
        )

    except Exception as e:

        print(
            "❌ Model Load Error:",
            e
        )

else:

    print(
        "Model not found or TensorFlow unavailable"
    )

# =========================
# CLASS LABELS
# =========================

default_classes = [
    "Acne",
    "Eczema",
    "Melanoma",
    "Normal"
]

if os.path.exists(CLASS_NAMES_PATH):
    with open(CLASS_NAMES_PATH, "r") as label_file:
        classes = json.load(label_file)
else:
    classes = default_classes

# =========================
# PREDICTION FUNCTION
# =========================

def predict_disease(img_path):

    try:

        # =========================
        # REAL AI PREDICTION
        # =========================

        if model is not None:

            img = image.load_img(

                img_path,

                target_size=(224, 224)

            )

            img_array = image.img_to_array(
                img
            )

            img_array = (
                img_array / 255.0
            )

            img_array = np.expand_dims(

                img_array,

                axis=0

            )

            prediction = model.predict(
                img_array
            )

            class_index = np.argmax(
                prediction
            )

            predicted_class = classes[
                class_index
            ]

            confidence = float(

                np.max(prediction)

            )

            return (
                predicted_class,
                confidence
            )

        # =========================
        # MODEL UNAVAILABLE OUTPUT
        # =========================

        else:

            return (
                "Model not loaded",
                0.0
            )

    except Exception as e:

        print(
            "Prediction Error:",
            e
        )

        return (
            "Error",
            0.0
        )
