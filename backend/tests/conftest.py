
import warnings
def pytest_configure(config):
    warnings.filterwarnings("ignore", message="No uuidRepresentation is specified!")

