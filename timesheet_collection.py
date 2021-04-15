from flask import Flask, render_template, url_for, request, redirect, flash

from datetime import datetime, timedelta
import sqlite3 
from sqlite3 import Error
import pandas as pd
import re

app = Flask(__name__) 


conn = sqlite3.connect('plf_database1.db')
c = conn.cursor()

c.execute("""CREATE TABLE if not exists trial4(
            date TEXT,
            time_in TEXT,
            number INTEGER
        )""")

@app.route('/')
def hello_world():
    author = "Me"
    name = "You"
    return render_template('index.html', author=author, name=name)


# @app.route('/signup', methods = ['POST'])
# def signup():
#     email = request.form['email']
#     print("The email address is '" + email + "'")
#     return redirect('/')

@app.route('/my_form', methods = ['POST'])
def my_form():
    print('hii')
    conn = sqlite3.connect('plf_database1.db')
    c = conn.cursor()


    print('connection successfull')
    if request.method == "POST":
        print('logic ran')
        # name = request.form['name']
        date = request.form['date']
        time_in = request.form['time_in']
        number = request.form['number']
        print(date, time_in, number)

 
        try:
            # sql = ("INSERT INTO databasename.tablename (columnName,columnName,columnName,columnName Ci) VALUES (%s, %s, %s, %s)")
            c.execute("INSERT INTO trial4 VALUES (:date, :time_in, :number)",
                {
                    'date' : str(date),
                    'time_in' : str(time_in),
                    'number': int(number)
                })
            conn.commit()
            conn.close()
            #or "conn.commit()" (one of the two)
            # flash('Session Added!')
            return redirect('/')
        except:
            return 'Failed to update database'
    else:
        return 'Something went wrong'

@app.route('/my_form_0', methods = ['POST'])

def my_form_0():
    print('form _0 hii')
    conn = sqlite3.connect('plf_database1.db')
    c = conn.cursor()


    print('connection successfull')
    if request.method == "POST":
        print('form _0 logic ran')
        timestamps = []
        # name = request.form['name']
        date_0 = request.form['date_0']
        time_in_0 = request.form['time_in_0']
        time_out_0 = request.form['time_out_0']
        number = 0
        print(date_0, time_in_0, time_out_0, number)

        try:
            start_hr = datetime.strptime(str(time_in_0),"%H:%M:%S")
            print('start_hr',start_hr)
            end_hr = datetime.strptime(str(time_out_0),"%H:%M:%S")
            print('end_hr', end_hr)
            diff = str(end_hr - start_hr)
            print('diff', diff)
            run_time = 0
            if int(diff[2]) == 0:

                run_time = int(diff[0]) *2
            else:

                run_time = (int(diff[0]) +1) *2

            print('diff :',diff, 'run_time :', run_time)
            for i in range(run_time):
                timestamps.append(start_hr.strftime("%H:%M:%S"))
                start_hr = start_hr + timedelta(minutes = 30)
         
            # sql = ("INSERT INTO databasename.tablename (columnName,columnName,columnName,columnName Ci) VALUES (%s, %s, %s, %s)")
                c.execute("INSERT INTO trial4 VALUES (:date, :time_in, :number)",
                    {
                        'date' : str(date_0),
                        'time_in' : str(start_hr)[11:],
                        'number': 0
                    })
                conn.commit()
                start_hr = start_hr + timedelta(minutes = 30)
            conn.close()
            print('timestamps ', timestamps)
            return redirect('/')
        except:
            return 'Failed to update database'
    else:
        return 'Something went wrong'







@app.route('/querry', methods = ['POST'])
def querry():
    conn = sqlite3.connect('plf_database1.db')
    c = conn.cursor()
    print('connection successfull')
    if request.method == "POST":
        print('querry logic ran')
        c.execute("SELECT *, oid FROM trial4")
        records = c.fetchall()
        print('records : ', records)
        df= pd.DataFrame()
        df['Session ID'] = [i[3] for i in records]
        df['Date'] = [i[0] for i in records]
        df['Sign-in-Time'] = [i[1] for i in records]
        df['Number-of-students'] = [i[2] for i in records]
        df = df.set_index('Session ID')
        df_html = df.to_html()
        
        conn.close()
        # return render_template("querry_page.html", to_send=df)
        # return render_template('querry_page.html')
        return df_html
    else:
        return 'bad key'

@app.route("/delete", methods=['POST'])
def delete_session():
    print('delete ran')
    #Moving forward code
    conn = sqlite3.connect('plf_database1.db')
    c = conn.cursor()
    
    if request.method == "POST":
        c.execute("SELECT oid FROM trial4")

        records = c.fetchall()
        existing_indices = [i[0] for i in records]
        index = request.form['delete_id']
        print(records)
        if '-'  not in index:
            try:
                index = int(request.form['delete_id'])
                print('index: ', index)
                if (index == '')|(int(index) not in existing_indices):
                    return 'bad id'
                else:
                    c.execute("DELETE from trial4 WHERE oid = " + str(index))
                    conn.commit()
                    conn.close()
                    return redirect('/')
            
            except:
                return 'bad key'
        else:
            indices = re.split('-',index)
            print('range of indices ',indices)
            start_index = int(indices[0])
            end_index = int(indices[1])
            for i in range(start_index, end_index+1):

                if i in existing_indices:
                    c.execute("DELETE from trial4 WHERE oid = " + str(i))
                    conn.commit()
                    
                else:
                    return 'bad indices'
            conn.close()     
            
            return redirect('/')

    else:
        return 'bad key'
    
    return records



if __name__ == '__main__':
    app.run(debug=True)
    c.execute("SELECT *, oid FROM trial4")
    records1 = c.fetchall()
    print('records1', records1)

