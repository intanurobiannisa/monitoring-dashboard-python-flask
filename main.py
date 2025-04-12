from flask import Flask, render_template, send_file, redirect, url_for, request, flash
from flask_bootstrap import Bootstrap5
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy import func
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from forms import RegisterForm, LoginForm
import time
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI", 'sqlite:///tables.db')

Bootstrap5(app)
db = SQLAlchemy()
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)

class Participants(db.Model):
    __tablename__ = "participants"
    id = db.Column(db.Integer, primary_key=True)
    UNITAP = db.Column(db.String(250), nullable=False)
    UNITUP = db.Column(db.String(250), nullable=False)
    NOAGENDA = db.Column(db.String(250), nullable=False)
    NOREGISTER = db.Column(db.String(250), nullable=False)
    IDPEL = db.Column(db.String(250), nullable=False)
    NAMA = db.Column(db.String(250), nullable=False)
    ALAMAT = db.Column(db.String(250), nullable=False)
    NOTELP = db.Column(db.String(250), nullable=True)
    NOTELP_HP = db.Column(db.String(250), nullable=True)
    JENIS_PROGRAM = db.Column(db.String(250), nullable=False)
    TARIF_LAMA = db.Column(db.String(250), nullable=False)
    DAYA_LAMA = db.Column(db.String(250), nullable=False)
    TARIF = db.Column(db.String(250), nullable=False)
    DAYA = db.Column(db.String(250), nullable=False)
    TGLBAYAR = db.Column(db.TIMESTAMP, default=datetime.datetime.utcnow)

class Template(db.Model):
    __tablename__ = "template"
    id = db.Column(db.Integer, primary_key=True)
    IDPEL = db.Column(db.String(250), nullable=True)
    M_7 = db.Column(db.Float, nullable=True)
    M_6 = db.Column(db.Float, nullable=True)
    M_5 = db.Column(db.Float, nullable=True)
    M_4 = db.Column(db.Float, nullable=True)
    M_3 = db.Column(db.Float, nullable=True)
    M_2 = db.Column(db.Float, nullable=True)
    M_1 = db.Column(db.Float, nullable=True)
    M = db.Column(db.Float, nullable=True)

class Potentials(db.Model):
    __tablename__ = "potentials"
    id = db.Column(db.Integer, primary_key=True)
    IDPEL = db.Column(db.String(250), nullable=True)

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)

with app.app_context():
    db.create_all()

"""
Add Data to Database
"""
df = pd.read_excel("Book1.xlsx")
df2 = pd.read_csv('cleaned_consumption_data.csv')

def add_template():
    template_data = ['225000145232',32.4,0,32.4,64.7,64.7,129.4,129.4,0]
    with app.app_context():
        temp = Template(IDPEL = template_data[0],
                        M_7 = template_data[1],
                        M_6 = template_data[2],
                        M_5 = template_data[3],
                        M_4 = template_data[4],
                        M_3 = template_data[5],
                        M_2 = template_data[6],
                        M_1 = template_data[7],
                        M = template_data[8])
        db.session.add(temp)
        db.session.commit()

def add_data(df):
    UNITAP = [df.UNITAP[x] for x in range(0, len(df.IDPEL))]
    UNITUP = [df.UNITUP[x] for x in range(0, len(df.IDPEL))]
    NOAGENDA = [df.NOAGENDA[x] for x in range(0, len(df.IDPEL))]
    NOREGISTER = [df.NOREGISTER[x] for x in range(0, len(df.IDPEL))]
    IDPEL = [df.IDPEL[x] for x in range(0, len(df.IDPEL))]
    NAMA = [df.NAMA[x] for x in range(0, len(df.IDPEL))]
    ALAMAT = [df.ALAMAT[x] for x in range(0, len(df.IDPEL))]
    NOTELP = [df.NOTELP[x] for x in range(0, len(df.IDPEL))]
    NOTELP_HP = [df.NOTELP_HP[x] for x in range(0, len(df.IDPEL))]
    JENIS_PROGRAM = [df.JENIS_PROGRAM[x] for x in range(0, len(df.IDPEL))]
    TARIF_LAMA = [df.TARIF_LAMA[x] for x in range(0, len(df.IDPEL))]
    DAYA_LAMA = [df.DAYA_LAMA[x] for x in range(0, len(df.IDPEL))]
    TARIF = [df.TARIF[x] for x in range(0, len(df.IDPEL))]
    DAYA = [df.DAYA[x] for x in range(0, len(df.IDPEL))]
    TGLBAYAR = [df.TGLBAYAR[x] for x in range(0, len(df.IDPEL))]
    with app.app_context():
        for x in range(0,len(IDPEL)):
            data = Participants(UNITAP = UNITAP[x],
                            UNITUP = int(UNITUP[x]),
                            NOAGENDA = int(NOAGENDA[x]),
                            NOREGISTER = int(NOREGISTER[x]),
                            IDPEL=int(IDPEL[x]),
                            NAMA = NAMA[x],
                            ALAMAT = ALAMAT[x],
                            NOTELP = NOTELP[x],
                            NOTELP_HP = int(NOTELP_HP[x]),
                            JENIS_PROGRAM = JENIS_PROGRAM[x],
                            TARIF_LAMA = TARIF_LAMA[x],
                            DAYA_LAMA = int(DAYA_LAMA[x]),
                            TARIF = TARIF[x],
                            DAYA = int(DAYA[x]),
                            TGLBAYAR = TGLBAYAR[x])
            db.session.add(data)
            db.session.commit()

