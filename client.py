import xmlrpc.client
from datetime import date, datetime, timedelta
from threading import Thread
from os import system, name
from time import sleep

# buat stub (proxy) untuk client
server = xmlrpc.client.ServerProxy('http://26.60.48.126:8080')

def clear(need_continue=True):
    if need_continue:
        input("Press Enter to continue...")
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def daftarkan_diri():
    clear(need_continue=False)
    while True:
        i = 0
        for klinik, jumlah in server.getKlinik().items():
            i+=1
            kondisi = 'Buka' if jumlah <= 3 else 'Penuh'
            print(f"{i}. {klinik} ({kondisi})")
        break

    while True:
        input_klinik = input('Masukan nomor klinik: ')
        if server.cekKlinik(input_klinik):
            input_klinik = int(input_klinik)
            if (server.masukKlinik(input_klinik)):
                break
            else:
                print("[Error] Klinik sudah penuh")
        else:
            print("[Error] Tidak ditemukan klinik dengan nomor tersebut")

    date = datetime.today()
    no_rekam_medis = date.strftime('%d%m%Y') + '.' + date.strftime('%H%M')
    
    nama = input('Masukan nama lengkap: ')
    tgl_lahir = input('Masukan tanggal lahir: ')
    server.daftarPasien(input_klinik, no_rekam_medis, nama, tgl_lahir)
    print('Pasien Telah Terdaftar!')

def cek_antrean():
    print('No. Antrean \t Nama Pasien \t Klinik')
    if server.getAntrean() != None:
        for pasien in server.getAntrean():
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']} \t\t {pasien['klinik']}")
    else:
        print('Tidak ada antrean')

def print_antrean(antrean):
    if (antrean == None):
        print('=======================')
        print('Belum ada antrean')
        print('=======================')
    else:
        date_converted = datetime.strptime(str(antrean[0]['jam_check_up']), "%Y%m%dT%H:%M:%S")
        print('=======================')
        print(f"Nomor Antrean Sekarang: {antrean[0]['no_antrean']}")
        print(f"Waktu Masuk: {date_converted}")
        print('=======================')

while True:
    antrean = server.getAntrean()
    print_antrean(antrean)
    print("Daftar Layanan Rumah Sakit Kelompok 2")
    print("1. Daftarkan Diri ")
    print("2. Cek Antrean")
    print("3. Keluar")
    while True:
        inpt_opt = input("Masukan menu pilihan: ")
        if inpt_opt.isdigit():
            inpt_opt = int(inpt_opt)
            if inpt_opt in range(1, 4):
                break
            else:
                print("[Error] Tidak terdapat opsi tersebut!")
        else:
            print("[Error] Masukan sebuah angka!")

    if inpt_opt == 1:
        daftarkan_diri()
        clear()
    elif inpt_opt == 2:
        cek_antrean()
        clear()
    elif inpt_opt == 3 :
        break
