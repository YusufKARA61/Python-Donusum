from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "phyevv"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Resimlerin kaydedileceği klasör
UPLOAD_FOLDER = 'static/admin/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

@app.route("/")
def main():
    return render_template("frontend/main.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Mesaj gönderme işlemleri

        # Mesaj gönderildi bildirimini göster
        message = "Mesaj gönderildi"
        return render_template("frontend/contact.html", notification=message)
    
    return render_template("frontend/contact.html", notification=None)

@app.route("/save_contact", methods=["POST"])
def save_contact():
    name = request.form['name']
    email = request.form['email']
    subject = request.form['subject']
    message = request.form['message']

    cursor = mysql.connection.cursor()
    query = "INSERT INTO tbl_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, email, subject, message))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('contact'))

@app.route("/blog")
def blog():
    return render_template("frontend/blog.html")



@app.route("/sorularim")
def sorularim():
    if 'user_id' in session:
        return render_template("frontend/sorularim.html")
    else:
        return redirect(url_for('login'))

@app.route("/mesajlar")
def mesajlar():
    if 'user_id' in session:
        cursor = mysql.connection.cursor()
        query = "SELECT id, name, email, subject, message, is_read FROM tbl_messages"
        cursor.execute(query)
        messages = cursor.fetchall()
        cursor.close()

        return render_template("admin/mesajlar.html", messages=messages)
    else:
        return redirect(url_for('login'))

@app.route("/profilayar")
def profilayar():
    if 'user_id' in session:
        return render_template("frontend/profilayar.html")
    else:
        return redirect(url_for('login'))

@app.route("/ayarlar")
def ayarlar():
    if 'user_id' in session:
        return render_template("admin/ayarlar.html")
    else:
        return redirect(url_for('login'))

@app.route("/donusum")
def donusum():
    return render_template("frontend/donusum.html")

@app.route("/faq")
def faq():
    return render_template("frontend/faq.html")

@app.route("/admin")
def admin():
    if 'user_id' in session:
        return render_template("admin/main.html")
    else:
        return redirect(url_for('login'))

@app.route('/profil')
def profil():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    
    cur = mysql.connection.cursor()
    query = "SELECT user_name, user_email FROM tbl_user WHERE user_id = %s"
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    cur.close()
    
    return render_template('frontend/profil.html', user=user)


# Mysql Kullanıcı Ekleme
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("frontend/register.html")
    else:
        reg_type = request.form.get('reg_type')
        reg_name = request.form.get('reg_name')
        reg_tc = request.form.get('reg_tc')
        reg_email = request.form.get('reg_email')
        reg_tel = request.form.get('reg_tel')
        reg_dogum = request.form.get('reg_dogum')
        reg_pass1 = request.form.get('reg_pass1')
        user_pass = bcrypt.generate_password_hash(reg_pass1).decode('utf-8')

        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_user (user_type, user_name, user_tc, user_tel, user_dogum, user_email, user_pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (reg_type, reg_name, reg_tc, reg_tel, reg_dogum, reg_email, user_pass))
        mysql.connection.commit()
        cursor.close()

        session['reg_name'] = reg_name

        return render_template("frontend/main.html")

# Mysql Kullanıcı Giriş
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        reg_email = request.form['reg_email']
        reg_pass1 = request.form['reg_pass1']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_user WHERE user_email = %s"
        cursor.execute(query, (reg_email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['user_pass'], reg_pass1):
            session['reg_name'] = user['user_name']
            session['user_id'] = user['user_id']
            
            if user['admin'] == 1:
                return redirect(url_for('admin'))
            else:
                return render_template("frontend/main.html")
        else:
            return "Hatalı giriş bilgileri"

    else:
        return render_template("frontend/login.html")


# Mysql Adres Ekleme
@app.route('/hesap', methods=["GET", "POST"])
def hesap():
    if request.method == 'GET':
        return render_template("frontend/hesap.html")
    else:
        user_id = request.form.get('user_id')
        reg_tc = request.form.get('reg_tc')
        reg_tel = request.form.get('reg_tel')
        reg_mahalle = request.form.get('reg_mahalle')
        reg_sokak = request.form.get('reg_sokak')
        reg_kapino = request.form.get('reg_kapino')
        reg_ickapino = request.form.get('reg_ickapino')
        reg_ada = request.form.get('reg_ada')
        reg_parsel = request.form.get('reg_parsel')

        # Sadece oturum açmış kullanıcının kimliğini alın
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_talep (user_id, user_tc, user_tel, user_mahalle, user_sokak, user_kapino, user_ickapino, user_ada, user_parsel) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query, (user_id, reg_tc, reg_tel, reg_mahalle, reg_sokak, reg_kapino, reg_ickapino, reg_ada, reg_parsel))
        mysql.connection.commit()
        cursor.close()

        # Eklenen veriyi almak için yeni bir sorgu yapın
        query = "SELECT * FROM tbl_talep WHERE user_id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(query, (user_id,))
        basvurular = cursor.fetchall()
        cursor.close()

        return render_template("frontend/basvurularim.html", basvurular=basvurular)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('main'))


