// Datos consolidados de ciudades y rutas para el mapa interactivo de España
const CAPITALES_ESPAÑA = {
  "A Coruña": {
    "lat": 43.3454621,
    "lon": -8.4138519
  },
  "Albacete": {
    "lat": 38.9950921,
    "lon": -1.8559154
  },
  "Alicante": {
    "lat": 38.3436365,
    "lon": -0.4881708
  },
  "Almería": {
    "lat": 36.8685739,
    "lon": -2.3120282
  },
  "Ávila": {
    "lat": 40.657195,
    "lon": -4.6626677
  },
  "Badajoz": {
    "lat": 38.878187,
    "lon": -6.9701115
  },
  "Barcelona": {
    "lat": 41.3825802,
    "lon": 2.177073
  },
  "Bilbao": {
    "lat": 43.2630018,
    "lon": -2.9350039
  },
  "Burgos": {
    "lat": 42.3448498,
    "lon": -3.6812477
  },
  "Cáceres": {
    "lat": 39.4745175,
    "lon": -6.3716761
  },
  "Cádiz": {
    "lat": 36.5297438,
    "lon": -6.2928976
  },
  "Castellón de la Plana": {
    "lat": 39.9860347,
    "lon": -0.0377354
  },
  "Ciudad Real": {
    "lat": 38.9597347,
    "lon": -3.8828744
  },
  "Córdoba": {
    "lat": 37.8845813,
    "lon": -4.7760138
  },
  "Cuenca": {
    "lat": 40.0661031,
    "lon": -2.1313528
  },
  "Girona": {
    "lat": 41.9793006,
    "lon": 2.8199439
  },
  "Granada": {
    "lat": 37.1734995,
    "lon": -3.5995337
  },
  "Guadalajara": {
    "lat": 40.7399963,
    "lon": -2.50593
  },
  "Huelva": {
    "lat": 37.2575874,
    "lon": -6.9484945
  },
  "Huesca": {
    "lat": 42.1360615,
    "lon": -0.0298027
  },
  "Jaén": {
    "lat": 37.7728858,
    "lon": -3.7883289
  },
  "León": {
    "lat": 42.6341451,
    "lon": -5.9714151
  },
  "Lleida": {
    "lat": 41.6147605,
    "lon": 0.6267842
  },
  "Logroño": {
    "lat": 42.4661196,
    "lon": -2.4396676
  },
  "Lugo": {
    "lat": 43.0395266,
    "lon": -7.4567985
  },
  "Madrid": {
    "lat": 40.416782,
    "lon": -3.703507
  },
  "Málaga": {
    "lat": 36.7647913,
    "lon": -4.4422005
  },
  "Murcia": {
    "lat": 37.9347521,
    "lon": -1.1131029
  },
  "Ourense": {
    "lat": 42.1939629,
    "lon": -7.537124
  },
  "Oviedo": {
    "lat": 43.3533452,
    "lon": -5.8795096
  },
  "Palencia": {
    "lat": 42.4096322,
    "lon": -4.6161004
  },
  "Pamplona": {
    "lat": 42.815686,
    "lon": -1.6522353
  },
  "Pontevedra": {
    "lat": 42.428065,
    "lon": -8.6041447
  },
  "Salamanca": {
    "lat": 40.9651572,
    "lon": -5.6640182
  },
  "San Sebastián": {
    "lat": 43.3224219,
    "lon": -1.9838889
  },
  "Santander": {
    "lat": 43.4618932,
    "lon": -3.8100255
  },
  "Segovia": {
    "lat": 40.9481192,
    "lon": -4.1172101
  },
  "Sevilla": {
    "lat": 37.3886303,
    "lon": -5.9953403
  },
  "Soria": {
    "lat": 41.6012505,
    "lon": -2.721938
  },
  "Tarragona": {
    "lat": 41.1172364,
    "lon": 1.2546057
  },
  "Teruel": {
    "lat": 40.6005259,
    "lon": -0.9229282
  },
  "Toledo": {
    "lat": 39.8558913,
    "lon": -4.024265
  },
  "Valencia": {
    "lat": 39.4697065,
    "lon": -0.3763353
  },
  "Valladolid": {
    "lat": 41.6200024,
    "lon": -4.7259906
  },
  "Vitoria-Gasteiz": {
    "lat": 42.8505845,
    "lon": -2.66145
  },
  "Zamora": {
    "lat": 41.6857693,
    "lon": -5.942315
  },
  "Zaragoza": {
    "lat": 41.6915847,
    "lon": -0.9101268
  }
};

