from ultralytics import YOLO
from pathlib import Path
import openvino as ov
import shutil
import os

ROOT_PATH = Path("/root/dlstreamer/perform_limit")
DET_MODEL_NAME = "yolo11n"
DET_MODEL_PATH = ROOT_PATH / "models" / f"{DET_MODEL_NAME}.pt"

MODEL_TYPE = "yolo_v11"
SEG_MODEL_TYPES = ["YOLOv8-SEG", "yolo_v11_seg"]

core = ov.Core()
model = YOLO(str(DET_MODEL_PATH))
model.info()


def export_openvino(batch=None, dynamic=False, save_dir=None):
    """Export YOLO to OpenVINO and post-process"""
    if dynamic:
        converted_path = model.export(format="openvino", dynamic=True)
    else:
        converted_path = model.export(format="openvino", batch=batch)

    converted_model = Path(converted_path) / f"{DET_MODEL_NAME}.xml"
    ov_model = core.read_model(model=str(converted_model))

    # segmentation output rename (if needed)
    if MODEL_TYPE in SEG_MODEL_TYPES:
        ov_model.output(0).set_names({"boxes"})
        ov_model.output(1).set_names({"masks"})

    # add runtime info
    ov_model.set_rt_info(MODEL_TYPE, ["model_info", "model_type"])

    # save
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = save_dir / f"{DET_MODEL_NAME}.xml"
    ov.save_model(ov_model, str(save_path), compress_to_fp16=True)

    # cleanup temp export dir
    shutil.rmtree(converted_path)
    print(f"Saved: {save_path}")


# ========== Dynamic batch ==========
dynamic_save_dir = ROOT_PATH / "models" / f"{DET_MODEL_NAME}_openvino_model_dynamic"
export_openvino(dynamic=True, save_dir=dynamic_save_dir)

# ========== Static batch ==========
static_root = ROOT_PATH / "models" / f"{DET_MODEL_NAME}_openvino_model_static"
for batch in range(1, 9):
    batch_dir = static_root / f"batch{batch}"
    export_openvino(batch=batch, save_dir=batch_dir)