@app.route("/tipprojeler")
def tipprojeler():
    if 'user_id' in session:
        conn = mysql.connection
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM tbl_proje")
        data = cursor.fetchall()

        cursor.close()

        if data:
            return render_template("admin/tipprojeler.html", data=data)
        else:
            message = "Veri bulunamadı."
            return render_template("admin/tipprojeler.html", message=message)
    else:
        return redirect(url_for('login'))

    
@app.route("/basvurularim")
def basvurularim():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_talep WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        basvurularim = cursor.fetchall()

        return render_template("frontend/basvurularim.html", basvurularim=basvurularim)
    else:
        return redirect(url_for('login'))

    
@app.route("/kullanicilar")
def kullanicilar():
    if 'user_id' in session:
        # Veritabanı bağlantısını yap
        conn = mysql.connection
        cursor = conn.cursor()

        # Verileri sorgula
        cursor.execute("SELECT * FROM tbl_user")
        data = cursor.fetchall()

        # Veritabanı bağlantısını kapat
        cursor.close()

        if data:
            # Verileri şablonla birlikte gönder
            return render_template("admin/kullanicilar.html", data=data)
        else:
            # Veri bulunamadı durumunda mesaj gönder
            message = "Veri bulunamadı."
            return render_template("admin/kullanicilar.html", message=message)
    else:
        # Kullanıcı girişi yapılmamışsa login sayfasına yönlendir
        return redirect(url_for('login'))
    
@app.route("/kullaniciekle")
def kullanici_ekle():
    return render_template("admin/kullanici_ekle.html")

@app.route("/projeekle", methods=['GET', 'POST'])
def proje_ekle():
    if request.method == 'POST':
        # Formdan gelen verileri al
        proje_adi = request.form.get('proje_adi')
        yapi_sinifi = request.form.get('yapi_sinifi')
        oda_sayisi = request.form.getlist('oda_sayisi')
        kat_sayisi = request.form.get('kat_sayisi')
        ev_metrekare = request.form.get('ev_metrekare')
        proje_resim = request.files['proje_resim']

        # Resimleri kaydetme işlemi
        if proje_resim:
            proje_resim_filename = proje_resim.filename
            proje_resim.save(os.path.join(app.config['UPLOAD_FOLDER'], proje_resim_filename))
        else:
            proje_resim_filename = None

        # Veritabanına verileri kaydet
        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_proje (proje_adi, proje_yapi_sinifi, proje_oda_sayisi, proje_kat_adet, proje_metre, proje_resim) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (proje_adi, yapi_sinifi, oda_sayisi, kat_sayisi, ev_metrekare, proje_resim_filename)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        # Başarılı bir şekilde kaydedildi mesajını döndür
        message = "Proje başarıyla kaydedildi."
        return render_template("admin/proje_ekle.html", message=message)

    # POST isteği değilse veya form gönderilmemişse sayfayı normal şekilde render et
    return render_template("admin/proje_ekle.html")

@app.route("/projeler", methods=['GET'])
def projeler():
    # Filtreleme için yapı sınıfı ve oda sayısı parametrelerini al
    proje_yapi_sinifi = request.args.get('proje_yapi_sinifi')
    proje_oda_sayisi = request.args.get('proje_oda_sayisi')

    # Veritabanından projeleri filtrele
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM tbl_proje WHERE 1=1"
    values = []

    if proje_yapi_sinifi is not None:
        query += " AND proje_yapi_sinifi = %s"
        values.append(proje_yapi_sinifi)

    if proje_oda_sayisi is not None:
        query += " AND proje_oda_sayisi = %s"
        values.append(proje_oda_sayisi)

    cursor.execute(query, values)
    projeler = cursor.fetchall()
    cursor.close()

    return render_template("frontend/projeler.html", projeler=projeler)

@app.route("/projedetay/<int:proje_id>")
def projedetay(proje_id):
    # Proje detaylarını veritabanından alın
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM tbl_proje WHERE proje_id = %s"
    values = (proje_id,)
    cursor.execute(query, values)
    proje = cursor.fetchone()
    cursor.close()

    # Proje detaylarını ilgili HTML sayfasına aktar
    return render_template("frontend/projedetay.html", proje=proje)



if __name__ == '__main__':
    app.secret_key = 'f3cfe9ed8fae309f02079dbf'
    app.run(debug=True)
