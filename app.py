import json
import os
from datetime import datetime

from kivy.app import App
from kivy.lang import Builder
from kivy.core.text import LabelBase
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty, DictProperty, NumericProperty
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.behaviors.togglebutton import ToggleButtonBehavior

# --- KONFIGURASI APLIKASI ---
LabelBase.register(name="FredokaOne", fn_regular="assets/Fredoka-Regular.ttf") 
NAMA_HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
DATA_FILE = "data.json"

# --- MODEL DATA ---
class User:
    def __init__(self, username, nama, role):
        self.username = username
        self.nama = nama
        self.role = role

class Siswa(User):
    def __init__(self, username, nama, nomor_induk, kelas):
        super().__init__(username, nama, "Siswa")
        self.nomor_induk = nomor_induk
        self.kelas = kelas

class Guru(User):
    def __init__(self, username, nama, nip, mata_pelajaran):
        super().__init__(username, nama, "Guru")
        self.nip = nip
        self.mata_pelajaran = mata_pelajaran

# --- WIDGET KUSTOM & POPUP ---
class PilihWaktuPopup(ModalView):
    on_set = ObjectProperty(None)
    jam = StringProperty("07")
    menit = StringProperty("00")
    def ubahWaktu(self, bagian, jumlah):
        if bagian == "Jam": self.jam = f"{(int(self.jam) + jumlah) % 24:02d}"
        elif bagian == "Menit": self.menit = f"{(int(self.menit) + jumlah) % 60:02d}"
    def setWaktu(self):
        if self.on_set: self.on_set(f"{int(self.jam):02d}:{int(self.menit):02d}")
        self.dismiss()

class TambahJadwalPopup(ModalView):
    namaHari = StringProperty("")
    waktuMulai = StringProperty("07:00")
    waktuSelesai = StringProperty("08:00")
    kategori = StringProperty("Mata Pelajaran")
    item_id = StringProperty(None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.item_id:
            app = App.get_running_app()
            all_jadwal = app.jadwal
            item_data = next((item for item in all_jadwal.get(self.namaHari, []) if item['id'] == self.item_id), None)
            if item_data:
                self.ids.aktifitas.text = item_data.get('aktivitas', '')
                self.ids.ruang.text = item_data.get('ruang', '')
                self.waktuMulai = item_data.get('mulai', '07:00')
                self.waktuSelesai = item_data.get('selesai', '08:00')
                self.kategori = item_data.get('kategori', 'Mata Pelajaran')
                for button in self.ids.kategori_box.children:
                    if hasattr(button, 'text') and button.text == self.kategori:
                        button.state = 'down'

    def atur_kategori(self, kategori_terpilih):
        self.kategori = kategori_terpilih

    def showPilihWaktu(self, tipeWaktu):
        pilihWaktu = PilihWaktuPopup()
        def updateWaktu(waktuDipilih):
            if tipeWaktu == "Mulai": self.waktuMulai = waktuDipilih
            else: self.waktuSelesai = waktuDipilih
        pilihWaktu.on_set = updateWaktu
        pilihWaktu.open()

    def simpanJadwal(self):
        namaAktivitas = self.ids.aktifitas.text.strip()
        ruang = self.ids.ruang.text.strip()
        if namaAktivitas:
            dataJadwal = {
                "id": self.item_id if self.item_id else f"{datetime.now().timestamp()}",
                "kategori": self.kategori,
                "aktivitas": namaAktivitas,
                "ruang": ruang,
                "mulai": self.waktuMulai,
                "selesai": self.waktuSelesai,
            }
            app = App.get_running_app()
            if self.item_id:
                app.edit_jadwal(self.namaHari, self.item_id, dataJadwal)
            else:
                app.tambah_jadwal(self.namaHari, dataJadwal)
            self.dismiss()

class KonfirmasiPopup(ModalView):
    namaHari = StringProperty("")
    itemId = StringProperty("")
    def konfirmasiHapus(self):
        if self.namaHari and self.itemId: 
            App.get_running_app().hapus_jadwal(self.namaHari, self.itemId)
        self.dismiss()

class DaftarJadwal(BoxLayout):
    data = DictProperty()
    namaHari = StringProperty("")
    is_guru = BooleanProperty(False)

    def hapusItem(self):
        if self.data and self.is_guru:
            KonfirmasiPopup(namaHari=self.namaHari, itemId=self.data['id']).open()
    
    def editItem(self):
        if self.data and self.is_guru:
            TambahJadwalPopup(namaHari=self.namaHari, item_id=self.data['id']).open()

class LihatHari(ToggleButtonBehavior, BoxLayout):
    namaHari = StringProperty("")
    daftarJadwal = ListProperty([])
    is_guru = BooleanProperty(False)
    hariIni = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.updateTampilan)

    def on_state(self, instance, value):
        app = App.get_running_app()
        if value == 'down':
            app.hari_aktif = self.namaHari
        elif app.hari_aktif == self.namaHari:
             app.hari_aktif = ""

    def updateTampilan(self, *args):
        gridJadwal = self.ids.grid_jadwal
        gridJadwal.clear_widgets()
        if not self.daftarJadwal:
            gridJadwal.add_widget(Label(text="Tidak ada jadwal", color=(0.5, 0.5, 0.5, 1), font_size='14sp', halign='center'))
        else:
            sortirJadwal = sorted(self.daftarJadwal, key=lambda x: x['mulai'])
            for item in sortirJadwal:
                itemWidget = DaftarJadwal(data=item, namaHari=self.namaHari, is_guru=self.is_guru)
                gridJadwal.add_widget(itemWidget)

    def bukaTambahPopup(self):
        if self.is_guru:
            TambahJadwalPopup(namaHari=self.namaHari).open()

