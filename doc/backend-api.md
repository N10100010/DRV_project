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
