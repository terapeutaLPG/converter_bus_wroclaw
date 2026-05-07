Oto dokładny plik `README.md` dla Twojego kodu:

```markdown
# GTFS to JSON - Przetwarzanie linii autobusowych

Skrypt do przetwarzania danych GTFS (General Transit Feed Specification) i wyodrębniania informacji o liniach autobusowych (route_type = 3) do formatu JSON.

## 📋 Wymagania

- Python 3.7+
- Pandas
- Pathlib (wbudowane)

### Instalacja zależności

```bash
pip install pandas
```

## 🚀 Użycie

1. Umieść pliki GTFS w katalogu głównym skryptu:
   - `routes.txt` (wymagany)
   - `trips.txt` (wymagany)
   - `stop_times.txt` (wymagany)
   - `stops.txt` (wymagany)
   - `calendar.txt` (opcjonalny)
   - `calendar_dates.txt` (opcjonalny)

2. Uruchom skrypt:

```bash
python script.py
```

## 📁 Struktura wejściowa (GTFS)

Skrypt oczekuje następujących plików GTFS w bieżącym katalogu:

| Plik | Wymagany | Opis |
|------|----------|------|
| `routes.txt` | ✅ | Informacje o liniach komunikacyjnych |
| `trips.txt` | ✅ | Kursy dla poszczególnych linii |
| `stop_times.txt` | ✅ | Czasy przyjazdów/odjazdów na przystankach |
| `stops.txt` | ✅ | Lokalizacje i nazwy przystanków |
| `calendar.txt` | ❌ | Regularne rozkłady jazdy |
| `calendar_dates.txt` | ❌ | Wyjątki w rozkładach |

## 📂 Struktura wyjściowa

```
output/transit/
├── bus_meta.json              # Metadane o przetwarzaniu
├── bus_services.json          # Kalendarze kursowania
├── bus_routes_index.json      # Indeks wszystkich linii
└── buses/                     # Folder z danymi linii
    ├── line_100.json
    ├── line_101.json
    └── ...
```

## 📄 Opis plików wyjściowych

### 1. `bus_meta.json`
Metadane dotyczące źródła danych i przetwarzania:

```json
{
  "source_format": "GTFS",
  "vehicle_type": "bus",
  "route_type": "3",
  "calendar_included": true,
  "calendar_dates_included": true
}
```

### 2. `bus_services.json`
Informacje o kalendarzach kursowania (service_id):

```json
{
  "service_id_1": {
    "service_id": "1",
    "monday": "1",
    "tuesday": "1",
    "wednesday": "1",
    "thursday": "1",
    "friday": "1",
    "saturday": "0",
    "sunday": "0",
    "start_date": "20240101",
    "end_date": "20241231",
    "exceptions": []
  }
}
```

### 3. `bus_routes_index.json`
Indeks wszystkich przetworzonych linii:

```json
{
  "100": {
    "line": "100",
    "file": "buses/line_100.json",
    "trips_count": 42
  }
}
```

### 4. Pliki linii (`buses/line_XXX.json`)
Szczegółowe dane dla konkretnej linii:

```json
{
  "line": "100",
  "trips": [
    {
      "trip_id": "trip_001",
      "direction_id": "0",
      "headsign": "Dworzec Główny",
      "service_id": "weekdays",
      "stops": [
        {
          "stop_sequence": 1,
          "stop_id": "stop_001",
          "stop_name": "Przystanek A",
          "arrival_time": "06:00:00",
          "departure_time": "06:00:00",
          "lat": 52.123456,
          "lon": 21.123456
        }
      ]
    }
  ]
}
```

## 🔧 Dostosowanie

### Zmiana katalogów źródłowych i wyjściowych

Edytuj zmienne na początku skryptu:

```python
GTFS_DIR = Path(".")           # Katalog z plikami GTFS
OUT_DIR = Path("output/transit")  # Katalog wyjściowy
```

### Zmiana typu pojazdu

Skrypt domyślnie filtruje `route_type == "3"` (autobusy). Aby zmienić typ:

```python
bus_routes = routes[routes["route_type"] == "3"]  # Zmień "3" na inny typ
```

Typowe wartości `route_type` w GTFS:
- `0` – Tramwaj
- `1` – Metro
- `2` – Kolej
- `3` – Autobus
- `4` – Prom
- `5` – Kolej linowa
- `6` – Gondola
- `7` – Funicular

## ⚠️ Obsługa błędów

Skrypt sprawdza istnienie wymaganych plików:
- Brak `routes.txt`, `trips.txt`, `stop_times.txt` lub `stops.txt` → błąd krytyczny
- Brak `calendar.txt` lub `calendar_dates.txt` → kontynuacja bez kalendarzy

## 📊 Informacje zwrotne

Podczas działania skrypt wyświetla:
- Liczbę znalezionych linii autobusowych
- Liczbę kursów
- Liczbę wpisów przystankowych
- Postęp zapisywania poszczególnych linii
- Podsumowanie na końcu

## 📝 Uwagi

- Wszystkie ID (`route_id`, `trip_id`, `stop_id`, `service_id`) są konwertowane na stringi
- Nazwy plików są oczyszczane z niedozwolonych znaków (spacje, `/`, `\`)
- Współrzędne geograficzne są konwertowane na typ float (jeśli dostępne)
- Kolejność przystanków jest zachowana przez sortowanie po `stop_sequence`

## 📄 Licencja

MIT
```

Ten README zawiera wszystkie niezbędne informacje o działaniu skryptu, strukturze danych, wymaganiach i możliwościach dostosowania.