def mean_line():
    plt.figure(figsize=(14, 6))
    ax = sns.lineplot(df2[['M-7', 'M-6', 'M-5', 'M-4', 'M-3', 'M-2', 'M-1', 'M', 'M+1', 'M+2', 'M+3', 'M+4', 'M+5', 'M+6',
                      'M+7']].mean(), marker='o', color='#DF07A2')
    sns.set_style("whitegrid", {'font.family': ['Open Sans']})
    plt.xlabel('Time (Month)')
    plt.ylabel('kWh')
    plt.tight_layout()
    plt.savefig('static/assets/img/mean_line_wide_chart.png')
    plt.close()

def program_bar():
    plt.figure(figsize=(7, 7))
    ax = sns.countplot(data=df, x="JENIS_PROGRAM", color='#DF07A2')
    for container in ax.containers:
        ax.bar_label(container)
    plt.xticks(rotation=90)
    sns.set_style("whitegrid", {'font.family': ['Open Sans']})
    plt.xlabel('')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/assets/img/program_bar_chart.png')
    plt.close()

def program_bar_2022():
    df2022 = df[pd.to_datetime(df.TGLBAYAR).dt.year == 2022]
    plt.figure(figsize=(7, 7))
    ax = sns.countplot(data=df2022, x="JENIS_PROGRAM", color='#DF07A2')
    for container in ax.containers:
        ax.bar_label(container)
    plt.xticks(rotation=90)
    sns.set_style("whitegrid", {'font.family': ['Open Sans']})
    plt.xlabel('')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/assets/img/program2022_bar_chart.png')
    plt.close()

def program_bar_2023():
    df2023 = df[pd.to_datetime(df.TGLBAYAR).dt.year == 2023]
    plt.figure(figsize=(7, 7))
    ax = sns.countplot(data=df2023, x="JENIS_PROGRAM", color='#DF07A2')
    for container in ax.containers:
        ax.bar_label(container)
    plt.xticks(rotation=90)
    sns.set_style("whitegrid", {'font.family': ['Open Sans']})
    plt.xlabel('')
    plt.ylabel('Count')
    plt.tight_layout()
    plt.savefig('static/assets/img/program2023_bar_chart.png')
    plt.close()

def kmeans_lda(pot_cust):
    df2 = pd.read_csv('cleaned_consumption_data.csv')
    df2 = df2.fillna(0)
    X = df2.drop(['IDPEL','TARIF_LAMA','DAYA_LAMA','TARIF','DAYA','TGLBAYAR','M+1',
                 'M+2','M+3','M+4','M+5','M+6','M+7','MEAN_BEFORE','MEAN_AFTER','GROWTH_RATE'],axis=1)
    scaler = StandardScaler()
    scaled_X = scaler.fit_transform(X)
    model = KMeans(n_clusters=6,n_init='auto',random_state=101)
    model.fit(scaled_X)
    k_cluster = model.labels_
    # pot_cust = pd.read_excel("template_form.xlsx")
    predict_pot_cust = pot_cust.drop('IDPEL', axis=1)
    lda = LinearDiscriminantAnalysis()
    lda.fit(X, k_cluster)
    new_labels = lda.predict(predict_pot_cust)
    pot_cust['label'] = new_labels


