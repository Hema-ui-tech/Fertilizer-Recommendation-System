import pickle
import pandas as pd
from flask import Flask, request, render_template_string

app = Flask(__name__)

with open("crop_model.pkl", "rb") as f:
    crop_model = pickle.load(f)

with open("fertilizer_model.pkl", "rb") as f:
    fert = pickle.load(f)

fert_model = fert["model"]
soil_enc = fert["soil_encoder"]
crop_enc = fert["crop_encoder"]
fert_enc = fert["fertilizer_encoder"]

PAGE = """
<!DOCTYPE html>
<html>
<head>
<title>Fertilizer Recommendation System</title>
<style>
  body { font-family: Arial, sans-serif; background: #eef5ee; margin: 0; padding: 20px; }
  .box { max-width: 560px; margin: auto; background: #fff; padding: 24px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,.15); }
  h1 { color: #2e7d32; text-align: center; font-size: 24px; }
  h2 { color: #2e7d32; font-size: 18px; margin-top: 24px; }
  label { display: block; margin-top: 10px; font-size: 14px; }
  input, select { width: 100%; padding: 8px; margin-top: 4px; box-sizing: border-box; }
  button { margin-top: 16px; width: 100%; padding: 10px; background: #2e7d32; color: #fff; border: 0; border-radius: 6px; font-size: 16px; cursor: pointer; }
  .result { margin-top: 16px; padding: 12px; background: #e8f5e9; border-left: 4px solid #2e7d32; }
  hr { margin: 28px 0; }
</style>
</head>
<body>
<div class="box">
  <h1>Fertilizer Recommendation System</h1>

  <h2>1. Crop Recommendation</h2>
  <form method="post" action="/predict_crop">
    <label>Nitrogen (N)<input type="number" step="any" name="N" required></label>
    <label>Phosphorus (P)<input type="number" step="any" name="P" required></label>
    <label>Potassium (K)<input type="number" step="any" name="K" required></label>
    <label>Temperature (&deg;C)<input type="number" step="any" name="temperature" required></label>
    <label>Humidity (%)<input type="number" step="any" name="humidity" required></label>
    <label>Soil pH<input type="number" step="any" name="ph" required></label>
    <label>Rainfall (mm)<input type="number" step="any" name="rainfall" required></label>
    <button type="submit">Recommend Crop</button>
  </form>
  {% if crop_result %}<div class="result">Recommended crop: <b>{{ crop_result }}</b></div>{% endif %}

  <hr>

  <h2>2. Fertilizer Recommendation</h2>
  <form method="post" action="/predict_fertilizer">
    <label>Temperature (&deg;C)<input type="number" step="any" name="temperature" required></label>
    <label>Humidity (%)<input type="number" step="any" name="humidity" required></label>
    <label>Moisture (%)<input type="number" step="any" name="moisture" required></label>
    <label>Soil Type
      <select name="soil">{% for s in soils %}<option>{{ s }}</option>{% endfor %}</select>
    </label>
    <label>Crop Type
      <select name="crop">{% for c in crops %}<option>{{ c }}</option>{% endfor %}</select>
    </label>
    <label>Nitrogen<input type="number" step="any" name="nitrogen" required></label>
    <label>Potassium<input type="number" step="any" name="potassium" required></label>
    <label>Phosphorus<input type="number" step="any" name="phosphorus" required></label>
    <button type="submit">Recommend Fertilizer</button>
  </form>
  {% if fert_result %}<div class="result">Recommended fertilizer: <b>{{ fert_result }}</b></div>{% endif %}
</div>
</body>
</html>
"""


def render(**kwargs):
    return render_template_string(
        PAGE,
        soils=list(soil_enc.classes_),
        crops=list(crop_enc.classes_),
        **kwargs,
    )


@app.route("/")
def home():
    return render()


@app.route("/predict_crop", methods=["POST"])
def predict_crop():
    values = pd.DataFrame([{
        "N": float(request.form["N"]),
        "P": float(request.form["P"]),
        "K": float(request.form["K"]),
        "temperature": float(request.form["temperature"]),
        "humidity": float(request.form["humidity"]),
        "ph": float(request.form["ph"]),
        "rainfall": float(request.form["rainfall"]),
    }])
    return render(crop_result=crop_model.predict(values)[0])


@app.route("/predict_fertilizer", methods=["POST"])
def predict_fertilizer():
    values = pd.DataFrame([{
        "Temperature": float(request.form["temperature"]),
        "Humidity": float(request.form["humidity"]),
        "Moisture": float(request.form["moisture"]),
        "Soil Type": soil_enc.transform([request.form["soil"]])[0],
        "Crop Type": crop_enc.transform([request.form["crop"]])[0],
        "Nitrogen": float(request.form["nitrogen"]),
        "Potassium": float(request.form["potassium"]),
        "Phosphorus": float(request.form["phosphorus"]),
    }])
    result = fert_enc.inverse_transform(fert_model.predict(values))[0]
    return render(fert_result=result)


if __name__ == "__main__":
    app.run(debug=True)
