import socket
import os

# Konfigurasi host dan port server
host = 'localhost'  # Alamat IP atau hostname server
port = 21929

# Membuat koneksi socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)

print("Menunggu koneksi dari client...")

# Menerima koneksi dari client
conn, addr = s.accept()
print("Terhubung dengan client:", addr)

while True:
    # Menerima perintah dari client
    data = conn.recv(1024).decode()
    if not data:
        break

    # Memisahkan perintah dan argumen
    command_parts = data.split()
    command = command_parts[0].lower()
    args = command_parts[1:]

    # Eksekusi perintah dan kirim output ke client
    output = ""

    if command == 'listdir':
        # Menampilkan daftar file dan direktori dalam direktori saat ini
        file_list = os.listdir()
        output = "\n".join(file_list)

    elif command == 'getfile':
        # Memeriksa jumlah argumen
        if len(command_parts) > 1:
            # Mendapatkan nama file dari perintah
            file_name = command_parts[1].lower()
            print(file_name)
            # Memeriksa apakah file ada
            if os.path.isfile(file_name):
                # Mengirimkan tanda bahwa file ditemukan
                conn.send(b'FOUND')
                # Membuka file dalam mode baca biner
                with open(file_name, 'rb') as file:
                    # Membaca dan mengirimkan file dalam chunk ke client
                    while True:
                        file_data = file.read(1024)
                        if not file_data:
                            break
                        conn.send(file_data)
                output = "File {} telah berhasil dikirim".format(file_name)
            else:
                # Mengirimkan tanda bahwa file tidak ditemukan
                conn.send(b'NOTFOUND')
                output = "File tidak ditemukan."
        else:
            output = "Argumen tidak valid untuk perintah getfile"

    elif command == 'putfile':
        # Menerima file dari client dan menyimpannya
        if len(args) > 0:
            file_name = args[0]
            file_data = conn.recv(131072)
            with open(file_name, 'wb') as file:
                file.write(file_data)
            output = "File berhasil disimpan."
        else:
            output = "Argumen tidak valid."

    elif command == 'exit':
        # Keluar dari koneksi
        break

    else:
        output = "Perintah tidak dikenali."

    # Mengirim output ke client
    conn.send(output.encode())

# Menutup koneksi
conn.close()
s.close()
