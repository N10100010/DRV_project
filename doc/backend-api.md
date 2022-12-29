# Backend API

Dokumentation des Backend API Designs

# User Story für Rennstrukturanalyse

Als User möchte ich den Rennverlauf eines einzelnen Rennens analysieren.

## User: Auswahl Navigationspunkt Rennstrukturanalye

**Request**

```http
GET /get_competition_category
```
**Response**

Liefert JSON mit möglichen Wettkampfklassen (DisplayName, ID)

```json
[
  { "id": 2,  "display_name": "Coastal Championships" },
  { "id": 5,  "display_name": "World Rowing Cup" },
  { "id": 1,  "display_name": "Youth Olympic Games" },
  { "id": 77, "display_name": "Indoor Championships" },
  { "id": 8,  "display_name": "European Rowing Championships" },
]
```

## User: Auswahl Jahr (einzeln) und Wettkampfklasse (z.B. Olympics)

**Request**

```http
POST /analysis
```

Bekommt JSON mit Jahreszahl und Wettkampfklasse

```json
{
  "year": 2008,
  "competition_category_id": 5
}
```

**Response**

Liefert JSON mit Competitions (DisplayName, ID, Location, Start/End Date, Altersgruppe, Wettkampfklasse), Events (DisplayName, ID) und Races (DisplayName, ID)

```json
[
  {
    "id": 395871,
    "display_name": "2022 World Rowing Cup II",
    "venue": "Malta/Poznan, Poland",
    "start_date": "2022-06-16 00:00:00",
    "competition_category": "World Rowing Cup",
    "events": [
      {
        "id": 734839,
        "display_name": "Lightweight Women's Single Sculls",
        "races": [
          { "id": 187573, "display_name": "Final FB" },
          { "id": 424754, "display_name": "Heat 1" }
        ]
      },
      {
        "id": 748394,
        "display_name": "Men's Four",
        "races": [
          { "id": 195638, "display_name": "Men's Eight Heat 1" },
          { "id": 823759, "display_name": "Men's Eight Final FA" },
          { "id": 748394, "display_name": "Men's Eight Repechage" },
          { "id": 839473, "display_name": "Men's Eight Heat 2" }
        ]
      }
    ]
  }
]
```

**Request** (nachdem einzelnes Rennen ausgewählt ist)

```http
POST /get_race/<race_id>
```

**Response**
* bestTimeBoatClassCurrentOZ (noch unklar, was das genau sein soll)
* Rückstand über Distanz [m] fehlt noch; auf welcher Grundlage sollen wir das berechnen können? Haben ja nur 
Speed/Stroke in GPS Daten und keine genauen Strecken. Auch das zurückrechnen via s = v * t wäre schwierig, weil Werte fehlen.
* propulsion soll Vortrieb heißen; wer ein besseres englisches Wort dafür kennt, gerne her damit :D
* lag = Rückstand
```json
[
  {
    "race_id": 195638,
    "displayName": "Men's Eight Heat 1",
    "startDate": "2022-06-16 00:00:00",
    "venue": "Malta/Poznan, Poland",
    "boatClass": "M8",
    "worldBestTimeBoatClass": "00:05:58,36",
    "bestTimeBoatClassCurrentOZ": "00:05:58,36",
    "data": [
      {
        "nation_ioc": "DEU",
        "lane": 3,
        "rank": 1,
        "run": "FA",
        "athletes": [
          {
            "firstName": "Athlete first name",
            "lastName": "Athlete last name"
          }
        ],
        "intermediates": {
            "500": {
              "time [t]": "00:02:24,12",
              "pace [t]": "00:02:24,12",
              "rank": 2,
              "lag [s]": "00:00:03,12",
              "relDiffToAvgSpeed [%]": -1.3
            },
            "1000": {
              "time [t]": "00:04:15,82",
              "pace [t]": "00:01:50,72",
              "rank": 1,
              "lag [s]": "00:00:00,00",
              "relDiffToAvgSpeed [%]": 4.3
            }
        },
        "gpsData": {
          "distance": {
            "50": {
              "speed [m/s]": 5.2,
              "stroke [1/min]": 34.1,
              "propulsion [m/stroke]": 8.3
            }, 
            "100": {
              "speed [m/s]": 4.9,
              "stroke [1/min]": 33.4,
              "propulsion [m/stroke]": 8.8
            }, 
            "150": {
              "speed [m/s]": 4.8,
              "stroke [1/min]": 34.0,
              "propulsion [m/stroke]": 8.1
            }
          }
        }
      }
    ]
  }
]
```








# User Story für Berichte

Als User möchte ich Zusammenfassungen von Fahrzeiten als statistisches Maß über einen gegebenen Zeitraum betrachten.

## User: Bekommt direkt Tabelle mit Daten gezeigt (default Filter zunächst wie bei u-row)
**Request**

```http
GET /get_report_filter_options
```
**Response** (JSON mit möglichen Filtern)

Nation IOC eher optional (?) Sonst müsste man komplette Liste mit allen Code/Klartextnamen schicken...
```json
{
  "boat_class": [
    {
      "displayName": "Men Single Sculls", 
      "id": "98132421"
    }
  ],
  "year": [
    {
      "start_year": 1950
    },
    {
      "end_year": 2025
    }
  ],
  "competition_category_ids": [
    { 
      "displayName":  "Olympics", 
      "id": "89346342"
    } 
  ],
  "runs": [
    { 
      "displayName":  "FA", 
      "id": "89346342"
    } 
  ],
  "rank": "1",
  "nation_ioc": "FRA"
}
```

## User: Kann (ausgehend vom Standard-Setting) Filter aktivieren/deaktivieren

**Filter-Optionen im Frontend (Prio von groß nach klein):**
* Altersklasse/Bootsklasse (z.B. U23 Women Double Sculls) --> To discuss: Soll das Filter oder Menüeintrag werden?
* Zeitraum (Start Jahr / End Jahr)
* Wettkampfklasse (z.B. Olympics)
* Lauf (z.B. FA, FB etc.)
* Platzierung (1, 2, 3, 4-6)
* Nation_IOC (Country Code, z.B. FRA) --> hier ist nicht spezifiziert, ob Mehrfachauswahl möglich sein soll...

**Request**

```http
GET /get_report
```
JSON mit Filtern
```json
{
  "boat_class": null // default: alle (z.B. wenn null) oder einzelne z.B. Men Single Sculls (wahrscheinlich als ID)
  "year": [
    { "start_year": 2010 },
    { "end_year": 2016 }
  ],
  "competition_category_ids": ["5", "3", "6"] // default: alle außer Qualifications
  "runs": ["FA", "FB", "FC", "FD", "SA/B" ...] // default: analog zu u-row
  "rank": "1" // Hier mal Typ string weil laut DRV Excel auch "4-6" angegeben werden können soll
}
```

**Response**

JSON mit allen Daten, die für Tabelle relevant sind
```json
{
  "boat_class": null,
  "world_best_time_boat_class": "00:05:02,67",
  "mean": 42,
  "standard_deviation": 5.2,
  ...
  "filter_selection": {
    "year": [
    { "start_year": 2010 },
    { "end_year": 2016 }
  ],
  "competition_category_ids": ["5", "3", "6"],
  "runs": ["FA", "FB", "FC", "FD", "SA/B"],
  "rank": "1" 
  }
}
```
