
import os

# Main project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Generated images directory
GENERATED_IMAGES_DIR = os.path.join(BASE_DIR, "generated_images")

# Database configuration
DATABASE_PATH = os.path.join(BASE_DIR, "database", "images.db")

# Flask configuration
SECRET_KEY = os.getenv("SECRET_KEY", "development-secret-key")
DEBUG = True

# AI image generation settings
IMAGE_SIZE = "1024x1024"
MAX_PROMPT_LENGTH = 1000

