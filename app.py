from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import flash
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "phyevv"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

#app.config['MAIL_SERVER'] = 'smtp.gmail.com'
#app.config['MAIL_PORT'] = 465
#app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
#app.config['MAIL_PASSWORD'] = 'your-password'
#app.config['MAIL_USE_TLS'] = False
#app.config['MAIL_USE_SSL'] = True

#mail = Mail(app)

# Resimlerin kaydedileceği klasör
UPLOAD_FOLDER = 'static/admin/img'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)

ayarlar = None

@app.before_first_request
def get_ayarlar():
    global ayarlar

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tbl_ayar")
    ayarlar = cursor.fetchone()
    cursor.close()


@app.route("/")
def main():
    

    return render_template("frontend/main.html", ayar=ayarlar)



@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Mesaj gönderme işlemleri

        # Mesaj gönderildi bildirimini göster
        message = "Mesaj gönderildi"
        return render_template("frontend/contact.html", notification=message, ayar=ayarlar)
    
    return render_template("frontend/contact.html", notification=None, ayar=ayarlar)

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
    cursor = mysql.connection.cursor()
    query = "SELECT tbl_post.*, tbl_category.name AS category_name FROM tbl_post JOIN tbl_category ON tbl_post.category_id = tbl_category.category_id"
    cursor.execute(query)
    posts = cursor.fetchall()
    cursor.close()
    return render_template("frontend/blog.html", posts=posts, ayar=ayarlar)

@app.route("/blog/<int:post_id>")
def show_post(post_id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM tbl_post WHERE post_id = %s"
    cursor.execute(query, (post_id,))
    post = cursor.fetchone()
    cursor.close()
    return render_template("frontend/post.html", post=post, ayar=ayarlar)





@app.route("/sorularim")
def sorularim():
    if 'user_id' in session:
        return render_template("frontend/sorularim.html", ayar=ayarlar)
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
        user_id = session['user_id']  # Kullanıcı oturumu kontrol edilerek user_id değeri alınıyor
        cur = mysql.connection.cursor()
        query = "SELECT user_name, user_email, user_type FROM tbl_user WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()
        return render_template("frontend/profilayar.html", user=user, ayar=ayarlar)
    else:
        return redirect(url_for('login'))
    
@app.route("/taleplerim")
def taleplerim():
    if 'user_id' in session:
        user_id = session['user_id']
        
        # Kullanıcının taleplerini al
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_talepler WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        talepler = cursor.fetchall()
        cursor.close()
        
        # Her talebin ilgili projesinin verilerini al
        for talep in talepler:
            proje_id = talep['proje_id']
            cursor = mysql.connection.cursor()
            query = "SELECT * FROM tbl_proje WHERE proje_id = %s"
            values = (proje_id,)
            cursor.execute(query, values)
            proje = cursor.fetchone()
            talep['proje'] = proje
            cursor.close()
        
        # Kullanıcının bilgilerini al
        cur = mysql.connection.cursor()
        query = "SELECT user_name, user_email, user_type FROM tbl_user WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()
        
        return render_template("frontend/taleplerim.html", talepler=talepler, user=user, ayar=ayarlar)
    else:
        return redirect(url_for('index'))





@app.route("/ayarlar")
def ayarlar():
    if 'user_id' in session:
        return render_template("admin/ayarlar.html", ayar=ayarlar)
    else:
        return redirect(url_for('login'))

@app.route('/ayar_guncelle', methods=["POST"])
def ayar_guncelle():
    site_name = request.form['site_name']
    site_title = request.form['site_title']
    site_logo = request.files['site_logo']
    google_analytics = request.form['site_analytics']
    site_instagram = request.form['site_instagram']
    site_facebook = request.form['site_facebook']
    site_twiter = request.form['site_twiter']
    site_youtube = request.form['site_youtube']

    # Resimleri kaydetme işlemi
    if site_logo:
        site_logo_filename = site_logo.filename
        site_logo.save(os.path.join(app.config['UPLOAD_FOLDER'], site_logo_filename))
    else:
        site_logo_filename = None

    cursor = mysql.connection.cursor()
    query = "UPDATE tbl_ayar SET site_name = %s, site_title = %s, site_logo = %s, site_analytics = %s, site_instagram = %s, site_facebook = %s, site_twiter = %s, site_youtube = %s WHERE id = 1"
    cursor.execute(query, (site_name, site_title, site_logo_filename, google_analytics, site_instagram, site_facebook, site_twiter, site_youtube))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('ayarlar'))



