import socket

# Konfigurasi host dan port server
host = 'localhost'  # Alamat IP atau hostname server
port = 21929

# Membuat koneksi socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
output = ''
while True:
    # Memasukkan perintah
    command = input("Masukkan perintah (atau 'keluar' untuk keluar): ")

    if command == 'keluar':
        break

    # Mengirim perintah ke server
    s.send(command.encode())

    # Menerima output dari server
    data = s.recv(1024).decode()
    output += data
    if len(data) < 1024:
        break
    print("Output dari server:", output)

# Menutup koneksi
s.close()
