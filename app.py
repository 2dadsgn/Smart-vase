import datetime
import os
import time

from flask import Flask, render_template, request, redirect, url_for, session
from flask_pymongo import PyMongo


def create_app(test_config=None):


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config["MONGO_URI"] = "mongodb://localhost:27017/db-progetto"
    mongo = PyMongo(app)



    app.secret_key = b'_52ksaLF3Q8znxec]/'

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    #route principale
    @app.route('/')
    def index():
        return render_template('index.html')



    #route con metodo per controllare nome utente e password
    @app.route('/', methods = ['POST', 'GET'])
    def index_login():

        username = request.form['username']
        password = request.form['password']
        db_username = mongo.db.utenti.find_one({'username': username})
        print(db_username)
        error = None
        if db_username== None :
            error = 'Utente non registrato'
            return render_template('index.html', error_name=error)

        else :
            if db_username['password'] == password:
                session['username']=username
                return redirect(url_for('gestione_get_user', username=username))
            else:
                error = 'password errata'
                return render_template('index.html', error=error)


    @app.route('/logging_out')
    def logging_out():
        time.sleep(5)
        return redirect(url_for('logout'))

    #route for logging out the user
    @app.route('/logout')
    def logout():
        session.pop('username',None)
        return  render_template('index.html')

    #route per la pagina sessione attiva gestione sensori
    @app.route('/gestione/session?<username>', methods=['POST','GET'])
    def gestione_get_user(username):

        username=session['username']
        user = mongo.db.utenti.find_one({"username":session['username']})

        #this way i get the actuale date and time
        now = datetime.datetime.now()
        actual_date = now.strftime("%Y-%m-%d")
        actual_month= now.strftime("%Y-%m")


        #this gets the mongoDB's cursor onto the data inserted by the specific sensor
        #for the actual day and it sorts them
        try:
            daysdata = mongo.db.sensori.find({"data":actual_date}).sort("time",-1)

        except:
            print("**-errore nella ricerca sensori per utente--*")

        #select su dati del mese
        try:
            monthsdata = mongo.db.sensori.find({"data": { "$gt": actual_month }}).sort("time",-1)
        except:
            print("errore su ricerca dati del mese")
        dictionaryday = []
        dictionarymonth = []

        #select last data
        for x in daysdata:
            dictionaryday.append(x)

        # select last data
        for x in monthsdata:
            dictionarymonth.append(x)
            print(x)



        return render_template('gestione.html',daytemp=dictionaryday, monthtemp=dictionarymonth, username=username )



    @app.route('/register')
    def register():

        return render_template('register.html')

    #route for user's sign up
    #form input = name,password and sensor's unique code
    @app.route('/register', methods=['POST'])
    def register_insert():
        error=None
        username=request.form['username']
        password= request.form['password']
        password_repeat = request.form['password_repeat']
        code_sensor = request.form['code']
        result=mongo.db.utenti.find_one({"username":username})
        if result==None :
            if  password==password_repeat:
                mongo.db.utenti.insert_one({"username":username,
                                            "password":password,
                                           "code": code_sensor})
                return render_template('index.html')
            else:
                error = 'passwords do not match'
                return render_template('register.html', error_pass=error)
        else :
            error = 'user already registered'
            return render_template('register.html', error_username=error)



    return app