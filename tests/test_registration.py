import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Fixture untuk menyiapkan database sebelum pengujian dan membersihkannya setelah selesai."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Fixture untuk mendapatkan koneksi database dan menutupnya setelah pengujian."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Menguji pembuatan database dan tabel pengguna."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Tabel 'users' harus ada dalam database."

def test_add_new_user(setup_database, connection):
    """Menguji penambahan pengguna baru."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Pengguna harus ditambahkan ke database."
def test_authenticate_user_success(setup_database, connection):
    """Menguji keberhasilan autentikasi pengguna."""
    add_user('authuser', 'authuser@example.com', 'password123')
    result = authenticate_user('authuser', 'password123')
    assert result, "Autentikasi pengguna harus berhasil."
def test_authenticate_user_failure(setup_database, connection):
    """Menguji kegagalan autentikasi pengguna."""
    add_user('authuser', 'authuser@example.com', 'password123')
    result = authenticate_user('authuser', 'wrongpassword')
    assert not result, "Autentikasi pengguna harus gagal."
def test_authenticate_nonexistent_user(setup_database, connection):
    """Menguji autentikasi pengguna yang tidak ada."""
    result = authenticate_user('nonexistentuser', 'password123')
    assert not result, "Autentikasi pengguna yang tidak ada harus gagal."
def test_display_users(capsys, setup_database, connection):
    """Menguji tampilan yang benar dari daftar pengguna."""
    add_user('displayuser1', 'displayuser1@example.com', 'password123')
def test_authenticate_incorrect_password(setup_database, connection):
    """Menguji autentikasi dengan kata sandi yang salah."""
    add_user('wrongpassuser', 'wrongpassuser@example.com', 'password123')
    result = authenticate_user('wrongpassuser', 'incorrectpassword')
    assert not result, "Autentikasi dengan kata sandi yang salah harus gagal."

# Berikut adalah pengujian yang bisa ditulis:
"""
Menguji percobaan menambahkan pengguna dengan nama pengguna yang sudah ada.
Menguji keberhasilan autentikasi pengguna.
Menguji autentikasi pengguna yang tidak ada.
Menguji autentikasi dengan kata sandi yang salah.
Menguji tampilan yang benar dari daftar pengguna.
"""

#1. idk
#2. check
#3. check
#4. check
#5. check

#ini 12345 bekas saya tadi kira tugasnya cuman ngetest masuk dan daftarnya di terminal, 
# ternyata harus di pytestjuga, jadi saya buru2 pake copiloy