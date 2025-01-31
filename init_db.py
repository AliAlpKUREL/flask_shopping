import sqlite3

# Veritabanı bağlantısı kurma
connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Ürünler tablosunu oluşturma (eğer varsa yeniden oluşturma)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        image TEXT NOT NULL,
        category TEXT NOT NULL
    )
''')

# Ürünler listesi
products = [
    ("T-shirt", "Pamuklu t-shirt, yazlık rahat kullanım için uygun", 199.99, "tshirt.jpeg", "Giyim"),
    ("Pantolon", "Klasik kesim pantolon, iş yerinde şık görünüm", 249.99, "pantolon.jpg", "Giyim"),
    ("Gömlek", "Beyaz gömlek, her türlü kombin için ideal", 299.99, "gömlek.jpg", "Giyim"),
    ("Ceket", "Siyah deri ceket, soğuk havalarda şıklık", 499.99, "siyahceket.jpg", "Giyim"),
    ("Eldiven", "Sıcak tutan kış eldiveni, soğuk havalarda kullanıma uygun", 99.99, "eldiven.jpeg", "Giyim"),

    ("Ayakkabı", "Rahat spor ayakkabı, günlük kullanım için ideal", 349.99, "ayakkabı.jpeg", "Ayakkabı"),
    ("Bot", "Kış botu, kar ve yağmurlu havalar için tasarlanmış", 499.99, "bot.jpg", "Ayakkabı"),
    ("Spor Ayakkabı", "Koşu ayakkabısı, spor aktiviteleri için uygun", 399.99, "spor ayakkabı.jpg", "Ayakkabı"),

    ("Saat", "Su geçirmez kol saati, spor ve günlük kullanım için", 799.99, "saat.jpeg", "Aksesuar"),
    ("Kolye", "Altın kolye, özel günlerde şıklık", 1299.99, "kolye.jpeg", "Aksesuar"),

    ("Telefon", "Akıllı telefon, en son teknolojilerle donatılmış", 2499.99, "Telelfon.jpg", "Elektronik"),
    ("Laptop", "Dizüstü bilgisayar, iş ve eğlence için yüksek performans", 4999.99, "Laptop.jpg", "Elektronik"),
]

# Ürünleri veritabanına ekle
try:
    cursor.executemany("INSERT INTO products (name, description, price, image, category) VALUES (?, ?, ?, ?, ?)", products)
    # Commit değişikliklerini kaydet
    connection.commit()
    print("Ürünler başarıyla veritabanına eklendi.")
except sqlite3.Error as e:
    # Hata durumunda geri al işlemi
    connection.rollback()
    print(f"Hata oluştu: {e}")
finally:
    # Bağlantıyı kapat
    connection.close()
