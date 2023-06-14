from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import flash
import os

from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB, MYSQL_CURSORCLASS, UPLOAD_FOLDER

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = MYSQL_HOST
app.config['MYSQL_USER'] = MYSQL_USER
app.config['MYSQL_PASSWORD'] = MYSQL_PASSWORD
app.config['MYSQL_DB'] = MYSQL_DB
app.config['MYSQL_CURSORCLASS'] = MYSQL_CURSORCLASS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

mysql = MySQL(app)


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



@app.route('/blogs')
def blogs():
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

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor = mysql.connection.cursor()
        query = "INSERT INTO tbl_post (title, content, image, category_id) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (title, content, filename, category_id))
        mysql.connection.commit()
        cursor.close()

        flash('Makale başarıyla eklendi.')
        return redirect(url_for('blogs'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tbl_category")
    categories = cursor.fetchall()
    cursor.close()

    return render_template('admin/add_post.html', categories=categories)


@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    if request.method == 'POST':
        # Düzenleme formundan gelen verileri alın
        title = request.form.get('title')
        category_id = request.form.get('category')
        content = request.form.get('content')
        image = request.files['proje_resim']

        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        cursor = mysql.connection.cursor()
        query = "UPDATE tbl_post SET title=%s, content=%s, image=%s, category_id=%s WHERE post_id=%s"
        cursor.execute(query, (title, content, filename, category_id, post_id))
        mysql.connection.commit()
        cursor.close()

        flash('Makale başarıyla güncellendi.')
        return redirect(url_for('blogs'))

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM tbl_category")
    categories = cursor.fetchall()

    cursor.execute("SELECT * FROM tbl_post WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()

    cursor.close()

    return render_template('admin/edit_post.html', post=post, categories=categories)


@app.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post(post_id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM tbl_post WHERE post_id = %s", (post_id,))
    mysql.connection.commit()
    cursor.close()

    flash('Makale başarıyla silindi.')
    return redirect(url_for('blogs'))

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




