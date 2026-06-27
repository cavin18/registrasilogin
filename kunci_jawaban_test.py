import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Fixture untuk menyiapkan database sebelum pengujian dan membersihkannya setelahnya."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
     """Fixture untuk terhubung dengan database dan menutupnya setelah pengujian."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()

def test_create_db(setup_database, connection):
    """Menguji pembuatan database dan tabel users."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "Tabel 'users' seharusnya ada dalam database."

def test_add_new_user(setup_database, connection):
    """Menguji penambahan pengguna baru."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Pengguna seharusnya ditambahkan ke database."

def test_add_existing_user(setup_database):
    """Menguji upaya menambahkan pengguna dengan username yang sudah ada."""
    add_user('existinguser', 'existinguser@example.com', 'password123')
    response = add_user('existinguser', 'existinguser2@example.com', 'password1234') 
    assert not response, "Pengguna dengan username yang sudah ada seharusnya tidak disimpan."

def test_authenticate_user_success(setup_database):
    """Menguji autentikasi pengguna yang berhasil."""
    add_user('testauth', 'testauth@example.com', 'password123')
    assert authenticate_user('testauth', 'password123') == True

def test_authenticate_nonexistent_user(setup_database):
    """Menguji autentikasi pengguna yang tidak ada."""
    assert authenticate_user('nonexistentuser', 'password') == False

def test_authenticate_user_wrong_password(setup_database):
    """Menguji autentikasi dengan password yang salah."""
    add_user('wrongpass', 'wrongpass@example.com', 'password123')
    assert authenticate_user('wrongpass', 'wrongpassword') == False

def test_display_users(setup_database, capsys):
    """Menguji tampilan daftar pengguna yang benar."""
    add_user('displaytest', 'displaytest@example.com', 'password123')
    display_users()
    captured = capsys.readouterr()
    assert 'displaytest' in captured.out, "Fungsi tampilan seharusnya menampilkan username pengguna."
    assert 'password123' not in captured.out, "Password seharusnya tidak ditampilkan."
