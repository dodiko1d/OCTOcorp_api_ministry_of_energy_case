""" Configuration tests file, do not write test here, use separated tests in api description folders.
 Run with "python -m pytest". """

# Side libraries.
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Project imports.
from database import Base
from main import app
from prediction.router import get_db as product_get_db

# Modules for database after-test deletion.
import os
import atexit


# Project setting a bit overwritten for testing.
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)


Base.metadata.create_all(bind=engine)


# Tests session database connector.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[product_get_db] = override_get_db


# Test client instance.
client = TestClient(app)


# Import are specifically connected this way, to adding a new micro-apis add tests here.
from prediction.tests import test_city_data_getter


# Handler that deletes testing database every time tests finish to ensure you won't need rewrite tests.
# def exit_handler():
#     os.unlink('test.db')
#
#
# atexit.register(exit_handler)
