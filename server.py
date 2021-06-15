# import SimpleXMLRPCServer
from xmlrpc.client import DateTime
from xmlrpc.server import SimpleXMLRPCServer
# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler

import threading
import datetime
import random

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

# Buat server
server = SimpleXMLRPCServer(("26.60.48.126", 8080),requestHandler=RequestHandler, allow_none=True) 
server.register_introspection_functions()

# buat data struktur array untuk menampung klinik di rumah sakit
# klinik_rumah_sakit = ['Klinik Gigi', 'Klinik Penyakit Dalam', 'Klinik C']
klinik = {'Klinik Gigi':0 , 'Klinik Penyakit Dalam':0, 'Klinik Anak': 0, 'Klinik Kulit': 0}    
antrean_pasien = []

# kode setelah ini adalah critical section, menambahkan vote tidak boeh terjadi race condition
# siapkan lock
lock = threading.Lock()

# buat fungsi bernama reverse
def reverse(x):
    return [ele for ele in reversed(x)]

#  buat fungsi bernama check_rekam_medis()
# def check_rekam_medis(no_rekam_medis):
#     # melakukan pengecekan apakah nomor rekam medis sudah ada
#     for pasien in antrean_pasien:
#         if pasien['no_rek_medis'] == no_rekam_medis:
#             return False
#     return True

# # register check_rekam_medis sebagai cekRekamMedis
# server.register_function(check_rekam_medis, 'cekRekamMedis')

#  buat fungsi bernama check_klinik()
def check_klinik(no_klinik):
    # melakukan pengecekan apakah nomor klinik terdaftar
    if no_klinik.isdigit():
        if int(no_klinik) in range(len(klinik)+1):
            return True
        else:
            return False
    else:
        print("[Error] Masukan Angka!")

# register check_klinik sebagai cekKlinik
server.register_function(check_klinik, 'cekKlinik')

#  buat fungsi bernama get_antrean()
def get_antrean():
    if len(antrean_pasien) == 0:
        return None
    return antrean_pasien

# register get_antrean sebagai getAntrean
server.register_function(get_antrean, 'getAntrean')

#  buat fungsi bernama get_klinik()
def get_klinik():
    return klinik

# register get_klinik sebagai getKlinik
server.register_function(get_klinik, 'getKlinik')

# buat fungsi bernama masuk_klinik()
def masuk_klinik(no_klinik):
    klinik_keys = list(klinik)
    if (klinik[klinik_keys[no_klinik-1]] <= 3):
        return True
    else:
        return False

# register masuk_klinik sebagai masukKlinik
server.register_function(masuk_klinik, 'masukKlinik')

# buat fungsi bernama registrasi_pasien()
def registrasi_pasien(no_rekam_medis, nama, tgl_lahir):
    # membuat struktur data dictionary menampung data pasien
    x = {
        'no_rek_medis' : no_rekam_medis,
        'nama_pasien' : nama,
        'tgl_lahir' : tgl_lahir,
    }
    return x

# buat fungsi bernama cari_nomor_antrean()
def cari_nomor_antrean(klinik):
    # membalikan list antrean pasien agar data yang terbaru menjadi di depan
    temp_list = reverse(antrean_pasien)

    # mencari nomor antrean
    for pasien in temp_list:
        if pasien['klinik'] == klinik:
            return pasien['no_antrean']+1

    # membalikan nomor antrean 1 jika tidak ditemukan pasien pada klinik tsb
    return 1

# buat fungsi bernama daftarkan_pasien()
def daftarkan_pasien(input_klinik, no_rekam_medis, nama, tgl_lahir):
    # critical section dimulai
    lock.acquire()

    pasien = registrasi_pasien(no_rekam_medis, nama, tgl_lahir)

    klinik_keys = list(klinik)
    klinik[klinik_keys[input_klinik-1]] = klinik.get(klinik_keys[input_klinik-1]) + 1
    pasien['klinik'] = klinik_keys[input_klinik-1]
    pasien['no_antrean'] = cari_nomor_antrean(klinik_keys[input_klinik-1])

    if pasien['no_antrean'] == 1:
        pasien['jam_check_up'] = datetime.datetime.now() + datetime.timedelta(minutes= 1)
    else:
        pasien['jam_check_up'] = antrean_pasien[-1]['jam_check_up'] + datetime.timedelta(minutes= random.randint(5, 8))
    antrean_pasien.append(pasien)
    print(pasien)

    # critical section berakhir
    lock.release()

# register daftarkan_pasien sebagai daftarPasien
server.register_function(daftarkan_pasien, 'daftarPasien')

# Jalankan server
def run_server():
    print('Running server...')
    server.serve_forever()

def update():
    while True:
        if len(antrean_pasien) != 0:
            pasien = antrean_pasien[0]
            if datetime.datetime.now() >= pasien['jam_check_up']:

                lock.acquire()
                antrean_pasien.pop()
                klinik[pasien['klinik']] = klinik.get(pasien['klinik']) - 1
                print('[POP] Data selesai')
                lock.release()


if __name__ == '__main__':
    threading.Thread(target = run_server).start()
    threading.Thread(target = update).start()
