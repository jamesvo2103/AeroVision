# ml_model/predictor.py
#
# One shared object that turns a clean-airfoil image into an airflow image
# using the pix2pix-turbo model.
#
# Two modes, chosen automatically:
#   - REAL mode: if a trained checkpoint (.pkl) is available, load Pix2Pix_Turbo
#     and run it. Needs a GPU (the model code uses CUDA).
#   - STUB mode: if no checkpoint is set/found, return a simple placeholder
#     image so the frontend + backend can be developed and tested without a GPU.
#
# Controlled by environment variables:
#   AEROVISION_MODEL_PATH  -> path to the trained .pkl checkpoint (enables REAL mode)
#   AEROVISION_DEVICE      -> "cuda" or "cpu" (default: cuda if available, else cpu)

import os
import sys

import cv2
import numpy as np

# Make the model source importable (src/pix2pix_turbo.py imports "model", etc.)
_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.join(_HERE, "src")
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

MODEL_PATH = os.environ.get("AEROVISION_MODEL_PATH", "").strip()


def _pick_device():
    forced = os.environ.get("AEROVISION_DEVICE", "").strip().lower()
    if forced in ("cpu", "cuda"):
        return forced
    try:
        import torch
        return "cuda" if torch.cuda.is_available() else "cpu"
    except Exception:
        return "cpu"


def build_prompt(angle_of_attack: int) -> str:
    """Turn the angle of attack into a text prompt the model was trained on.

    The training captions describe three flow regimes. We pick the closest one
    to the requested angle so the wording matches what the model has seen.
    """
    a = float(angle_of_attack)
    if a <= 8:
        regime = ("Smooth, attached laminar airflow over an airfoil "
                  "at {a:.0f} degrees angle of attack")
    elif a <= 26:
        regime = ("Airflow visualization showing significant flow separation "
                  "near the leading edge, creating a turbulent wake over the top "
                  "surface of an airfoil at {a:.0f} degrees angle of attack")
    else:
        regime = ("Deep aerodynamic stall showing chaotic, fully separated flow "
                  "and a large turbulent wake over an airfoil at {a:.0f} degrees "
                  "angle of attack")
    return regime.format(a=a)


def _to_rgb_512(input_image: np.ndarray) -> np.ndarray:
    """Ensure a 3-channel RGB image sized to a multiple of 8 (512x512)."""
    img = input_image
    if img.ndim == 2:  # grayscale mask from preprocess_airfoil
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    elif img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    return cv2.resize(img, (512, 512), interpolation=cv2.INTER_LANCZOS4)


class ModelPredictor:
    def __init__(self):
        self.device = _pick_device()
        self.model = None
        self.mode = "stub"

        if MODEL_PATH and os.path.exists(MODEL_PATH):
            self._load_real_model()
        else:
            reason = "no AEROVISION_MODEL_PATH set" if not MODEL_PATH else f"checkpoint not found: {MODEL_PATH}"
            print(f"[predictor] STUB mode ({reason}). Set AEROVISION_MODEL_PATH to a trained .pkl to enable the real model.")

    def _load_real_model(self):
        # Imported lazily so STUB mode has no torch / GPU dependency.
        import torch  # noqa: F401
        from pix2pix_turbo import Pix2Pix_Turbo

        print(f"[predictor] Loading pix2pix-turbo checkpoint on {self.device}: {MODEL_PATH}")
        model = Pix2Pix_Turbo(pretrained_path=MODEL_PATH)
        model.set_eval()
        self.model = model
        self.mode = "real"

    def predict(self, input_image: np.ndarray, angle_of_attack: int) -> np.ndarray:
        """Clean airfoil image (+ angle) -> RGB airflow image as a uint8 array."""
        rgb = _to_rgb_512(input_image)
        prompt = build_prompt(angle_of_attack)

        if self.mode == "stub":
            return self._stub_output(rgb, angle_of_attack)

        import torch
        import torchvision.transforms.functional as F

        c_t = F.to_tensor(rgb).unsqueeze(0).to(self.device)  # [1,3,512,512] in [0,1]
        with torch.no_grad():
            output = self.model(c_t, prompt)  # [-1, 1]
        out = (output[0].cpu() * 0.5 + 0.5).clamp(0, 1).permute(1, 2, 0).numpy()
        return (out * 255.0).astype(np.uint8)

    def _stub_output(self, rgb: np.ndarray, angle_of_attack: int) -> np.ndarray:
        """Placeholder airflow: draw simple streamlines + a label over the input
        so the end-to-end flow is visible before a real checkpoint exists."""
        out = rgb.copy()
        h, w = out.shape[:2]
        for y in range(20, h, 28):
            bend = int(12 * np.sin(np.deg2rad(angle_of_attack)))
            cv2.line(out, (0, y), (w, y + bend), (60, 140, 255), 1, cv2.LINE_AA)
        cv2.putText(out, f"STUB airflow  AoA={angle_of_attack}deg", (12, h - 16),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2, cv2.LINE_AA)
        return out


# Single shared instance used across the app.
model_predictor = ModelPredictor()
