from flask import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "phyevv"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

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
    sorgu = "INSERT INTO tbl_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)"
    cursor.execute(sorgu, (name, email, subject, message))
    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('contact'))

@app.route("/blog")
def blog():
    return render_template("frontend/blog.html")

@app.route("/basvurularim")
def basvurularim():
    if 'user_id' in session:
        user_id = session['user_id']

        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM tbl_talep WHERE user_id = %s"
        cursor.execute(sorgu, (user_id,))
        basvurularim = cursor.fetchall()

        return render_template("frontend/basvurularim.html", basvurularim=basvurularim)
    else:
        return redirect(url_for('login'))


@app.route("/sorularim")
def sorularim():
    if 'user_id' in session:
        return render_template("frontend/sorularim.html")
    else:
        return redirect(url_for('login'))

@app.route("/profilayar")
def profilayar():
    if 'user_id' in session:
        return render_template("frontend/profilayar.html")
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
    return render_template("admin/main.html")

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


@app.route("/projeler")
def projeler():
    return render_template("frontend/projeler.html")

# Mysql Kullanıcı Ekleme
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'GET':
        return render_template("frontend/register.html")
    else:
        reg_name = request.form.get('reg_name')
        reg_tc = request.form.get('reg_tc')
        reg_email = request.form.get('reg_email')
        reg_tel = request.form.get('reg_tel')
        reg_dogum = request.form.get('reg_dogum')
        reg_pass1 = request.form.get('reg_pass1')
        user_pass = bcrypt.generate_password_hash(reg_pass1)

        cursor = mysql.connection.cursor()
        sorgu = "INSERT INTO tbl_user VALUES(NULL, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sorgu, (reg_name, reg_tc, reg_tel, reg_dogum, reg_email, user_pass))
        mysql.connection.commit()

        session['reg_name'] = reg_name

        return render_template("frontend/main.html")

# Mysql Kullanıcı Giriş
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        reg_email = request.form['reg_email']
        reg_pass1 = request.form['reg_pass1']

        cursor = mysql.connection.cursor()
        sorgu = "SELECT * FROM tbl_user WHERE user_email = %s"
        cursor.execute(sorgu, (reg_email,))
        user = cursor.fetchone()
        cursor.close()

        if user and bcrypt.check_password_hash(user['user_pass'], reg_pass1):
            session['reg_name'] = user['user_name']
            session['user_id'] = user['user_id']
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
        sorgu = "INSERT INTO tbl_talep VALUES(NULL, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sorgu, (user_id, reg_tc, reg_tel, reg_mahalle, reg_sokak, reg_kapino, reg_ickapino, reg_ada, reg_parsel))
        mysql.connection.commit()

        # Eklenen veriyi almak için yeni bir sorgu yapın
        sorgu = "SELECT * FROM tbl_talep WHERE user_id = %s"
        cursor.execute(sorgu, (user_id,))
        basvurular = cursor.fetchall()

        return render_template("frontend/basvurularim.html", basvurular=basvurular)


@app.route("/logout")
def logout():
    session.clear()
    return render_template("frontend/main.html")


@app.route("/satinal")
def satinal():
    if 'user_id' in session:
        return render_template("frontend/satinal.html")
    else:
        return redirect(url_for('login'))

# Anakartları veritabanından çekme
@app.route('/anakartlar')
def get_anakartlar():
    cur = mysql.connection.cursor()
    cur.execute("SELECT anakart_id, marka, fiyat FROM anakartlar")
    anakartlar = cur.fetchall()
    cur.close()
    return jsonify(anakartlar)

# İşlemcileri veritabanından çekme
@app.route('/islemciler/<int:anakart_id>')
def get_islemciler(anakart_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, marka, fiyat FROM islemciler WHERE anakart_id = %s", (anakart_id,))
    islemciler = cur.fetchall()
    cur.close()
    return jsonify(islemciler)

# Ramleri veritabanından çekme
@app.route('/ramler/<int:islemci_id>')
def get_ramler(islemci_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, marka, fiyat FROM ramler WHERE islemci_id = %s", (islemci_id,))
    ramler = cur.fetchall()
    cur.close()
    return jsonify(ramler)

if __name__ == '__main__':
    app.secret_key = 'f3cfe9ed8fae309f02079dbf'
    app.run(debug=True)

