from fastapi.testclient import TestClient
from app.main import create_application
import pytest



@pytest.fixture(scope="function")
def testing_app():
    app = create_application()
    testing_app = TestClient(app)
    return testing_app


@pytest.fixture
def testing_rate_limit() -> int:
    return 50
