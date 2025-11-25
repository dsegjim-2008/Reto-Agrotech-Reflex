import reflex as rx
import datetime
import csv
import json
import io
import logging
from sqlmodel import select, and_
from typing import Any, Optional
from app.database import Parcel, Sensor, SensorData, User
from app.states.auth_state import AuthState


class AnalyticsState(rx.State):
    """State management for the data analytics and visualization page.

    Controls chart configuration, data fetching, sensor selection, and date
    range filtering for historical data analysis.
    """

    available_sensors: list[dict] = []
    selected_sensor_ids: list[int] = []
    date_range_preset: str = "7d"
    start_date: str = ""
    end_date: str = ""
    chart_type: str = "line"
    aggregation: str = "raw"
    chart_data: list[dict] = []
    sensor_stats: list[dict] = []
    is_loading: bool = False
    colors: list[str] = ["#3B82F6", "#10B981", "#F59E0B", "#EF4444", "#8B5CF6"]

    @rx.var
    def current_sensors_legend(self) -> list[dict]:
        """Get legend data for currently selected sensors."""
        legend = []
        for idx, s_id in enumerate(self.selected_sensor_ids):
            sensor = next((s for s in self.available_sensors if s["id"] == s_id), None)
            if sensor:
                legend.append(
                    {
                        "name": f"{sensor['parcel_name']} - {sensor['name']}",
                        "color": self.colors[idx % len(self.colors)],
                        "data_key": f"sensor_{s_id}",
                    }
                )
        return legend

    @rx.event
    async def load_initial_data(self):
        """Load available sensors and default data."""
        if not self.start_date:
            self.set_preset_dates("7d")
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            return
        with rx.session() as session:
            query = (
                select(Sensor, Parcel)
                .join(Parcel)
                .where(Parcel.farmer_id == auth_state.user.id)
            )
            results = session.exec(query).all()
            self.available_sensors = [
                {
                    "id": r.Sensor.id,
                    "name": r.Sensor.name,
                    "type": r.Sensor.type,
                    "parcel_name": r.Parcel.name,
                    "full_label": f"{r.Parcel.name} - {r.Sensor.name} ({r.Sensor.type})",
                }
                for r in results
            ]
            if not self.selected_sensor_ids and self.available_sensors:
                self.selected_sensor_ids = [self.available_sensors[0]["id"]]
        await self.fetch_analytics_data()

    @rx.event
    def set_preset_dates(self, preset: str):
        """Helper to calculate dates from preset."""
        now = datetime.datetime.utcnow()
        self.end_date = now.strftime("%Y-%m-%d")
        if preset == "7d":
            start = now - datetime.timedelta(days=7)
        elif preset == "30d":
            start = now - datetime.timedelta(days=30)
        elif preset == "90d":
            start = now - datetime.timedelta(days=90)
        else:
            return
        self.start_date = start.strftime("%Y-%m-%d")

    @rx.event
    async def set_range_preset(self, value: str):
        self.date_range_preset = value
        if value != "custom":
            self.set_preset_dates(value)
        await self.fetch_analytics_data()

    @rx.event
    async def set_custom_start_date(self, value: str):
        self.start_date = value
        self.date_range_preset = "custom"
        await self.fetch_analytics_data()

    @rx.event
    async def set_custom_end_date(self, value: str):
        self.end_date = value
        self.date_range_preset = "custom"
        await self.fetch_analytics_data()

    @rx.event
    async def toggle_sensor(self, sensor_id: int, checked: bool):
        if checked:
            if len(self.selected_sensor_ids) >= 5:
                return rx.toast.warning("Max 5 sensors can be compared at once.")
            if sensor_id not in self.selected_sensor_ids:
                self.selected_sensor_ids.append(sensor_id)
        elif sensor_id in self.selected_sensor_ids:
            self.selected_sensor_ids.remove(sensor_id)
        await self.fetch_analytics_data()

    @rx.event
    def set_chart_type_val(self, value: str):
        self.chart_type = value

    @rx.event
    async def set_aggregation_val(self, value: str):
        self.aggregation = value
        await self.fetch_analytics_data()

    @rx.event
    async def fetch_analytics_data(self):
        """Fetch historical sensor data and process it for visualization.

        Retrieves data from the database based on selected sensors and date range,
        then aggregates it (raw, hourly, or daily) to populate the chart.
        """
        self.is_loading = True
        yield
        if not self.selected_sensor_ids or not self.start_date or (not self.end_date):
            self.chart_data = []
            self.sensor_stats = []
            self.is_loading = False
            return
        try:
            start_dt = datetime.datetime.strptime(self.start_date, "%Y-%m-%d")
            end_dt = datetime.datetime.strptime(
                self.end_date, "%Y-%m-%d"
            ) + datetime.timedelta(days=1)
        except ValueError as e:
            logging.exception(f"Error parsing dates: {e}")
            self.is_loading = False
            yield rx.toast.error("Invalid date format")
            return
        with rx.session() as session:
            query = (
                select(SensorData)
                .where(
                    SensorData.sensor_id.in_(self.selected_sensor_ids),
                    SensorData.timestamp >= start_dt,
                    SensorData.timestamp < end_dt,
                )
                .order_by(SensorData.timestamp)
            )
            raw_data = session.exec(query).all()
        buckets = {}
        sensor_values = {s_id: [] for s_id in self.selected_sensor_ids}
        for record in raw_data:
            ts = record.timestamp
            val = record.value
            s_id = record.sensor_id
            if self.aggregation == "hour":
                key = ts.strftime("%Y-%m-%d %H:00")
            elif self.aggregation == "day":
                key = ts.strftime("%Y-%m-%d")
            else:
                key = ts.strftime("%Y-%m-%d %H:%M:%S")
            if key not in buckets:
                buckets[key] = {"timestamp": key, "original_ts": ts}
            if f"values_{s_id}" not in buckets[key]:
                buckets[key][f"values_{s_id}"] = []
            buckets[key][f"values_{s_id}"].append(val)
            sensor_values[s_id].append(val)
        final_data = []
        sorted_keys = sorted(buckets.keys())
        for key in sorted_keys:
            item = {"name": key}
            bucket = buckets[key]
            for s_id in self.selected_sensor_ids:
                vals = bucket.get(f"values_{s_id}", [])
                if vals:
                    avg_val = sum(vals) / len(vals)
                    item[f"sensor_{s_id}"] = round(avg_val, 2)
            final_data.append(item)
        self.chart_data = final_data
        stats = []
        for s_id in self.selected_sensor_ids:
            vals = sensor_values[s_id]
            sensor_info = next(
                (s for s in self.available_sensors if s["id"] == s_id), None
            )
            if vals and sensor_info:
                stats.append(
                    {
                        "name": sensor_info["name"],
                        "parcel": sensor_info["parcel_name"],
                        "type": sensor_info["type"],
                        "min": round(min(vals), 2),
                        "max": round(max(vals), 2),
                        "avg": round(sum(vals) / len(vals), 2),
                        "count": len(vals),
                    }
                )
        self.sensor_stats = stats
        self.is_loading = False

    @rx.event
    def download_csv(self):
        """Generate and download CSV export."""
        if not self.chart_data:
            return rx.toast.error("No data to export.")
        output = io.StringIO()
        writer = csv.writer(output)
        headers = ["Timestamp"]
        for item in self.current_sensors_legend:
            headers.append(item["name"])
        writer.writerow(headers)
        for row in self.chart_data:
            csv_row = [row["name"]]
            for item in self.current_sensors_legend:
                key = item["data_key"]
                csv_row.append(row.get(key, ""))
            writer.writerow(csv_row)
        return rx.download(
            data=output.getvalue(),
            filename=f"sensor_data_{self.start_date}_to_{self.end_date}.csv",
        )

    @rx.event
    def download_json(self):
        """Generate and download JSON export."""
        if not self.chart_data:
            return rx.toast.error("No data to export.")
        data_export = {
            "period": {"start": self.start_date, "end": self.end_date},
            "sensors": [s["name"] for s in self.current_sensors_legend],
            "data": self.chart_data,
            "statistics": self.sensor_stats,
        }
        return rx.download(
            data=json.dumps(data_export, indent=2),
            filename=f"sensor_data_{self.start_date}_to_{self.end_date}.json",
        )