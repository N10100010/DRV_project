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
        "display_name": "Lightweight Women"s Single Sculls",
        "races": [
          { "id": 187573, "display_name": "Final FB" },
          { "id": 424754, "display_name": "Heat 1" }
        ]
      },
      {
        "id": 748394,
        "display_name": "Men"s Four",
        "races": [
          { "id": 195638, "display_name": "Men"s Eight Heat 1" },
          { "id": 823759, "display_name": "Men"s Eight Final FA" },
          { "id": 748394, "display_name": "Men"s Eight Repechage" },
          { "id": 839473, "display_name": "Men"s Eight Heat 2" }
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
* Rückstand über Distanz [m] fehlt noch; auf welcher Grunddeficite sollen wir das berechnen können? Haben ja nur 
Speed/Stroke in GPS Daten und keine genauen Strecken. Auch das zurückrechnen via s = v * t wäre schwierig, weil Werte fehlen.
* propulsion soll Vortrieb heißen; wer ein besseres englisches Wort dafür kennt, gerne her damit :D
* deficit = Rückstand

* UPDATE: Disziplin hinzugefügt (!) soll sowas wie Steuermann/Steuerfrau etc. darstellen
* UPDATE: pdf_urls hinzugefügt (!)
```json
[
  {
    "raceId": 195638,
    "displayName": "Men's Eight Heat 1",
    "startDate": "2022-06-16 14:12:00",
    "venue": "Malta/Poznan, Poland",
    "boatClass": "Men's Eight",
    "worldBestTimeBoatClass": "00:05:58,36",
    "bestTimeBoatClassCurrentOZ": "00:05:58,36",
    "pdf_urls": {
      "result": "https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/WCH_2018/WCH_2018_ROWWSCULL2------------HEAT000100--_C73X7962.PDF",
      "race_data": "https://d3fpn4c9813ycf.cloudfront.net/pdfDocuments/ECM2022/ECM2022_ROWXSCULL2--PR2-------PREL000100--_C77X3426.PDF"
    },
    "data": [
      {
        "nationIoc": "CZE",
        "nationDisplayName": "Tschechien",
        "lane": 2,
        "rank": 1,
        "run": "FB",
        "progressionCode": "1-3SA/B 4..SC/D",
        "athletes": [
          {
            "id": 98245435,
            "firstName": "Lukas",
            "lastName": "Helesic",
            "discipline": "b"
          },
          {
            "id": 954345365,
            "firstName": "S Jakub",
            "lastName": "Podrazil",
            "discipline": "b"
          }
        ],
        "intermediates": {
            "500": {
              "time [t]": "00:02:24,12",
              "pace [t]": "00:02:24,12",
              "rank": 2,
              "deficit [s]": "00:00:03,12",
              "relDiffToAvgSpeed [%]": -1.3
            },
            "1000": {
              "time [t]": "00:03:13,82",
              "pace [t]": "00:01:50,72",
              "rank": 1,
              "deficit [s]": "00:00:00,00",
              "relDiffToAvgSpeed [%]": 4.3
            },
            "1500": {
                "time [t]": "00:04:52,00",
                "pace [t]": "00:01:50,72",
                "rank": 1,
                "deficit [s]": "00:00:00,00",
                "relDiffToAvgSpeed [%]": 2.3
              },
            "2000": {
                  "time [t]": "00:06:29,14",
                  "pace [t]": "00:01:50,72",
                  "rank": 1,
                  "deficit [s]": "00:00:00,00",
                  "relDiffToAvgSpeed [%]": 1.3
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
              "speed [m/s]": 4.7,
              "stroke [1/min]": 35.0,
              "propulsion [m/stroke]": 7.1
            },
            "200": {
              "speed [m/s]": 4.6,
              "stroke [1/min]": 38.0,
              "propulsion [m/stroke]": 8.1
            },
            "250": {
              "speed [m/s]": 4.9,
              "stroke [1/min]": 32.0,
              "propulsion [m/stroke]": 7.2
            }
          }
        }
      }
    ]
  }
]
```


# User Story für Wettkampfresultate analog zu Rennstrukturanalyse

Einziger Unterschied wäre, dass zusätzlich die folgenden zwei Daten integriert werden:
* Rückstand_Sieger (in Sekunden?)
* %_aktuelle Weltbestzeit Bootsklasse


# User Story für Berichte

Als User möchte ich Zusammenfassungen von Fahrzeiten als statistisches Maß über einen gegebenen Zeitraum betrachten.

## User: Bekommt direkt Tabelle mit Daten gezeigt (default Filter zunächst wie bei u-row)
**Request**

```http
GET /get_report_filter_options
```
**Response** (JSON mit möglichen Filtern)
```json
[
  {"year": [{"start_year": 1950}, {"end_year": 2025}],
            "boat_class": {
                "men": {
                    "junior": {
                        "single": {"JM1x": "Junior Men's Single Sculls"},
                        "double": {"JM2x": "Junior Men's Double Sculls"},
                        "quad": {"JM4x": "Junior Men's Quadruple Sculls"},
                        "pair": {"JM2-": "Junior Men's Pair"},
                        "coxed_four": {"JM4+": "Junior Men's Coxed Four"},
                        "four": {"JM4-": "Junior Men's Four"} ,
                        "eight": {"JM8-": "Junior Men's Eight"}
                    },
                    "u19": {},
                    "u23": {
                        "single": {"BM1x": "U23 Men's Single Sculls"},
                        "double": {"BM2x": "U23 Men's Double Sculls"},
                        "quad": {"BM4x": "U23 Men's Quadruple Sculls"},
                        "pair": {"BM2-": "U23 Men's Pair"},
                        "coxed_four": {"BM4+": "U23 Men's Coxed Four"},
                        "four": {"BM4-": "U23 Men's Four"},
                        "eight": {"BM8+": "U23 Men's Eight"},
                        "lw_single": {"BLM1x": "U23 Lightweight Men's Single Sculls"},
                        "lw_double": {"BLM2x": "U23 Lightweight Men's Double Sculls"},
                        "lw_quad": {"BLM4x": "U23 Lightweight Men's Quadruple Sculls"},
                        "lw_pair": {"BLM2-": "U23 Lightweight Men's Pair"},
                    },
                    "adult": {
                        "single": {"M1x": "Men's Single Sculls"},
                        'double': {"M2x": "Men's Double Sculls"},
                        'quad': {"M4x": "Men's Quadruple Sculls"},
                        'pair': {"M2-": "Men's Pair"},
                        'four': {"M4-": "Men's Four"},
                        'eight': {"M8+": "Men's Eight"},
                        'lw_single': {"LM1x": "Lightweight Men's Single Sculls"},
                        'lw_double': {"LM2x": "Lightweight Men's Double Sculls"},
                        'lw_quad': {"LM4x": "Lightweight Men's Quadruple Sculls"},
                        'lw_pair': {"LM2-": "Lightweight Men's Pair"},
                    },
                    'pr': {
                        '1': {"PR1 M1x": "PR1 Men's Single Sculls"},
                        '2': {"PR2 M1x": "PR2 Men's Single Sculls"},
                        '3': {"PR3 M2-": "PR3 Men's Pair"}
                    }
                },
                'women': {
                    'junior': {
                        'single': {"JW1x": "Junior Women's Single Sculls"},
                        'double': {"JW2x": "Junior Women's Double Sculls"},
                        'quad': {"JW4x": "Junior Women's Quadruple Sculls"},
                        'pair': {"JW2-": "Junior Women's Pair"},
                        'coxed_four': {"JW4+": "Junior Women's Coxed Four"},
                        'four': {"JW4-": "Junior Women's Four"} ,
                        'eight': {"JW8-": "Junior Women's Eight"}
                    },
                    'u19': {},
                    'u23': {
                        'single': {"BW1x": "U23 Women's Single Sculls"},
                        'double': {"BW2x": "U23 Women's Double Sculls"},
                        'quad': {"BW4x": "U23 Women's Quadruple Sculls"},
                        'pair': {"BW2-": "U23 Women's Pair"},
                        'coxed_four': {"BW4+": "U23 Women's Coxed Four"},
                        'four': {"BW4-": "U23 Women's Four"},
                        'eight': {"BW8+": "U23 Women's Eight"},
                        'lw_single': {"BLW1x": "U23 Lightweight Women's Single Sculls"},
                        'lw_double': {"BLW2x": "U23 Lightweight Women's Double Sculls"},
                        'lw_quad': {"BLW4x": "U23 Lightweight Women's Quadruple Sculls"},
                        'lw_pair': {"BLW2-": "U23 Lightweight Women's Pair"},
                    },
                    'adult': {
                        'single': {"W1x": "Women's Single Sculls"},
                        'double': {"W2x": "Women's Double Sculls"},
                        'quad': {"W4x": "Women's Quadruple Sculls"},
                        'pair': {"W2-": "Women's Pair"},
                        'four': {"W4-": "Women's Four"},
                        'eight': {"W8+": "Women's Eight"},
                        'lw_single': {"LW1x": "Lightweight Women's Single Sculls"},
                        'lw_double': {"LW2x": "Lightweight Women's Double Sculls"},
                        'lw_quad': {"LW4x": "Lightweight Women's Quadruple Sculls"},
                        'lw_pair': {"LW2-": "Lightweight Women's Pair"},
                    },
                    'pr': {
                        '1': {"PR1 W1x": "PR1 Women's Single Sculls"},
                        '2': {"PR2 W1x": "PR2 Women's Single Sculls"},
                        '3': {"PR3 W2-": "PR3 Women's Pair"}
                    }
                },
                'mixed': {
                    'double_2': {"PR2 Mix2x": "PR2 Mixed Double Sculls"},
                    'double_3': {"PR3 Mix2x": "PR3 Mixed Double Sculls"},
                    'four': {"PR3 Mix4+": "PR3 Mixed Coxed Four"},
                }
            },
            "competition_category_ids": [
                {"displayName":  "Olympics", "id": "89346342"},
                {"displayName":  "World Rowing Championships", "id": "89346362"},
                {"displayName":  "Qualifications", "id": "89346362"},
            ],
            "runs": {
                "finale": [
                    {"displayName": "fa"},
                    {"displayName": "fb"},
                    {"displayName": "fc"},
                    {"displayName": "fd"},
                    {"displayName": "f..."}
                ],
                "halbfinale": [
                    {"displayName": "sa/b, sa/b/c"},
                    {"displayName": "sc/d, sd/e/f"},
                    {"displayName": "s..."}
                ],
                "viertelfinale": [
                    {"displayName": "q1-4"},
                ],
                "hoffnungslaeufe": null,
                "vorlaeufe": null,
            },
            "ranks": ["1", "2", "3", "4-6"],
        }]
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
Hier nur mal sinngemäß: Es sollen jeweils Listen übergeben, die alle ausgewählten Filtermöglichkeiten abbilden.
Per default sind vorraussichtlich einige Kriterien gesetzt: z.B. alle möglichen competition_category_ids.
Bei groups (meint Altersgruppen bzw. elite, para etc.) und runs macht es ggf. auch Sinn mit IDs anstelle der Klarnamen zu arbeiten.
```json
{
  "years": {
    "start_year": 2010, 
    "end_year": 2016
  },
  "competition_category_ids": ["38666", "27396", "86122"],
  "boat_classes": ["9845666", "83947534", "839405354"],
  "runs": ["FA", "FB", "FC", "FD", "SA/B"],
  "ranks": ["1", "2", "3", "4-6"]
}
```

Damit wir den Fall abgebildet haben, in dem alle Bootsklassen ausgewählt werden brauchen wir 
wahrscheinlich eine Fallunterscheidung, die wie folgt aussehen könnte...

**Response (Fall Einzelne Bootsklasse ausgewählt)**

* results = Anzahl der Treffer (n)

```json
[
  {
    "filter_selection": {
      "start_date": "2020-06-16 14:12:00",
      "end_date": "2022-06-16 14:12:00"
    },
    "data": [
      {
        "results": 872,
        "boat_class": "Men's Eight",
        "world_best_time_boat_class": "00:05:58,36",
        "best_in_period": "00:05:58,36",
        "mean": {
          "mm:ss,00": "00:05:58,36",
          "m/s": 4.54,
          "pace 500m": "00:02:05,40",
          "pace 1000m": "00:02:05,40"
        },
        "std_dev": "00:00:23,42",
        "median": "00:05:32,36",
        "gradation_fastest": {
          "no_of_samples": 345,
          "time": "00:06:06,36"
        },
        "gradation_medium": {
          "no_of_samples": 239,
          "time": "00:06:13,52"
        },
        "gradation_slow": {
          "no_of_samples": 167,
          "time": "00:07:52,37"
        },
        "gradation_slowest": {
          "no_of_samples": 463,
          "time": "00:08:04,62"
        },
        "plot_data": {
          "histogram": {
            "labels": [
              "00:06:34",
              "00:06:36",
              "00:06:38",
              "00:06:40",
              "00:06:42",
              "00:06:44",
              "00:06:46",
              "00:06:48",
              "00:06:50",
              "00:06:52",
              "00:06:54",
              "00:06:56",
              "00:06:58",
              "00:07:00",
              "00:07:02",
              "00:07:04",
              "00:07:06",
              "00:07:08"
            ],
            "data": [
              20,
              26,
              45,
              180,
              503,
              98,
              55,
              23,
              16,
              4,
              2,
              3,
              1,
              3,
              1,
              4,
              3,
              2
            ]
          },
          "scatterPlot": {
            "labels": [
              "1930-01-01",
              "1940-01-01",
              "1950-01-01",
              "1960-01-01",
              "1970-01-01",
              "1980-01-01",
              "1990-01-01",
              "2000-01-01",
              "2010-01-01",
              "2020-01-01"
            ],
            "data": [
              "00:06:54",
              "00:06:53",
              "00:06:55",
              "00:06:50",
              "00:06:48",
              "00:06:43",
              "00:06:46",
              "00:06:40",
              "00:06:39",
              "00:06:40"
            ]
          }
        }
      }
    ]
  }
]
```

**Response (Generischer Fall: Alle Bootsklassen ausgewählt)**

* results = Anzahl der Treffer (n)
* Nur Tabelle, daher keine Plot Daten
* im Data Key kommen dann für jede Bootsklasse jeweils ein Objekt mit den Daten

```json
[
  {
    "filter_selection": {
      "start_date": "2020-06-16 14:12:00",
      "end_date": "2022-06-16 14:12:00"
    },
    "data": [
      {
      "results": 872,
      "boat_class": {
        "id": 98345325,
        "display_name": "M8"
      },
      "world_best_time_boat_class": "00:05:58,36",
      "best_in_period": "00:05:58,36",
      "mean": {
        "mm:ss,00": "00:05:58,36",
        "m/s": 4.54,
        "pace 500m": "00:02:05,40",
        "pace 1000m": "00:02:05,40"
      },
      "std_dev": "00:00:23,42",
      "median": "00:05:32,36",
      "gradation_fastest": {
        "no_of_samples": 345,
        "time": "00:06:06,36"
      },
      "gradation_medium": {
        "no_of_samples": 239,
        "time": "00:06:13,52"
      },
      "gradation_slow": {
        "no_of_samples": 167,
        "time": "00:07:52,37"
      },
      "gradation_slowest": {
        "no_of_samples": 463,
        "time": "00:08:04,62"
      }
    },
      {
    "results": 672,
    "boat_class": {
      "id": 53245325,
      "display_name": "M2+"
    },
    "world_best_time_boat_class": "00:05:58,36",
    "best_in_period": "00:05:58,36",
    "mean": {
      "mm:ss,00": "00:05:58,36",
      "m/s": 4.54,
      "pace 500m": "00:02:05,40",
      "pace 1000m": "00:02:05,40"
    },
    "std_dev": "00:00:23,42",
    "median": "00:05:32,36",
    "gradation_fastest": {
      "no_of_samples": 345,
      "time": "00:06:06,36"
    },
    "gradation_medium": {
      "no_of_samples": 239,
      "time": "00:06:13,52"
    },
    "gradation_slow": {
      "no_of_samples": 167,
      "time": "00:07:52,37"
    },
    "gradation_slowest": {
      "no_of_samples": 463,
      "time": "00:08:04,62"
    }
  }]
  }
]
```


# User Story für Medaillenspiegel

Als User möchte ich eine Übersicht der Medailienspiegel und eine Darstellung im Längsschnitt.

**Request**

```http
GET /get_medaillenspiegel_filter_options
```
**Response** (JSON mit möglichen Filtern)

```json
[
  {
    "year": {
      "start_year": 1950,
      "end_year": 2025
    },
    "boat_class": {
      "men": {
        "junior": {
          "single": {
            "JM1x": "Junior Men's Single Sculls"
          },
          "double": {
            "JM2x": "Junior Men's Double Sculls"
          },
          "quad": {
            "JM4x": "Junior Men's Quadruple Sculls"
          },
          "pair": {
            "JM2-": "Junior Men's Pair"
          },
          "coxed_four": {
            "JM4+": "Junior Men's Coxed Four"
          },
          "four": {
            "JM4-": "Junior Men's Four"
          },
          "eight": {
            "JM8-": "Junior Men's Eight"
          }
        },
        "u19": {
        },
        "u23": {
          "single": {
            "BM1x": "U23 Men's Single Sculls"
          },
          "double": {
            "BM2x": "U23 Men's Double Sculls"
          },
          "quad": {
            "BM4x": "U23 Men's Quadruple Sculls"
          },
          "pair": {
            "BM2-": "U23 Men's Pair"
          },
          "coxed_four": {
            "BM4+": "U23 Men's Coxed Four"
          },
          "four": {
            "BM4-": "U23 Men's Four"
          },
          "eight": {
            "BM8+": "U23 Men's Eight"
          },
          "lw_single": {
            "BLM1x": "U23 Lightweight Men's Single Sculls"
          },
          "lw_double": {
            "BLM2x": "U23 Lightweight Men's Double Sculls"
          },
          "lw_quad": {
            "BLM4x": "U23 Lightweight Men's Quadruple Sculls"
          },
          "lw_pair": {
            "BLM2-": "U23 Lightweight Men's Pair"
          }
        },
        "adult": {
          "single": {
            "M1x": "Men's Single Sculls"
          },
          "double": {
            "M2x": "Men's Double Sculls"
          },
          "quad": {
            "M4x": "Men's Quadruple Sculls"
          },
          "pair": {
            "M2-": "Men's Pair"
          },
          "four": {
            "M4-": "Men's Four"
          },
          "eight": {
            "M8+": "Men's Eight"
          },
          "lw_single": {
            "LM1x": "Lightweight Men's Single Sculls"
          },
          "lw_double": {
            "LM2x": "Lightweight Men's Double Sculls"
          },
          "lw_quad": {
            "LM4x": "Lightweight Men's Quadruple Sculls"
          },
          "lw_pair": {
            "LM2-": "Lightweight Men's Pair"
          }
        },
        "pr": {
          "1": {
            "PR1 M1x": "PR1 Men's Single Sculls"
          },
          "2": {
            "PR2 M1x": "PR2 Men's Single Sculls"
          },
          "3": {
            "PR3 M2-": "PR3 Men's Pair"
          }
        }
      },
      "women": {
        "junior": {
          "single": {
            "JW1x": "Junior Women's Single Sculls"
          },
          "double": {
            "JW2x": "Junior Women's Double Sculls"
          },
          "quad": {
            "JW4x": "Junior Women's Quadruple Sculls"
          },
          "pair": {
            "JW2-": "Junior Women's Pair"
          },
          "coxed_four": {
            "JW4+": "Junior Women's Coxed Four"
          },
          "four": {
            "JW4-": "Junior Women's Four"
          },
          "eight": {
            "JW8-": "Junior Women's Eight"
          }
        },
        "u19": {
        },
        "u23": {
          "single": {
            "BW1x": "U23 Women's Single Sculls"
          },
          "double": {
            "BW2x": "U23 Women's Double Sculls"
          },
          "quad": {
            "BW4x": "U23 Women's Quadruple Sculls"
          },
          "pair": {
            "BW2-": "U23 Women's Pair"
          },
          "coxed_four": {
            "BW4+": "U23 Women's Coxed Four"
          },
          "four": {
            "BW4-": "U23 Women's Four"
          },
          "eight": {
            "BW8+": "U23 Women's Eight"
          },
          "lw_single": {
            "BLW1x": "U23 Lightweight Women's Single Sculls"
          },
          "lw_double": {
            "BLW2x": "U23 Lightweight Women's Double Sculls"
          },
          "lw_quad": {
            "BLW4x": "U23 Lightweight Women's Quadruple Sculls"
          },
          "lw_pair": {
            "BLW2-": "U23 Lightweight Women's Pair"
          }
        },
        "adult": {
          "single": {
            "W1x": "Women's Single Sculls"
          },
          "double": {
            "W2x": "Women's Double Sculls"
          },
          "quad": {
            "W4x": "Women's Quadruple Sculls"
          },
          "pair": {
            "W2-": "Women's Pair"
          },
          "four": {
            "W4-": "Women's Four"
          },
          "eight": {
            "W8+": "Women's Eight"
          },
          "lw_single": {
            "LW1x": "Lightweight Women's Single Sculls"
          },
          "lw_double": {
            "LW2x": "Lightweight Women's Double Sculls"
          },
          "lw_quad": {
            "LW4x": "Lightweight Women's Quadruple Sculls"
          },
          "lw_pair": {
            "LW2-": "Lightweight Women's Pair"
          }
        },
        "pr": {
          "1": {
            "PR1 W1x": "PR1 Women's Single Sculls"
          },
          "2": {
            "PR2 W1x": "PR2 Women's Single Sculls"
          },
          "3": {
            "PR3 W2-": "PR3 Women's Pair"
          }
        }
      },
      "mixed": {
        "double_2": {
          "PR2 Mix2x": "PR2 Mixed Double Sculls"
        },
        "double_3": {
          "PR3 Mix2x": "PR3 Mixed Double Sculls"
        },
        "four": {
          "PR3 Mix4+": "PR3 Mixed Coxed Four"
        }
      }
    },
    "competition_category_ids": [
      {
        "displayName": "Olympics",
        "id": "89346342"
      },
      {
        "displayName": "World Rowing Championships",
        "id": "89346362"
      },
      {
        "displayName": "Qualifications",
        "id": "89346362"
      }
    ],
    "nations": {
      "AFG": "Afghanistan",
      "ALB": "Albanien",
      "ALG": "Algerien",
      "AND": "Andorra",
      "ANG": "Angola",
      "ANT": "Antigua und Barbuda",
      "ARG": "Argentinien",
      "ARM": "Armenien",
      "ARU": "Aruba",
      "ASA": "Amerikanisch Samoa",
      "AUS": "Australien",
      "AUT": "Österreich",
      "AZE": "Aserbaidschan",
      "BAH": "Bahamas",
      "BAN": "Bangladesch",
      "BAR": "Barbados",
      "BDI": "Burundi",
      "BEL": "Belgien",
      "BEN": "Benin",
      "BER": "Bermuda",
      "BHU": "Bhutan",
      "BIH": "Bosnien und Herzegowina",
      "BIZ": "Belize",
      "BLR": "Belarus",
      "BOL": "Bolivien",
      "BOT": "Botswana",
      "BRA": "Brasilien",
      "BRN": "Bahrain",
      "BRU": "Brunei",
      "BUL": "Bulgarien",
      "BUR": "Burkina Faso",
      "CAF": "Zentralafrikanische Republik",
      "CAM": "Kambodscha",
      "CAN": "Kanada",
      "CAY": "Kaimaninseln",
      "CGO": "Republik Kongo",
      "CHA": "Tschad",
      "CHI": "Chile",
      "CHN": "China",
      "CIV": "Elfenbeinküste",
      "CMR": "Kamerun",
      "COD": "Demokratische Republik Kongo",
      "COK": "Cookinseln",
      "COL": "Kolumbien",
      "COM": "Komoren",
      "CPV": "Kap Verde",
      "CRC": "Costa Rica",
      "CRO": "Kroatien",
      "CUB": "Kuba",
      "CYP": "Zypern",
      "CZE": "Tschechien",
      "DEN": "Dänemark",
      "DJI": "Dschibuti",
      "DMA": "Dominica",
      "DOM": "Dominikanische Republik",
      "ECU": "Ecuador",
      "EGY": "Ägypten",
      "ERI": "Eritrea",
      "ESA": "El Salvador",
      "ESP": "Spanien",
      "EST": "Estland",
      "ETH": "Äthiopien",
      "FIJ": "Fidschi",
      "FIN": "Finnland",
      "FRA": "Frankreich",
      "FSM": "Föderierte Staaten von Mikronesien",
      "GAB": "Gabun",
      "GAM": "Gambia",
      "GBR": "Vereinigtes Königreich",
      "GBS": "Guinea-Bissau",
      "GEO": "Georgien",
      "GEQ": "Äquatorialguinea",
      "GER": "Deutschland",
      "GHA": "Ghana",
      "GRE": "Griechenland",
      "GRN": "Grenada",
      "GUA": "Guatemala",
      "GUI": "Guinea",
      "GUM": "Guam",
      "GUY": "Guyana",
      "HAI": "Haiti",
      "HKG": "Hongkong",
      "HON": "Honduras",
      "HUN": "Ungarn",
      "INA": "Indonesien",
      "IND": "Indien",
      "IRI": "Iran",
      "IRL": "Irland",
      "IRQ": "Irak",
      "ISL": "Island",
      "ISR": "Israel",
      "ISV": "Jungferninseln (US)",
      "ITA": "Italien",
      "IVB": "Jungferninseln (UK)",
      "JAM": "Jamaika",
      "JOR": "Jordanien",
      "JPN": "Japan",
      "KAZ": "Kasachstan",
      "KEN": "Kenia",
      "KGZ": "Kirgisistan",
      "KIR": "Kiribati",
      "KOR": "Südkorea",
      "KOS": "Kosovo",
      "KSA": "Saudi-Arabien",
      "KUW": "Kuwait",
      "LAO": "Laos",
      "LAT": "Lettland",
      "LBA": "Libyen",
      "LBN": "Libanon",
      "LBR": "Liberia",
      "LCA": "St. Lucia",
      "LES": "Lesotho",
      "LIE": "Liechtenstein",
      "LTU": "Litauen",
      "LUX": "Luxemburg",
      "MAD": "Madagaskar",
      "MAR": "Marokko",
      "MAS": "Malaysia",
      "MAW": "Malawi",
      "MDA": "Moldawien",
      "MDV": "Malediven",
      "MEX": "Mexiko",
      "MGL": "Mongolei",
      "MHL": "Marshallinseln",
      "MKD": "Nordmazedonien",
      "MLI": "Mali",
      "MLT": "Malta",
      "MNE": "Montenegro",
      "MON": "Fürstentum Monaco",
      "MOZ": "Mosambik",
      "MRI": "Mauritius",
      "MTN": "Mauretanien",
      "MYA": "Myanmar",
      "NAM": "Namibia",
      "NCA": "Nicaragua",
      "NED": "Niederlande",
      "NEP": "Nepal",
      "NGR": "Nigeria",
      "NIG": "Niger",
      "NOR": "Norwegen",
      "NRU": "Nauru",
      "NZL": "Neuseeland",
      "OMA": "Oman",
      "PAK": "Pakistan",
      "PAN": "Panama",
      "PAR": "Paraguay",
      "PER": "Peru",
      "PHI": "Philippinen",
      "PLE": "Palästina",
      "PLW": "Palau",
      "PNG": "Papua-Neuguinea",
      "POL": "Polen",
      "POR": "Portugal",
      "PRK": "Nordkorea",
      "PUR": "Puerto Rico",
      "QAT": "Katar",
      "ROU": "Rumänien",
      "RSA": "Südafrika",
      "RUS": "Russland",
      "RWA": "Ruanda",
      "SAM": "Samoa",
      "SEN": "Senegal",
      "SEY": "Seychellen",
      "SGP": "Singapur",
      "SKN": "St. Kitts und Nevis",
      "SLE": "Sierra Leone",
      "SLO": "Slowenien",
      "SMR": "San Marino",
      "SOL": "Salomonen",
      "SOM": "Somalia",
      "SRB": "Serbien",
      "SRI": "Sri Lanka",
      "STP": "São Tomé und Príncipe",
      "SUD": "Sudan",
      "SUI": "Schweiz",
      "SUR": "Suriname",
      "SVK": "Slowakei",
      "SWE": "Schweden",
      "SWZ": "Eswatini",
      "SYR": "Syrien",
      "TAN": "Tansania",
      "TGA": "Tonga",
      "THA": "Thailand",
      "TJK": "Tadschikistan",
      "TKM": "Turkmenistan",
      "TLS": "Osttimor",
      "TOG": "Togo",
      "TPE": "Taiwan",
      "TTO": "Trinidad und Tobago",
      "TUN": "Tunesien",
      "TUR": "Türkei",
      "TUV": "Tuvalu",
      "UAE": "Vereinigte Arabische Emirate",
      "UGA": "Uganda",
      "UKR": "Ukraine",
      "URU": "Uruguay",
      "USA": "Vereinigte Staaten von Amerika",
      "UZB": "Usbekistan",
      "VAN": "Vanuatu",
      "VEN": "Venezuela",
      "VIE": "Vietnam",
      "VIN": "St. Vincent und die Grenadinen",
      "YEM": "Jemen",
      "ZAM": "Sambia",
      "ZIM": "Simbabwe",
      "RPC": null
    },
    "medal_types": [
      {
        "displayName": "Gesamt",
        "id": "0"
      },
      {
        "displayName": "Olympisch",
        "id": "1"
      },
      {
        "displayName": "Nicht-Olympisch",
        "id": "2"
      }
    ],
    "medal_bar_chart_data": {
      "labels": [
        "Gold",
        "Silber",
        "Bronze",
        "Gesamt"
      ],
      "data": [
        4,
        5,
        1,
        10
      ]
    }
  }
]
```

**Request**
Anfrage die Daten bzgl. Medaillenspiegel liefert...
```http
POST /get_medaillenspiegel
```
Request Body (bei nations und medal types wahrscheinlich auch eher id?)
```json
[
  {
    "year": {
      "start_year": 1950,
      "end_year": 2025
    },
    "boat_classes": ["8350353"],
    "competition_category_ids": ["89346342", "89346362", "89346362"],
    "nations": ["AUS"],
    "medal_types": ["Olympisch"]
  }
]
```

**Response**
Datentypen/Format unklar (klären wir mit DRV): rank, points, final_a und final_b

```json
[
  {
    "filter_selection": {
      "start_date": "2020-06-16 14:12:00",
      "end_date": "2022-06-16 14:12:00",
      "nations": "AUS"
    },
    "data": [
      {
        "results": 872,
        "medals_gold": 5,
        "medals_silver": 5,
        "medals_bronze": 5,
        "medals_total": 15,
        "rank": {
          "gold": 500,
          "silver": 400,
          "bronze": 300
        },
        "points": 700,
        "final_a": true,
        "final_b": false
      }
    ]
  }
]
```


## Home/Allgemeines
**Request**

Anfrage für Kalenderdaten auf der Startseite. Liefert array mit Kalendereinträgen.
```http
POST /get_calender
```
**Response**
```json
{
  "calender_data": [
    {
      "key": 1,
      "customData": {
        "title": "Olympics"
      }, 
      "dates": {
        "start": "2023-01-17 14:00:0",
        "end": "2023-01-19 14:00:00"
      }
    }
  ]
}
```