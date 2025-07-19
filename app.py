import streamlit as st
import sqlite3
import hashlib

# Şifreleme fonksiyonu
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Şifre doğrulama fonksiyonu
def check_password(hashed_password, input_password):
    return hashed_password == hashlib.sha256(input_password.encode()).hexdigest()

# Veritabanı oluşturma
def create_usertable():
    conn = sqlite3.connect('forecastx.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)')
    conn.commit()
    conn.close()

# Yeni kullanıcı kaydı
def add_user(username, password):
    conn = sqlite3.connect('forecastx.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?, ?)', (username, hash_password(password)))
    conn.commit()
    conn.close()

# Giriş kontrolü
def login_user(username, password):
    conn = sqlite3.connect('forecastx.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    data = c.fetchall()
    conn.close()
    return data

# Ana uygulama arayüzü
def main():
    st.title("📊 ForecastX - Giriş Sistemi")

    menu = ["Giriş", "Kayıt Ol"]
    choice = st.sidebar.selectbox("Menü", menu)

    create_usertable()  # Uygulama başladığında tabloyu oluşturalım

    if choice == "Giriş":
        st.subheader("Giriş Yap")
        username = st.text_input("Kullanıcı Adı")
        password = st.text_input("Şifre", type='password')
        if st.button("Giriş"):
            result = login_user(username, password)
            if result:
                st.success(f"Giriş başarılı. Hoş geldin, {username}!")
                st.write("---")
                run_forecast_app(username)
            else:
                st.warning("Hatalı kullanıcı adı veya şifre.")
    
    elif choice == "Kayıt Ol":
        st.subheader("Yeni Hesap Oluştur")
        new_user = st.text_input("Kullanıcı Adı")
        new_pass = st.text_input("Şifre", type='password')
        if st.button("Hesap Oluştur"):
            add_user(new_user, new_pass)
            st.success("Hesap başarıyla oluşturuldu. Giriş yapabilirsiniz.")

# Giriş yaptıktan sonra açılacak ekran
def run_forecast_app(username):
    st.write(f"📈 Forecast paneline hoş geldin, {username}")
    st.write("Buraya tahmin uygulamanı, grafiklerini ve analizlerini yerleştirebilirsin.")
    # Örnek:
    st.info("Bu alan giriş yapan kullanıcıya özel.")
    # Daha sonra buraya CSV yükleme, Prophet tahminleri ve yorumlama ekranlarını entegre edeceğiz.

# Uygulamayı başlat
if __name__ == '__main__':
    main()