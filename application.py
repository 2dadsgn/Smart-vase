import os
import time

from flask import Flask, render_template, request, redirect, url_for, session, abort
from flask_mail import Mail, Message
from flask_pymongo import PyMongo
from random_password import random_password
from werkzeug.security import generate_password_hash, check_password_hash


def create_app(test_config=None):


    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)


    app.config["MONGO_URI"] = "mongodb://localhost:27017/db-progetto"
    mongo = PyMongo(app)

    app.secret_key = b'_52ksaLF3Q8znxec]/'
    mail = Mail(app)

    app.config['MAIL_SERVER'] = 'out.virgilio.it'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'smartvaseprj@virgilio.it'
    app.config['MAIL_PASSWORD'] = 'progettodb52'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    mail = Mail(app)

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
        error = None

        if db_username== None :
            error="User not registered"
            return render_template('index.html', error_name=error)


        else :
            if check_password_hash(db_username['password'], password):

                if db_username["confirmed"]==True:

                    session['username'] = username
                    return redirect(url_for('gestione'))

                else:
                    try:
                        token = request.form['token']
                        if check_password_hash(db_username["token"], token):

                            mongo.db.utenti.update_one({'username': username}, {"$set": {"confirmed": True}})
                            session['username'] = username
                            return redirect(url_for('gestione'))
                        else:
                            error = "Wrong confirmation code"
                            return render_template('index.html', error=error, confirmed=False)
                    except:
                        session["username"]=username
                        return redirect(url_for("sending_email"))


            else:
                error = 'Wrong password'
                return render_template('index.html', error=error)

    @app.route('/confirm_email')
    def confirm_email():
        return render_template('confirm_address.html')

    @app.route('/changing_password',methods=['POST'])
    def changing_password():
        email = request.form['email']
        token = random_password(length=4, characters=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', '1', '2', '3', '4', '5', '6'])
        mongo.db.utenti.update_one({"email":email},
                                   {"$set": {"token": generate_password_hash(token)}})
        result = mongo.db.utenti.find_one({"email": email})

        try:
            msg = Message('Confirmation Code', sender='smartvaseprj@virgilio.it', recipients=[email])
            msg.body = f"Hello from Smart vase prj, please copy and paste this code in the login page to confirm your identity --> {token} <--  "
            mail.send(msg)
            return render_template('change_password.html')
        except:
            error="Email not valid"
            return render_template('confirm_address.html',error=error)



    @app.route('/change_password',methods=['POST'])
    def change_password():
        username = request.form['username']
        newpassword = request.form['newpassword']
        newpasswordrepeat = request.form['newpasswordrepeat']
        token = request.form['token']
        result = mongo.db.utenti.find_one({"username": username})
        if result == None :
            error="This user is not registered"
            return render_template("change_password.html",error=error)
        else:
            if newpassword == newpasswordrepeat:

                if check_password_hash(result["token"], token):
                    mongo.db.utenti.update_one({"username": username},
                                               {"$set": {"password": generate_password_hash(newpassword)}})
                    return redirect(url_for('index'))
                else:
                    error = "Confirmation Code not valid"
                    return render_template("change_password.html", error=error)
            else:
                error = "Passwords do not match"
                return render_template("change_password.html", error=error)


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
    @app.route('/gestione')
    def gestione():

        # effettuo controllo se la sessione è attiva, altrimenti reinderizzo a index
        if not session['username']:
            return render_template('index.html')

        user = mongo.db.utenti.find_one({"username":session['username']})


        #this way i get the actuale date and time
        #now = datetime.datetime.now()
        # actual_date = now.strftime("%Y-%m-%d")
        # actual_month= now.strftime("%Y-%m")

        #smart vase is not connected yet so i cant get up to date data
        #so i m using a fake date to fetch data from DB
        #------RICORDARSI DI CANCELLARE QUESTA RIGA DI CODICE--------
        actual_date = "2019-06-30"
        actual_month = "2019-06"
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

        # FOR cycle to can create a multidimensional array that can store all the sensor's data
        #  organized in each array's cell  dayily data s array & monthly data s array go into two
        #  separeted cells ---> dati_sensore                 _         _          _ _ _ _ _
        # dati_sensore array  go into -----> sensori array  |_| -|--> |_|  --->  |_|_|_|_|_|  daily data  array
        #                                                   | |  '--> |_|  -      _ _ _ _ _
        #                                                                   '--> |_|_|_|_|_|  monthly data array
        for i in listasensori :
            print(i)
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

        vuoto = []
        # FOR cycle to controll if sensor's data are available in the DB
        for i in user['sensore']:
            cursor_day = mongo.db.sensori.find_one({"code":i['code'], "data":actual_date})

            print(cursor_day)
            if cursor_day == None:
                vuoto.append(0)
            else:
                vuoto.append(1)

        return render_template('gestione.html', username=session['username'],numero_sensori=numero_sensori,sensori=sensori,
                               data=actual_date, nomi_sensori=nomi_sensori,vuoto=vuoto)


    @app.route('/register')
    def register():

        return render_template('register.html')

    #route for user's sign up
    #form input = name,password and sensor's unique code
    @app.route('/register', methods=['POST'])
    def register_insert():
        error=None
        username=request.form['username']
        email = request.form['email']
        password= request.form['password']
        password_repeat = request.form['password_repeat']
        code_sensor = request.form['code']
        plantsname = request.form['plantsname']
        result=mongo.db.utenti.find_one({"username":username})
        if result==None :
            if  password==password_repeat:
                token = random_password(length=4, characters=['A','B','C','D','E','F','G','H','I','1','2','3','4','5','6'])
                mongo.db.utenti.insert_one({"username":username,
                                            "email":email,
                                            "password":generate_password_hash(password),
                                            "confirmed":False,
                                            "token": generate_password_hash(token),
                                           "sensore": [{
                                               "code":code_sensor,
                                               "name":plantsname
                                           }]
                                            })
                try:
                    msg = Message('Confirmation Code', sender='smartvaseprj@virgilio.it', recipients=[email])
                    msg.body = f"Hello {username} from Smart vase prj, please copy and paste this code in the login page to confirm your identity --> {token} <--  "
                    mail.send(msg)
                    print(msg)
                    return render_template("index.html", confirmed=False)
                except:
                    mongo.db.utenti.delete_one({"username":username})
                    return render_template("register.html",error_email="Email not valid")
            else:
                error = 'passwords do not match'
                return render_template('register.html', error_pass=error)
        else :
            error = 'user already registered'
            return render_template('register.html', error_username=error)

    # route to can send emails with the verification code
    @app.route("/sendingemail")
    def sending_email():
        token = random_password(length=4, characters=['A','B','C','D','E','F','G','H','I','1','2','3','4','5','6'])
        mongo.db.utenti.update_one({"username": session['username']},
                                   {"$set": {"token":generate_password_hash(token)}})
        result=mongo.db.utenti.find_one({"username":session["username"]})
        msg = Message('Confirmation Code', sender='smartvaseprj@virgilio.it', recipients=[result["email"]])
        msg.body = f"Hello {session['username']} from Smart vase prj, please copy and paste this code in the login page to confirm your identity --> {token} <--  "
        print(msg)
        mail.send(msg)
        session.pop('username',None)
        return render_template("index.html",confirmed=False)

    #route to can add a new plant's tab in the managing page
    @app.route('/addnewplant')
    def addnewplant():
        return render_template('add-new-plant.html')

    # route to can add a new plant's tab in the managing page
    @app.route('/adding', methods=['POST','GET'])
    def add_plant():
        plantsname = request.form['plantsname']
        code = request.form['sensorcode']
        mongo.db.utenti.update_one({"username": session['username']}, {"$push": {"sensore":{"code":code, "name":plantsname}}}
                                   ,upsert=True)
        return redirect(url_for('gestione'))

    # route to can delete a plant's tabe in the managing page
    @app.route('/deleting')
    def delete_sensor():
        return render_template('delete-sensor.html')

    # route to can delete a plant's tabe in the managing page
    @app.route('/delete', methods=['POST', 'GET'])
    def delete():
        plantsname = request.form['plantsname']
        code = request.form['sensorcode']
        mongo.db.utenti.update_one({"username": session['username']},
                                   {"$pull": {"sensore": {"code": code, "name": plantsname}}})
        return redirect(url_for('gestione'))

    # route to can modify a plant's tabe in the managing page
    @app.route('/modifying')
    def modify_sensor():
        return render_template('modify-sensor.html')

    # route to can modify a plant's tabe in the managing page
    @app.route('/modify', methods=['POST', 'GET'])
    def modify():
        plantsname = request.form['plantsname']
        code = request.form['sensorcode']
        mongo.db.utenti.update_one({"username": session['username']},
                                   {"$set": {"sensore": [{"code": code, "name": plantsname}]}})
        return redirect(url_for('gestione'))



    @app.route('/errore')
    def errore():
        abort(404)




    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('404.html'),404




    return app