from typing import NoReturn
import xmlrpc.client

# buat stub (proxy) untuk client
s = xmlrpc.client.ServerProxy('http://127.0.0.1:8080')

def daftarkan_diri():
    print("\n")
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

    while True:
        no_rekam_medis = input('Masukan nomor rekam medis: ')
        if s.cekRekamMedis(no_rekam_medis):
            break
    
    nama = input('Masukan nama lengkap: ')
    tgl_lahir = input('Masukan tanggal lahir: ')
    print(s.daftarPasien(input_klinik, no_rekam_medis, nama, tgl_lahir))

def cek_antrean():
    for pasien in s.getAntrean():
        print(pasien)

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
