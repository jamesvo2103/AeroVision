# In file: AeroVision/ml_model/predictor.py

import torch
from omegaconf import OmegaConf
from PIL import Image
import numpy as np
from T2I.ldm.models.diffusion.ddim import DDIMSampler
from T2I.ldm.util import load_model_from_config

class ModelPredictor:
    # ... __init__ method stays the same

    def predict(self, input_image: np.ndarray, angle_of_attack: int) -> np.ndarray:
        """
        Takes a preprocessed image and an angle of attack, then returns the
        airflow visualization.
        """
        init_image = Image.fromarray(input_image).convert("L").resize((512, 512))
        init_image = np.array(init_image)[None, None, ...]
        init_image = torch.from_numpy(init_image).to(torch.float32) / 255.0
        init_image = init_image.to(self.device)

        # Use the angle of attack to create a descriptive prompt for the model
        prompt = f"Airflow over an airfoil at {angle_of_attack} degrees angle of attack, fluid dynamics, CFD"
        
        with torch.no_grad():
            # ... the rest of the prediction logic stays exactly the same
            uc = self.model.get_learned_conditioning(1 * [""])
            c = self.model.get_learned_conditioning(1 * [prompt])
            z_enc = self.sampler.stochastic_encode(init_image, torch.tensor([0] * 1).to(self.device))
            t_enc = int(self.strength * self.ddim_steps)
            samples = self.sampler.decode(z_enc, c, t_enc, unconditional_guidance_scale=self.scale,
                                          unconditional_conditioning=uc, use_original_cond=False)
            output_image = self.model.decode_first_stage(samples)
            output_image = torch.clamp((output_image + 1.0) / 2.0, min=0.0, max=1.0)
            output_image = 255. * output_image[0].permute(1, 2, 0).cpu().numpy()

        return output_image.astype(np.uint8)

# This creates a single instance of the model to be shared across the app.
model_predictor = ModelPredictor()