from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {

  "apiKey": "AIzaSyD5hnqX8TuuOGFT3EkOOdGCIiPQMwDhnk4",
  "authDomain": "my-project1-7013b.firebaseapp.com",
  "projectId": "my-project1-7013b",
  "storageBucket": "my-project1-7013b.appspot.com",
  "messagingSenderId": "797068426043",
  "appId": "1:797068426043:web:98ae1b47de42ac86b3551e",
  "databaseURL":"https://my-project1-7013b-default-rtdb.europe-west1.firebasedatabase.app/"

}
fireBase = pyrebase.initialize_app(config)
auth = fireBase.auth()
db = fireBase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
citiesss = ['haifa','gaza',"Be'er Sheva",'Ashdod','Netanya','Rishon LeTsiyon','nazarth','jerusalem','tel-aviv']
@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        username = request.form['username']
        your_city = request.form['your_city']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID = login_session['user']['localId']
            user = {"email": email, "name" : name, "username" : username, "your_city" : your_city}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('choosing'))
        except Exception as e:
            print("SIGN UP ERROR:", e)
            error = "Authentication failed"
    return render_template("signup.html")


@app.route('/choosing', methods=['GET', 'POST'])
def choosing():
    error = ""
    if request.method == 'POST':
        try:
            city = request.form['city']
            login_session['city'] = city
            return redirect(url_for('rating'))
        except:
            error = "no city"
    return render_template("choosing.html")

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('choosing'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/rating', methods=['GET', 'POST'])
def rating():
    error = ""
    city = login_session['city']
    if request.method == 'POST':
        try:
            rating = request.form['rating']
            city_info = {"city": city,"rating": rating}
            db.child(city).push(city_info)
            return redirect(url_for('billboard'))

        except:
            error = "Authentication failed"
    return render_template("rating.html", city=city)

@app.route('/billboard', methods=['GET', 'POST'])
def billboard():
    error = ""
    city_data = {}
    for city in citiesss:
        ratings = db.child(city).get().val()
        counter = 0
        sum_rating = 0
        if ratings != None :
            for key in ratings:
                counter += 1
                sum_rating += int(ratings[key]['rating'])
            avg = sum_rating / counter
        else:
            avg = 0
        city_data[city] = avg





    # cities_data = {'gaza': db.child('gaza').get().val(), "Be'er Sheva": db.child("Be'er Sheva").get().val(), 'Ashdod': db.child('Ashdod').get().val(), 'Netanya': db.child('Netanya').get().val(), 'Rishon LeTsiyon': db.child('Rishon LeTsiyon').get().val(), 'nazarth': db.child('nazarth').get().val(), 'jerusalem': db.child('jerusalem').get().val(), 'haifa': db.child('haifa').get().val()}

    return render_template('billboard.html', data = city_data)


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)