import joblib
import pandas as pd
import os

class MLInference:
    _models = {}

    @classmethod
    def load_model(cls, model_name):
        """Lazy loads models from the assets directory."""
        if model_name not in cls._models:
            # Asset path within the package
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "assets", f"{model_name}.pkl")
            
            if os.path.exists(path):
                cls._models[model_name] = joblib.load(path)
            else:
                raise FileNotFoundError(f"Model {model_name} not found at {path}")
        return cls._models[model_name]

    @classmethod
    def predict_shortage(cls, city, blood_group, units):
        model = cls.load_model("shortage_model")
        le_city = cls.load_model("le_city")
        le_group = cls.load_model("le_group")

        try:
            city_enc = le_city.transform([city])[0]
            group_enc = le_group.transform([blood_group])[0]

            features = pd.DataFrame(
                [[city_enc, group_enc, float(units)]],
                columns=["city", "blood_group", "thalassemia_units_required"]
            )
            return model.predict(features)[0]
        except Exception as e:
            print(f"Shortage Prediction Error: {e}")
            return None

    @classmethod
    def predict_donor_likelihood(cls, recency, frequency, monetary, time):
        model = cls.load_model("donor_model")
        try:
            features = pd.DataFrame(
                [[float(recency), float(frequency), float(monetary), float(time)]],
                columns=["Recency", "Frequency", "Monetary", "Time"]
            )
            return model.predict(features)[0]
        except Exception as e:
            print(f"Donor Prediction Error: {e}")
            return None
