
import os
import mlflow
import mlflow.sklearn
import joblib

# Read DagsHub credentials from environment variables
os.environ["MLFLOW_TRACKING_USERNAME"] = "ZeinabD"
os.environ["MLFLOW_TRACKING_PASSWORD"] = os.environ["DAGSHUB_TOKEN"]

# Connect to DagsHub
mlflow.set_tracking_uri(
    "https://dagshub.com/ZeinabD/mlops-assignment.mlflow"
)

# Find the newest logged model in Experiment 0
models = mlflow.search_logged_models(
    experiment_ids=["0"],
    max_results=1,
    order_by=[
        {"field_name": "creation_time", "ascending": False}
    ],
    output_format="list"
)

if not models:
    raise RuntimeError("No logged models found in DagsHub.")

latest_model = models[0]

print("Selected model:", latest_model.name)
print("Model ID:", latest_model.model_id)

# Download the model from DagsHub
model_uri = f"models:/{latest_model.model_id}"
loaded_model = mlflow.sklearn.load_model(model_uri)

# Save the model locally
os.makedirs("model", exist_ok=True)

joblib.dump(loaded_model, "model/model.joblib")

print("Model downloaded successfully!")
