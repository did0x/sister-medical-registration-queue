# import SimpleXMLRPCServer
import klinik
from klinik import check_pasien, check_klinik, get_antrean, get_klinik, masuk_klinik, registrasi_pasien
from klinik import pop_klinik
from xmlrpc.server import SimpleXMLRPCServer
# import SimpleXMLRPCRequestHandler
from xmlrpc.server import SimpleXMLRPCRequestHandler

from redis import Redis
from rq import Queue

import threading

# inisialisasi queue untuk redis
redis = Redis(host='127.0.0.1', port=6379, db=0)
print(redis.ping())
q = Queue(connection=redis)
job = q.enqueue(print, "hello")
while not job.is_finished:
    pass

if job.is_failed:
    print("cannot test queue...close server")
    exit

# Batasi hanya pada path /RPC2 saja supaya tidak bisa mengakses path lainnya


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Buat server
server = SimpleXMLRPCServer(
    ("127.0.0.1", 8080), requestHandler=RequestHandler, allow_none=True)
server.register_introspection_functions()

# kode setelah ini adalah critical section, menambahkan vote tidak boeh terjadi race condition
# siapkan lock
lock = threading.Lock()

# buat fungsi bernama check_klinik()


# register check_pasien sebagai cekPasien
server.register_function(check_pasien, 'cekPasien')

# register check_klinik sebagai cekKlinik
server.register_function(check_klinik, 'cekKlinik')

# register get_antrean sebagai getAntrean
server.register_function(get_antrean, 'getAntrean')

# register get_klinik sebagai getKlinik
server.register_function(get_klinik, 'getKlinik')

# register masuk_klinik sebagai masukKlinik
server.register_function(masuk_klinik, 'masukKlinik')


# buat fungsi bernama daftarkan_pasien()


def daftarkan_pasien(input_klinik, no_rekam_medis, nama, tgl_lahir):
    # critical section dimulai
    lock.acquire()

    job = q.enqueue(registrasi_pasien, input_klinik,
                    no_rekam_medis, nama, tgl_lahir)

    while not job.is_finished:
        pass

    pasien = job.result

    q.enqueue_at(pasien['jam_check_up'], pop_klinik, pasien['klinik'])
    # push_to_queue(pasien['jam_check_up'], pasien['klinik'])

    # critical section berakhir
    lock.release()


# register daftarkan_pasien sebagai daftarPasien
server.register_function(daftarkan_pasien, 'daftarPasien')

# Jalankan server


def run_server():
    print('Running server...')
    server.serve_forever()


if __name__ == '__main__':
    threading.Thread(target=run_server).start()
    # while True:
    #     print(val)