@app.route('/')
def home():
    tarif_counts = db.session.query(Participants.TARIF_LAMA, func.count(Participants.TARIF_LAMA)).group_by(
        Participants.TARIF_LAMA).order_by(func.count(Participants.TARIF_LAMA).desc()).all()
    daya_counts = db.session.query(Participants.DAYA_LAMA, func.count(Participants.DAYA_LAMA)).group_by(
        Participants.DAYA_LAMA).order_by(func.count(Participants.DAYA_LAMA).desc()).all()
    year_counts = db.session.query(func.extract('year', Participants.TGLBAYAR), func.count()).group_by(
        func.extract('year', Participants.TGLBAYAR)).all()
    options = ['ALL','2022','2023']
    charts = ['static/assets/img/program_bar_chart.png','static/assets/img/program2022_bar_chart.png','static/assets/img/program2023_bar_chart.png']
    len_opt = len(options)
    return render_template("pages/dashboard.html",tariffs=tarif_counts,dayas=daya_counts, years=year_counts, options=options, charts=charts, len=len_opt)

@app.route('/tables')
def tables():
    result = db.session.execute(db.select(Participants))
    all_data = result.scalars().all()
    return render_template("pages/tables.html", datas=all_data)

@app.route('/upload_table_data', methods=['POST'])
def upload_table_data():
    file = request.files['file']
    while file.filename == '':
        time.sleep(2)
    data = pd.read_excel(file)
    add_data(df=data)
    return redirect(url_for("tables"))

@app.route('/export_excel')
def export_excel():
    # Retrieve data from the database
    data = Participants.query.all()
    # Create DataFrame from the retrieved data
    dataframe = pd.DataFrame([(item.UNITAP,
                               item.UNITUP,
                               item.NOAGENDA,
                               item.NOREGISTER,
                               item.IDPEL,
                               item.NAMA,
                               item.ALAMAT,
                               item.NOTELP,
                               item.NOTELP_HP,
                               item.JENIS_PROGRAM,
                               item.TARIF_LAMA,
                               item.DAYA_LAMA,
                               item.TARIF,
                               item.DAYA,
                               item.TGLBAYAR)
                              for item in data],
                             columns=['UNITAP', 'UNITUP', 'NOAGENDA', 'NOREGISTER', 'IDPEL', 'NAMA', 'ALAMAT',
                                      'NOTELP', 'NOTELP_HP', 'JENIS_PROGRAM', 'TARIF_LAMA', 'DAYA_LAMA',
                                      'TARIF', 'DAYA', 'TGLBAYAR'])
    # Create Excel file
    excel_file_path = 'tables.xlsx'
    dataframe.to_excel(excel_file_path, index=False)
    # Serve Excel file as a downloadable attachment
    return send_file(excel_file_path, as_attachment=True)

@app.route('/export_template')
def export_template():
    data = Template.query.all()
    dataframe = pd.DataFrame([(item.IDPEL, item.M_7, item.M_6, item.M_5, item.M_4, item.M_3, item.M_2, item.M_1, item.M)
                              for item in data],
                             columns=['IDPEL', 'M-7', 'M-6', 'M-5', 'M-4', 'M-3', 'M-2', 'M-1', 'M'])
    excel_file_path = 'template_form.xlsx'
    dataframe.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True)

@app.route('/potentials')
def potentials():
    result = db.session.execute(db.select(Potentials))
    all_data = result.scalars().all()
    if db.session.query(Potentials).count() == 0:
        is_empty = True
    else:
        is_empty = False
    return render_template("pages/potentials.html", datas=all_data, is_empty=is_empty)


@app.route('/upload_potential', methods=['POST'])
def upload_potential():
    file = request.files['file']
    while file.filename == '':
        time.sleep(2)
    pot_cust = pd.read_excel(file)
    kmeans_lda(pot_cust)
    pot_idpel = pot_cust[pot_cust.label == 2].IDPEL.tolist()
    for x in range(0,len(pot_idpel)):
        data = Potentials(IDPEL=int(pot_idpel[x]))
        db.session.add(data)
        db.session.commit()
    return redirect(url_for("potentials"))

@app.route('/export_potential')
def export_potential():
    data = Potentials.query.all()
    dataframe = pd.DataFrame([item.IDPEL for item in data],
                             columns=['IDPEL'])
    excel_file_path = 'potential_customers.xlsx'
    dataframe.to_excel(excel_file_path, index=False)
    db.session.query(Potentials).delete()
    db.session.commit()
    return send_file(excel_file_path, as_attachment=True)

@app.route('/profile')
def profile():
    return render_template("pages/profile.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            # User already exists
            flash("That email has been registered, please sign in.")
            return redirect(url_for('signup'))
        # Hashing and salting the password entered by the user
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("pages/sign-up.html", form=form, current_user=current_user)

@app.route("/signin", methods=["GET", "POST"])
def signin():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        # Check stored password hash against entered password hashed.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('signin'))
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('signin'))
        else:
            login_user(user)
            return redirect(url_for("home"))
    return render_template("pages/sign-in.html", form=form, current_user=current_user)

@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
