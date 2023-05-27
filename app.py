from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL, MySQLdb
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

@app.route("/contact")
def contact():
    return render_template("frontend/contact.html")

@app.route("/blog")
def blog():
    return render_template("frontend/blog.html")

@app.route("/basvurularim")
def basvurularim():
    return render_template("frontend/basvurularim.html")

@app.route("/sorularim")
def sorularim():
    return render_template("frontend/sorularim.html")

@app.route("/profilayar")
def profilayar():
    return render_template("frontend/profilayar.html")


@app.route("/donusum")
def donusum():
    return render_template("frontend/donusum.html")

@app.route("/faq")
def faq():
    return render_template("frontend/faq.html")

@app.route("/admin")
def admin():
    return render_template("admin/main.html")

@app.route("/profil")
def profile():
    return render_template("frontend/profil.html")

@app.route("/projeler")
def projeler():
    return render_template("frontend/projeler.html")


# Mysql Kullanıcı Ekleme
@app.route('/register', methods=["GET","POST"])
def register():    
    if request.method == 'GET':
        return render_template("frontend/register.html")

    else :

      reg_name = request.form.get('reg_name')
      reg_tc = request.form.get('reg_tc')
      reg_email = request.form.get('reg_email')
      reg_tel = request.form.get('reg_tel')
      reg_dogum = request.form.get('reg_dogum')
      reg_pass1 = request.form.get('reg_pass1')
      hash_regpass = bcrypt.generate_password_hash(reg_pass1)


      bcrypt.check_password_hash(hash_regpass, reg_pass1)

      cursor = mysql.connection.cursor()

      sorgu = "INSERT INTO tbl_user VALUES(%s,%s,%s,%s,%s,%s,%s)"

      cursor.execute(sorgu,(None,reg_name,reg_tc,reg_tel,reg_dogum,reg_email,hash_regpass))
      mysql.connection.commit()

      session['reg_name'] = reg_name

      return render_template("frontend/main.html")

# Mysql Kullanıcı Giriş

@app.route('/login', methods=["GET", "POST"])
def login():
        if request.method == "POST":
            reg_email = request.form['reg_email']
            reg_pass1 = request.form['reg_pass1']
            hash_regpass = bcrypt.generate_password_hash(reg_pass1)

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            sorgu = "SELECT * FROM tbl_user WHERE user_email=%s"

            cursor.execute(sorgu,(reg_email,))
            reg_name = cursor.fetchone()
            cursor.close()
            

            if len(reg_name) > 0:
                if bcrypt.check_password_hash(hash_regpass, reg_pass1):
                    
                    session['reg_name'] = reg_name['user_name']
                   

                    return render_template("frontend/main.html",)
            else:
                return "hata"
        else:
                return render_template("frontend/login.html")  

# Mysql Kullanıcı Ekleme
@app.route('/hesap', methods=["GET","POST"])
def hesap():    
    if request.method == 'GET':
        return render_template("frontend/hesap.html")

    else :

      reg_tc = request.form.get('reg_tc')
      reg_tel = request.form.get('reg_tel')
      reg_mahalle= request.form.get('reg_mahalle')
      reg_sokak= request.form.get('reg_sokak')
      reg_kapino = request.form.get('reg_kapino')
      reg_ickapino = request.form.get('reg_ickapino')
      reg_ada = request.form.get('reg_ada')
      reg_parsel = request.form.get('reg_parsel')


      cursor = mysql.connection.cursor()

      sorgu = "INSERT INTO tbl_talep VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)"

      cursor.execute(sorgu,(None,reg_tc,reg_tel,reg_mahalle,reg_sokak,reg_kapino,reg_ickapino,reg_ada,reg_parsel))
      mysql.connection.commit()


      return render_template("frontend/profil.html")   

@app.route("/logout")
def logout():
    session.clear()
    return render_template("frontend/main.html")   







if __name__ == '__main__':
    app.secret_key = 'f3cfe9ed8fae309f02079dbf'
    app.run(debug = True)