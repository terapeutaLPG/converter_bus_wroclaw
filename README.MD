# GTFS to JSON - automatyczna konwersja

Repozytorium konwertuje dane GTFS do plików JSON z rozkładami jazdy autobusów
(`route_type = 3`).

## Jak używać bez uruchamiania programu na komputerze

1. Wejdź na stronę repozytorium na GitHubie.
2. Otwórz folder `input/`. Jeśli go nie ma, utwórz go przy dodawaniu pliku.
3. Wybierz **Add file → Upload files**.
4. Wgraj **jeden plik ZIP** z danymi GTFS, np.
   `OtwartyWroclaw_rozklad_jazdy_GTFS_07112026.zip`.
5. Zatwierdź zmianę przyciskiem **Commit changes** do gałęzi `main`.

Po zatwierdzeniu GitHub Actions automatycznie:

1. wykryje zmianę w `input/`,
2. rozpakowuje ZIP,
3. znajdzie pliki GTFS także wtedy, gdy ZIP zawiera dodatkowy podkatalog,
4. sprawdzi wymagane pliki i uruchomi `convert.py`,
5. zapisze gotowe pliki JSON w `output/transit/`,
6. wykona osobny commit z wygenerowanymi wynikami.

Konwersję można śledzić w zakładce **Actions**. Jeśli pliku brakuje albo format
jest nieprawidłowy, zadanie zakończy się błędem widocznym w logach. W folderze
`input/` powinien znajdować się tylko jeden ZIP.

Nie trzeba pobierać repozytorium ani instalować Pythona na swoim komputerze.

## Jakie dane są wymagane

W ZIP-ie muszą znajdować się:

| Plik | Wymagany | Opis |
|---|---:|---|
| `routes.txt` | tak | informacje o liniach |
| `trips.txt` | tak | kursy |
| `stop_times.txt` | tak | godziny i kolejność przystanków |
| `stops.txt` | tak | przystanki i współrzędne |
| `calendar.txt` | nie | regularne dni kursowania |
| `calendar_dates.txt` | nie | wyjątki od kalendarza |

Pozostałe pliki GTFS mogą pozostać w archiwum, ale ten konwerter ich nie
przetwarza.

## Wynik

Wygenerowane dane znajdują się w `output/transit/`:

```text
output/transit/
├── bus_meta.json
├── bus_services.json
├── bus_routes_index.json
└── buses/
    ├── line_100.json
    ├── line_101.json
    └── ...
```

`bus_routes_index.json` zawiera listę linii i wskazuje plik JSON każdej linii.
Pliki `buses/line_XXX.json` zawierają kursy, przystanki, godziny i współrzędne.

## Ręczne uruchomienie

Można również umieścić wymagane pliki `.txt` bezpośrednio w katalogu głównym
repozytorium i uruchomić:

```bash
python convert.py
```

Wymagany jest Python 3.7+ oraz biblioteka `pandas`:

```bash
pip install pandas
```

## Ważne informacje

- Konwertowane są tylko linie autobusowe z `route_type = 3`.
- Identyfikatory są zapisywane jako tekst.
- Wyniki są sortowane według linii, kursu i kolejności przystanków.
- Workflow uruchamia się również ręcznie z zakładki **Actions** przez
  **Run workflow**.
