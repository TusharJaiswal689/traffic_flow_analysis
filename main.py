import json
import os
from dotenv import load_dotenv
from traffic import TrafficAnalyzer

load_dotenv()

API_KEY: str = os.getenv("TOM_TOM_API_KEY")
streets_raw = os.getenv("STREETS")
# print(streets_raw)
STREETS: list[str] = json.loads(streets_raw)

# print(STREETS)
if __name__ == "__main__":
    tracker = TrafficAnalyzer(streets=STREETS, api_key=API_KEY)
    tracker.run()
