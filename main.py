import os
from dotenv import load_dotenv
from src.traffic import TrafficAnalyzer

load_dotenv()

API_KEY: str = os.getenv("TOM_TOM_API_KEY")

if os.path.isfile("streets.txt"):
    with open("streets.txt", "r") as f:
        STREETS = [line.strip() for line in f]
else:
    print("Create a file 'streets.txt' in project root and add roads to analyze in each line.")


# print(STREETS)
if __name__ == "__main__":
    tracker = TrafficAnalyzer(streets=STREETS, api_key=API_KEY)
    tracker.run()
