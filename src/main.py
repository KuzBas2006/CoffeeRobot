import recognition
import processState
from src.processState import process_state
from src.recognition import QRScanner
import json

if __name__ == "__main__":

    ang = 45
    dist = 70

    data = {
        "angle": ang,
        "distance": dist
    }
    json_string = json.dumps(data)

    process_state(json_string)