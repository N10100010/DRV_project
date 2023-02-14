import axios from "axios";
import {defineStore} from "pinia";
import {resolve} from "chart.js/helpers";

const formatMilliseconds = ms => new Date(ms).toISOString().slice(14, -2);

export const useBerichteState = defineStore({
    id: "berichte",
    state: () => ({
        filterOpen: false,
        tableExport: [],
        lastFilterConfig: null,
        selectedBoatClass: {0: "Alle"},
        filterOptions: [{
            "years": [{"start_year": 0}, {"end_year": 0}],
            "boat_classes": {
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
                    'elite': {
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
                    'para': {
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
                    'elite': {
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
                    'para': {
                        '1': {"PR1 W1x": "PR1 Women's Single Sculls"},
                        '2': {"PR2 W1x": "PR2 Women's Single Sculls"},
                        '3': {"PR3 W2-": "PR3 Women's Pair"}
                    }
                },
                'mixed': {
                    'double_2': {"PR2 Mix2x": "PR2 Mixed Double Sculls"},
                    'double_3': {"PR3 Mix2x": "PR3 Mixed Double Sculls"},
                    'four': {"PR3 Mix4+": "PR3 Mixed Coxed Four"},
                },
                'all': {
                    'all': {"Alle Bootsklassen": "Alle"}
                },
            },
            "competition_categories": [
                {"display_name": "OG", "id": "89346342"},
                {"display_name": "EM", "id": "89346362"},
                {"display_name": "WCh", "id": "89346362"},
                {"display_name": "WCI", "id": "89346362"},
                {"display_name": "WCII", "id": "89346362"},
                {"display_name": "WCIII", "id": "89346362"},
                {"display_name": "LS", "id": "89346362"}
            ],
            "runs": {
                "finale": [
                    {"display_name": "fa"},
                    {"display_name": "fb"},
                    {"display_name": "fc"},
                    {"display_name": "fd"},
                    {"display_name": "f..."}
                ],
                "halbfinale": [
                    {"display_name": "sa/b, sa/b/c"},
                    {"display_name": "sc/d, sd/e/f"},
                    {"display_name": "s..."}
                ],
                "viertelfinale": [
                    {"display_name": "q1-4"},
                ],
                "hoffnungslauf": null,
                "vorlauf": null,
            },
            "ranks": ["1", "2", "3", "4-6"],
        }],
        data: {
            "results": null,
            "boat_classes": null,
            "start_date": "2020-06-16 14:12:00",
            "end_date": "2022-06-16 14:12:00",
            "world_best_time_boat_class": 0,
            "best_in_period": 0,
            "mean": {
                "mm:ss,00": 0,
                "m/s": 0,
                "pace 500m": 0,
                "pace 1000m": 0
            },
            "std_dev": 43360,
            "median": 432360,
            "gradation_fastest": {
                "no_of_samples": 345,
                "time": 358360
            },
            "gradation_medium": {
                "no_of_samples": 239,
                "time": 358360
            },
            "gradation_slow": {
                "no_of_samples": 167,
                "time": 358360
            },
            "gradation_slowest": {
                "no_of_samples": 463,
                "time": 358360
            },
            "plot_data": {
                "histogram": {
                    "labels": [],
                    "data": []
                },
                "scatter_plot": {
                    "labels": [],
                    "data": []
                },
                "scatter_1_sd_high": {
                    "labels": [],
                    "data": []
                },
                "scatter_1_sd_low": {
                    "labels": [],
                    "data": []
                },
                "scatter_mean": {
                    "labels": [],
                    "data": []
                }
            }
            },
        matrixdata: [
            {
                "results": 127973,
                "men": {
                    "junior": {
                        "single": {
                            "JM1x": "Junior Men's Single Sculls",
                            "WB [t]": 378360,
                            "avg [t]": 378360,
                            "delta [s]": 378360,
                            "num_of_boats": 2384
                        },
                        "double": {
                            "JM2x": "Junior Men's Double Sculls",
                            "WB [t]": 983745083746,
                            "avg [t]": 983745083746,
                            "delta [s]": 983745083746,
                            "num_of_boats": 2385
                        },
                        "quad": {
                            "JM4x": "Junior Men's Quadruple Sculls",
                            "WB [t]": 983745083747,
                            "avg [t]": 983745083747,
                            "delta [s]": 983745083747,
                            "num_of_boats": 2386
                        },
                        "pair": {
                            "JM2-": "Junior Men's Pair",
                            "WB [t]": 983745083748,
                            "avg [t]": 983745083748,
                            "delta [s]": 983745083748,
                            "num_of_boats": 2387
                        },
                        "coxed_four": {
                            "JM4+": "Junior Men's Coxed Four",
                            "WB [t]": 983745083749,
                            "avg [t]": 9837450837459,
                            "delta [s]": 983745083749,
                            "num_of_boats": 2388
                        },
                        "four": {
                            "JM4-": "Junior Men's Four",
                            "WB [t]": 983745083750,
                            "avg [t]": 983745083750,
                            "delta [s]": 98324234251,
                            "num_of_boats": 2389
                        },
                        "eight": {
                            "JM8-": "Junior Men's Eight",
                            "WB [t]": 983745083752,
                            "avg [t]": 983745083752,
                            "delta [s]": 983732434252,
                            "num_of_boats": 2390
                        }
                    },
                    "u19": {},
                    "u23": {
                        "single": {
                            "BM1x": "U23 Men's Single Sculls",
                            "WB [t]": 983745083753,
                            "avg [t]": 9837450834464,
                            "delta [s]": 983745083754,
                            "num_of_boats": 2391
                        },
                        "double": {
                            "BM2x": "U23 Men's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2392
                        },
                        "quad": {
                            "BM4x": "U23 Men's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2393
                        },
                        "pair": {
                            "BM2-": "U23 Men's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2394
                        },
                        "coxed_four": {
                            "BM4+": "U23 Men's Coxed Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2395
                        },
                        "four": {
                            "BM4-": "U23 Men's Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2396
                        },
                        "eight": {
                            "BM8+": "U23 Men's Eight",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2397
                        },
                        "lw_single": {
                            "BLM1x": "U23 Lightweight Men's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2398
                        },
                        "lw_double": {
                            "BLM2x": "U23 Lightweight Men's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2399
                        },
                        "lw_quad": {
                            "BLM4x": "U23 Lightweight Men's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2400
                        },
                        "lw_pair": {
                            "BLM2-": "U23 Lightweight Men's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2401
                        }
                    },
                    "elite": {
                        "single": {
                            "M1x": "Men's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2402
                        },
                        "double": {
                            "M2x": "Men's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2403
                        },
                        "quad": {
                            "M4x": "Men's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2404
                        },
                        "pair": {
                            "M2-": "Men's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2405
                        },
                        "four": {
                            "M4-": "Men's Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2406
                        },
                        "eight": {
                            "M8+": "Men's Eight",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2407
                        },
                        "lw_single": {
                            "LM1x": "Lightweight Men's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2408
                        },
                        "lw_double": {
                            "LM2x": "Lightweight Men's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2409
                        },
                        "lw_quad": {
                            "LM4x": "Lightweight Men's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2410
                        },
                        "lw_pair": {
                            "LM2-": "Lightweight Men's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2411
                        }
                    },
                    "para": {
                        "1": {
                            "PR1 M1x": "PR1 Men's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2412
                        },
                        "2": {
                            "PR2 M1x": "PR2 Men's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2413
                        },
                        "3": {
                            "PR3 M2-": "PR3 Men's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2414
                        }
                    }
                },
                "women": {
                    "junior": {
                        "single": {
                            "JW1x": "Junior Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2415
                        },
                        "double": {
                            "JW2x": "Junior Women's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2416
                        },
                        "quad": {
                            "JW4x": "Junior Women's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2417
                        },
                        "pair": {
                            "JW2-": "Junior Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2418
                        },
                        "coxed_four": {
                            "JW4+": "Junior Women's Coxed Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2419
                        },
                        "four": {
                            "JW4-": "Junior Women's Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2420
                        },
                        "eight": {
                            "JW8-": "Junior Women's Eight",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2421
                        }
                    },
                    "u19": {},
                    "u23": {
                        "single": {
                            "BW1x": "U23 Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2422
                        },
                        "double": {
                            "BW2x": "U23 Women's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2423
                        },
                        "quad": {
                            "BW4x": "U23 Women's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2424
                        },
                        "pair": {
                            "BW2-": "U23 Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2425
                        },
                        "coxed_four": {
                            "BW4+": "U23 Women's Coxed Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2426
                        },
                        "four": {
                            "BW4-": "U23 Women's Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2427
                        },
                        "eight": {
                            "BW8+": "U23 Women's Eight",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2428
                        },
                        "lw_single": {
                            "BLW1x": "U23 Lightweight Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2429
                        },
                        "lw_double": {
                            "BLW2x": "U23 Lightweight Women's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2430
                        },
                        "lw_quad": {
                            "BLW4x": "U23 Lightweight Women's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2431
                        },
                        "lw_pair": {
                            "BLW2-": "U23 Lightweight Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2432
                        }
                    },
                    "elite": {
                        "single": {
                            "W1x": "Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2433
                        },
                        "double": {
                            "W2x": "Women's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2434
                        },
                        "quad": {
                            "W4x": "Women's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2435
                        },
                        "pair": {
                            "W2-": "Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2436
                        },
                        "four": {
                            "W4-": "Women's Four",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2437
                        },
                        "eight": {
                            "W8+": "Women's Eight",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2438
                        },
                        "lw_single": {
                            "LW1x": "Lightweight Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2439
                        },
                        "lw_double": {
                            "LW2x": "Lightweight Women's Double Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2440
                        },
                        "lw_quad": {
                            "LW4x": "Lightweight Women's Quadruple Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2441
                        },
                        "lw_pair": {
                            "LW2-": "Lightweight Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2442
                        }
                    },
                    "para": {
                        "1": {
                            "PR1 W1x": "PR1 Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2443
                        },
                        "2": {
                            "PR2 W1x": "PR2 Women's Single Sculls",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2444
                        },
                        "3": {
                            "PR3 W2-": "PR3 Women's Pair",
                            "WB [t]": 983745083745,
                            "avg [t]": 983745083745,
                            "delta [s]": 983745083745,
                            "num_of_boats": 2445
                        }
                    }
                },
                "mixed": {
                    "double_2": {
                        "PR2 Mix2x": "PR2 Mixed Double Sculls",
                        "WB [t]": 983745083745,
                        "avg [t]": 983745083745,
                        "delta [s]": 983745083745,
                        "num_of_boats": 2446
                    },
                    "double_3": {
                        "PR3 Mix2x": "PR3 Mixed Double Sculls",
                        "WB [t]": 983745083745,
                        "avg [t]": 983745083745,
                        "delta [s]": 983745083745,
                        "num_of_boats": 2447
                    },
                    "four": {
                        "PR3 Mix4+": "PR3 Mixed Coxed Four",
                        "WB [t]": 983745083745,
                        "avg [t]": 983745083745,
                        "delta [s]": 983745083745,
                        "num_of_boats": 2448
                    }
                }
            }
        ]
    }),
    getters: {
        getFilterState(state) {
            return state.filterOpen
        },
        getReportFilterOptions(state) {
            return state.filterOptions
        },
        getTableData(state) {
            return state.data
        },
        getMatrixTableResults(state) {
            return state.matrixdata[0].results
        },
        getLastFilterConfig(state) {
            return state.lastFilterConfig
        },
        getMatrixTableData(state) {

            const subHeaders = {
                "OPEN MEN": Object.values(state.matrixdata[0].men.elite),
                "OPEN WOMEN": Object.values(state.matrixdata[0].women.elite),
                "PARA MEN": Object.values(state.matrixdata[0].men.para),
                "PARA WOMEN": Object.values(state.matrixdata[0].women.para),
                "U23 MEN": Object.values(state.matrixdata[0].men.u23),
                "U23 WOMEN": Object.values(state.matrixdata[0].women.u23),
                "U19 MEN": Object.values(state.matrixdata[0].men.u19),
                "U19 WOMEN": Object.values(state.matrixdata[0].women.u19)
            }

            let rowValues = []

            Object.entries(subHeaders).forEach(([key, value], idx) => {
                rowValues.push(key)
                for (const item of value) {
                    rowValues.push([Object.keys(item)[0], formatMilliseconds(item["WB [t]"]), formatMilliseconds(item["avg [t]"]), formatMilliseconds(item["delta [s]"]), item["num_of_boats"]])
                }
            })
            state.tableExport = rowValues
            return rowValues
        },
        getSelectedBoatClass(state) {
            return state.selectedBoatClass === "Alle"
        },
        getBarChartData(state) {
            return {
                labels: state.data.plot_data.histogram.labels.map(x => formatMilliseconds(x)),
                datasets: [

                    /*
                    {
                        type: 'line',
                        data: [
                            {x: formatMilliseconds(366360), y: 0},
                            {
                                x: formatMilliseconds(366360),
                                y: Math.ceil(Math.max(...Object.values(state.data.plot_data.histogram.data)) / 100) * 100
                            }],
                        label: "25. Perzentil",
                        borderColor: "darkgrey",
                        backgroundColor: "darkgrey",
                        borderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    },
                    {
                        type: 'line',
                        data: [
                            {x: formatMilliseconds(376360), y: 0},
                            {
                                x: formatMilliseconds(376360),
                                y: Math.ceil(Math.max(...Object.values(state.data.plot_data.histogram.data)) / 100) * 100
                            }],
                        label: "75. Perzentil",
                        borderColor: "darkgrey",
                        backgroundColor: "darkgrey",
                        borderWidth: 2,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    },
                    */
                    {
                        type: 'line',
                        backgroundColor: "red",
                        borderColor: "red",
                        borderWidth: 1.5,
                        pointRadius: 1.5,
                        tension: 0.2,
                        label: "Anzahl Boote",
                        data: state.data.plot_data.histogram.data,
                    },
                    {
                        type: 'bar',
                        backgroundColor: '#5cc5ed',
                        data: state.data.plot_data.histogram.data,
                        label: "Anzahl Boote"
                    }
                ]
            }
        },
        getBarChartOptions(state) {
            return {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Zeit [mm:ss]'
                        }
                    },
                    y: {
                        min: 0,
                        // max: Math.ceil(Math.max(...Object.values(state.data.plot_data.histogram.data)) / 100) * 100,
                        title: {
                            display: true,
                            text: 'Anzahl Rennen'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true
                    },
                    title: {
                        display: true,
                        text: `${state.data.boat_classes} (n = ${state.data.results})`
                    }
                }
            }
        },
        getScatterChartData(state) {

            const scatterData = state.data.plot_data.scatter_plot;
            const scatter1SDHigh = state.data.plot_data.scatter_1_sd_high;
            const scatter1SDLow = state.data.plot_data.scatter_1_sd_low;
            const scatterMeanValues = state.data.plot_data.scatter_mean;

            const plotData = scatterData.labels.map((label, i) => ({
                x: new Date(label),
                y: formatMilliseconds(scatterData.data[i])
            }));
            const sd1Low = scatter1SDLow.labels.map((label, i) => ({
                x: new Date(label),
                y: formatMilliseconds(scatter1SDLow.data[i])
            }));
            const sd1High = scatter1SDHigh.labels.map((label, i) => ({
                x: new Date(label),
                y: formatMilliseconds(scatter1SDHigh.data[i])
            }));
            const meanValues = scatterMeanValues.labels.map((label, i) => ({
                x: new Date(label),
                y: formatMilliseconds(scatterMeanValues.data[i])
            }));

            return {
                datasets: [
                    {
                        type: 'scatter',
                        data: plotData,
                        label: "Einzelergebnisse",
                        backgroundColor: '#5cc5ed',
                        borderColor: '#5cc5ed'
                    },
                    {
                        type: 'line',
                        data: sd1Low,
                        label: "-1SD",
                        borderColor: "darkgrey",
                        backgroundColor: "darkgrey",
                        borderWidth: 1,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    },
                    {
                        type: 'line',
                        data: meanValues,
                        label: "Mittelwert",
                        borderColor: "grey",
                        backgroundColor: "grey",
                        borderWidth: 1.5,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    },
                    {
                        type: 'line',
                        data: sd1High,
                        label: "+1SD",
                        borderColor: "darkgrey",
                        backgroundColor: "darkgrey",
                        borderWidth: 1,
                        pointRadius: 0,
                        pointHoverRadius: 0,
                    }
                ]
            }
        },
        getScatterChartOptions(state) {
            return {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'month',
                            parser: 'yyyy–mm–dd'
                        },
                        title: {
                            display: true,
                            text: 'Jahr'
                        }
                    },
                    y: {
                        type: 'time',
                        time: {
                            parser: 'HH:mm:ss',
                            unit: "seconds",
                            tooltipFormat: 'HH:mm:ss',
                            displayFormats: {
                                'seconds': "HH:mm:ss"
                            },
                            unitStepSize: 30
                        },
                        title: {
                            display: true,
                            text: 'Zeit [mm:ss.ms]'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                    },
                    title: {
                        display: true,
                        text: `${String(state.data.boat_classes)} (n = ${state.data.results})`
                    }
                }
            }
        }
    },
    actions: {
        async fetchReportFilterOptions() {
            await axios.get('http://localhost:5000/get_report_filter_options')
                .then(response => {
                    this.filterOptions = response.data
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
        async postFormData(data) {
            this.selectedBoatClass = data.boat_classes
            await axios.post('http://localhost:5000/get_report_boat_class', {data})
                .then(response => {
                    this.data = response.data
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
         async postFormDataMatrix(data) {
            await axios.post('http://localhost:5000/matrix', {data})
                .then(response => {
                    this.matrixdata = response.data
                }).catch(error => {
                    console.error(`Request failed: ${error}`)
                })
        },
        setFilterState(filterState) {
            this.filterOpen = !filterState
        },
        setLastFilterConfig(filterConfig) {
            this.lastFilterConfig = filterConfig
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
            link.setAttribute("download", "berichte.csv");
            document.body.appendChild(link);
            link.click();
        }
    }
})
