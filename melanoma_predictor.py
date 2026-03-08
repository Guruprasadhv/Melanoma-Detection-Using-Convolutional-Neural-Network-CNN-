
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

class MelanomaPredictor:
    def __init__(self, model_path='skin.h5'):
        """
        Initialize the predictor with the model.
        """
        self.model_path = model_path
        self.model = None
        self._load_model()
        
    def _load_model(self):
        """
        Loads the Keras model if it exists.
        """
        if os.path.exists(self.model_path):
            try:
                # Suppress TF logs
                os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
                self.model = load_model(self.model_path)
            except Exception as e:
                pass
        else:
            pass

    def predict(self, img_path):
        """
        Predicts whether an image is Benign or Malignant.
        
        Args:
            img_path (str): Path to the image file.
            
        Returns:
            dict: Dictionary containing 'label', 'score', and 'status'.
        """
        if self.model is None:
            return {'error': 'Model not loaded'}
            
        if not os.path.exists(img_path):
            return {'error': 'Image file not found'}
            
        try:
            # Preprocess image
            img = image.load_img(img_path, target_size=(224, 224))
            img_array = image.img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            
            # Predict
            prediction = self.model.predict(img_array, verbose=0)[0][0]
            
            # Logic: > 0.5 is Malignant (based on previous testing)
            is_malignant = prediction > 0.5
            label = "MALIGNANT" if is_malignant else "BENIGN"
            confidence = prediction if is_malignant else 1 - prediction
            
            return {
                'label': label,
                'score': float(prediction),
                'confidence': float(confidence),
                'status': 'success'
            }
            
        except Exception as e:
            return {'error': str(e)}

# Simple command line usage for testing
if __name__ == "__main__":
    predictor = MelanomaPredictor()
    # Test on a dummy path if needed
    print("Predictor initialized. Import this class to use it.")
