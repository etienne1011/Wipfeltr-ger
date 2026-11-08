import requests

# --- API-Daten abrufen ---
url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=28.6&longitude=77.2&current=european_aqi,pm10,pm2_5"

answer = requests.get(url)
data = answer.json()
# print("Data:", data)

schadstoffe = data["current"]["european_aqi"]
feinstaub = data["current"]["pm2_5"]
# print("Schadstoffe:", schadstoffe)
# print("Feinstaub:", feinstaub)

# --- Logik ---

health = max(0, min(100, 100 - schadstoffe)) # negative %, Fehler
print("Waldgesundheit:", health)

anzahl_baeume = 100
gesunde_baeume = int(anzahl_baeume * (health/100))
kranke_baeume = anzahl_baeume - gesunde_baeume

if health >= 75:
    zustand = "Dem Wald geht es prima!"
    emoji_diagramm = "🌲" * gesunde_baeume + "🍃" * kranke_baeume
elif health >= 50:
    zustand = "Der Wald Atmet schwerer!"
    emoji_diagramm = "🌳" * gesunde_baeume + "🍂" * kranke_baeume
else:
    zustand = "Der Wald ist in Gefahr!"
    emoji_diagramm = "🍂" * gesunde_baeume + "🪵" * kranke_baeume

print(zustand)
print(emoji_diagramm)