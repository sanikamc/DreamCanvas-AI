
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from backend.config import GENERATED_IMAGES_DIR, MAX_PROMPT_LENGTH
from backend.database import (
    initialize_database,
    save_image,
    get_image_history
)
from backend.image_generator import generate_image

app = Flask(__name__)

CORS(app)

# Initialize database
os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)
initialize_database()


@app.route("/")
def home():
    return jsonify({
        "message": "AI Text-to-Image Generator API is running!"
    })


@app.route("/api/generate", methods=["POST"])
def generate():

    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()

    if not prompt:
        return jsonify({"error": "Please enter an image prompt."}), 400

    if len(prompt) > MAX_PROMPT_LENGTH:
        return jsonify({"error": "Prompt is too long."}), 400

    try:
        image_path = generate_image(prompt)

        filename = os.path.basename(image_path)
        save_image(prompt, filename)

        return jsonify({
            "message": "Image generated successfully!",
            "image_url": f"/generated_images/{filename}",
            "prompt": prompt
        })

    except Exception as error:
        app.logger.exception("Image generation failed")
        return jsonify({
            "error": str(error)
        }), 500


@app.route("/api/history", methods=["GET"])
def history():

    images = get_image_history()

    return jsonify([
        {
            "id": image["id"],
            "prompt": image["prompt"],
            "image_url": f"/generated_images/{image['image_path']}",
            "created_at": image["created_at"]
        }
        for image in images
    ])


@app.route("/generated_images/<filename>")
def serve_image(filename):

    return send_from_directory(
        GENERATED_IMAGES_DIR,
        filename
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
