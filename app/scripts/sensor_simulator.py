import requests
import time
import random
import math
import datetime
import argparse
import logging

API_BASE_URL = "http://localhost:8000/api"


def get_temperature(hour):
    base = 20
    variation = 10 * math.sin((hour - 8) / 24 * 2 * math.pi)
    noise = random.uniform(-1, 1)
    return round(base + variation + noise, 2)


def get_humidity(hour):
    base = 60
    variation = 20 * math.cos((hour - 8) / 24 * 2 * math.pi)
    noise = random.uniform(-5, 5)
    return round(base + variation + noise, 1)


def get_value(sensor_type, hour):
    if sensor_type == "temperature":
        return get_temperature(hour)
    elif sensor_type == "soil_humidity":
        return get_humidity(hour)
    elif sensor_type == "luminosity":
        if 6 <= hour <= 19:
            return random.uniform(500, 1000)
        return random.uniform(0, 10)
    else:
        return random.uniform(10, 100)


def run_simulation(api_key, interval=5):
    print(f"Starting Agrotech Sensor Simulator...")
    print(f"Target: {API_BASE_URL}")
    print(f"Interval: {interval} seconds")
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    try:
        print("Fetching sensor list...")
        parcels_resp = requests.get(f"{API_BASE_URL}/parcels", headers=headers)
        if parcels_resp.status_code != 200:
            print(f"Error fetching parcels: {parcels_resp.text}")
            return
        parcels = parcels_resp.json()
        sensors = []
        for parcel in parcels:
            s_resp = requests.get(
                f"{API_BASE_URL}/parcels/{parcel['id']}/sensors", headers=headers
            )
            if s_resp.status_code == 200:
                p_sensors = s_resp.json()
                for s in p_sensors:
                    s["parcel_name"] = parcel["name"]
                    sensors.append(s)
        if not sensors:
            print("No sensors found to simulate.")
            return
        print(f"Found {len(sensors)} sensors across {len(parcels)} parcels.")
        while True:
            current_hour = datetime.datetime.now().hour
            for sensor in sensors:
                value = get_value(sensor["type"], current_hour)
                payload = {
                    "value": value,
                    "timestamp": datetime.datetime.utcnow().isoformat(),
                }
                try:
                    resp = requests.post(
                        f"{API_BASE_URL}/sensors/{sensor['id']}/data",
                        json=payload,
                        headers=headers,
                    )
                    status = (
                        "OK" if resp.status_code == 200 else f"ERR {resp.status_code}"
                    )
                    print(
                        f"[{status}] Sensor {sensor['id']} ({sensor['type']}) -> {value}"
                    )
                except Exception as e:
                    logging.exception(f"Request failed: {e}")
            print(f"Sleeping for {interval}s...")
            time.sleep(interval)
    except Exception as e:
        logging.exception(f"Simulation stopped: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Agrotech Sensor Simulator")
    parser.add_argument(
        "--key", type=str, default="key_farmer_12345", help="API Key for authentication"
    )
    parser.add_argument(
        "--interval", type=int, default=10, help="Seconds between readings"
    )
    args = parser.parse_args()
    run_simulation(args.key, args.interval)