# from multiprocessing import connection
from flask import Flask, redirect, render_template, request, jsonify, url_for
import pickle
from flask import session, redirect, url_for
import database
import secrets
from flask import make_response
from flask import request
import mysql.connector
from datetime import datetime

# Generate a random secret key
cursor=database.connection.cursor()
# cursor.close()
print("Closed successfully..........")
secret_key = secrets.token_hex(16)  # You can adjust the length as needed

app = Flask(__name__)
app.secret_key = secret_key




# new added code

@app.route('/')
def index():
    if 'username' in session:
        # If the user is logged in, redirect to the homepage
        return redirect(url_for('homepage'))
    else:
        # If the user is not logged in, render the login page
        return render_template('login.html')


# @app.route('/')
# def index():
#     return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/documentation')
def documentation():
    return render_template('documentation.html')



@app.route('/Anxiety')
def Anxiety():
    return render_template('Anxiety.html')



# old homepage
data1 =[[]]
data=[]
@app.route('/homepage')
def homepage():
    print("homepaage route.......")
    if 'username' in session:
        currentUser=session['username']
        newdata, fn = database.fetchDetails(currentUser)
        global data1
        data1=newdata
        print("===============>",data1)
    
    return render_template('homepage.html', data=data1)



from flask import jsonify
@app.route('/logout')
def logout():
    session.pop('username', None)
    print("user removed successfuly........")
    return render_template('login.html')


@app.route('/registeruser', methods=['POST'])
def registeruser():
    if request.method == 'POST':
        fullname=request.form['fullname']
        email=request.form['email']
        password=request.form['password']
        gender=request.form['gender']
        dob=request.form['dob']
        
        
        tf=database.registerUserIntoDb(fullname,email,password,gender,dob)
        if(tf):
            session.pop('username', None)
            response_data = {'message': 'Registration successful\nNow you can Login'}
            return jsonify(response_data)
        else:
            response_data = {'message': 'Email already exist'}
            return jsonify(response_data)
            # print("Unable to insert")


currentUser=""
fullName =""
output =""
@app.route('/validatelogin', methods=['POST','GET'])
def validatelogin():
    print("*************************> validatelogin Endpoint Hitted")
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']

        checklogin = database.login_user(email, password)
        print("====================> id password matched",checklogin)
        if checklogin:
            session['username'] = checklogin
            global currentUser
            currentUser = checklogin
            global fullName
            global data
            data, fullName = database.fetchDetails(checklogin)
            print("=================> Validate data 0:",data[0])
            print("=================> Validate data 1:",data[1])
            print("=================> Validate data 2:",data[2])

            print("=================> Validate Full Name:",fullName)

            print("=================> Login Successfully")
            return render_template('homepage.html',data=data)
        else:
           
            response_data = {'success': False, 'message': 'Invalid email or password. Please try again.'}
            return jsonify(response_data)



@app.route('/predict', methods=['POST'])
def predict():
    input_text = request.form['input_text']
    if(input_text==""):
        response_data = {'success': False, 'message': 'Enter text to predict...'}
        return jsonify(response_data)
    prediction_type = request.form['prediction_type']
    print(currentUser,"-----------------")
    if prediction_type == 'basic':
        result1, result2 = perform_basic_prediction(input_text)
        result1_int = int(result1)
        result2_int=int(result2)
        print(currentUser, fullName)
        # t = date.fromtimestamp()
        t = datetime.now()
        print("time is mos afc ",t)
        # print(t,"date is printed.........")
        msg=""
        if(result1_int ==0 and result2_int ==0 ):
            msg ="Sucidial:False Depression:False."
        if(result1_int ==0 and result2_int ==1 ):
            msg ="Sucidial:False Depression:True."
        if(result1_int ==1 and result2_int ==0 ):
            msg ="Sucidial:True Depression:False."
        if(result1_int ==1 and result2_int ==1 ):
            msg ="Sucidial:True Depression:True."

        data = (currentUser, fullName[0], input_text, t, msg)
        print("Data----------",data)
        database.insertBasicOnPredict(data)
        newdata, fn = database.fetchDetails(currentUser)
        global data1
        data1=newdata
        print("data11111111111111111111111",data1)
       
        return render_template('result.html', result1=result1, result2=result2)

    elif prediction_type == 'advance':
        data,msg = perform_advance_prediction(input_text)


        if(data):
            newmsg="True"
        else:
            newmsg="False"


        if(data):
            data="You have Suicide... \n"+msg
        else:
            data="Congrats..."

        t = datetime.now()
        print("time is mos afc ",t)
        # print(t,"date is printed.........")

        
        

        datanew = (currentUser, fullName[0], input_text, t, newmsg)
        database.insertBasicOnPredict(datanew)
        print("Data Inserted==========>",datanew)

        newdata, fn = database.fetchDetails(currentUser)
        
        data1=newdata
        print("==========> All data with current user:",data1)
    
        return render_template('result2.html', data=data)

    else:
        prediction_result = "Invalid prediction type"


    
    return ""

import pickle
from sklearn.feature_extraction.text import CountVectorizer


with open('count_vectorizer.pkl', 'rb') as file:
    count_vectorizer = pickle.load(file)


with open('suicide_model.pickle', 'rb') as file:
    suicide_model = pickle.load(file)

with open('count_vectorizer_depress.pkl', 'rb') as file:
    count_vectorizer_depress = pickle.load(file)


with open('depression_model.pickle', 'rb') as file:
    depression_model = pickle.load(file)


with open('anxiety.pkl', 'rb') as file:
    Anxiety_model = pickle.load(file)





def perform_basic_prediction(input_text):
    # Transforming the new text data using the fitted vectorizer
    new_text_vectorized = count_vectorizer.transform([input_text])
    
    result1 = suicide_model.predict(new_text_vectorized)
    # print("Predicted Label:", result[0])
    # Return the prediction result

    new_text_vectorized2 = count_vectorizer_depress.transform([input_text])
    result2 = depression_model.predict(new_text_vectorized2)
    return result1[0], result2[0]



def perform_advance_prediction(input_text):
    data,msg=ap.getResponse(input_text)
    print("=================> Advance Prediction Result:",data,msg)
    return data,msg

@app.route('/anxiety', methods=['POST'])
def anxiety():
    phq = request.form['phq_score']
    gad = request.form['gad_score']
    epw = request.form['epworth_score']

    result=Anxiety_model.predict([[float(phq),float(gad),float(epw)]])
    t = datetime.now()
    print("time is mos afc ",t)
    # print(t,"date is printed.........")
    print("Full name ....",fullName)
    print("Current User ,,,,",currentUser)
    data = (currentUser, fullName, phq, gad, epw, t, result[0])
    print("Data----------",data)
    database.insertAnxietyOnPredict(data)
    print("Data inserted in anxiety table,...")
    return render_template('resultAnxiety.html',result=result[0])


import advPrediction as ap
if __name__ == '__main__':
    app.run(debug=True)


# 1718