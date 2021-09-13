import pytest
from app import create_app
from store_core.database.gateway import DBGateway
from store_core.repositories import DogRepository


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!
    dog_repository = DogRepository()
    dog_repository.clear_all_data(DBGateway)
