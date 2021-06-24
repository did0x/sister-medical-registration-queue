import xmlrpc.client
from datetime import datetime
from os import system, name

# buat stub (proxy) untuk client
server = xmlrpc.client.ServerProxy('http://26.60.48.126:8080')

# membuat fungsi clear() untuk menghapus screen terminal
def clear(need_continue=True):
    if need_continue:
        input("Press Enter to continue...")
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# membuat fungsi daftarkan_diri() untuk melakukan pendaftaran pasien
def daftarkan_diri():
    clear(need_continue=False)
    # menampilkan seluruh klinik beserta statusnya
    while True:
        i = 0
        for klinik, jumlah in server.getKlinik().items():
            i+=1
            kondisi = 'Buka' if jumlah <= 3 else 'Penuh'
            print(f"{i}. {klinik} ({kondisi})")
        break
    # meminta input user untuk memilih klinik berdasarkan nomor klinik
    while True:
        input_klinik = input('Masukan nomor klinik: ')
        # mengecek apakah terdapat klinik dengan nomor yang diinput
        if server.cekKlinik(input_klinik):
            input_klinik = int(input_klinik)
            # mengecek apakah klinik masih dapat menambah pasien atau sudah penuh
            if (server.masukKlinik(input_klinik)):
                break
            else:
                print("[Error] Klinik sudah penuh")
        else:
            print("[Error] Tidak ditemukan klinik dengan nomor tersebut")

    # membuat nomor rekam medis berdasarkan waktu pendaftaran pasien
    date = datetime.today()
    no_rekam_medis = date.strftime('%d%m%Y') + '.' + date.strftime('%H%M')
    # meminta input user berupa nama lengkap dan tanggal lahir
    nama = input('Masukan nama lengkap: ')
    tgl_lahir = input('Masukan tanggal lahir: ')
    # meminta prosedur daftarPasien() pada server untuk menyimpan data pasien
    server.daftarPasien(input_klinik, no_rekam_medis, nama, tgl_lahir)

    print('Pasien Telah Terdaftar!')
    # mengambil data pasien yang baru mendaftar
    pasien = server.cekPasien(no_rekam_medis)
    # mengambil data waktu check up pasien untuk ditampilkan
    date_converted = datetime.strptime(str(pasien['jam_check_up']), "%Y%m%dT%H:%M:%S")
    date = date_converted.strftime("%H:%M - %A")
    # menampilkan informasi pasien yang sudah terdaftar
    print(f"| No Antrean: {pasien['no_antrean']}")
    print(f"| Jam Checkup: {date}")
    print(f"| Nama: {pasien['nama_pasien']}")

# membuat fungsi cek_antrean() untuk menampilkan antrean yang sedang berjalan pada seluruh klinik
def cek_antrean():
    # mengambil data seluruh klinik
    klinik_anak, klinik_gigi, klinik_kulit, klinik_p_dalam = server.getAntrean()
    # mengecek apakah terdapat data pada klinik anak
    if klinik_anak:
        print("===Klinik Anak===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_anak:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    # mengecek apakah terdapat data pada klinik gigi
    if klinik_gigi:
        print("===Klinik Gigi===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_gigi:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    # mengecek apakah terdapat data pada klinik kulit
    if klinik_kulit:
        print("===Klinik Kulit===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_kulit:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    # mengecek apakah terdapat data pada klinik penyakit dalam
    if klinik_p_dalam:
        print("===Klinik Penyaktit Dalam===")
        print('No. Antrean \t Nama Pasien')
        for pasien in klinik_p_dalam:
            print(f"{pasien['no_antrean']} \t\t {pasien['nama_pasien']}")
    # jika tidak ada data pas seluruh antrean tampilkan informasi tidak ada antrean
    if not(klinik_anak) and not(klinik_gigi) and not(klinik_kulit) and not(klinik_p_dalam):
        print('Tidak ada antrean')

# mengambil data seluruh klinik dan menjadikannya list
def seluruh_antren():
    klinik_anak, klinik_gigi, klinik_kulit, klinik_p_dalam = server.getAntrean()
    return [klinik_anak, klinik_gigi, klinik_kulit, klinik_p_dalam]

# menampilkan informasi antrean pada menu utama
def print_antrean(antrean):
    # jika tidak ada pasien disetiap klinik tampilkan informasi belum ada antrean
    if not any(antrean):
        print('=======================')
        print('Belum ada antrean')
        print('=======================')
    # jika ada lakukan looping untuk menampilkan antrean per setiap klinik
    for data in antrean:
        if data:
            date_converted = datetime.strptime(str(data[0]['jam_check_up']), "%Y%m%dT%H:%M:%S")
            print('=======================')
            print(f"{data[0]['klinik']}")
            print(f"Nomor Antrean Sekarang: {data[0]['no_antrean']}")
            print(f"Waktu Masuk: {date_converted}")
            print('=======================')

# membuat menu utama
while True:
    print_antrean(seluruh_antren())
    print("Daftar Layanan Rumah Sakit Kelompok 2")
    print("1. Daftarkan Diri ")
    print("2. Cek Antrean")
    print("3. Keluar")
    while True:
        # meminta input user untuk memilih menu sesuai nomor menu
        inpt_opt = input("Masukan menu pilihan: ")
        # mengecek apakah input user berupa angka atau tidak
        if inpt_opt.isdigit():
            inpt_opt = int(inpt_opt)
            # jika input user sesuai akan mengeksekusi perintah selanjutnya
            if inpt_opt in range(1, 4):
                break
            else:
                print("[Error] Tidak terdapat opsi tersebut!")
        else:
            print("[Error] Masukan sebuah angka!")
    # memanggil fungsi berdasarkan nomor menu yang dipilih user
    if inpt_opt == 1:
        daftarkan_diri()
        clear()
    elif inpt_opt == 2:
        cek_antrean()
        clear()
    elif inpt_opt == 3 :
        break
