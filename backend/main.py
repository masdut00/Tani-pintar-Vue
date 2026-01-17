from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel # Alat bantu untuk membaca JSON dari Vue
from google import genai
from PIL import Image
import io
import requests # Untuk panggil Open-Meteo

# --- KONFIGURASI ---
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GOOGLE_API_KEY = "AIzaSyDqRDhPtUloyWoVCRwCfW8Bng9GQ3_LksE"
try:    
    client = genai.Client(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error Client: {e}")

# --- MODEL DATA (Schema) ---
# Ini amplop agar Python mengerti data JSON yang dikirim Vue untuk fitur cuaca
class WeatherRequest(BaseModel):
    lokasi: str
    suhu: str
    kondisi: str
    angin: str
    tanaman: str
    fase: str

# --- ENDPOINT 1: DIAGNOSIS (Yang tadi sudah sukses) ---
@app.post("/api/diagnose")
async def diagnose_plant(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        prompt = """
        Kamu Dokter Tanaman. Analisis gambar ini.
        Jawab format JSON: {"penyakit": "...", "solusi": "..."}
        """
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[prompt, image]
        )
        return {"status": "sukses", "data": response.text}
    except Exception as e:
        return {"status": "error", "pesan": str(e)}

# --- ENDPOINT 2: CARI KOTA (Baru) ---
@app.get("/api/search-city")
def search_city(keyword: str):
    try:
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={keyword}&count=10&language=id&format=json"
        resp = requests.get(url).json()
        
        if not resp.get('results'):
            return {"results": []}
            
        # Rapikan data untuk Vue
        data_bersih = []
        for item in resp['results']:
            label = f"{item['name']}, {item.get('admin1', '')}, {item.get('country','')}"
            data_bersih.append({
                "id": item['id'],
                "label": label,
                "lat": item['latitude'],
                "lon": item['longitude']
            })
        return {"results": data_bersih}
    except Exception as e:
        return {"results": [], "error": str(e)}

# --- ENDPOINT 3: AMBIL DATA CUACA REAL (Baru) ---
@app.get("/api/get-weather")
def get_weather_data(lat: float, lon: float):
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code,wind_speed_10m&timezone=auto"
        resp = requests.get(url).json()
        current = resp['current']
        
        # Translate Kode Cuaca
        code = current['weather_code']
        kondisi = "Cerah/Berawan"
        if code in [51, 53, 55, 61, 63, 65, 80, 81, 82]: kondisi = "Hujan"
        elif code in [95, 96, 99]: kondisi = "Badai Petir"
        
        return {
            "suhu": f"{current['temperature_2m']} °C",
            "kondisi": kondisi,
            "angin": f"{current['wind_speed_10m']} km/h"
        }
    except Exception as e:
        return {"error": str(e)}

# --- ENDPOINT 4: KONSULTASI STRATEGI KE GEMINI (Baru) ---
@app.post("/api/ask-weather-strategy")
def ask_gemini_weather(data: WeatherRequest):
    # 'data' otomatis berisi JSON yang dikirim Vue
    try:
        prompt = f"""
        Bertindaklah sebagai Ahli Meteorologi Pertanian.
        Lokasi: {data.lokasi}
        Cuaca Real-time: {data.suhu}, {data.kondisi}, Angin {data.angin}.
        Tanaman Petani: {data.tanaman} (Fase: {data.fase}).
        
        Berikan strategi bertani SINGKAT (poin-poin) menghadapi cuaca ini.
        Format JSON: {{"strategi": "..."}}
        """
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return {"status": "sukses", "data": response.text}
    except Exception as e:
        return {"status": "error", "pesan": str(e)}