mosaxleoba = [
    {"saxeli": "papuna", "asaki": 19, "saqartvelosMoqalaqe": True, "piradiNomeri": 1234},
    {"saxeli": "lasha", "asaki": 22, "saqartvelosMoqalaqe": True, "piradiNomeri": 23523352},
    {"saxeli": "dato", "asaki": 14, "saqartvelosMoqalaqe": True, "piradiNomeri": 1255534},
    {"saxeli": "mariami", "asaki": 26, "saqartvelosMoqalaqe": False, "piradiNomeri": 1234343334},
]

archevnebshiMonawileobisMigeba = []

for mosaxle in mosaxleoba:
    if mosaxle["saqartvelosMoqalaqe"] and mosaxle['asaki'] >=18:
        archevnebshiMonawileobisMigeba.append(mosaxle['piradiNomeri'])


print(archevnebshiMonawileobisMigeba)