const ITINERARIO_ACO_EXPLORADOR = [
  {
    "paso": 1,
    "origen": "Madrid",
    "destino": "Toledo",
    "costo_tramo": 24.74,
    "costo_acumulado": 24.74
  },
  {
    "paso": 2,
    "origen": "Toledo",
    "destino": "Ciudad Real",
    "costo_tramo": 26.93,
    "costo_acumulado": 51.67
  },
  {
    "paso": 3,
    "origen": "Ciudad Real",
    "destino": "Albacete",
    "costo_tramo": 39.5,
    "costo_acumulado": 91.17
  },
  {
    "paso": 4,
    "origen": "Albacete",
    "destino": "Cuenca",
    "costo_tramo": 32.07,
    "costo_acumulado": 123.24
  },
  {
    "paso": 5,
    "origen": "Cuenca",
    "destino": "Guadalajara",
    "costo_tramo": 32.28,
    "costo_acumulado": 155.52
  },
  {
    "paso": 6,
    "origen": "Guadalajara",
    "destino": "Soria",
    "costo_tramo": 34.26,
    "costo_acumulado": 189.78
  },
  {
    "paso": 7,
    "origen": "Soria",
    "destino": "Logroño",
    "costo_tramo": 29.84,
    "costo_acumulado": 219.62
  },
  {
    "paso": 8,
    "origen": "Logroño",
    "destino": "Vitoria-Gasteiz",
    "costo_tramo": 23.19,
    "costo_acumulado": 242.81
  },
  {
    "paso": 9,
    "origen": "Vitoria-Gasteiz",
    "destino": "Pamplona",
    "costo_tramo": 18.53,
    "costo_acumulado": 261.34
  },
  {
    "paso": 10,
    "origen": "Pamplona",
    "destino": "San Sebastián",
    "costo_tramo": 16.66,
    "costo_acumulado": 278.0
  },
  {
    "paso": 11,
    "origen": "San Sebastián",
    "destino": "Bilbao",
    "costo_tramo": 19.95,
    "costo_acumulado": 297.95
  },
  {
    "paso": 12,
    "origen": "Bilbao",
    "destino": "Santander",
    "costo_tramo": 19.98,
    "costo_acumulado": 317.93
  },
  {
    "paso": 13,
    "origen": "Santander",
    "destino": "Oviedo",
    "costo_tramo": 36.8,
    "costo_acumulado": 354.73
  },
  {
    "paso": 14,
    "origen": "Oviedo",
    "destino": "A Coruña",
    "costo_tramo": 51.68,
    "costo_acumulado": 406.41
  },
  {
    "paso": 15,
    "origen": "A Coruña",
    "destino": "Lugo",
    "costo_tramo": 19.76,
    "costo_acumulado": 426.17
  },
  {
    "paso": 16,
    "origen": "Lugo",
    "destino": "Pontevedra",
    "costo_tramo": 32.58,
    "costo_acumulado": 458.75
  },
  {
    "paso": 17,
    "origen": "Pontevedra",
    "destino": "Ourense",
    "costo_tramo": 33.86,
    "costo_acumulado": 492.61
  },
  {
    "paso": 18,
    "origen": "Ourense",
    "destino": "Zamora",
    "costo_tramo": 52.12,
    "costo_acumulado": 544.73
  },
  {
    "paso": 19,
    "origen": "Zamora",
    "destino": "León",
    "costo_tramo": 38.58,
    "costo_acumulado": 583.31
  },
  {
    "paso": 20,
    "origen": "León",
    "destino": "Palencia",
    "costo_tramo": 35.33,
    "costo_acumulado": 618.64
  },
  {
    "paso": 21,
    "origen": "Palencia",
    "destino": "Burgos",
    "costo_tramo": 17.57,
    "costo_acumulado": 636.21
  },
  {
    "paso": 22,
    "origen": "Burgos",
    "destino": "Valladolid",
    "costo_tramo": 24.18,
    "costo_acumulado": 660.39
  },
  {
    "paso": 23,
    "origen": "Valladolid",
    "destino": "Segovia",
    "costo_tramo": 21.68,
    "costo_acumulado": 682.07
  },
  {
    "paso": 24,
    "origen": "Segovia",
    "destino": "Ávila",
    "costo_tramo": 23.22,
    "costo_acumulado": 705.29
  },
  {
    "paso": 25,
    "origen": "Ávila",
    "destino": "Salamanca",
    "costo_tramo": 21.58,
    "costo_acumulado": 726.87
  },
  {
    "paso": 26,
    "origen": "Salamanca",
    "destino": "Cáceres",
    "costo_tramo": 37.87,
    "costo_acumulado": 764.74
  },
  {
    "paso": 27,
    "origen": "Cáceres",
    "destino": "Badajoz",
    "costo_tramo": 19.91,
    "costo_acumulado": 784.65
  },
  {
    "paso": 28,
    "origen": "Badajoz",
    "destino": "Sevilla",
    "costo_tramo": 40.67,
    "costo_acumulado": 825.32
  },
  {
    "paso": 29,
    "origen": "Sevilla",
    "destino": "Huelva",
    "costo_tramo": 17.34,
    "costo_acumulado": 842.66
  },
  {
    "paso": 30,
    "origen": "Huelva",
    "destino": "Cádiz",
    "costo_tramo": 39.4,
    "costo_acumulado": 882.06
  },
  {
    "paso": 31,
    "origen": "Cádiz",
    "destino": "Córdoba",
    "costo_tramo": 47.64,
    "costo_acumulado": 929.7
  },
  {
    "paso": 32,
    "origen": "Córdoba",
    "destino": "Jaén",
    "costo_tramo": 22.96,
    "costo_acumulado": 952.66
  },
  {
    "paso": 33,
    "origen": "Jaén",
    "destino": "Granada",
    "costo_tramo": 17.8,
    "costo_acumulado": 970.46
  },
  {
    "paso": 34,
    "origen": "Granada",
    "destino": "Málaga",
    "costo_tramo": 26.8,
    "costo_acumulado": 997.26
  },
  {
    "paso": 35,
    "origen": "Málaga",
    "destino": "Almería",
    "costo_tramo": 42.55,
    "costo_acumulado": 1039.81
  },
  {
    "paso": 36,
    "origen": "Almería",
    "destino": "Murcia",
    "costo_tramo": 38.24,
    "costo_acumulado": 1078.05
  },
  {
    "paso": 37,
    "origen": "Murcia",
    "destino": "Alicante",
    "costo_tramo": 28.89,
    "costo_acumulado": 1106.94
  },
  {
    "paso": 38,
    "origen": "Alicante",
    "destino": "Valencia",
    "costo_tramo": 32.84,
    "costo_acumulado": 1139.78
  },
  {
    "paso": 39,
    "origen": "Valencia",
    "destino": "Castellón de la Plana",
    "costo_tramo": 15.44,
    "costo_acumulado": 1155.22
  },
  {
    "paso": 40,
    "origen": "Castellón de la Plana",
    "destino": "Tarragona",
    "costo_tramo": 34.84,
    "costo_acumulado": 1190.06
  },
  {
    "paso": 41,
    "origen": "Tarragona",
    "destino": "Barcelona",
    "costo_tramo": 19.78,
    "costo_acumulado": 1209.84
  },
  {
    "paso": 42,
    "origen": "Barcelona",
    "destino": "Girona",
    "costo_tramo": 20.05,
    "costo_acumulado": 1229.89
  },
  {
    "paso": 43,
    "origen": "Girona",
    "destino": "Lleida",
    "costo_tramo": 42.29,
    "costo_acumulado": 1272.18
  },
  {
    "paso": 44,
    "origen": "Lleida",
    "destino": "Huesca",
    "costo_tramo": 18.57,
    "costo_acumulado": 1290.75
  },
  {
    "paso": 45,
    "origen": "Huesca",
    "destino": "Zaragoza",
    "costo_tramo": 23.12,
    "costo_acumulado": 1313.87
  },
  {
    "paso": 46,
    "origen": "Zaragoza",
    "destino": "Teruel",
    "costo_tramo": 41.18,
    "costo_acumulado": 1355.05
  },
  {
    "paso": 47,
    "origen": "Teruel",
    "destino": "Madrid",
    "costo_tramo": 66.49,
    "costo_acumulado": 1421.54
  }
];

