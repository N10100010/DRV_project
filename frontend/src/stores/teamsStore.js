import axios from "axios";
import { defineStore } from "pinia";

export const useTeamsState = defineStore({
    id: "teams",
    state: () => ({
        filterOpen: false,
        tableExport: [],
        filterOptions: [{
            "year": [{ "start_year": 1950 }, { "end_year": 2025 }],
            "boat_class": {
                'men': {
                    'junior': {
                        'single': { "JM1x": "Junior Men's Single Sculls" },
                        'double': { "JM2x": "Junior Men's Double Sculls" },
                        'quad': { "JM4x": "Junior Men's Quadruple Sculls" },
                        'pair': { "JM2-": "Junior Men's Pair" },
                        'coxed_four': { "JM4+": "Junior Men's Coxed Four" },
                        'four': { "JM4-": "Junior Men's Four" },
                        'eight': { "JM8-": "Junior Men's Eight" }
                    },
                    'u19': {},
                    'u23': {
                        'single': { "BM1x": "U23 Men's Single Sculls" },
                        'double': { "BM2x": "U23 Men's Double Sculls" },
                        'quad': { "BM4x": "U23 Men's Quadruple Sculls" },
                        'pair': { "BM2-": "U23 Men's Pair" },
                        'coxed_four': { "BM4+": "U23 Men's Coxed Four" },
                        'four': { "BM4-": "U23 Men's Four" },
                        'eight': { "BM8+": "U23 Men's Eight" },
                        'lw_single': { "BLM1x": "U23 Lightweight Men's Single Sculls" },
                        'lw_double': { "BLM2x": "U23 Lightweight Men's Double Sculls" },
                        'lw_quad': { "BLM4x": "U23 Lightweight Men's Quadruple Sculls" },
                        'lw_pair': { "BLM2-": "U23 Lightweight Men's Pair" },
                    },
                    'elite': {
                        'single': { "M1x": "Men's Single Sculls" },
                        'double': { "M2x": "Men's Double Sculls" },
                        'quad': { "M4x": "Men's Quadruple Sculls" },
                        'pair': { "M2-": "Men's Pair" },
                        'four': { "M4-": "Men's Four" },
                        'eight': { "M8+": "Men's Eight" },
                        'lw_single': { "LM1x": "Lightweight Men's Single Sculls" },
                        'lw_double': { "LM2x": "Lightweight Men's Double Sculls" },
                        'lw_quad': { "LM4x": "Lightweight Men's Quadruple Sculls" },
                        'lw_pair': { "LM2-": "Lightweight Men's Pair" },
                    },
                    'para': {
                        '1': { "PR1 M1x": "PR1 Men's Single Sculls" },
                        '2': { "PR2 M1x": "PR2 Men's Single Sculls" },
                        '3': { "PR3 M2-": "PR3 Men's Pair" }
                    }
                },
                'women': {
                    'junior': {
                        'single': { "JW1x": "Junior Women's Single Sculls" },
                        'double': { "JW2x": "Junior Women's Double Sculls" },
                        'quad': { "JW4x": "Junior Women's Quadruple Sculls" },
                        'pair': { "JW2-": "Junior Women's Pair" },
                        'coxed_four': { "JW4+": "Junior Women's Coxed Four" },
                        'four': { "JW4-": "Junior Women's Four" },
                        'eight': { "JW8-": "Junior Women's Eight" }
                    },
                    'u19': {},
                    'u23': {
                        'single': { "BW1x": "U23 Women's Single Sculls" },
                        'double': { "BW2x": "U23 Women's Double Sculls" },
                        'quad': { "BW4x": "U23 Women's Quadruple Sculls" },
                        'pair': { "BW2-": "U23 Women's Pair" },
                        'coxed_four': { "BW4+": "U23 Women's Coxed Four" },
                        'four': { "BW4-": "U23 Women's Four" },
                        'eight': { "BW8+": "U23 Women's Eight" },
                        'lw_single': { "BLW1x": "U23 Lightweight Women's Single Sculls" },
                        'lw_double': { "BLW2x": "U23 Lightweight Women's Double Sculls" },
                        'lw_quad': { "BLW4x": "U23 Lightweight Women's Quadruple Sculls" },
                        'lw_pair': { "BLW2-": "U23 Lightweight Women's Pair" },
                    },
                    'elite': {
                        'single': { "W1x": "Women's Single Sculls" },
                        'double': { "W2x": "Women's Double Sculls" },
                        'quad': { "W4x": "Women's Quadruple Sculls" },
                        'pair': { "W2-": "Women's Pair" },
                        'four': { "W4-": "Women's Four" },
                        'eight': { "W8+": "Women's Eight" },
                        'lw_single': { "LW1x": "Lightweight Women's Single Sculls" },
                        'lw_double': { "LW2x": "Lightweight Women's Double Sculls" },
                        'lw_quad': { "LW4x": "Lightweight Women's Quadruple Sculls" },
                        'lw_pair': { "LW2-": "Lightweight Women's Pair" },
                    },
                    'para': {
                        '1': { "PR1 W1x": "PR1 Women's Single Sculls" },
                        '2': { "PR2 W1x": "PR2 Women's Single Sculls" },
                        '3': { "PR3 W2-": "PR3 Women's Pair" }
                    }
                },
                'mixed': {
                    'double_2': { "PR2 Mix2x": "PR2 Mixed Double Sculls" },
                    'double_3': { "PR3 Mix2x": "PR3 Mixed Double Sculls" },
                    'four': { "PR3 Mix4+": "PR3 Mixed Coxed Four" },
                }
            },
            "competition_category_ids": [
                { "displayName": "Olympics", "id": "89346342" },
                { "displayName": "World Rowing Championships", "id": "89346362" },
                { "displayName": "Qualifications", "id": "89346362" },
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
            },
        }],
        data: [{
                "year": [{ "start_year": 1950 }, { "end_year": 2025 }],
                "nation_ioc": "GER",
                "results": 127973,
                "men": {
                    "junior": {
                        "single": {
                            "JM1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "double": {
                            "JM2x": [
                                {
                                    "id": 1113333,
                                    "firstName": "Kay",
                                    "lastName": "Winkert"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "quad": {
                            "JM4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "pair": {
                            "JM2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "coxed_four": {
                            "JM4+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "four": {
                            "JM4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "eight": {
                            "JM8-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        }
                    },
                    "u19": {
                    },
                    "u23": {
                        "single": {
                            "BM1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "double": {
                            "BM2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "quad": {
                            "BM4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "pair": {
                            "BM2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "coxed_four": {
                            "BM4+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "four": {
                            "BM4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "eight": {
                            "BM8+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_single": {
                            "BLM1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_double": {
                            "BLM2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_quad": {
                            "BLM4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_pair": {
                            "BLM2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        }
                    },
                    "adult": {
                        "single": {
                            "M1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "double": {
                            "M2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "quad": {
                            "M4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "pair": {
                            "M2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "four": {
                            "M4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "eight": {
                            "M8+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_single": {
                            "LM1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_double": {
                            "LM2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_quad": {
                            "LM4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "lw_pair": {
                            "LM2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        }
                    },
                    "pr": {
                        "1": {
                            "PR1 M1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Kai",
                                    "lastName": "Winkert"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "2": {
                            "PR2 M1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        },
                        "3": {
                            "PR3 M2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                }
                            ]
                        }
                    }
                },
                "women": {
                    "junior": {
                        "single": {
                            "JW1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "double": {
                            "JW2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "quad": {
                            "JW4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "pair": {
                            "JW2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "coxed_four": {
                            "JW4+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "four": {
                            "JW4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "eight": {
                            "JW8-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        }
                    },
                    "u19": {
                    },
                    "u23": {
                        "single": {
                            "BW1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "double": {
                            "BW2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "quad": {
                            "BW4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "pair": {
                            "BW2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "coxed_four": {
                            "BW4+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "four": {
                            "BW4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "eight": {
                            "BW8+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_single": {
                            "BLW1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_double": {
                            "BLW2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_quad": {
                            "BLW4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_pair": {
                            "BLW2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        }
                    },
                    "adult": {
                        "single": {
                            "W1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "double": {
                            "W2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "quad": {
                            "W4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "pair": {
                            "W2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "four": {
                            "W4-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "eight": {
                            "W8+": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_single": {
                            "LW1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_double": {
                            "LW2x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_quad": {
                            "LW4x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "lw_pair": {
                            "LW2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        }
                    },
                    "pr": {
                        "1": {
                            "PR1 W1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "2": {
                            "PR2 W1x": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        },
                        "3": {
                            "PR3 W2-": [
                                {
                                    "id": 1111111,
                                    "firstName": "Jan",
                                    "lastName": "Kuster"
                                },
                                {
                                    "id": 2222222,
                                    "firstName": "Markus",
                                    "lastName": "Last"
                                },
                            ]
                        }
                    }
                },
                "mixed": {
                    "double_2": {
                        "PR2 Mix2x": [
                            {
                                "id": 1111111,
                                "firstName": "Jan",
                                "lastName": "Kuster"
                            },
                            {
                                "id": 2222222,
                                "firstName": "Markus",
                                "lastName": "Last"
                            },
                        ]
                    },
                    "double_3": {
                        "PR3 Mix2x": [
                            {
                                "id": 1111111,
                                "firstName": "Jan",
                                "lastName": "Kuster"
                            },
                            {
                                "id": 2222222,
                                "firstName": "Markus",
                                "lastName": "Last"
                            },
                        ]
                    },
                    "four": {
                        "PR3 Mix4+": [
                            {
                                "id": 1111111,
                                "firstName": "Jan",
                                "lastName": "Kuster"
                            },
                            {
                                "id": 2222222,
                                "firstName": "Markus",
                                "lastName": "Last"
                            },
                        ]
                    }
                }
            }
        ]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getTeamsFilterOptions(state) {
            return state.filterOptions
        },
        getMetaData(state) {
            return state.data[0]
        },
        getTableData(state) {
            const subHeaders = {
                "OPEN MEN": Object.values(state.data[0].men.adult),
                "OPEN WOMEN": Object.values(state.data[0].women.adult),
                "PARA MEN": Object.values(state.data[0].men.pr),
                "PARA WOMEN": Object.values(state.data[0].women.pr),
                "U23 MEN": Object.values(state.data[0].men.u23),
                "U23 WOMEN": Object.values(state.data[0].women.u23),
                "U19 MEN": Object.values(state.data[0].men.u19),
                "U19 WOMEN": Object.values(state.data[0].women.u19)
            }
            let rowValues = []
            Object.entries(subHeaders).forEach(([key, value], idx) => {
                rowValues.push(key)
                for (const item of value) {
                    let members = []
                    const itemList = Object.values(item)
                    itemList.forEach((value, idx) => {
                        value.forEach(entry => {
                            members.push(entry.firstName + " " + entry.lastName)
                        })
                    })
                    rowValues.push([Object.keys(item)[0], members])
                }
            })
            state.tableExport = rowValues
            return rowValues
        }
    },
    actions: {
        async postFormData(formData) {
            await axios.post('https://jsonplaceholder.typicode.com/users', { formData })
                .then(response => {
                    // Bearbeite die Antwort des Backends hier

                }).catch(error => {
                    // Bearbeite den Fehler hier
                })
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        },
        exportTableData() {
             const csvContent = "data:text/csv;charset=utf-8," + this.tableExport.map(row => {
                if (Array.isArray(row)) {
                    return row.map(cell => {
                        if (typeof cell === "string") {
                            return `"${cell}"`;
                        }
                        return cell;
                    }).join(",");
                }
                return row;
            }).join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "teams.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
})