from functools import wraps
from sqlalchemy.orm import Session
from Database.model import get_engine

import os

KEY = "TEST"


def set_test_env():
    os.environ[KEY] = "True"

def _get_engine():
    if os.environ.get(KEY):
        engine = get_engine("_test")
    else:
        engine = get_engine()
    
    return engine

def session(func):
    @wraps(func)
    def test_create(self, *args, **kwargs):
        self.ENGINE = _get_engine()

        with Session(autoflush=True, bind=self.ENGINE) as db:
            return func(self, db, *args, **kwargs)
    
    return test_create
