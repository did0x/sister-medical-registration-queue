import xmlrpc.client
from datetime import date, datetime, timedelta
from threading import Thread
from os import system, name
from time import sleep

# buat stub (proxy) untuk client
server = xmlrpc.client.ServerProxy('http://127.0.0.1:8080')

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
        for klinik in server.getKlinik():
            i+=1
            print(f"{i}. {klinik}")
        break

    while True:
        input_klinik = input('Masukan nomor klinik: ')
        if server.cekKlinik(input_klinik):
            input_klinik = int(input_klinik)
            break

    date = datetime.today()
    no_rekam_medis = date.strftime('%d%m%Y') + '.' + date.strftime('%H%M')
    
    nama = input('Masukan nama lengkap: ')
    tgl_lahir = input('Masukan tanggal lahir: ')
    server.daftarPasien(input_klinik, no_rekam_medis, nama, tgl_lahir)
    print('Pasien Telah Terdaftar!')

def cek_antrean():
    print('No. Antrean \t Nama Pasien')
    for pasien in server.getAntrean():
        print(f"{pasien.get('no_antrean')} \t\t {pasien.get('nama_pasien')}")

def print_antrean(antrean):
    if (len(antrean) == 0):
        print('Belum ada antrean')
    else:
        print('=======================')
        print(f"Nomor Antrean Sekarang: {antrean[0].get('no_antrean')}")
        print('=======================')

while True:
    print("\n Daftar Layanan Rumah Sakit Kelompok 2")
    print("1. Daftarkan Diri ")
    print("2. Cek Antrean")
    print("3. Keluar")
    while True:
        inpt_opt = input("Masukan angka: ")
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
    elif inpt_opt == 2:
        cek_antrean()
    elif inpt_opt == 3 :
        break
