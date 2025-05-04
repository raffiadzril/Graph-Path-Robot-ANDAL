# Import library untuk visualisasi grafik 3D
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from collections import deque  # Import deque untuk implementasi BFS (queue)

# Inisialisasi koordinat awal (start), tujuan (goal), dan posisi bom
start = (0, 0, 0)  # Titik awal robot
goal = (9, 9, 9)   # Titik tujuan robot
bombs = [  # Daftar koordinat bom yang harus dihindari
    (0,1,0), (1,1,0), (2,2,0),
    (3,3,3), (5,5,5), (7,7,7),
    (8,8,8), (9,9,8)
]

# Fungsi untuk memvalidasi apakah gerakan ke koordinat tertentu valid
def is_valid(x, y, z, visited, bombs):
    return (0 <= x < 10) and (0 <= y < 10) and (0 <= z < 10) and \
           ((x, y, z) not in visited) and ((x, y, z) not in bombs)  # Pastikan koordinat lebih dari sama dengan 0 dan kurang dari 10 dan belum dikunjungi dan bukan bom

# Fungsi BFS untuk mencari rute terpendek dari start ke goal
def bfs(start, goal, bombs):
    queue = deque()  # Inisialisasi queue untuk BFS
    visited = set()  # Set untuk menyimpan koordinat yang sudah dikunjungi
    parent = {}  # Dictionary untuk melacak jalur (parent-child relationship)

    queue.append(start)  # Tambahkan titik awal ke queue
    visited.add(start)  # Tandai titik awal sebagai sudah dikunjungi

    # Definisi 6 arah pergerakan (atas, bawah, kiri, kanan, depan, belakang)
    directions = [
        (1, 0, 0), (-1, 0, 0),  # Gerakan di sumbu X
        (0, 1, 0), (0, -1, 0),  # Gerakan di sumbu Y
        (0, 0, 1), (0, 0, -1)   # Gerakan di sumbu Z
    ]

    while queue:  # Selama masih ada elemen di queue
        current = queue.popleft()  # Ambil elemen pertama dari queue

        if current == goal:  # Jika mencapai tujuan
            # Rekonstruksi jalur dari goal ke start
            path = []
            while current != start:  # Telusuri parent hingga mencapai start
                path.append(current)
                current = parent[current]
            path.append(start)  # Tambahkan titik awal ke jalur
            path.reverse()  # Balikkan jalur agar urut dari start ke goal
            return path  # Kembalikan jalur yang ditemukan

        # Iterasi untuk setiap arah pergerakan
        for dx, dy, dz in directions:
            nx, ny, nz = current[0] + dx, current[1] + dy, current[2] + dz  # Hitung koordinat baru
            if is_valid(nx, ny, nz, visited, bombs):  # Periksa apakah koordinat valid
                next_pos = (nx, ny, nz)  # Simpan koordinat baru
                queue.append(next_pos)  # Tambahkan ke queue
                visited.add(next_pos)  # Tandai sebagai sudah dikunjungi
                parent[next_pos] = current  # Simpan parent dari koordinat baru

    return None  # Jika tidak ada jalur yang ditemukan, kembalikan None

# Panggil fungsi BFS untuk mendapatkan jalur dari start ke goal
path = bfs(start, goal, bombs)

# Tampilkan hasil ke terminal
if path:  # Jika jalur ditemukan
    print("Rute ditemukan!")
    print(f"Panjang rute: {len(path)} langkah")  # Panjang jalur
    print("Rutenya:")
    for step in path:  # Cetak setiap langkah dalam jalur
        print(step)
else:  # Jika tidak ada jalur yang ditemukan
    print("Tidak ada rute yang bisa ditemukan dari START ke GOAL (terhalang bom).")

# Visualisasi jalur dalam grafik 3D
fig = plt.figure(figsize=(10, 8))  # Buat figure dengan ukuran tertentu
ax = fig.add_subplot(111, projection='3d')  # Tambahkan subplot 3D

# Plot posisi bom
if bombs:
    bx, by, bz = zip(*bombs)  # Pisahkan koordinat bom menjadi x, y, z
    ax.scatter(bx, by, bz, c='red', marker='x', label='Bombs')  # Plot bom dengan warna merah

# Plot jalur yang ditemukan
if path:
    px, py, pz = zip(*path)  # Pisahkan koordinat jalur menjadi x, y, z
    ax.plot(px, py, pz, c='blue', label='Path')  # Plot jalur dengan warna biru
    ax.scatter([start[0]], [start[1]], [start[2]], c='green', marker='o', s=100, label='Start')  # Plot titik awal
    ax.scatter([goal[0]], [goal[1]], [goal[2]], c='purple', marker='^', s=100, label='Goal')  # Plot titik tujuan
else:
    ax.text2D(0.3, 0.5, "No path found", transform=ax.transAxes)  # Tampilkan teks jika tidak ada jalur

# Tambahkan label dan pengaturan sumbu
ax.set_xlabel('X')  # Label sumbu X
ax.set_ylabel('Y')  # Label sumbu Y
ax.set_zlabel('Z')  # Label sumbu Z
ax.set_xticks(range(10))  # Tampilkan angka 0–9 di sumbu X
ax.set_yticks(range(10))  # Tampilkan angka 0–9 di sumbu Y
ax.set_zticks(range(10))  # Tampilkan angka 0–9 di sumbu Z
ax.set_title('Robot Path in 3D Rubik-like Building')  # Judul grafik
ax.legend()  # Tampilkan legenda
plt.tight_layout()  # Atur tata letak agar tidak tumpang tindih
plt.show()  # Tampilkan grafik