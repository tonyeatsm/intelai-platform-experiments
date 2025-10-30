from ultralytics import YOLO
from pathlib import Path


ROOT_PATH = "/root/openvino/sources/benchmark_app"
DET_MODEL_NAME = "yolo11n"
DET_MODEL_PATH = f"{ROOT_PATH}/models/{DET_MODEL_NAME}.pt"
model = YOLO(DET_MODEL_PATH)

det_model_path = Path(f"{ROOT_PATH}/models/{DET_MODEL_NAME}_openvino_model/{DET_MODEL_NAME}.xml")
if not det_model_path.exists():
    model.export(format="openvino", dynamic=True, half=True)