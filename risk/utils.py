from django.conf import settings
from joblib import load
import pandas as pd
import numpy as np
import threading
import sys

# --------------------------------------------------
# PICKLE COMPATIBILITY FIX
# --------------------------------------------------
from .bundle_shim import DeployedBundle
sys.modules["__main__"].DeployedBundle = DeployedBundle

_model_lock = threading.Lock()
_art = None

def get_artifact():
    global _art
    if _art is None:
        with _model_lock:
            if _art is None:
                _art = load(settings.MODEL_BUNDLE_PATH)
    return _art


def predict_one(row):
    """
    Multiclass severity prediction
    """
    art = get_artifact()

    model = art.model
    scaler = art.scaler
    features = art.feature_list
    class_map = art.class_mapping

    df = pd.DataFrame([row])
    Xs = scaler.transform(df[features])

    probs = model.predict_proba(Xs)[0]
    pred_class = int(np.argmax(probs))
    confidence = float(np.max(probs))

    return {
        "severity_id": pred_class,
        "severity": class_map[pred_class],
        "confidence": round(confidence, 4),
        "probs": {
            class_map[i]: round(float(p), 4)
            for i, p in enumerate(probs)
        }
    }
