from flask import Flask, render_template, request
import os
import pickle
import numpy as np

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "iris_kmeans_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "iris_scaler.pkl")

FEATURE_NAMES = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width",
]
DEFAULT_VALUES = ["5.1", "3.5", "1.4", "0.2"]


def load_pickle(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Required file not found: {os.path.basename(path)}"
        )
    with open(path, "rb") as file:
        return pickle.load(file)


# Load the trained K-Means model and its matching fitted scaler.
try:
    kmeans = load_pickle(MODEL_PATH)
    scaler = load_pickle(SCALER_PATH)
    MODEL_READY = True
except Exception as exc:
    print(f"Model/scaler loading error: {exc}")
    kmeans = None
    scaler = None
    MODEL_READY = False


def render_page(page, cluster=None, error=None, values=None):
    return render_template(
        "index.html",
        page=page,
        cluster=cluster,
        error=error,
        values=values if values is not None else DEFAULT_VALUES.copy(),
        model_ready=MODEL_READY,
    )


@app.route("/", methods=["GET"])
def home():
    return render_page("dashboard")


@app.route("/prediction", methods=["GET", "POST"])
def prediction():
    cluster = None
    error = None
    values = DEFAULT_VALUES.copy()

    if request.method == "POST":
        values = [request.form.get(name, "").strip() for name in FEATURE_NAMES]

        if not all(values):
            error = "Please enter all four flower measurements."
        elif not MODEL_READY:
            error = (
                "The model or scaler could not be loaded. Put "
                "'iris_kmeans_model.pkl' and 'iris_scaler.pkl' beside app.py."
            )
        else:
            try:
                measurements = np.array(
                    [[float(value) for value in values]], dtype=float
                )

                if not np.all(np.isfinite(measurements)):
                    raise ValueError("Measurements must be finite numbers.")

                if np.any(measurements <= 0) or np.any(measurements > 20):
                    raise ValueError(
                        "Measurements must be greater than 0 and at most 20 cm."
                    )

                # Use the exact fitted scaler used when training this model.
                scaled_measurements = scaler.transform(measurements)
                cluster = int(kmeans.predict(scaled_measurements)[0])

            except ValueError as exc:
                error = str(exc) or "Please enter valid numeric measurements."
            except Exception:
                app.logger.exception("Prediction failed")
                error = (
                    "Prediction failed. Verify that your model and scaler "
                    "were trained together with the four Iris features."
                )

    # Critical: the template receives page='prediction' after form submission.
    return render_page(
        "prediction",
        cluster=cluster,
        error=error,
        values=values,
    )


@app.route("/analytics", methods=["GET"])
def analytics():
    return render_page("analytics")


@app.route("/about", methods=["GET"])
def about():
    return render_page("about")


@app.errorhandler(404)
def page_not_found(_error):
    return render_page("dashboard"), 404


if __name__ == "__main__":
    app.run(debug=True)