const ITINERARIO_ACO_BASE = [
  {
    "paso": 1,
    "origen": "Córdoba",
    "destino": "Jaén",
    "costo_tramo": 22.96,
    "costo_acumulado": 22.96
  },
  {
    "paso": 2,
    "origen": "Jaén",
    "destino": "Granada",
    "costo_tramo": 17.8,
    "costo_acumulado": 40.76
  },
  {
    "paso": 3,
    "origen": "Granada",
    "destino": "Málaga",
    "costo_tramo": 26.8,
    "costo_acumulado": 67.56
  },
  {
    "paso": 4,
    "origen": "Málaga",
    "destino": "Almería",
    "costo_tramo": 42.55,
    "costo_acumulado": 110.11
  },
  {
    "paso": 5,
    "origen": "Almería",
    "destino": "Murcia",
    "costo_tramo": 38.24,
    "costo_acumulado": 148.35
  },
  {
    "paso": 6,
    "origen": "Murcia",
    "destino": "Alicante",
    "costo_tramo": 28.89,
    "costo_acumulado": 177.24
  },
  {
    "paso": 7,
    "origen": "Alicante",
    "destino": "Valencia",
    "costo_tramo": 32.84,
    "costo_acumulado": 210.08
  },
  {
    "paso": 8,
    "origen": "Valencia",
    "destino": "Castellón de la Plana",
    "costo_tramo": 15.44,
    "costo_acumulado": 225.52
  },
  {
    "paso": 9,
    "origen": "Castellón de la Plana",
    "destino": "Tarragona",
    "costo_tramo": 34.84,
    "costo_acumulado": 260.36
  },
  {
    "paso": 10,
    "origen": "Tarragona",
    "destino": "Barcelona",
    "costo_tramo": 19.78,
    "costo_acumulado": 280.14
  },
  {
    "paso": 11,
    "origen": "Barcelona",
    "destino": "Girona",
    "costo_tramo": 20.05,
    "costo_acumulado": 300.19
  },
  {
    "paso": 12,
    "origen": "Girona",
    "destino": "Zaragoza",
    "costo_tramo": 71.13,
    "costo_acumulado": 371.32
  },
  {
    "paso": 13,
    "origen": "Zaragoza",
    "destino": "Huesca",
    "costo_tramo": 23.23,
    "costo_acumulado": 394.55
  },
  {
    "paso": 14,
    "origen": "Huesca",
    "destino": "Lleida",
    "costo_tramo": 19.01,
    "costo_acumulado": 413.56
  },
  {
    "paso": 15,
    "origen": "Lleida",
    "destino": "Teruel",
    "costo_tramo": 53.32,
    "costo_acumulado": 466.88
  },
  {
    "paso": 16,
    "origen": "Teruel",
    "destino": "Cuenca",
    "costo_tramo": 42.65,
    "costo_acumulado": 509.53
  },
  {
    "paso": 17,
    "origen": "Cuenca",
    "destino": "Albacete",
    "costo_tramo": 31.53,
    "costo_acumulado": 541.06
  },
  {
    "paso": 18,
    "origen": "Albacete",
    "destino": "Ciudad Real",
    "costo_tramo": 40.02,
    "costo_acumulado": 581.08
  },
  {
    "paso": 19,
    "origen": "Ciudad Real",
    "destino": "Toledo",
    "costo_tramo": 26.77,
    "costo_acumulado": 607.85
  },
  {
    "paso": 20,
    "origen": "Toledo",
    "destino": "Madrid",
    "costo_tramo": 24.74,
    "costo_acumulado": 632.59
  },
  {
    "paso": 21,
    "origen": "Madrid",
    "destino": "Ávila",
    "costo_tramo": 34.7,
    "costo_acumulado": 667.29
  },
  {
    "paso": 22,
    "origen": "Ávila",
    "destino": "Segovia",
    "costo_tramo": 23.36,
    "costo_acumulado": 690.65
  },
  {
    "paso": 23,
    "origen": "Segovia",
    "destino": "Guadalajara",
    "costo_tramo": 46.89,
    "costo_acumulado": 737.54
  },
  {
    "paso": 24,
    "origen": "Guadalajara",
    "destino": "Soria",
    "costo_tramo": 34.26,
    "costo_acumulado": 771.8
  },
  {
    "paso": 25,
    "origen": "Soria",
    "destino": "Logroño",
    "costo_tramo": 29.84,
    "costo_acumulado": 801.64
  },
  {
    "paso": 26,
    "origen": "Logroño",
    "destino": "Pamplona",
    "costo_tramo": 26.92,
    "costo_acumulado": 828.56
  },
  {
    "paso": 27,
    "origen": "Pamplona",
    "destino": "San Sebastián",
    "costo_tramo": 16.66,
    "costo_acumulado": 845.22
  },
  {
    "paso": 28,
    "origen": "San Sebastián",
    "destino": "Vitoria-Gasteiz",
    "costo_tramo": 19.51,
    "costo_acumulado": 864.73
  },
  {
    "paso": 29,
    "origen": "Vitoria-Gasteiz",
    "destino": "Bilbao",
    "costo_tramo": 21.05,
    "costo_acumulado": 885.78
  },
  {
    "paso": 30,
    "origen": "Bilbao",
    "destino": "Santander",
    "costo_tramo": 19.98,
    "costo_acumulado": 905.76
  },
  {
    "paso": 31,
    "origen": "Santander",
    "destino": "Oviedo",
    "costo_tramo": 36.8,
    "costo_acumulado": 942.56
  },
  {
    "paso": 32,
    "origen": "Oviedo",
    "destino": "Lugo",
    "costo_tramo": 42.87,
    "costo_acumulado": 985.43
  },
  {
    "paso": 33,
    "origen": "Lugo",
    "destino": "A Coruña",
    "costo_tramo": 19.52,
    "costo_acumulado": 1004.95
  },
  {
    "paso": 34,
    "origen": "A Coruña",
    "destino": "Pontevedra",
    "costo_tramo": 43.22,
    "costo_acumulado": 1048.17
  },
  {
    "paso": 35,
    "origen": "Pontevedra",
    "destino": "Ourense",
    "costo_tramo": 33.86,
    "costo_acumulado": 1082.03
  },
  {
    "paso": 36,
    "origen": "Ourense",
    "destino": "León",
    "costo_tramo": 54.79,
    "costo_acumulado": 1136.82
  },
  {
    "paso": 37,
    "origen": "León",
    "destino": "Palencia",
    "costo_tramo": 35.33,
    "costo_acumulado": 1172.15
  },
  {
    "paso": 38,
    "origen": "Palencia",
    "destino": "Burgos",
    "costo_tramo": 17.57,
    "costo_acumulado": 1189.72
  },
  {
    "paso": 39,
    "origen": "Burgos",
    "destino": "Valladolid",
    "costo_tramo": 24.18,
    "costo_acumulado": 1213.9
  },
  {
    "paso": 40,
    "origen": "Valladolid",
    "destino": "Zamora",
    "costo_tramo": 29.82,
    "costo_acumulado": 1243.72
  },
  {
    "paso": 41,
    "origen": "Zamora",
    "destino": "Salamanca",
    "costo_tramo": 24.9,
    "costo_acumulado": 1268.62
  },
  {
    "paso": 42,
    "origen": "Salamanca",
    "destino": "Cáceres",
    "costo_tramo": 37.87,
    "costo_acumulado": 1306.49
  },
  {
    "paso": 43,
    "origen": "Cáceres",
    "destino": "Badajoz",
    "costo_tramo": 19.91,
    "costo_acumulado": 1326.4
  },
  {
    "paso": 44,
    "origen": "Badajoz",
    "destino": "Cádiz",
    "costo_tramo": 62.84,
    "costo_acumulado": 1389.24
  },
  {
    "paso": 45,
    "origen": "Cádiz",
    "destino": "Sevilla",
    "costo_tramo": 23.83,
    "costo_acumulado": 1413.07
  },
  {
    "paso": 46,
    "origen": "Sevilla",
    "destino": "Huelva",
    "costo_tramo": 17.34,
    "costo_acumulado": 1430.41
  },
  {
    "paso": 47,
    "origen": "Huelva",
    "destino": "Córdoba",
    "costo_tramo": 44.22,
    "costo_acumulado": 1474.63
  }
];

