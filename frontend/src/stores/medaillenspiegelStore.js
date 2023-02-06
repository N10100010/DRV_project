import axios from "axios";
import {defineStore} from "pinia";

const COLORS = ['#0C67F7', '#93E9ED', '#E0A9FA', '#E0B696', '#E0FAAC', '#F0E95A'];

export const useMedaillenspiegelState = defineStore({
    id: "medaillenspiegel",
    state: () => ({
        filterOpen: false,
        tableExport: [],
        filterOptions: [{
            "year": [{"start_year": 1950}, {"end_year": 2025}],
            "boat_class": {
                'men': {
                    'junior': {
                        'single': {"JM1x": "Junior Men's Single Sculls"},
                        'double': {"JM2x": "Junior Men's Double Sculls"},
                        'quad': {"JM4x": "Junior Men's Quadruple Sculls"},
                        'pair': {"JM2-": "Junior Men's Pair"},
                        'coxed_four': {"JM4+": "Junior Men's Coxed Four"},
                        'four': {"JM4-": "Junior Men's Four"},
                        'eight': {"JM8-": "Junior Men's Eight"}
                    },
                    'u19': {},
                    'u23': {
                        'single': {"BM1x": "U23 Men's Single Sculls"},
                        'double': {"BM2x": "U23 Men's Double Sculls"},
                        'quad': {"BM4x": "U23 Men's Quadruple Sculls"},
                        'pair': {"BM2-": "U23 Men's Pair"},
                        'coxed_four': {"BM4+": "U23 Men's Coxed Four"},
                        'four': {"BM4-": "U23 Men's Four"},
                        'eight': {"BM8+": "U23 Men's Eight"},
                        'lw_single': {"BLM1x": "U23 Lightweight Men's Single Sculls"},
                        'lw_double': {"BLM2x": "U23 Lightweight Men's Double Sculls"},
                        'lw_quad': {"BLM4x": "U23 Lightweight Men's Quadruple Sculls"},
                        'lw_pair': {"BLM2-": "U23 Lightweight Men's Pair"},
                    },
                    'adult': {
                        'single': {"M1x": "Men's Single Sculls"},
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
                        'four': {"JW4-": "Junior Women's Four"},
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
                {"displayName": "OG", "id": "89346342"},
                {"displayName": "EM", "id": "89346362"},
                {"displayName": "WCh", "id": "89346362"},
                {"displayName": "WCI", "id": "89346362"},
                {"displayName": "WCII", "id": "89346362"},
                {"displayName": "WCIII", "id": "89346362"},
                {"displayName": "LS", "id": "89346362"}
            ],
            "runs": [{"displayName": "FA", "id": "89346342"}],
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
            },
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
        data: [
            {
                "results": 4,
                "start_date": "2020",
                "end_date": "2022",
                "events": "EM",
                "category": "Olympisch",
                "boat_classes": [
                    {"M1x": "Men's Single Sculls"},
                    {"M2x": "Men's Double Sculls"}
                ],
                "table_data": [
                    {
                        "nation_ioc": "GER",
                        "rank": "1",
                        "points": 900,
                        "medals_gold": 2,
                        "medals_silver": 5,
                        "medals_bronze": 5,
                        "medals_total": 17,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "FRA",
                        "rank": "2",
                        "points": 760,
                        "medals_gold": 5,
                        "medals_silver": 5,
                        "medals_bronze": 5,
                        "medals_total": 15,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "ITA",
                        "rank": "3",
                        "points": 700,
                        "medals_gold": 2,
                        "medals_silver": 3,
                        "medals_bronze": 5,
                        "medals_total": 10,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    },
                    {
                        "nation_ioc": "RUS",
                        "rank": "4",
                        "points": 500,
                        "medals_gold": 1,
                        "medals_silver": 4,
                        "medals_bronze": 6,
                        "medals_total": 11,
                        "final_a": 12,
                        "final_b": 6,
                        "final_c": 0,
                        "final_d": 0
                    }]
            }
        ]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getMedaillenspiegelFilterOptions(state) {
            return state.filterOptions
        },
        getFilterSelection(state) {
            return state.data[0]
        },
        getTableData(state) {
            let tableData = [["Platz", "Nation", "Punkte", "Gold", "Silber", "Bronze", "Medaillen", "Finale A", "Finale B", "Finale C", "Finale D"]];
            const valueKeys = ["rank", "nation_ioc", "points", "medals_gold", "medals_silver", "medals_bronze", "medals_total", "final_a", "final_b", "final_c", "final_d"];
            const data = state.data[0].table_data
            for (const el of data) {
                let temp1Array = []
                for (const valueKey of valueKeys) {
                    temp1Array.push(el[valueKey]);
                }
                tableData.push(temp1Array)
            }
            state.tableExport = tableData
            return tableData
        },
        getBarChartData(state) {
            const data = state.data[0].table_data
            let dataSets = []
            const labels = ["Gold", "Silver", "Bronze", "Total"]
            for (const [index, country] of data.entries()) {
                dataSets.push({
                    type: 'bar',
                    label: country.nation_ioc,
                    backgroundColor: COLORS[index % COLORS.length],
                    data: [country.medals_gold, country.medals_silver, country.medals_bronze, country.medals_total]
                })
            }
            return {
                labels: labels,
                datasets: dataSets
            }
        },
    },
    actions: {
        async postFormData(formData) {
            await axios.post('https://jsonplaceholder.typicode.com/users', {formData})
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
            const csvContent = "data:text/csv;charset=utf-8," + this.tableExport.map(e => e.join(",")).join("\n");
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "medaillenspiegel.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
})
