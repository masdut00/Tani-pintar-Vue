<script setup>
import { ref } from 'vue'
import axios from 'axios'

const keyword = ref("")
const hasilPencarian = ref([])
const lokasiTerpilih = ref(null)
const dataCuaca = ref(null)
const tanaman = ref("")
const fase = ref("Vegetatif")
const hasilSaran = ref("")
const loading = ref(false)

const cariKota = async () => {
    if(!keyword.value) return
    const res = await axios.get(`http://127.0.0.1:8000/api/search-city?keyword=${keyword.value}`)
    hasilPencarian.value = res.data.results
}

const pilihKota = async (kota) => {
    lokasiTerpilih.value = kota
    hasilPencarian.value = []
    const res = await axios.get(`http://127.0.0.1:8000/api/get-weather?lat=${kota.lat}&lon=${kota.lon}`)
    dataCuaca.value = res.data
}

const mintaSaran = async () => {
    loading.value = true
    try {
        const payload = {
            lokasi: lokasiTerpilih.value.label,
            suhu: dataCuaca.value.suhu,
            kondisi: dataCuaca.value.kondisi,
            angin: dataCuaca.value.angin,
            tanaman: tanaman.value,
            fase: fase.value
        }
        const res = await axios.post("http://127.0.0.1:8000/api/ask-weather-strategy", payload)
        const jsonRes = JSON.parse(res.data.data)
        hasilSaran.value = jsonRes.strategi
    } catch (e) {
        alert("Gagal koneksi AI")
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="cuaca-container">
    <h2 class="section-title">Konsultan Cuaca</h2>

    <div class="card">
        <div class="input-group">
            <input v-model="keyword" placeholder="Cari Desa/Kecamatan..." @keyup.enter="cariKota" class="input-field" />
            <button @click="cariKota" class="btn-icon">🔍</button>
        </div>
        
        <ul v-if="hasilPencarian.length" class="dropdown-list">
            <li v-for="kota in hasilPencarian" :key="kota.id" @click="pilihKota(kota)">
                📍 {{ kota.label }}
            </li>
        </ul>
    </div>

    <div v-if="dataCuaca" class="card weather-panel">
        <div class="location-badge">📍 {{ lokasiTerpilih.label.split(',')[0] }}</div>
        
        <div class="weather-grid">
            <div class="weather-item">
                <span class="val">{{ dataCuaca.suhu }}</span>
                <span class="lbl">Suhu</span>
            </div>
            <div class="weather-item">
                <span class="val">{{ dataCuaca.kondisi }}</span>
                <span class="lbl">Langit</span>
            </div>
            <div class="weather-item">
                <span class="val">{{ dataCuaca.angin }}</span>
                <span class="lbl">Angin</span>
            </div>
        </div>
    </div>

    <div v-if="dataCuaca" class="card">
        <label class="form-label">Tanaman Apa?</label>
        <input v-model="tanaman" placeholder="Contoh: Cabai" class="input-field mb-2" />
        
        <label class="form-label">Fase Tanam:</label>
        <select v-model="fase" class="input-field mb-3">
            <option>Semai</option>
            <option>Vegetatif</option>
            <option>Berbuah</option>
            <option>Panen</option>
        </select>
        
        <button class="btn-action" @click="mintaSaran" :disabled="loading">
            {{ loading ? 'Meracik Strategi...' : '✨ Minta Saran AI' }}
        </button>
    </div>

    <div v-if="hasilSaran" class="card result-box">
        <h3>📋 Strategi Tani:</h3>
        <div class="strategy-text">{{ hasilSaran }}</div>
    </div>
  </div>
</template>

<style scoped>
/* CONTAINER AGAR RAPI DI TENGAH */
.cuaca-container {
    max-width: 800px; /* Batasi lebar agar enak dibaca di laptop */
    margin: 0 auto;   /* Posisi tengah */
}

.section-title { font-size: 1.5rem; color: #1e293b; margin-bottom: 20px; font-weight: bold; }
.card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px; }

/* INPUT GROUP */
.input-group { display: flex; gap: 15px; }
.input-field { flex: 1; padding: 15px; border: 1px solid #e2e8f0; border-radius: 8px; outline: none; font-size: 1rem; }
.input-field:focus { border-color: #16a34a; box-shadow: 0 0 0 3px rgba(22, 163, 74, 0.1); }
.btn-icon { background: #f1f5f9; border: none; width: 60px; border-radius: 8px; cursor: pointer; font-size: 1.2rem; transition: 0.2s;}
.btn-icon:hover { background: #e2e8f0; }

/* WEATHER PANEL */
.weather-panel { background: linear-gradient(135deg, #0ea5e9, #2563eb); color: white; padding: 30px; }
.location-badge { background: rgba(255,255,255,0.2); display: inline-block; padding: 5px 15px; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }
.weather-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; text-align: center; }
.weather-item .val { display: block; font-weight: bold; font-size: 2rem; margin-bottom: 5px; }
.weather-item .lbl { font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px; }

/* FORM & BUTTON */
.form-label { display: block; font-size: 0.95rem; font-weight: 600; color: #475569; margin-bottom: 8px; }
.mb-2 { margin-bottom: 15px; }
.mb-3 { margin-bottom: 25px; }
.btn-action { width: 100%; background: #0284c7; color: white; border: none; padding: 15px; border-radius: 8px; font-weight: bold; font-size: 1.1rem; cursor: pointer; transition: 0.3s; }
.btn-action:hover { background: #0369a1; }

/* RESULT */
.result-box { border-left: 5px solid #0ea5e9; background: #f0f9ff; }
.strategy-text { white-space: pre-line; color: #334155; line-height: 1.8; font-size: 1rem; }
</style>