const ITINERARIO_GA = [
  {
    "paso": 1,
    "origen": "Madrid",
    "destino": "Toledo",
    "distancia_km": 74.81,
    "tiempo_h": 1.02,
    "peajes_eur": 9.35,
    "combustible_eur": 6.28,
    "costo_tramo": 24.71,
    "costo_acumulado": 24.71
  },
  {
    "paso": 2,
    "origen": "Toledo",
    "destino": "Ávila",
    "distancia_km": 134.44,
    "tiempo_h": 1.95,
    "peajes_eur": 0.0,
    "combustible_eur": 11.29,
    "costo_tramo": 28.64,
    "costo_acumulado": 53.35
  },
  {
    "paso": 3,
    "origen": "Ávila",
    "destino": "Segovia",
    "distancia_km": 68.97,
    "tiempo_h": 1.0,
    "peajes_eur": 8.62,
    "combustible_eur": 5.79,
    "costo_tramo": 23.31,
    "costo_acumulado": 76.66
  },
  {
    "paso": 4,
    "origen": "Segovia",
    "destino": "Valladolid",
    "distancia_km": 112.12,
    "tiempo_h": 1.31,
    "peajes_eur": 0.0,
    "combustible_eur": 9.42,
    "costo_tramo": 21.08,
    "costo_acumulado": 97.74
  },
  {
    "paso": 5,
    "origen": "Valladolid",
    "destino": "Palencia",
    "distancia_km": 114.32,
    "tiempo_h": 1.51,
    "peajes_eur": 0.0,
    "combustible_eur": 9.6,
    "costo_tramo": 23.04,
    "costo_acumulado": 120.78
  },
  {
    "paso": 6,
    "origen": "Palencia",
    "destino": "Burgos",
    "distancia_km": 91.73,
    "tiempo_h": 1.11,
    "peajes_eur": 0.0,
    "combustible_eur": 7.7,
    "costo_tramo": 17.58,
    "costo_acumulado": 138.36
  },
  {
    "paso": 7,
    "origen": "Burgos",
    "destino": "Logroño",
    "distancia_km": 113.16,
    "tiempo_h": 1.59,
    "peajes_eur": 0.0,
    "combustible_eur": 9.5,
    "costo_tramo": 23.65,
    "costo_acumulado": 162.01
  },
  {
    "paso": 8,
    "origen": "Logroño",
    "destino": "Vitoria-Gasteiz",
    "distancia_km": 63.35,
    "tiempo_h": 1.12,
    "peajes_eur": 7.92,
    "combustible_eur": 5.32,
    "costo_tramo": 23.21,
    "costo_acumulado": 185.22
  },
  {
    "paso": 9,
    "origen": "Vitoria-Gasteiz",
    "destino": "Pamplona",
    "distancia_km": 97.05,
    "tiempo_h": 1.17,
    "peajes_eur": 0.0,
    "combustible_eur": 8.15,
    "costo_tramo": 18.56,
    "costo_acumulado": 203.78
  },
  {
    "paso": 10,
    "origen": "Pamplona",
    "destino": "San Sebastián",
    "distancia_km": 82.97,
    "tiempo_h": 1.09,
    "peajes_eur": 0.0,
    "combustible_eur": 6.97,
    "costo_tramo": 16.67,
    "costo_acumulado": 220.45
  },
  {
    "paso": 11,
    "origen": "San Sebastián",
    "destino": "Bilbao",
    "distancia_km": 102.04,
    "tiempo_h": 1.28,
    "peajes_eur": 0.0,
    "combustible_eur": 8.57,
    "costo_tramo": 19.96,
    "costo_acumulado": 240.41
  },
  {
    "paso": 12,
    "origen": "Bilbao",
    "destino": "Santander",
    "distancia_km": 99.51,
    "tiempo_h": 1.31,
    "peajes_eur": 0.0,
    "combustible_eur": 8.36,
    "costo_tramo": 20.02,
    "costo_acumulado": 260.43
  },
  {
    "paso": 13,
    "origen": "Santander",
    "destino": "Oviedo",
    "distancia_km": 199.79,
    "tiempo_h": 2.25,
    "peajes_eur": 0.0,
    "combustible_eur": 16.78,
    "costo_tramo": 36.81,
    "costo_acumulado": 297.24
  },
  {
    "paso": 14,
    "origen": "Oviedo",
    "destino": "A Coruña",
    "distancia_km": 279.9,
    "tiempo_h": 3.17,
    "peajes_eur": 0.0,
    "combustible_eur": 23.51,
    "costo_tramo": 51.72,
    "costo_acumulado": 348.96
  },
  {
    "paso": 15,
    "origen": "A Coruña",
    "destino": "Lugo",
    "distancia_km": 102.16,
    "tiempo_h": 1.26,
    "peajes_eur": 0.0,
    "combustible_eur": 8.58,
    "costo_tramo": 19.79,
    "costo_acumulado": 368.76
  },
  {
    "paso": 16,
    "origen": "Lugo",
    "destino": "Pontevedra",
    "distancia_km": 152.54,
    "tiempo_h": 2.22,
    "peajes_eur": 0.0,
    "combustible_eur": 12.81,
    "costo_tramo": 32.57,
    "costo_acumulado": 401.32
  },
  {
    "paso": 17,
    "origen": "Pontevedra",
    "destino": "Ourense",
    "distancia_km": 141.54,
    "tiempo_h": 2.47,
    "peajes_eur": 0.0,
    "combustible_eur": 11.89,
    "costo_tramo": 33.87,
    "costo_acumulado": 435.2
  },
  {
    "paso": 18,
    "origen": "Ourense",
    "destino": "León",
    "distancia_km": 216.44,
    "tiempo_h": 4.11,
    "peajes_eur": 0.0,
    "combustible_eur": 18.18,
    "costo_tramo": 54.76,
    "costo_acumulado": 489.96
  },
  {
    "paso": 19,
    "origen": "León",
    "destino": "Zamora",
    "distancia_km": 164.55,
    "tiempo_h": 2.77,
    "peajes_eur": 0.0,
    "combustible_eur": 13.82,
    "costo_tramo": 38.47,
    "costo_acumulado": 528.43
  },
  {
    "paso": 20,
    "origen": "Zamora",
    "destino": "Salamanca",
    "distancia_km": 114.45,
    "tiempo_h": 1.72,
    "peajes_eur": 0.0,
    "combustible_eur": 9.61,
    "costo_tramo": 24.92,
    "costo_acumulado": 553.35
  },
  {
    "paso": 21,
    "origen": "Salamanca",
    "destino": "Cáceres",
    "distancia_km": 201.73,
    "tiempo_h": 2.35,
    "peajes_eur": 0.0,
    "combustible_eur": 16.94,
    "costo_tramo": 37.86,
    "costo_acumulado": 591.2
  },
  {
    "paso": 22,
    "origen": "Cáceres",
    "destino": "Badajoz",
    "distancia_km": 92.0,
    "tiempo_h": 1.37,
    "peajes_eur": 0.0,
    "combustible_eur": 7.73,
    "costo_tramo": 19.92,
    "costo_acumulado": 611.12
  },
  {
    "paso": 23,
    "origen": "Badajoz",
    "destino": "Huelva",
    "distancia_km": 234.07,
    "tiempo_h": 3.19,
    "peajes_eur": 0.0,
    "combustible_eur": 19.66,
    "costo_tramo": 48.05,
    "costo_acumulado": 659.18
  },
  {
    "paso": 24,
    "origen": "Huelva",
    "destino": "Sevilla",
    "distancia_km": 91.19,
    "tiempo_h": 1.08,
    "peajes_eur": 0.0,
    "combustible_eur": 7.66,
    "costo_tramo": 17.27,
    "costo_acumulado": 676.45
  },
  {
    "paso": 25,
    "origen": "Sevilla",
    "destino": "Cádiz",
    "distancia_km": 123.24,
    "tiempo_h": 1.54,
    "peajes_eur": 0.0,
    "combustible_eur": 10.35,
    "costo_tramo": 24.06,
    "costo_acumulado": 700.5
  },
  {
    "paso": 26,
    "origen": "Cádiz",
    "destino": "Córdoba",
    "distancia_km": 253.3,
    "tiempo_h": 2.96,
    "peajes_eur": 0.0,
    "combustible_eur": 21.27,
    "costo_tramo": 47.61,
    "costo_acumulado": 748.12
  },
  {
    "paso": 27,
    "origen": "Córdoba",
    "destino": "Ciudad Real",
    "distancia_km": 193.13,
    "tiempo_h": 2.37,
    "peajes_eur": 0.0,
    "combustible_eur": 16.22,
    "costo_tramo": 37.31,
    "costo_acumulado": 785.43
  },
  {
    "paso": 28,
    "origen": "Ciudad Real",
    "destino": "Jaén",
    "distancia_km": 183.17,
    "tiempo_h": 2.19,
    "peajes_eur": 0.0,
    "combustible_eur": 15.38,
    "costo_tramo": 34.87,
    "costo_acumulado": 820.3
  },
  {
    "paso": 29,
    "origen": "Jaén",
    "destino": "Granada",
    "distancia_km": 93.06,
    "tiempo_h": 1.12,
    "peajes_eur": 0.0,
    "combustible_eur": 7.82,
    "costo_tramo": 17.79,
    "costo_acumulado": 838.09
  },
  {
    "paso": 30,
    "origen": "Granada",
    "destino": "Málaga",
    "distancia_km": 130.87,
    "tiempo_h": 1.78,
    "peajes_eur": 0.0,
    "combustible_eur": 10.99,
    "costo_tramo": 26.83,
    "costo_acumulado": 864.92
  },
  {
    "paso": 31,
    "origen": "Málaga",
    "destino": "Almería",
    "distancia_km": 220.91,
    "tiempo_h": 2.7,
    "peajes_eur": 0.0,
    "combustible_eur": 18.55,
    "costo_tramo": 42.58,
    "costo_acumulado": 907.5
  },
  {
    "paso": 32,
    "origen": "Almería",
    "destino": "Murcia",
    "distancia_km": 204.88,
    "tiempo_h": 2.36,
    "peajes_eur": 0.0,
    "combustible_eur": 17.21,
    "costo_tramo": 38.21,
    "costo_acumulado": 945.72
  },
  {
    "paso": 33,
    "origen": "Murcia",
    "destino": "Alicante",
    "distancia_km": 89.15,
    "tiempo_h": 1.15,
    "peajes_eur": 11.14,
    "combustible_eur": 7.49,
    "costo_tramo": 28.87,
    "costo_acumulado": 974.58
  },
  {
    "paso": 34,
    "origen": "Alicante",
    "destino": "Albacete",
    "distancia_km": 167.55,
    "tiempo_h": 1.89,
    "peajes_eur": 0.0,
    "combustible_eur": 14.07,
    "costo_tramo": 30.89,
    "costo_acumulado": 1005.47
  },
  {
    "paso": 35,
    "origen": "Albacete",
    "destino": "Valencia",
    "distancia_km": 169.12,
    "tiempo_h": 2.14,
    "peajes_eur": 0.0,
    "combustible_eur": 14.2,
    "costo_tramo": 33.25,
    "costo_acumulado": 1038.72
  },
  {
    "paso": 36,
    "origen": "Valencia",
    "destino": "Castellón de la Plana",
    "distancia_km": 76.66,
    "tiempo_h": 1.01,
    "peajes_eur": 0.0,
    "combustible_eur": 6.44,
    "costo_tramo": 15.43,
    "costo_acumulado": 1054.15
  },
  {
    "paso": 37,
    "origen": "Castellón de la Plana",
    "destino": "Teruel",
    "distancia_km": 185.93,
    "tiempo_h": 2.85,
    "peajes_eur": 0.0,
    "combustible_eur": 15.62,
    "costo_tramo": 40.98,
    "costo_acumulado": 1095.13
  },
  {
    "paso": 38,
    "origen": "Teruel",
    "destino": "Tarragona",
    "distancia_km": 258.65,
    "tiempo_h": 4.29,
    "peajes_eur": 0.0,
    "combustible_eur": 21.72,
    "costo_tramo": 59.9,
    "costo_acumulado": 1155.03
  },
  {
    "paso": 39,
    "origen": "Tarragona",
    "destino": "Barcelona",
    "distancia_km": 96.36,
    "tiempo_h": 1.31,
    "peajes_eur": 0.0,
    "combustible_eur": 8.09,
    "costo_tramo": 19.75,
    "costo_acumulado": 1174.78
  },
  {
    "paso": 40,
    "origen": "Barcelona",
    "destino": "Girona",
    "distancia_km": 101.99,
    "tiempo_h": 1.29,
    "peajes_eur": 0.0,
    "combustible_eur": 8.57,
    "costo_tramo": 20.05,
    "costo_acumulado": 1194.83
  },
  {
    "paso": 41,
    "origen": "Girona",
    "destino": "Lleida",
    "distancia_km": 225.89,
    "tiempo_h": 2.62,
    "peajes_eur": 0.0,
    "combustible_eur": 18.97,
    "costo_tramo": 42.29,
    "costo_acumulado": 1237.12
  },
  {
    "paso": 42,
    "origen": "Lleida",
    "destino": "Huesca",
    "distancia_km": 93.75,
    "tiempo_h": 1.2,
    "peajes_eur": 0.0,
    "combustible_eur": 7.87,
    "costo_tramo": 18.55,
    "costo_acumulado": 1255.67
  },
  {
    "paso": 43,
    "origen": "Huesca",
    "destino": "Zaragoza",
    "distancia_km": 112.87,
    "tiempo_h": 1.53,
    "peajes_eur": 0.0,
    "combustible_eur": 9.48,
    "costo_tramo": 23.1,
    "costo_acumulado": 1278.77
  },
  {
    "paso": 44,
    "origen": "Zaragoza",
    "destino": "Soria",
    "distancia_km": 205.64,
    "tiempo_h": 2.94,
    "peajes_eur": 0.0,
    "combustible_eur": 17.27,
    "costo_tramo": 43.44,
    "costo_acumulado": 1322.2
  },
  {
    "paso": 45,
    "origen": "Soria",
    "destino": "Guadalajara",
    "distancia_km": 153.19,
    "tiempo_h": 2.43,
    "peajes_eur": 0.0,
    "combustible_eur": 12.87,
    "costo_tramo": 34.5,
    "costo_acumulado": 1356.7
  },
  {
    "paso": 46,
    "origen": "Guadalajara",
    "destino": "Cuenca",
    "distancia_km": 146.64,
    "tiempo_h": 2.29,
    "peajes_eur": 0.0,
    "combustible_eur": 12.32,
    "costo_tramo": 32.7,
    "costo_acumulado": 1389.4
  },
  {
    "paso": 47,
    "origen": "Cuenca",
    "destino": "Madrid",
    "distancia_km": 166.94,
    "tiempo_h": 1.98,
    "peajes_eur": 0.0,
    "combustible_eur": 14.02,
    "costo_tramo": 31.64,
    "costo_acumulado": 1421.04
  }
];
