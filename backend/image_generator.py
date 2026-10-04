
import os
import uuid

from dotenv import load_dotenv
from huggingface_hub import InferenceClient

from backend.config import GENERATED_IMAGES_DIR

# Load environment variables
load_dotenv()


def generate_image(prompt):
    """
    Generate an image using Hugging Face FLUX.1-schnell.
    """

    api_token = os.getenv("HF_TOKEN")

    if not api_token:
        raise ValueError(
            "Hugging Face API token is missing. "
            "Please configure HF_TOKEN in your .env file."
        )

    # Create the generated images folder
    os.makedirs(GENERATED_IMAGES_DIR, exist_ok=True)

    # Connect to Hugging Face
    client = InferenceClient(
        provider="auto",
        api_key=api_token,
        timeout=180
    )

    # Generate image
    image = client.text_to_image(
        prompt=prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )

    # Save generated image
    filename = f"{uuid.uuid4().hex}.png"
    image_path = os.path.join(GENERATED_IMAGES_DIR, filename)

    image.save(image_path, format="PNG")

    return image_path