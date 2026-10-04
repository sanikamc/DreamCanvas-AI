from backend import database


def test_save_and_get_image_history(tmp_path, monkeypatch):
    # Use a temporary database for testing
    test_db = tmp_path / "test_images.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_db))

    # Initialize the database
    database.initialize_database()

    # Save an image record
    database.save_image(
        "A beautiful castle",
        "generated_images/test.png"
    )

    # Retrieve image history
    images = database.get_image_history()

    # Verify the saved record
    assert len(images) == 1
    assert images[0]["prompt"] == "A beautiful castle"
    assert images[0]["image_path"] == "generated_images/test.png"


def test_empty_image_history(tmp_path, monkeypatch):
    test_db = tmp_path / "empty_images.db"

    monkeypatch.setattr(database, "DATABASE_PATH", str(test_db))

    database.initialize_database()

    images = database.get_image_history()

    assert len(images) == 0