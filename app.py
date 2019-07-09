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
                return redirect(url_for('gestione'))
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
    @app.route('/gestione', methods=['POST','GET'])
    def gestione():

        # effettuo controllo se la sessione è attiva, altrimenti reinderizzo a index
        if not session['username']:
            return render_template('index.html')

        user = mongo.db.utenti.find_one({"username":session['username']})


        #this way i get the actuale date and time
        #now = datetime.datetime.now()
        # actual_date = now.strftime("%Y-%m-%d")
        # actual_month= now.strftime("%Y-%m")

        #------RICORDARSI DI CANCELLARE QUESTA RIGA DI CODICE--------
        actual_date = "2019-07-05"
        actual_month = "2019-07"
        #------------------------------------------------------------


        listasensori = []

        # array for the month's and day's data
        dati_sensore_del_day = []
        dati_sensore_del_mese = []

        # array to store sennsor's data
        dati_sensore = []

        # latest array to store data in
        sensori = []

        # sensor's names list
        nomi_sensori = []

        # with a serie of FOR cicle I'm gonna create a multidimensional array
        # to store all the sensors and all their data
        for x in user["sensore"] :
            listasensori.append(x["code"])
            nomi_sensori.append(x["name"])

        # variabile passata a jinja per iterare i form dei sensori
        numero_sensori = len(listasensori)

        # FOR cycle to can creata a multidimensional array that can store all the sensor's data
        #  organized in each array's cell  dayily data s array & monthly data s array go into two
        #  separeted cells ---> dati_sensore                 _         _          _ _ _ _ _
        # dati_sensore array  go into -----> sensori array  |_| -|--> |_|  --->  |_|_|_|_|_|  daily data  array
        #                                                   | |  '--> |_|  -      _ _ _ _ _
        #                                                                   '--> |_|_|_|_|_|  monthly data array
        for i in listasensori :
            cursor_day = mongo.db.sensori.find({"code":i, "data":actual_date}).sort("time",-1)
            cursor_month = mongo.db.sensori.find({"code": i, "data": { "$gt": actual_month }}).sort("data",1)

            for c in cursor_day :
                # lista che contiente tutti dati raccolti dal sensore
                dati_sensore_del_day.append(c)
            for c in cursor_month :
                # lista che contiente tutti dati raccolti dal sensore
                dati_sensore_del_mese.append(c)
            # lista che contiente tutti i dati di tutti i sensori, ogni sensore ha un index
            dati_sensore.append(dati_sensore_del_day.copy())
            dati_sensore.append(dati_sensore_del_mese.copy())
            sensori.append(dati_sensore.copy())
            dati_sensore.clear()
            dati_sensore_del_mese.clear()
            dati_sensore_del_day.clear()

        return render_template('gestione.html', username=session['username'],numero_sensori=numero_sensori,sensori=sensori,
                               data=actual_date, nomi_sensori=nomi_sensori)


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
        plantsname = request.form['plantsname']
        result=mongo.db.utenti.find_one({"username":username})
        if result==None :
            if  password==password_repeat:
                mongo.db.utenti.insert_one({"username":username,
                                            "password":password,
                                           "sensore": [{
                                               "code":code_sensor,
                                               "name":plantsname
                                           }]
                                            })
                return render_template('index.html')
            else:
                error = 'passwords do not match'
                return render_template('register.html', error_pass=error)
        else :
            error = 'user already registered'
            return render_template('register.html', error_username=error)



    return app