import axios from "axios";
import { defineStore } from "pinia";

export const useMedaillenspiegelState = defineStore({
    id: "medaillenspiegel",
    state: () => ({
        filterOpen: false,
        filterOptions: [{
            "year": [{"start_year": 1950}, {"end_year": 2025}],
            "boat_class": [
                {"displayName": "Men Single Sculls", "id": "98132421"},
                {"displayName": "Women Single Sculls", "id": "92348234"},
            ],
            "competition_category_ids": [
                {"displayName":  "Olympics", "id": "89346342"},
                {"displayName":  "World Rowing Championships", "id": "89346362"},
                {"displayName":  "Qualifications", "id": "89346362"},
            ],
            "runs": [{"displayName":  "FA", "id": "89346342"}],
            "ranks": ["1", "2", "3", "4-6"],
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
                "SGP": "Singapur", /* SIN */
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
                "TPE": "Taiwan", /* ROC */
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
            }

            /*
            [
                {"displayName": "DEU", "id": "98132421"},
                {"displayName": "FRA", "id": "92348234"},
                {"displayName": "GBR", "id": "92348236"}
            ]
             */
            ,
            "medal_types": [
                {"displayName": "Gesamt", "id": "0"},
                {"displayName": "Olympisch", "id": "1"},
                {"displayName": "Nicht-Olympisch", "id": "2"},
            ]
        }],
        "medal_bar_chart_data": {
            "labels": ["Gold", "Silber", "Bronze", "Gesamt"],
            "data": [4, 5, 1, 10]
        },
        data: [{
            "results": 872,
            "boat_class": "Men's Eight",
            "start_date": "2020-06-16 14:12:00",
            "end_date": "2022-06-16 14:12:00",
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
                    "labels":
                        [
                            "00:06:34", "00:06:36", "00:06:38",
                            "00:06:40", "00:06:42", "00:06:44",
                            "00:06:46", "00:06:48", "00:06:50",
                            "00:06:52", "00:06:54", "00:06:56",
                            "00:06:58", "00:07:00", "00:07:02",
                            "00:07:04", "00:07:06", "00:07:08",
                        ],
                    "data": [20, 26, 45, 180, 503, 98, 55, 23, 16, 4, 2, 3, 1, 3, 1, 4, 3, 2]
                },
                "scatterPlot": {
                    "labels": [
                        '1930-01-01', '1940-01-01', '1950-01-01', '1960-01-01','1970-01-01',
                        '1980-01-01', '1990-01-01', '2000-01-01', '2010-01-01', '2020-01-01',
                    ],
                    "data": [
                        "00:06:54", "00:06:53", "00:06:55", "00:06:50", "00:06:48",
                        "00:06:43", "00:06:46", "00:06:40", "00:06:39", "00:06:40"
                    ]
                }
            }
        }]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getMedaillenspiegelFilterOptions(state) {
            return state.filterOptions
        },
        getBarChartData(state) {
            return {
                labels: state.medal_bar_chart_data.labels,
                datasets: [
                    {
                        type: 'bar',
                        label: "Medaillenübersicht",
                        backgroundColor: 'blue',
                        data: state.medal_bar_chart_data.data
                    },
                ]
            }
        },
    },
    actions: {
        async postFormData(formData) {
            await axios.post('https://jsonplaceholder.typicode.com/users',{ formData })
                .then(response => {
                    // Bearbeite die Antwort des Backends hier

                }).catch(error => {
                    // Bearbeite den Fehler hier
                })
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        }
    }
})
