from flask import Flask,request,render_template,redirect,url_for,session,logging,flash,send_from_directory
import pickle
import numpy as np
from flask_sqlalchemy import SQLAlchemy
import pymysql
pymysql.install_as_MySQLdb()
import os
from flask_login import login_user, login_required, current_user, logout_user, LoginManager, UserMixin
from flask_mail import Mail, Message
import random
from datetime import date,datetime
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'nakshautomation07@gmail.com'
app.config['MAIL_PASSWORD'] = "ngfougxfydzobnzw"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
posta = Mail(app)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1AKASHBAN@localhost/naksh_main'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
# creating content in database
class Naksh_main_tb(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(12), unique=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    hashCode = db.Column(db.String(120))
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1AKASHBAN@localhost/naksh_main'
db = SQLAlchemy(app)
# creating content in database
class Comment_tb(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.String(12), unique=False)
    name = db.Column(db.String(20), unique=True, nullable=False)
    comment = db.Column(db.String(2000), unique=True, nullable=False)
    answer = db.Column(db.String(2000), unique=True, nullable=True)
# open a file, where you stored the pickled data



app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1AKASHBAN@localhost/naksh_main'

db = SQLAlchemy(app)    
class Upload_tb(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    datetime = db.Column(db.String(12), unique=False)
    comment = db.Column(db.String(2000), unique=True, nullable=False)
    answer = db.Column(db.String(2000), unique=True, nullable=True)
    data = db.Column(db.String(20), unique=True, nullable=False)


file = open('/var/www/na/na/model.pkl', 'rb')

# dump load model information to that file
filea = pickle.load(file)

login_manager = LoginManager(app)  
@login_manager.user_loader
def load_user(user_id):
    return Naksh_main_tb.query.get(int(user_id))  
login_manager.login_view = "login"
login_manager.login_message_category = "info"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/nakshoverview')
# @login_required
def overview():
    
   # if 'uname' in session:
    #    uname=session['uname']

        
        return render_template("nakshoverview.html")
   # else:
        
    #    return redirect(url_for('login'))
@app.route('/plcove')
def plcove():
    return render_template('plcove.html')
@app.route('/flask')
def flask():
    return render_template('flaskintro.html')

@app.route('/flaskuser')
def flaskuser():
    return render_template('flaskuser.html')
@app.route('/register',methods=['GET','POST'])
def register():
    if(request.method=='POST'):
        "fetch entry from database"
        # u name is just a variable which is storing name content of form
        uname=request.form.get('uname')
        passw=request.form.get('passw')
        
        existing_entry=Naksh_main_tb.query.filter_by(email=uname).first()
        if existing_entry:
            flash("Email already exist","danger")
            return redirect(url_for("register"))
        # to add entry
        # email from database will store uname variable and password from database will store passw variable
        new_entry=Naksh_main_tb(email=uname,password=passw)
        db.session.add(new_entry)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if(request.method=='POST'):
        "fetch entry from database"
        louname=request.form.get('uname')
        lopassw=request.form.get('passw')
        session['uname']=request.form['uname']
        # now we will compare email from database with loname which stores the login username  ans same for password if this matches then only it will render to nakshoverview
        login=Naksh_main_tb.query.filter_by(email=louname,password=lopassw).first()
        if login is not None:
            # flash('pleas check')
            return render_template('plcpro.html')
            
            
        # else:
        #     return redirect(url_for("login"))
    flash('Please login to submit your queries',"danger")    
    return render_template("login.html")



@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method == "POST":
        print(request.form)
        # mydict will access the form using name
        mydict=request.form
        fever=int(mydict['fever'])
        age=int(mydict['age'])
        pain=int(mydict['pain'])
        runnynose=int(mydict['runnynose'])
        diffbreath=int(mydict['diffbreath'])
        
        
        
        # now here we can use names like fever pain inplace of values
        probability=filea.predict_proba([[fever,pain,age,runnynose,diffbreath]])
        # model.predictproba is used to predict probability

        prob=probability[0][1]
        if (prob>=0.490):
            proba='High Please Consult with Doctor'
        else:
            proba='Low Please Read Precautions Below.STAY SAFE'
        # to select the probabilty using index 1
        print(prob)
        #this will return inf value and display it in show.html
        # return redirect(url_for('index'))
        return render_template('show.html',inf=proba)
    return render_template('index.html')

@app.route('/ask',methods=['GET','POST'])
def register1():
    if(request.method=='POST'):
        "fetch entry from database"
        # u name is just a variable which is storing name content of form
        name=request.form.get('name')
        comment=request.form.get('comment')
        
       
        # to add entry
        # email from database will store uname variable and password from database will store passw variable
        new_entry=Comment_tb(name=name,comment=comment,datetime=date.today())
        db.session.add(new_entry)
        db.session.commit()
        login=Comment_tb.query.all()
        # loname=request.form.get('name')
        # locomment=request.form.get('comment')
        # return redirect(url_for("ans"))
        return render_template("ans.html",login=login)
    return render_template("ask.html")

@app.route('/ans')
def ans():
    login=Comment_tb.query.all()
    return render_template('ans.html',login=login)
@app.route('/editqanda/<int:sno>',methods=["GET","POST"])
def editqanda(sno):
    login=Comment_tb.query.get(sno)
    if(request.method=='POST'):
        login.answer=request.form['answer']
        db.session.commit()
        return redirect(url_for('ans'))
    else:
        return  render_template("editqanda.html",login=login)


@app.route('/pyhmi')
def pyhmi():
    return render_template('pyhmi.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')
@app.route('/plcwplsoft')
def plcwplsoft():
  
    return render_template('plcwplsoft.html')


@app.route('/reminder')
def reminder():
    return render_template('waterreminder.html')

@app.route('/sqlscada')
def sqlscada():
    return render_template('sqlscada.html')
@app.route('/flaskvalid')
def flaskvalid():
    return render_template('flaskvalid.html')
@app.route('/kep')
def kep():

    return render_template('kep.html')
@app.route('/pythonplc')
def pythonplc():
    return render_template('pythonplc.html')

APP_ROOT=os.path.dirname(os.path.abspath(__file__))
@app.route("/plcpro")
def problem():
    image=os.listdir('/var/www/na/na/images')
    question=Upload_tb.query.all()
    return  render_template("plcpro.html",image=image,question=question)



@app.route('/edit/<int:sno>',methods=["GET","POST"])
def edit(sno):
    question=Upload_tb.query.get(sno)
    if(request.method=='POST'):
        question.answer=request.form['answer']
        db.session.commit()
        return redirect(url_for('problem'))  
    else:
        return  render_template("edit.html",question=question)

@app.route("/uploader",methods=["GET","POST"])
def uploader():
    target=os.path.join(APP_ROOT,"images/")
    print(target)
    if not os.path.isdir(target):  #if folder does not exist . creat a folder
        os.mkdir(target)
    if(request.method=='POST'):
        if 'uname' in session:
            uname=session['uname']
            for secret_key,file in request.files.items():
                if file:
                 i=datetime.now()
                 filename=secure_filename(str(current_user)+ "-bild-" + str(i) +".png" )             
                 file.save(os.path.join(target,filename))
            text=request.form.get('comment')
            name=request.form.get('name')
            image=os.listdir('/var/www/na/na/images')
            existing_entry=Upload_tb.query.filter_by(comment=text).first()
            if existing_entry:
            # flash('Email already exist','danger')
               return  render_template("plcpro.html")

           # return redirect(url_for("plcpro"))
            new_entry=Upload_tb(comment=text,data=filename,name=name,datetime=date.today())
            db.session.add(new_entry)
            db.session.commit()
            question=Upload_tb.query.all()
        
            return render_template('plcpro.html',file=filename,text=text,image=image,question=question)
        else:
             # flash('Login to upload your question ',"danger")
              return redirect(url_for('login'))  
@app.route("/uploader/<filename>")
def send_img(filename):
    return send_from_directory("images",filename)
@app.route("/logout")
def logout():
    if 'uname' in session:
            uname=session['uname']
            logout_user()
            session.pop('uname',None)
            flash('You were logged Out',"success")
            return redirect(url_for('login'))
    else:
           # flash('Please login first',"danger")
            return redirect(url_for('login'))

@app.route('/form',methods=["POST","GET"])
def forgot():
    if request.method=="POST":
        mail = request.form['mail']
        check = Naksh_main_tb.query.filter_by(email=mail).first()

        if check:
            def get_random_string(length=24,allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
                return ''.join(random.choice(allowed_chars) for i in range(length))
            hashCode = get_random_string()
            check.hashCode = hashCode
            db.session.commit()
            msg = Message('Confirm Password Change', sender = 'nakshautomation07.com', recipients = [mail])
            msg.body = "Hello,\nWe've received a request to reset your password. If you want to reset your password, click the link below and enter your new password\n https://www.nakshautomation.live/" + check.hashCode
            posta.send(msg)
            return '''
                <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
     #brief {
            display: flex;
            flex-direction: column;
            padding: 65px 11px;
            height: 435px;
            /* to bring content to center */
            
            align-items: center;
            
            
        }
        .border {
    /* border: 1px black solid; */
    border-radius: 50px;
    background-color: aqua;
    height: 1208px;
    padding: 64px;
}
.center{
      text-align: center;

    }
    .qtitle{
      font-weight: 900;
    }
      

    </style>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
<section id="brief">
<div class="form-group border">
       <h2 class="qtitle center">Password Reset Link is sent to this Email Address</h2>
                </div>
                </section>

</body>
</html>
            '''
    else:
        return '''
             <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
     #brief {
            display: flex;
            flex-direction: column;
            padding: 65px 11px;
            height: 435px;
            /* to bring content to center */
            
            align-items: center;
            
            
        }
        .border {
    /* border: 1px black solid; */
    border-radius: 50px;
    background-color: aqua;
    height: 1208px;
    padding: 64px;
}
      

    </style>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
<section id="brief">
<div class="form-group border">
       <form action="/form" method="post" >
                    <label for="email">Enter the email address of the your account</label>
                    <input type="email" name="mail" id="mail" placeholder="username@mail.com" class="form-control"><br>
                    <input type="submit" value="Submit" class="btn btn-primary">
                </form>
                </div>
                </section>

</body>
</html>
        '''
    
@app.route("/<string:hashCode>",methods=["GET","POST"])
def hashcode(hashCode):
    check = Naksh_main_tb.query.filter_by(hashCode=hashCode).first()    
    if check:
        if request.method == 'POST':
            passw = request.form['passw']
            cpassw = request.form['cpassw']
            if passw == cpassw:
                check.password = passw
                check.hashCode= None
                db.session.commit()
                flash('Password Reset Successful','success')
                return redirect(url_for('login'))
            else:
            
                return '''
                    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
     #brief {
            display: flex;
            flex-direction: column;
            padding: 65px 11px;
            height: 435px;
            /* to bring content to center */
            
            align-items: center;
            
            
        }
        .border {
    /* border: 1px black solid; */
    border-radius: 50px;
    background-color: aqua;
    height: 1208px;
    padding: 64px;
}
      

    </style>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
<section id="brief">
<div class="form-group border">
<h4 class="center">Passwords did not match.Please type again</h4>

  <form method="post">
                        <label for="password">Enter New Password</label>
                        <input type="password" name="passw" id="passw" placeholder="password" class="form-control"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password" class="form-control"> <br>
                        <input type="submit" value="Submit" class="btn btn-primary">
                    </form>

       
                </div>
                </section>

</body>
</html> 
                '''
        else:
            return '''
                 <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <style>
     #brief {
            display: flex;
            flex-direction: column;
            padding: 65px 11px;
            height: 435px;
            /* to bring content to center */
            
            align-items: center;
            
            
        }
        .border {
    /* border: 1px black solid; */
    border-radius: 50px;
    background-color: aqua;
    height: 1208px;
    padding: 64px;
}
      

    </style>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"
    integrity="sha384-Vkoo8x4CGsO3+Hhxv8T/Q5PaXtkKtu6ug5TOeNV6gBiFeWPGFN9MuhOf23Q9Ifjh" crossorigin="anonymous">
</head>
<body>
<section id="brief">
<div class="form-group border">
       <form method="post">
                        <label for="password">Enter New Password</label>
                        <input type="password" name="passw" id="passw" placeholder="password" class="form-control"> <br>
                        <input type="password" name="cpassw" id="cpassw" placeholder="confirm password" class="form-control"> <br>
                        <input type="submit" value="Submit" class="btn btn-primary">
                    </form>
                
                </div>
                </section>

</body>
</html>
            '''
    else:
        return render_template('sitemap.xml')
