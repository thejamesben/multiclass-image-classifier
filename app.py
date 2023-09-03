import os
from flask import Flask, request, jsonify
import tensorflow as tf
from PIL import Image
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from flask_cors import CORS

app = Flask(
    __name__, static_folder="./frontend/build", static_url_path='/')

CORS(app)

# Load the model
try:
    model = tf.keras.models.load_model(
        './model/best_model.h5')
except:
    raise Exception("Failed to load the model.")

# Initialize the LabelBinarizer for decoding one-hot encoded predictions
labels = list('ABC')
label_binarizer = LabelBinarizer()
label_binarizer.fit(labels)


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if an image was posted
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        # Convert the image to the desired format and preprocess
        image = Image.open(request.files['file']).convert('L').resize((32, 32))
        image_array = np.array(image) / 255.0
        image_array_rgb = np.repeat(image_array[..., np.newaxis], 3, -1)
        image_array_rgb = np.expand_dims(
            image_array_rgb, axis=0)  # Add batch dimension

        # Predict the image's class
        prediction = model.predict(image_array_rgb)

        # Check the confidence of prediction
        confidence_threshold = 0.7
        max_confidence = prediction.max()

        if max_confidence < confidence_threshold:
            return jsonify({'error': 'The dataset was not trained to identify the image you uploaded'})

        predicted_class = label_binarizer.inverse_transform(prediction)[0]

        return jsonify({'class': predicted_class})

    except (AttributeError, tf.errors.NotFoundError):
        return jsonify({'error': 'Model error'}), 500
    except (ValueError, TypeError):
        return jsonify({'error': 'Processing error'}), 500
    except Exception as e:
        return jsonify({'error': f"Unexpected error: {str(e)}"}), 500


@app.errorhandler(500)
def internal_server_error(e):
    return jsonify({'error': 'Internal server error'}), 500
    
if __name__ == '__main__':
    app.run(debug=True)

# Uncomment this code for local development
# if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

