<script setup>
import { ref } from 'vue'
import axios from 'axios'
import FiturCuaca from './components/FiturCuaca.vue'

// State Halaman
const menuAktif = ref('diagnosis') 

// --- LOGIKA DIAGNOSIS (Tetap Sama) ---
const fileGambar = ref(null)
const pratinjauGambar = ref(null)
const hasilDiagnosis = ref(null)
const loading = ref(false)

const handlePilihFile = (event) => {
  const file = event.target.files[0]
  if (file) {
    fileGambar.value = file
    pratinjauGambar.value = URL.createObjectURL(file)
    hasilDiagnosis.value = null
  }
}

const kirimKeDokter = async () => {
  if (!fileGambar.value) return alert("Pilih foto dulu!")
  loading.value = true
  const formData = new FormData()
  formData.append("file", fileGambar.value)
  try {
    const response = await axios.post("http://127.0.0.1:8000/api/diagnose", formData)
    hasilDiagnosis.value = JSON.parse(response.data.data)
  } catch (err) {
    alert("Gagal koneksi server Python")
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="dashboard-container">
    
    <aside class="sidebar">
      <div class="brand">
        <h2>🌱 Tani-Selamat</h2>
        <p>Web Dashboard</p>
      </div>

      <nav class="menu-list">
        <button 
          :class="{ active: menuAktif === 'diagnosis' }" 
          @click="menuAktif = 'diagnosis'">
          🏥 Diagnosis Penyakit
        </button>
        <button 
          :class="{ active: menuAktif === 'cuaca' }" 
          @click="menuAktif = 'cuaca'">
          ☁️ Konsultan Cuaca
        </button>
      </nav>

      <div class="footer-sidebar">
        <p>© 2026 Tani-Selamat</p>
      </div>
    </aside>

    <main class="main-content">
      
      <header class="top-bar">
        <h3>{{ menuAktif === 'diagnosis' ? 'Diagnosis Tanaman' : 'Strategi Cuaca' }}</h3>
        <div class="user-profile">👤 Petani Cerdas</div>
      </header>

      <div v-if="menuAktif === 'diagnosis'" class="content-wrapper">
        <div class="grid-layout">
          
          <div class="card upload-section">
            <h3>📸 Upload Foto</h3>
            <div class="upload-area">
              <div v-if="pratinjauGambar" class="preview-box">
                <img :src="pratinjauGambar" />
              </div>
              <div v-else class="placeholder">
                <p>Seret foto kesini atau klik tombol</p>
              </div>
              
              <input type="file" id="fileInput" @change="handlePilihFile" accept="image/*" hidden />
              <label for="fileInput" class="btn-pilih">Pilih Gambar</label>
            </div>
            
            <button @click="kirimKeDokter" :disabled="loading || !fileGambar" class="btn-aksi">
              {{ loading ? 'Sedang Menganalisis...' : '🚀 Mulai Diagnosis' }}
            </button>
          </div>

          <div class="card result-section">
            <h3>📑 Hasil Analisis AI</h3>
            <div v-if="hasilDiagnosis">
              <div class="alert-box">
                <h4>{{ hasilDiagnosis.penyakit }}</h4>
              </div>
              <div class="solution-text">
                <p><strong>Solusi & Penanganan:</strong></p>
                <p>{{ hasilDiagnosis.solusi }}</p>
              </div>
            </div>
            <div v-else class="empty-state">
              <p>Hasil diagnosis akan muncul di sini setelah AI selesai bekerja.</p>
            </div>
          </div>

        </div>
      </div>

      <div v-if="menuAktif === 'cuaca'" class="content-wrapper">
        <FiturCuaca />
      </div>

    </main>
  </div>
</template>

<style scoped>
/* RESET DASAR */
* { box-sizing: border-box; }
.dashboard-container { display: flex; min-height: 100vh; font-family: 'Segoe UI', sans-serif; background-color: #f3f4f6; }

/* SIDEBAR STYLE */
.sidebar {
  width: 260px;
  background-color: #1e293b; /* Warna gelap profesional */
  color: white;
  display: flex;
  flex-direction: column;
  padding: 20px;
  position: fixed; /* Sidebar diam saat scroll */
  height: 100vh;
}
.brand h2 { margin: 0; color: #4ade80; }
.brand p { margin: 5px 0 30px; color: #94a3b8; font-size: 0.9rem; }
.menu-list button {
  background: transparent; border: none; color: #cbd5e1;
  width: 100%; text-align: left; padding: 15px;
  cursor: pointer; font-size: 1rem; border-radius: 8px;
  margin-bottom: 5px; transition: 0.3s;
}
.menu-list button:hover { background: #334155; color: white; }
.menu-list button.active { background: #16a34a; color: white; font-weight: bold; }
.footer-sidebar { margin-top: auto; color: #64748b; font-size: 0.8rem; text-align: center; }

/* MAIN CONTENT STYLE */
.main-content {
  flex: 1;
  margin-left: 260px; /* Memberi ruang untuk sidebar */
  display: flex; flex-direction: column;
}

.top-bar {
  background: white; padding: 15px 30px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}
.content-wrapper { padding: 30px; }

/* LAYOUT DIAGNOSIS (GRID) */
.grid-layout {
  display: grid;
  grid-template-columns: 1fr 1fr; /* Dua kolom sama besar */
  gap: 30px;
}
.card { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }

/* UPLOAD STYLE */
.upload-area { text-align: center; margin: 20px 0; }
.placeholder { border: 2px dashed #cbd5e1; padding: 40px; border-radius: 10px; color: #64748b; }
.preview-box img { max-width: 100%; max-height: 300px; border-radius: 8px; }
.btn-pilih { display: inline-block; background: #e2e8f0; padding: 10px 20px; border-radius: 5px; cursor: pointer; margin-top: 10px; font-weight: bold; }
.btn-aksi { width: 100%; background: #16a34a; color: white; padding: 15px; border: none; border-radius: 8px; font-size: 1.1rem; cursor: pointer; font-weight: bold; }
.btn-aksi:hover { background: #15803d; }
.btn-aksi:disabled { background: #cbd5e1; }

/* RESULT STYLE */
.empty-state { text-align: center; color: #94a3b8; padding: 50px; border: 2px dashed #e2e8f0; border-radius: 10px; }
.alert-box { background: #fee2e2; color: #991b1b; padding: 15px; border-radius: 8px; border-left: 5px solid #ef4444; margin-bottom: 20px; }
.solution-text { line-height: 1.6; color: #334155; }
</style>