# --- LAYAR APLIKASI ---
class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text.strip()
        password = self.ids.password_input.text.strip()
        App.get_running_app().login(username, password)

class MainScreen(Screen):
    pass

# --- APLIKASI UTAMA ---
class JadwalApp(App):
    current_user = ObjectProperty(None, allownone=True, rebind=True)
    jadwal = DictProperty()
    hari_aktif = StringProperty("")
    data_file_last_modified = NumericProperty(0)

    def build(self):
        self.root = Builder.load_file('jadwalKita.kv') 
        self.load_data_from_json()
        return self.root
    
    def on_start(self):
        Clock.schedule_interval(self.check_for_data_updates, 2)

    def check_for_data_updates(self, dt):
        try:
            current_mod_time = os.path.getmtime(DATA_FILE)
            if current_mod_time > self.data_file_last_modified:
                print("Perubahan data terdeteksi! Memuat ulang...")
                self.load_data_from_json(force_refresh=True)
        except FileNotFoundError:
            pass

    # on_jadwal tetap ada untuk menangani refresh dari polling file
    def on_jadwal(self, instance, value):
        self.refresh_ui()

    def on_current_user(self, instance, value):
        if value:
            self.hari_aktif = NAMA_HARI[datetime.today().weekday()]
            self.root.current = 'main'
            self.refresh_ui()
        else:
            self.root.current = 'login'
            self.hari_aktif = ""

    def login(self, username, password):
        try:
            with open(DATA_FILE, 'r') as f:
                self.data = json.load(f)
        except (json.JSONDecodeError, ValueError, FileNotFoundError):
            self._create_default_data()

        if username in self.data["users"] and self.data["users"][username]["password"] == password:
            user_data = self.data["users"][username]
            role = user_data["role"]
            if role == "Guru": 
                self.current_user = Guru(username, user_data["nama"], user_data["nip"], user_data["mata_pelajaran"])
            else: 
                self.current_user = Siswa(username, user_data["nama"], user_data["nomor_induk"], user_data["kelas"])
            self.jadwal = self.data["jadwal"]
            self.root.get_screen('login').ids.error_label.opacity = 0
        else:
            self.root.get_screen('login').ids.error_label.opacity = 1
    
    def logout(self):
        self.current_user = None
        self.jadwal = {}

    def tampilkanLayarUtama(self):
        layoutUtama = self.root.get_screen('main').ids.layout_utama
        layoutUtama.clear_widgets()
        if not self.current_user: return
        
        is_guru = isinstance(self.current_user, Guru)

        for hari in NAMA_HARI:
            hariIni = (hari == NAMA_HARI[datetime.today().weekday()])
            widgetHari = LihatHari(
                namaHari=hari, 
                hariIni=hariIni, 
                is_guru=is_guru, 
                daftarJadwal=self.jadwal.get(hari, []),
                state='down' if self.hari_aktif == hari else 'normal'
            )
            layoutUtama.add_widget(widgetHari)
            
            if hariIni and self.hari_aktif == hari:
                Clock.schedule_once(lambda dt, w=widgetHari: self.root.get_screen('main').ids.scroll_utama.scroll_to(w), 0.2)

    def refresh_ui(self):
        if self.root and self.root.current == 'main': 
            self.tampilkanLayarUtama()

    def tambah_jadwal(self, namaHari, dataJadwal):
        jadwal_baru = self.jadwal.copy()
        jadwal_baru.setdefault(namaHari, []).append(dataJadwal)
        self.hari_aktif = namaHari
        self.jadwal = jadwal_baru
        self.save_data_to_json()
        self.refresh_ui() # PANGGILAN LANGSUNG untuk memastikan refresh

    def hapus_jadwal(self, namaHari, itemId):
        jadwal_baru = self.jadwal.copy()
        jadwal_hari = jadwal_baru.get(namaHari, [])
        jadwal_baru[namaHari] = [item for item in jadwal_hari if item['id'] != itemId]
        self.hari_aktif = namaHari
        self.jadwal = jadwal_baru
        self.save_data_to_json()
        self.refresh_ui() # PANGGILAN LANGSUNG untuk memastikan refresh
    
    def edit_jadwal(self, namaHari, item_id, data_baru):
        jadwal_baru = self.jadwal.copy()
        jadwal_hari = jadwal_baru.get(namaHari, [])
        jadwal_baru[namaHari] = [item for item in jadwal_hari if item['id'] != item_id]
        jadwal_baru[namaHari].append(data_baru)
        self.hari_aktif = namaHari
        self.jadwal = jadwal_baru
        self.save_data_to_json()
        self.refresh_ui() # PANGGILAN LANGSUNG untuk memastikan refresh
        
    def load_data_from_json(self, force_refresh=False):
        if not os.path.exists(DATA_FILE): self._create_default_data()
        
        try:
            with open(DATA_FILE, 'r') as f:
                loaded_data = json.load(f)
            self.data_file_last_modified = os.path.getmtime(DATA_FILE)
        except (json.JSONDecodeError, ValueError, FileNotFoundError): 
            self._create_default_data()
            with open(DATA_FILE, 'r') as f:
                loaded_data = json.load(f)

        self.data = {"users": loaded_data.get("users", {})}
        new_jadwal = loaded_data.get('jadwal', {hari: [] for hari in NAMA_HARI})
        
        if self.jadwal != new_jadwal or force_refresh:
            self.jadwal = new_jadwal

    def save_data_to_json(self):
        data_to_save = {
            "users": self.data.get("users", {}),
            "jadwal": self.jadwal
        }
        with open(DATA_FILE, 'w') as f: json.dump(data_to_save, f, indent=4)
        
        try:
            self.data_file_last_modified = os.path.getmtime(DATA_FILE)
        except FileNotFoundError:
            pass

    def _create_default_data(self):
        # Data user yang diperbarui
        self.data = {
            "users": {
                "guru#": {"nama": "Budi Setiawan", "password": "cukuptau", "role": "Guru", "nip": "198501012010011001", "mata_pelajaran": "Matematika"},
                "siswa": {"nama": "nama_siswa", "password": "belajar", "role": "Siswa", "nomor_induk": "22001", "kelas": "XI-A"}
            },
            "jadwal": {hari: [] for hari in NAMA_HARI}
        }
        self.save_data_to_json()

if __name__ == '__main__':
    JadwalApp().run()