import xmlrpc.client
from datetime import datetime
from os import system, name
from time import sleep

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://127.0.0.1:8080')

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def daftarkan_diri():
    while True:
        i = 0
        for klinik in s.getKlinik():
            i+=1
            print(f"{i}. {klinik}")
        break

    while True:
        input_klinik = input('Masukan nomor klinik: ')
        if s.cekKlinik(input_klinik):
            input_klinik = int(input_klinik)
            break

    date = datetime.today()
    no_rekam_medis = 'MEDIS' + date.strftime('%d%m%Y')
    
    nama = input('Masukan nama lengkap: ')
    tgl_lahir = input('Masukan tanggal lahir: ')
    print(s.daftarPasien(input_klinik, no_rekam_medis, nama, tgl_lahir))

def cek_antrean():
    for pasien in s.getAntrean():
        print(pasien['no_rek_medis'])
        print(pasien)

def print_antrean(antrean):
    if (len(antrean) == 0):
        print('Belum ada antrean')
    else:
        print('=======================')
        print(f"Nomor Antrean Sekarang: {antrean[0].get('no_antrean')}")
        print('=======================')

# def update_antrean(antrean):

# show menu
while True:
    antrean = s.getAntrean()
    print_antrean(antrean)
    print("\nDaftar Layanan Rumah Sakit Kelompok 2")
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
        sleep(3)
        clear()
    elif inpt_opt == 2:
        cek_antrean()
    elif inpt_opt == 3 :
        break
