
#!flask/bin/python
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from flask import Flask, url_for,jsonify, render_template, flash, request, redirect, make_response, abort, Response, session
from flask_session import Session
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash,check_password_hash
from dateutil.relativedelta import relativedelta
import sys
import time
import json
from datetime import datetime
from collections import OrderedDict
from PygTrends import fetchtrends
import models as dbHandler

appy = Flask(__name__)
SESSION_TYPE = 'filesystem'
appy.config.from_object(__name__)
SECRET_KEY = '7d441f27d441f27567d441f2b6176a'
sess=Session()
sess.init_app(appy)

@appy.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

class ReusableForm(Form):
    Keywords = TextField('Keywords:', validators=[validators.required(),validators.Regexp(regex=r'([A-Za-z,])+')])

@appy.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@appy.route("/", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        users = dbHandler.retrieveUsers()
        for tup in users:
            if((list(tup)[0]).lower()==username.lower()):
                if (check_password_hash(list(tup)[1],password )):
                    session['username']=username
                    return redirect("/GT")
                else:
                    flash('Error: Invalid Username and Password. Try Again...')
                    return render_template('login.html')
        flash('Error: Invalid Username and Password. Try Again...')
        return render_template('login.html')
    else:
	return render_template('login.html')

@appy.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['repassword']
        if ( password.lower() == re_password.lower()):
            if dbHandler.checkUser(username)==0:
                hash = generate_password_hash(password)
                dbHandler.insertUser(username, hash)
                session['username']=username
                return redirect("/GT")
            else:
                flash('Error: This username is unavailable. Try Again...')
                return render_template('signup.html')
        else:
            flash('Error: The passwords do not match. Try Again...')
            return render_template('signup.html')

    else:
	return render_template('signup.html')

@appy.route("/GT", methods=['GET', 'POST'])
def hello():
    if(session['username']!=""):
        form = ReusableForm(request.form)
        #error=None
        #print(form.errors)
        if request.method == 'POST':
            #flash(' ')
            Keywords=request.form['Keywords']
            #password=request.form['password']

            #print name, " ", email, " ", password
            flag=0
            if form.validate():
                # Save the comment here.
                if all(x.isalpha() or x==" " or x=="," for x in Keywords):
                    now = datetime.now()
                    totime=now.strftime("%Y-%m-%d")
                    one_week = now - relativedelta(weeks=1)
                    #print(type(fromtime))
                    #print(totime)
                    fromtime=one_week.strftime("%Y-%m-%d")
                    #print(one_week)#.strftime("%Y-%m-%d")
                    #timeframe = one_week.strftime("%Y-%m-%d") + " " + now.strftime("%Y-%m-%d")

                    #visit="http://ec2-18-191-252-154.us-east-2.compute.amazonaws.com/?keywords="+Keywords+"&latitude=35.393528&longitude=-119.043732&from="+fromtime+"&to="+totime
                    #return redirect(visit, code=302)
                    #messages = json.dumps({'keywords':Keywords,'latitude':'35.393528','longitude':'-119.043732','from':fromtime,'to':totime})
                    session['keywords'] = Keywords
                    session['latitude'] = '35.393528'
                    session['longitude'] = '-119.043732'
                    session['from'] = fromtime
                    session['to'] = totime
                    return redirect("/fetchGT")
                else:
                   #abort(404)
                   flag=1

            else:
                if Keywords=="":
                    flash('Error: Invalid Input! Field cannot be empty. Try Again...')
                    form = ReusableForm(request.form)
                else:
                    flash('Error: Invalid Input! Only Words and Commas are Allowed. Try Again...')

            if flag==1:
                flash('Error: Invalid Input! Only Words and Commas are Allowed. Try Again...')
        return render_template('hello.html', form=form)
    else:
        flash('Session timed out.')
        return redirect('/')
@appy.route("/fetchGT", methods=['GET', 'POST'])
def index():
    if(session['username']!=""):
        try:
            keywords = session['keywords']
            kw_list = keywords.split(',')
            latitude = session['latitude']
            longitude = session['longitude']
            fromtime = session['from']
            totime = session['to']
            session.pop('_flashes', None)
            if(fromtime!=None and totime!=None):
                timeframe=fromtime+" "+totime
            else:
                timeframe=None
            if(timeframe==None):
                try:





                    flash('Error: Invalid Input! Field cannot be empty. Try Again...')
                    form = ReusableForm(request.form)
                else:
                    flash('Error: Invalid Input! Only Words and Commas are Allowed. Try Again...')

            if flag==1:
                flash('Error: Invalid Input! Only Words and Commas are Allowed. Try Again...')
        return render_template('hello.html', form=form)
    else:
        flash('Session timed out.')
        return redirect('/')
@appy.route("/fetchGT", methods=['GET', 'POST'])
def index():
    if(session['username']!=""):
        try:
            keywords = session['keywords']
            kw_list = keywords.split(',')
            latitude = session['latitude']
            longitude = session['longitude']
            fromtime = session['from']
            totime = session['to']
            session.pop('_flashes', None)
            if(fromtime!=None and totime!=None):
                timeframe=fromtime+" "+totime
            else:
                timeframe=None
            if(timeframe==None):
                try:
                    fetch_instance = fetchtrends(kw_list,latitude,longitude)
                except:
                    return '''Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL. 'from' and 'to' are optional.'''

            else:
                try:
                    fetch_instance = fetchtrends(kw_list,latitude,longitude,timeframe)
                except:
                    return '''Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL. 'from' and 'to' are optional.'''
            df=""
            try:
                df=fetch_instance.fetch()
            except:
                time.sleep(60)
                df=fetch_instance.fetch()
            finally:
                if (len(df)==0):
                    abort(404)
                df=df.drop(['isPartial'], axis=1)
                jdf=df.to_json(date_format='iso')
                actj=json.loads(jdf, object_pairs_hook=OrderedDict)
                for i in range(0,len(kw_list)):
                    new_list=[]
                    for vals in list(actj[kw_list[i]].items()):
                        lst=list(vals)
                        lst[0]=((datetime.strptime(lst[0],"%Y-%m-%dT%H:%M:%S.%fZ")).strftime("%Y-%m-%d"))
                        vals=tuple(lst)
                        new_list.append(vals)
                    actj[kw_list[i]]=OrderedDict(new_list)

               #jsondf=df.to_json(orient='index',date_format='iso')
                #tmp=json.loads(jsondf, object_pairs_hook=OrderedDict)
                #actual_json=OrderedDict(((datetime.strptime(k,"%Y-%m-%dT%H:%M:%S.%fZ")).strftime("%Y-%m-%d"),v) for k,v in tmp.items())
                return ''' <a style="float:right;" href="/logout"> Logout </a><br><a href="/GT"> <-Back</a><br><br><br>{}<br><br><br><a style="left-margin:2em" href="/GT"> <-Back</a>'''.format(json.dumps$
        except:
            return '''Sorry! Your search returned empty! Are you sure you have entered a valid input?\n'''
        header_text = '''
        <html>\n<head> <title>PyGT API</title> </head>\n<body>'''
        instructions = '''
        <p><em>Hint</em>: This is a RESTful web service! Append a list of 'keywords', 'latitude', 'longitude', 'from' (YYYY-MM-DD) and 'to' (YYYY-MM-DD) to the URL (for example: <code>/?keywords=keywrd&latitude=0.0&longitude=0.0&from=2000-01-01&to=2010-01-01/code>) to get Google Trends data for a specific keyword, location and timeframe.</p>\n'''

        footer_text = '</body>\n</html>'
    else:
	flash('Session timed out.')
        return redirect('/')


@appy.route("/logout", methods=['GET', 'POST'])
def logout():
    session['username']=""
    return ''' You have successfully logged out! '''


if __name__ == '__main__':
    appy.run(debug=True,threaded=True)
