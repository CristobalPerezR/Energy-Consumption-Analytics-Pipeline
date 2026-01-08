### RUN ML PIPELINE
from src.features.build_features import create_dataset
from src.ml.train_baseline import TrainingModels
import os

csv_dir = os.path.join("data", "processed")
csv_path = os.path.join(csv_dir, "household_power_consumption_processed.csv")

ml_path = os.path.join("data", "ml")
models_path = os.path.join(ml_path, "models")
metrics_path = os.path.join(ml_path, "metrics.json")

print("\n================= CREATING DATASET =================\n")

ml_ready_path = create_dataset(csv_path)

print("\n================= TRAINING MODELS =================\n")

trainer = TrainingModels(ml_ready_path)
trainer.train_models()

print("\n================= REPORTING =================\n")

trainer.report()

print("\n================= SAVING METRICS =================\n")

trainer.save_metrics(metrics_path)

print("\n================= SAVING MODELS =================\n")

trainer.save_models(models_path)

print("\n================= ML FINISHED =================\n")