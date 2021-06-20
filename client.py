import xmlrpc.client
from datetime import date, datetime, timedelta
from threading import Thread
from os import system, name

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
    pasien = server.cekPasien(no_rekam_medis)
    date_converted = datetime.strptime(str(pasien['jam_check_up']), "%Y%m%dT%H:%M:%S")
    date = date_converted.strftime("%H:%M - %A")

    print(f"| No Antrean: {pasien['no_antrean']}")
    print(f"| Jam Checkup: {date}")
    print(f"| Nama: {pasien['nama_pasien']}")

def cek_antrean():
    klinik_anak, klinik_gigi, klinik_kulit, klinik_p_dalam = server.getAntrean()
    # print('No. Antrean \t Nama Pasien \t Klinik')
    # if server.getAntrean() != None:
    #     for pasien in server.getAntrean():
    #         print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']} \t\t {pasien['klinik']}")
    if klinik_anak:
        print("===Klinik Anak===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_anak:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    if klinik_gigi:
        print("===Klinik Gigi===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_gigi:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    if klinik_kulit:
        print("===Klinik Kulit===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_kulit:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    if klinik_p_dalam:
        print("===Klinik Penyaktit Dalam===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_p_dalam:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    if not(klinik_anak) and not(klinik_gigi) and not(klinik_kulit) and not(klinik_p_dalam):
        print('Tidak ada antrean')

# def print_antrean(antrean):
#     if (antrean == None):
#         print('=======================')
#         print('Belum ada antrean')
#         print('=======================')
#     else:
#         date_converted = datetime.strptime(str(antrean[0]['jam_check_up']), "%Y%m%dT%H:%M:%S")
#         print('=======================')
#         print(f"Nomor Antrean Sekarang: {antrean[0]['no_antrean']}")
#         print(f"Waktu Masuk: {date_converted}")
#         print('=======================')

while True:
    # antrean = server.getAntrean()
    # print_antrean(antrean)
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
