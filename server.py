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
server = SimpleXMLRPCServer(("127.0.0.1", 8080),requestHandler=RequestHandler, allow_none=True) 
server.register_introspection_functions()

# buat data struktur array untuk menampung klinik di rumah sakit
# klinik_rumah_sakit = ['Klinik Gigi', 'Klinik Penyakit Dalam', 'Klinik C']
klinik = {'Klinik Gigi':0 , 'Klinik Penyakit Dalam':0, 'Klinik Anak': 0, 'Klinik Kulit': 0}    
klinik_gigi = []
klinik_pnykit_dalam = []
klinik_anak = []
klinik_kulit = []

# kode setelah ini adalah critical section, menambahkan vote tidak boeh terjadi race condition
# siapkan lock
lock = threading.Lock()

# buat fungsi bernama reverse
# def reverse(x):
#     return [ele for ele in reversed(x)]

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
    if len(klinik_gigi) == 0:
        return None
    return klinik_gigi

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
    if no_antrean == 1:
        return datetime.datetime.now() + datetime.timedelta(minutes= 1)
    else:
        if klinik == 'Klinik Gigi':
            return klinik_gigi[-1]['jam_check_up'] + datetime.timedelta(minutes= random.randint(5, 8))
        elif klinik == 'Klinik Penyakit Dalam':
            return klinik_pnykit_dalam[-1]['jam_check_up'] + datetime.timedelta(minutes= random.randint(5, 8))
        elif klinik == 'Klinik Anak':
            return klinik_anak[-1]['jam_check_up'] + datetime.timedelta(minutes= random.randint(5, 8))
        elif klinik == 'Klinik Kulit':
            return klinik_kulit[-1]['jam_check_up'] + datetime.timedelta(minutes= random.randint(5, 8))
        

# buat fungsi bernama daftarkan_pasien()
def daftarkan_pasien(input_klinik, no_rekam_medis, nama, tgl_lahir):
    # critical section dimulai
    lock.acquire()

    pasien = registrasi_pasien(no_rekam_medis, nama, tgl_lahir)

    klinik_keys = list(klinik)
    klinik[klinik_keys[input_klinik-1]] = klinik.get(klinik_keys[input_klinik-1]) + 1
    pasien['klinik'] = klinik_keys[input_klinik-1]
    pasien['no_antrean'] = cari_nomor_antrean(klinik_keys[input_klinik-1])
    pasien['jam_check_up'] = jam_check_up_pasien(pasien['no_antrean'], pasien['klinik'])


    if pasien['klinik'] == 'Klinik Gigi':
        klinik_gigi.append(pasien)
    elif pasien['klinik'] == 'Klinik Penyakit Dalam':
        klinik_pnykit_dalam.append(pasien)
    elif pasien['klinik'] == 'Klinik Anak':
        klinik_anak.append(pasien)
    elif pasien['klinik'] == 'Klinik Kulit':
        klinik_kulit.append(pasien)
    print(pasien)

    # critical section berakhir
    lock.release()

# register daftarkan_pasien sebagai daftarPasien
server.register_function(daftarkan_pasien, 'daftarPasien')

# Jalankan server
def run_server():
    print('Running server...')
    server.serve_forever()

def update_klinik_kulit():
    while True:
        if len(klinik_kulit) != 0:
            pasien = klinik_kulit[0]
            if datetime.datetime.now() >= pasien['jam_check_up']:
                del klinik_kulit[0]
                klinik[pasien['klinik']] = klinik.get(pasien['klinik']) - 1
                print('[POP] Data selesai')

def update_klinik_gigi():
    while True:
        if len(klinik_gigi) != 0:
            pasien = klinik_gigi[0]
            if datetime.datetime.now() >= pasien['jam_check_up']:
                del klinik_gigi[0]
                klinik[pasien['klinik']] = klinik.get(pasien['klinik']) - 1
                print('[POP] Data selesai')

def update_klinik_anak():
    while True:
        if len(klinik_anak) != 0:
            pasien = klinik_anak[0]
            if datetime.datetime.now() >= pasien['jam_check_up']:
                del klinik_anak[0]
                klinik[pasien['klinik']] = klinik.get(pasien['klinik']) - 1
                print('[POP] Data selesai')

def update_klinik_pnykit_dalam():
    while True:
        if len(klinik_pnykit_dalam) != 0:
            pasien = klinik_pnykit_dalam[0]
            if datetime.datetime.now() >= pasien['jam_check_up']:
                del klinik_pnykit_dalam[0]
                klinik[pasien['klinik']] = klinik.get(pasien['klinik']) - 1
                print('[POP] Data selesai')

if __name__ == '__main__':
    threading.Thread(target = run_server).start()
    threading.Thread(target = update_klinik_kulit).start()
    threading.Thread(target = update_klinik_gigi).start()
    threading.Thread(target = update_klinik_anak).start()
    threading.Thread(target = update_klinik_pnykit_dalam).start()
