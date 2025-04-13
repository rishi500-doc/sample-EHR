from flask import Flask,request,render_template,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)
my_database="patient.db"

def conn_db():  
    con=sql.connect(my_database)
    con.row_factory= sql.Row
    return con

def create_table():
    conn=conn_db()

    conn.execute('''create table if not exists patients 
                 (id integer primary key ,
                 name text not null,
                 age integer,
                 gender text,
                 comorbidities text,
                 chief_complaints text,
                 diagnosis text)
                 ''')
    conn.commit()
    conn.close()

create_table()

@app.route('/')
def home():
    return render_template("pt_form.html")

@app.route('/create',methods=["GET","POST"])
def add():
    if request.method=='GET':
        return render_template('create.html')

    elif request.method=='POST':
        conn=conn_db()
        id=request.form.get("id")
        name=request.form.get("name")
        age=request.form.get("age")
        gender=request.form.get("gender")
        comorbidities=request.form.get("comorbidities")
        chief_complaints=request.form.get("chief_complaints")
        diagnosis=request.form.get("diagnosis")
        conn.execute(' insert into patients(id,name,age,gender,comorbidities,chief_complaints,diagnosis) values (?,?,?,?,?,?,?)',(id,name,age,gender,comorbidities,chief_complaints,diagnosis))
        conn.commit()
        conn.close()
        return redirect(url_for('pt_record'))
        

@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    if request.method=="GET":
        conn=conn_db()
        patient=conn.execute('select * from patients where id= ?',(id,)).fetchone()
        return render_template('update.html',patient=patient)
    elif request.method=="POST":
        conn=conn_db()
        id=request.form.get("id")
        name=request.form.get("name")
        age=request.form.get("age")
        gender=request.form.get("gender")
        comorbidities=request.form.get("comorbidities")
        chief_complaints=request.form.get("chief_complaints")
        diagnosis=request.form.get("diagnosis")
        patient=conn.execute('update patients set name= ?,age= ?,gender= ?,comorbidities= ?,chief_complaints= ?,diagnosis= ? where id= ?',(name,age,gender,comorbidities,chief_complaints,diagnosis,id))
        conn.commit()
        conn.close()
        return redirect(url_for('pt_record'))
        
       
    
@app.route('/delete/<int:id>',methods=['GET'])
def delete(id):
    conn=conn_db()
    conn.execute('delete from patients where id= ?',(id,))
    conn.commit()
    conn.close()
    return redirect(url_for('pt_record'))

@app.route('/patient')
def pt_record():
    conn=conn_db()
    patients=conn.execute('select * from patients').fetchall()
    conn.commit()
    conn.close()
    return render_template('pt_record.html',patients=patients)
    
        


if __name__=='__main__':
    app.run(debug=True)



        

    




    

    

