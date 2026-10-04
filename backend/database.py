
import sqlite3
from backend.config import DATABASE_PATH


def get_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the images table if it doesn't exist."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS generated_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            image_path TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_image(prompt, image_path):
    """Save generated image information."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO generated_images (prompt, image_path)
        VALUES (?, ?)
    """, (prompt, image_path))

    connection.commit()
    connection.close()


def get_image_history():
    """Retrieve previously generated images."""

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM generated_images
        ORDER BY created_at DESC
    """)

    images = cursor.fetchall()
    connection.close()

    return images

