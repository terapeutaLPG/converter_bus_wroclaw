import json
from pathlib import Path

import pandas as pd


GTFS_DIR = Path(".")
OUT_DIR = Path("output/transit")
BUSES_DIR = OUT_DIR / "buses"


def read_txt(name, required=True):
    path = GTFS_DIR / name

    if not path.exists():
        if required:
            raise FileNotFoundError(f"Brakuje wymaganego pliku: {path}")
        return None

    return pd.read_csv(path, dtype=str)


def safe_filename(value):
    return str(value).replace("/", "_").replace("\\", "_").replace(" ", "_")


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BUSES_DIR.mkdir(parents=True, exist_ok=True)

    print("Wczytywanie plików GTFS...")

    routes = read_txt("routes.txt")
    trips = read_txt("trips.txt")
    stop_times = read_txt("stop_times.txt")
    stops = read_txt("stops.txt")

    calendar = read_txt("calendar.txt", required=False)
    calendar_dates = read_txt("calendar_dates.txt", required=False)

    print("Filtrowanie linii autobusowych...")

    routes["route_type"] = routes["route_type"].astype(str).str.strip()
    routes["route_short_name"] = routes["route_short_name"].astype(str).str.strip()
    routes["route_id"] = routes["route_id"].astype(str).str.strip()

    bus_routes = routes[routes["route_type"] == "3"].copy()

    print(f"Liczba linii autobusowych: {bus_routes['route_short_name'].nunique()}")

    bus_trips = trips.merge(
        bus_routes[["route_id", "route_short_name"]],
        on="route_id",
        how="inner"
    )

    print(f"Liczba kursów autobusowych: {len(bus_trips)}")

    print("Łączenie kursów z przystankami i godzinami...")

    data = (
        stop_times
        .merge(bus_trips, on="trip_id", how="inner")
        .merge(stops, on="stop_id", how="left")
    )

    data["stop_sequence_num"] = data["stop_sequence"].astype(int)

    data = data.sort_values(
        ["route_short_name", "trip_id", "stop_sequence_num"]
    )

    print(f"Liczba wpisów przystankowych: {len(data)}")

    print("Przetwarzanie kalendarzy kursowania...")

    calendar_by_service = {}

    if calendar is not None:
        for _, row in calendar.iterrows():
            service_id = str(row["service_id"])

            calendar_by_service[service_id] = {
                "service_id": service_id,
                "monday": row.get("monday"),
                "tuesday": row.get("tuesday"),
                "wednesday": row.get("wednesday"),
                "thursday": row.get("thursday"),
                "friday": row.get("friday"),
                "saturday": row.get("saturday"),
                "sunday": row.get("sunday"),
                "start_date": row.get("start_date"),
                "end_date": row.get("end_date"),
                "exceptions": []
            }

    if calendar_dates is not None:
        for _, row in calendar_dates.iterrows():
            service_id = str(row["service_id"])

            if service_id not in calendar_by_service:
                calendar_by_service[service_id] = {
                    "service_id": service_id,
                    "monday": None,
                    "tuesday": None,
                    "wednesday": None,
                    "thursday": None,
                    "friday": None,
                    "saturday": None,
                    "sunday": None,
                    "start_date": None,
                    "end_date": None,
                    "exceptions": []
                }

            calendar_by_service[service_id]["exceptions"].append({
                "date": row.get("date"),
                "exception_type": row.get("exception_type")
            })

    meta = {
        "source_format": "GTFS",
        "vehicle_type": "bus",
        "route_type": "3",
        "calendar_included": calendar is not None,
        "calendar_dates_included": calendar_dates is not None
    }

    print("Zapisywanie metadanych i kalendarzy...")

    with open(OUT_DIR / "bus_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    with open(OUT_DIR / "bus_services.json", "w", encoding="utf-8") as f:
        json.dump(calendar_by_service, f, ensure_ascii=False, indent=2)

    routes_index = {}

    print("Dzielenie danych na osobne pliki dla każdej linii...")

    for line, line_df in data.groupby("route_short_name"):
        line = str(line)
        safe_line = safe_filename(line)

        route_data = {
            "line": line,
            "trips": []
        }

        for trip_id, trip_df in line_df.groupby("trip_id"):
            first = trip_df.iloc[0]
            service_id = str(first.get("service_id"))

            trip = {
                "trip_id": str(trip_id),
                "direction_id": first.get("direction_id"),
                "headsign": first.get("trip_headsign"),
                "service_id": service_id,
                "stops": []
            }

            for _, row in trip_df.iterrows():
                lat = None
                lon = None

                if pd.notna(row.get("stop_lat")):
                    lat = float(row["stop_lat"])

                if pd.notna(row.get("stop_lon")):
                    lon = float(row["stop_lon"])

                trip["stops"].append({
                    "stop_sequence": int(row["stop_sequence"]),
                    "stop_id": row.get("stop_id"),
                    "stop_name": row.get("stop_name"),
                    "arrival_time": row.get("arrival_time"),
                    "departure_time": row.get("departure_time"),
                    "lat": lat,
                    "lon": lon
                })

            route_data["trips"].append(trip)

        line_file = f"buses/line_{safe_line}.json"

        routes_index[line] = {
            "line": line,
            "file": line_file,
            "trips_count": len(route_data["trips"])
        }

        with open(OUT_DIR / line_file, "w", encoding="utf-8") as f:
            json.dump(route_data, f, ensure_ascii=False, indent=2)

        print(f"Zapisano linię {line}: {line_file}")

    print("Zapisywanie indeksu linii...")

    with open(OUT_DIR / "bus_routes_index.json", "w", encoding="utf-8") as f:
        json.dump(routes_index, f, ensure_ascii=False, indent=2)

    print()
    print("Gotowe.")
    print(f"Folder wyjściowy: {OUT_DIR}")
    print(f"Liczba linii autobusowych: {len(routes_index)}")
    print(f"Liczba service_id: {len(calendar_by_service)}")
    print()
    print("Wygenerowane pliki:")
    print(f"- {OUT_DIR / 'bus_meta.json'}")
    print(f"- {OUT_DIR / 'bus_services.json'}")
    print(f"- {OUT_DIR / 'bus_routes_index.json'}")
    print(f"- {BUSES_DIR}/line_XXX.json")


if __name__ == "__main__":
    main()