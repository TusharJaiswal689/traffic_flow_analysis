import csv
import os
from datetime import datetime
from urllib.parse import quote
import requests

from src import analysis
from app_logging import logger

class TrafficAnalyzer:
    """Fetches, analyzes, and logs real-time TomTom traffic data for a list of streets."""

    def __init__(self, streets: list[str], api_key: str, output_file: str = "traffic_data.csv"):
        self.streets = streets
        self.api_key = api_key
        self.output_file = output_file

        # Geocode API configuration
        self.geocode_base_url = "https://api.tomtom.com/maps/orbis/places/geocode/"
        self.geocode_params = {
            "apiVersion": 1,
            "key": self.api_key,
            "limit": 1,
            "countrySet": "IN",
            "language": "en-GB",
        }

        # Traffic Flow API configuration
        self.flow_base_url = "https://api.tomtom.com/traffic/services/4/flowSegmentData"
        self.style = "absolute"
        self.zoom = 10
        self.unit = "KMPH"
        self.response_format = "json"

    def run(self) -> None:
        """Processes all streets and logs their traffic metrics."""
        for street in self.streets:
            try:
                lat, lon = self.get_coordinates(street)
                logger.debug(f"Street: {street}\nLatitude: {lat}\nLongitude: {lon}")

                flow_data = self.get_traffic_flow(lat, lon)

                self.log_traffic_data(flow_data, street, lat, lon)
                logger.debug(f"Logged traffic data for: {street}")

            except requests.exceptions.HTTPError as err:
                print(f"HTTP Error for '{street}' ({err.response.status_code}): {err.response.text}")
            except Exception as err:
                print(f"Error processing '{street}': {err}")

    def get_coordinates(self, street: str) -> tuple[float, float]:
        """Converts a street address into (latitude, longitude)."""
        encoded_address = quote(street)
        url = f"{self.geocode_base_url}{encoded_address}.json"

        response = requests.get(url, params=self.geocode_params, timeout=10)
        response.raise_for_status()

        results = response.json().get("results", [])
        if not results:
            raise ValueError(f"Could not find coordinates for: {street}")

        position = results[0]["position"]
        return position["lat"], position["lon"]

    def get_traffic_flow(self, lat: float, lon: float) -> dict:
        """Retrieves real-time traffic flow data for the given coordinates."""
        url = f"{self.flow_base_url}/{self.style}/{self.zoom}/{self.response_format}"
        params = {
            "key": self.api_key,
            "point": f"{lat},{lon}",
            "unit": self.unit,
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json().get("flowSegmentData", {})

    def log_traffic_data(self, flow_data: dict, street: str, lat: float, lon: float) -> None:
        """Calculates delay metrics and appends a row to the CSV file."""
        current_speed = flow_data.get("currentSpeed")
        free_flow_speed = flow_data.get("freeFlowSpeed")
        confidence = flow_data.get("confidence")
        road_closure = flow_data.get("roadClosure", False)
        timestamp = datetime.now().isoformat(timespec="seconds")

        delay_ratio, traffic_condition = analysis.traffic_delay_ratio(
            current_speed, free_flow_speed, road_closure
        )

        file_exists = os.path.isfile(self.output_file)
        headers = [
            "road",
            "datetime",
            "lat",
            "lon",
            "current_speed",
            "free_flow_speed",
            "confidence",
            "road_closure",
            "delay_ratio",
            "traffic_condition"
        ]
        row = [
            street,
            timestamp,
            lat,
            lon,
            current_speed,
            free_flow_speed,
            confidence,
            road_closure,
            delay_ratio,
            traffic_condition
        ]

        with open(self.output_file, mode="a", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(headers)
            writer.writerow(row)