@app.route("/donusum")
def donusum():
    return render_template("frontend/donusum.html")

@app.route("/faq")
def faq():
    return render_template("frontend/faq.html" , ayar=ayarlar)

@app.route("/admin")
def admin():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_user WHERE user_id = %s AND admin = 1"
        cursor.execute(query, (user_id,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return render_template("admin/main.html")
        else:
            return "Yetkisiz erişim!"
    else:
        return redirect(url_for('login'))


@app.route("/talep_olustur", methods=["POST"])
def talep_olustur():
    if request.method == "POST":
        proje_id = request.form['proje_id']
        user_id = request.form['user_id']
        talep_tarihi = request.form['talep_tarihi']
        
        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_talepler (user_id, proje_id, talep_tarihi) VALUES (%s, %s, %s)"
        values = (user_id, proje_id, talep_tarihi)
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('profil', user_id=user_id))  # Profil sayfasına yönlendir
    else:
        return redirect(url_for('index'))  # Eğer POST isteği değilse, ana sayfaya yönlendir
    
# Talebi iptal et
@app.route("/talep_iptal/<int:talep_id>", methods=["POST"])
def talep_iptal(talep_id):
    if 'user_id' in session:
        # Talebi sil
        cursor = mysql.connection.cursor()
        query = "DELETE FROM tbl_talepler WHERE talep_id = %s"
        cursor.execute(query, (talep_id,))
        mysql.connection.commit()
        cursor.close()

        # Talebe bağlı teklifleri sil
        cursor = mysql.connection.cursor()
        query = "DELETE FROM tbl_teklifler WHERE talep_id = %s"
        cursor.execute(query, (talep_id,))
        mysql.connection.commit()
        cursor.close()

        flash("Talep ve bağlı teklifler başarıyla silindi.")
        return redirect(url_for('tum_talepler'))
    else:
        return redirect(url_for('login'))
# Teklifleri gör
@app.route("/teklifleri_gor/<int:talep_id>")
def teklifleri_gor(talep_id):
    if 'user_id' in session:
        # Talebe verilen teklifleri al
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_teklifler WHERE talep_id = %s"
        cursor.execute(query, (talep_id,))
        teklifler = cursor.fetchall()
        cursor.close()

        return render_template("frontend/teklifler.html", teklifler=teklifler, ayar=ayarlar)
    else:
        return redirect(url_for('login'))

    
@app.route("/tum_talepler")
def tum_talepler():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_talepler"
        cursor.execute(query)
        talepler = cursor.fetchall()

        # Talepleri döngüye alarak ilgili verileri çekme
        for talep in talepler:
            talep_id = talep['talep_id']
            proje_id = talep['proje_id']
            user_id = talep['user_id']

            # Talep bilgilerini çekme
            cursor.execute("SELECT * FROM tbl_talepler WHERE talep_id = %s", (talep_id,))
            talep_bilgisi = cursor.fetchone()

            # Kullanıcı bilgilerini çekme
            cursor.execute("SELECT * FROM tbl_user WHERE user_id = %s", (user_id,))
            kullanici_bilgisi = cursor.fetchone()

            # Proje bilgilerini çekme
            cursor.execute("SELECT * FROM tbl_proje WHERE proje_id = %s", (proje_id,))
            proje_bilgisi = cursor.fetchone()

            # İlgili verileri talep sözlüğüne ekleyerek güncelleme
            talep['talep_bilgisi'] = talep_bilgisi
            talep['kullanici_bilgisi'] = kullanici_bilgisi
            talep['proje_bilgisi'] = proje_bilgisi

        cursor.close()

        # Kullanıcının bilgilerini al
        cur = mysql.connection.cursor()
        query = "SELECT user_name, user_email, user_type FROM tbl_user WHERE user_id = %s"
        cur.execute(query, (user_id,))
        user = cur.fetchone()
        cur.close()

        return render_template("frontend/tum_talepler.html", talepler=talepler, user=user, ayar=ayarlar)
    else:
        return redirect(url_for('login'))


@app.route("/teklif_ver/<int:talep_id>", methods=["GET", "POST"])
def teklif_ver(talep_id):
    if 'user_id' in session:
        user = None  # user değişkenini None olarak tanımla
        if request.method == "POST":
            teklif_miktari = request.form['teklif_miktari']
            teklif_aciklama = request.form['teklif_aciklama']
            teklif_tarihi = request.form['teklif_tarihi']

            # Kullanıcının bilgilerini al
            user_id = session['user_id']
            cur = mysql.connection.cursor()
            query = "SELECT user_name, user_id, user_type FROM tbl_user WHERE user_id = %s"
            cur.execute(query, (user_id,))
            user = cur.fetchone()
            cur.close()

            # Teklifi veritabanına kaydet
            cursor = mysql.connection.cursor()
            query = "INSERT INTO tbl_teklifler (talep_id, user_id, teklif_miktari, teklif_aciklama, teklif_tarihi) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (talep_id, user_id, teklif_miktari, teklif_aciklama, teklif_tarihi))
            mysql.connection.commit()
            cursor.close()

            flash("Teklifiniz başarıyla kaydedildi.")
            return redirect(url_for('tum_talepler'))

        return render_template("frontend/teklif_ver.html", talep_id=talep_id, user=user, ayar=ayarlar)
    else:
        return redirect(url_for('login'))
    
@app.route("/tekliflerim")
def tekliflerim():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_teklifler WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        teklifler = cursor.fetchall()
        cursor.close()

        return render_template("frontend/tekliflerim.html", teklifler=teklifler, ayar=ayarlar)
    else:
        return redirect(url_for('login'))


@app.route('/profil')
def profil():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    cur = mysql.connection.cursor()
    query = "SELECT user_name, user_email, user_type FROM tbl_user WHERE user_id = %s"
    cur.execute(query, (user_id,))
    user = cur.fetchone()
    cur.close()

    return render_template('frontend/profil.html', user=user, ayar=ayarlar)



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("frontend/register.html", ayar=ayarlar)
    else:
        reg_email = request.form.get('reg_email')

        # Veritabanında e-posta kontrolü yapılması
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_user WHERE user_email = %s"
        cursor.execute(query, (reg_email,))
        user = cursor.fetchone()
        cursor.close()

        if user:
            flash('Bu e-posta adresi zaten kayıtlı.')
            return redirect(url_for('register'))

        reg_type = request.form.get('reg_type')
        reg_name = request.form.get('reg_name')
        reg_tel = request.form.get('reg_tel')
        reg_pass1 = request.form.get('reg_pass1')
        reg_pass2 = request.form.get('reg_pass2')
        activation_code = request.form.get('activation_code')

        if reg_pass1 != reg_pass2:
            flash('Girilen şifreler uyuşmuyor.')
            return redirect(url_for('register'))

        user_pass = bcrypt.generate_password_hash(reg_pass1).decode('utf-8')

        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_user (user_type, user_name, user_tel, user_email, user_pass, is_active) VALUES (%s, %s, %s, %s, %s, %s)"
        #activation_code = generate_activation_code()  # Benzersiz bir aktivasyon kodu oluşturun
        cursor.execute(query, (reg_type, reg_name, reg_tel, reg_email, user_pass, activation_code))
        mysql.connection.commit()
        user_id = cursor.lastrowid  # Yeni kullanıcının ID'sini alın
        cursor.close()

        session['reg_name'] = reg_name
        session['user_id'] = user_id
        session['user_type'] = reg_type  # Oturum bilgilerini doğrudan atayın

        # E-posta gönderme işlemi
       # activation_link = url_for('activate_account', activation_code=activation_code, _external=True)
       # msg = Message("Hesap Aktivasyonu", sender="your-email@gmail.com", recipients=[reg_email])
       # msg.body = "Hesabınızı etkinleştirmek için aşağıdaki bağlantıya tıklayın: {activation_link}".format(activation_link=activation_link)
       # mail.send(msg)

        return redirect(url_for('main'))

#@app.route('/activate/<activation_code>')
#def activate_account(activation_code):
    #cursor = mysql.connection.cursor()
    #query = "SELECT * FROM tbl_user WHERE activation_code = %s"
    #cursor.execute(query, (activation_code,))
    #user = cursor.fetchone()
#
    #if user:
        # Kullanıcının hesabını etkinleştirin
       # query = "UPDATE tbl_user SET is_active = 1 WHERE activation_code = %s"
       # cursor.execute(query, (activation_code,))
        #mysql.connection.commit()
        #flash('Hesabınız başarıyla etkinleştirildi. Giriş yapabilirsiniz.')
   # else:
       # flash('Geçersiz aktivasyon kodu.')

    #cursor.close()
   # return redirect(url_for('login'))

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

        if user:
            if user['is_active'] == 0:
                flash('Hesabınız henüz etkinleştirilmemiş.')
                return redirect(url_for('login'))
            
            if bcrypt.check_password_hash(user['user_pass'], reg_pass1):
                session['reg_name'] = user['user_name']
                session['user_id'] = user['user_id']
                session['user_type'] = user['user_type']
                
                if user['admin'] == 1:
                    return redirect(url_for('admin'))
                else:
                    return render_template("frontend/main.html", ayar=ayarlar)
        
        flash('Hatalı giriş bilgileri')
        return redirect(url_for('login'))

    else:
        return render_template("frontend/login.html", ayar=ayarlar)



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

        return render_template("frontend/basvurularim.html", basvurularim=basvurularim, ayar=ayarlar)
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

    return render_template("frontend/projeler.html", projeler=projeler, ayar=ayarlar)

@app.route("/projedetay/<int:proje_id>")
def projedetay(proje_id):
    # Proje detaylarını veritabanından alın
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM tbl_proje WHERE proje_id = %s"
    values = (proje_id,)
    cursor.execute(query, values)
    proje = cursor.fetchone()
    cursor.close()

    # Kullanıcı girişi kontrolü yapılması
    if 'user_id' in session:
        user_id = session['user_id']
        # Kullanıcı girişi varsa, kullanıcı verilerini alın
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM tbl_user WHERE user_id = %s"
        values = (user_id,)
        cursor.execute(query, values)
        user = cursor.fetchone()
        cursor.close()

        # Tarih bilgisini al
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Proje detaylarını ilgili HTML sayfasına ve kullanıcı verilerini aktar
        return render_template("frontend/projedetay.html", proje=proje, ayar=ayarlar, user=user, current_date=current_date)
    else:
        # Kullanıcı girişi yoksa sadece proje detaylarını aktar
        return render_template("frontend/projedetay.html", proje=proje, ayar=ayarlar)
    
@app.route('/blogs')
def blogs():
    # Veritabanından makale verilerini alın
    cursor = mysql.connection.cursor()
    query = "SELECT tbl_post.post_id, tbl_post.title, tbl_post.content, tbl_post.image, tbl_post.created_at, tbl_category.name AS category_name FROM tbl_post JOIN tbl_category ON tbl_post.category_id = tbl_category.category_id"
    cursor.execute(query)
    blogs = cursor.fetchall()
    cursor.close()

    return render_template('admin/blogs.html', blogs=blogs)



    
@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form.get('title')
        category_id = request.form.get('category')
        content = request.form.get('content')
        image = request.files['proje_resim']
        
        # Resim dosyasını kaydetme işlemi
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Veritabanında makale oluşturma işlemi
        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_post (title, content, image, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, content, filename, category_id))
        mysql.connection.commit()
        cursor.close()
        
        flash('Makale başarıyla eklendi.')
        return redirect(url_for('blogs'))
    
    # Kategori listesini almak için veritabanından sorgu yapma
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tbl_category")
    categories = cursor.fetchall()
    cursor.close()
    
    return render_template('admin/add_post.html', categories=categories)

@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    # Posta ilişkin düzenleme işlemleri burada yapılır
    # post_id parametresi ile ilgili gönderiyi alabilir ve düzenleme formunu görüntüleyebilirsiniz
    # GET ve POST işlemlerini yönetmek için gereken kodları buraya ekleyebilirsiniz
    return render_template('admin/edit_post.html', post_id=post_id)

@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    # Posta ilişkin silme işlemleri burada yapılır
    # post_id parametresi ile ilgili gönderiyi silebilirsiniz
    # Silme işleminden sonra uygun bir yönlendirme yapabilirsiniz
    return redirect(url_for('blogs'))




if __name__ == '__main__':
    app.secret_key = 'f3cfe9ed8fae309f02079dbf'
    app.run(debug=True)
