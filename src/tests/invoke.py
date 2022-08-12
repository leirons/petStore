import pytest
import sys


class MyPlugin:
    def pytest_sessionfinish(self):
        print("*** test run reporting finishing")


if __name__ == "__main__":
    print('started')
    sys.exit(pytest.main(["-qq"], plugins=[MyPlugin()]))