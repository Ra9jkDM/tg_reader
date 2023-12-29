from os import environ

KEY="TEST"

def set_test_env():
    environ[KEY] = "True"