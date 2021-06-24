import datetime
import random
import pickle
from os import path

# membuat class DB untuk menyimpan data pada file 'db'
class DB:
    # inisialisasi class DB
    def __init__(self, filename):
        # jika file belum dibuat, maka inisialisasi data dan filenya
        if not path.exists(filename):
            self.data = {
                "klinik": {'Klinik Gigi': 0, 'Klinik Penyakit Dalam': 0,
                           'Klinik Anak': 0, 'Klinik Kulit': 0},
                "klinik_gigi": [],
                "klinik_pnykit_dalam": [],
                "klinik_anak": [],
                "klinik_kulit": [],
            }
            file = open(filename, 'wb')
            pickle.dump(self.data, file)

        self.filename = filename
    # fungsi untuk menyimpan data pada file
    def save(self, data):
        file = open(self.filename, 'wb')
        pickle.dump(data, file)
        file.close()
    # fungsi untuk membaca data pada file
    def load(self):
        file = open(self.filename, 'rb')
        data = pickle.load(file)
        file.close()
        return data

# init class db
db = DB('db')

#  buat fungsi bernama check_klinik()
def check_klinik(no_klinik):
    # melakukan pengecekan apakah nomor klinik terdaftar
    if no_klinik.isdigit():
        if int(no_klinik) in range(len(db.load()["klinik"])+1):
            return True
        else:
            return False
    else:
        print("[Error] Masukan Angka!")

# buat fungsi check pasien
def check_pasien(no_rekam_medis):
    data = db.load()
    # dilakukan pengecekan no rekam medis di setiap klinik
    for pasien in data["klinik_anak"]:
        if pasien['no_rek_medis'] == no_rekam_medis:
            return pasien
    for pasien in data["klinik_gigi"]:
        if pasien['no_rek_medis'] == no_rekam_medis:
            return pasien
    for pasien in data["klinik_kulit"]:
        if pasien['no_rek_medis'] == no_rekam_medis:
            return pasien
    for pasien in data["klinik_pnykit_dalam"]:
        if pasien['no_rek_medis'] == no_rekam_medis:
            return pasien
    return None


#  buat fungsi bernama get_antrean()
def get_antrean():
    data = db.load()
    return data["klinik_anak"], data["klinik_gigi"], data["klinik_kulit"], data["klinik_pnykit_dalam"]

#  buat fungsi bernama get_klinik()
def get_klinik():
    return db.load()["klinik"]

# buat fungsi bernama masuk_klinik()
def masuk_klinik(no_klinik):
    klinik = db.load()["klinik"]
    klinik_keys = list(klinik)
    if (klinik[klinik_keys[no_klinik-1]] <= 3):
        return True
    else:
        return False

# buat fungsi bernama registrasi_pasien()
def registrasi_pasien(input_klinik, no_rekam_medis, nama, tgl_lahir):
    data = db.load()
    klinik = data["klinik"]
    klinik_kulit = data["klinik_kulit"]
    klinik_gigi = data["klinik_gigi"]
    klinik_anak = data["klinik_anak"]
    klinik_pnykit_dalam = data["klinik_pnykit_dalam"]

    # membuat struktur data dictionary menampung data pasien
    pasien = {
        'no_rek_medis': no_rekam_medis,
        'nama_pasien': nama,
        'tgl_lahir': tgl_lahir,
    }

    klinik_keys = list(klinik)
    klinik[klinik_keys[input_klinik-1]
           ] = klinik.get(klinik_keys[input_klinik-1]) + 1
    pasien['klinik'] = klinik_keys[input_klinik-1]
    pasien['no_antrean'] = cari_nomor_antrean(klinik_keys[input_klinik-1])
    pasien['jam_check_up'] = jam_check_up_pasien(
        pasien['no_antrean'], pasien['klinik'])

    if pasien['klinik'] == 'Klinik Gigi':
        klinik_gigi.append(pasien)
    elif pasien['klinik'] == 'Klinik Penyakit Dalam':
        klinik_pnykit_dalam.append(pasien)
    elif pasien['klinik'] == 'Klinik Anak':
        klinik_anak.append(pasien)
    elif pasien['klinik'] == 'Klinik Kulit':
        klinik_kulit.append(pasien)

    db.save({
        "klinik": klinik,
        "klinik_gigi": klinik_gigi,
        "klinik_pnykit_dalam": klinik_pnykit_dalam,
        "klinik_anak": klinik_anak,
        "klinik_kulit": klinik_kulit
    })
    return pasien

# buat fungsi bernama cari_nomor_antrean()
def cari_nomor_antrean(klinik):
    data = db.load()

    klinik_kulit = data["klinik_kulit"]
    klinik_gigi = data["klinik_gigi"]
    klinik_anak = data["klinik_anak"]
    klinik_pnykit_dalam = data["klinik_pnykit_dalam"]

    # membalikan list pasien agar data yang terbaru menjadi di depan
    if klinik == 'Klinik Gigi':
        temp_list = klinik_gigi
    elif klinik == 'Klinik Penyakit Dalam':
        temp_list = klinik_pnykit_dalam
    elif klinik == 'Klinik Anak':
        temp_list = klinik_anak
    elif klinik == 'Klinik Kulit':
        temp_list = klinik_kulit

    # mencari nomor antrean
    if len(temp_list) == 0:
        return 1
    else:
        return temp_list[-1]['no_antrean'] + 1

# buat fungsi bernama jam_check_up_pasien()
def jam_check_up_pasien(no_antrean, klinik):
    data = db.load()

    klinik_kulit = data["klinik_kulit"]
    klinik_gigi = data["klinik_gigi"]
    klinik_anak = data["klinik_anak"]
    klinik_pnykit_dalam = data["klinik_pnykit_dalam"]

    if no_antrean == 1:
        return datetime.datetime.now() + datetime.timedelta(minutes=1)
    else:
        if klinik == 'Klinik Gigi':
            return klinik_gigi[-1]['jam_check_up'] + datetime.timedelta(minutes=random.randint(5, 8))
        elif klinik == 'Klinik Penyakit Dalam':
            return klinik_pnykit_dalam[-1]['jam_check_up'] + datetime.timedelta(minutes=random.randint(5, 8))
        elif klinik == 'Klinik Anak':
            return klinik_anak[-1]['jam_check_up'] + datetime.timedelta(minutes=random.randint(5, 8))
        elif klinik == 'Klinik Kulit':
            return klinik_kulit[-1]['jam_check_up'] + datetime.timedelta(minutes=random.randint(5, 8))


def pop_klinik(k):
    data = db.load()

    klinik = data["klinik"]
    klinik_kulit = data["klinik_kulit"]
    klinik_gigi = data["klinik_gigi"]
    klinik_anak = data["klinik_anak"]
    klinik_pnykit_dalam = data["klinik_pnykit_dalam"]

    if k == 'Klinik Gigi':
        del klinik_gigi[0]
    elif k == 'Klinik Penyakit Dalam':
        del klinik_pnykit_dalam[0]
    elif k == 'Klinik Anak':
        del klinik_anak[0]
    elif k == 'Klinik Kulit':
        del klinik_kulit[0]

    klinik[k] = klinik.get(k) - 1

    db.save({
        "klinik": klinik,
        "klinik_gigi": klinik_gigi,
        "klinik_pnykit_dalam": klinik_pnykit_dalam,
        "klinik_anak": klinik_anak,
        "klinik_kulit": klinik_kulit
    })
    print('[POP] Data selesai')
