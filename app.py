import os
import env
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 


app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'handover_manager'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', "Env value not loaded")

mongo = PyMongo(app)


@app.route('/')
@app.route('/get_handover')
def get_handover():
    return render_template("handover.html", handover=mongo.db.handover.find())

@app.route('/')
@app.route('/get_addhandover')
def get_addhandover():
    return render_template('addhandover.html',
    sections=mongo.db.sections.find())

@app.route('/insert_handover', methods=['POST'])
def insert_handover():
    handover = mongo.db.handover
    handover.insert_one(request.form.to_dict())
    return redirect(url_for('get_handover'))  

@app.route('/edit_handover/<handover_id>')
def edit_handover(handover_id):
    the_handover =  mongo.db.handover.find_one({"_id": ObjectId(handover_id)})
    all_sections =  mongo.db.sections.find()
    return render_template('edithandover.html', handover=the_handover,
                           sections=all_sections)   

@app.route('/update_handover/<handover_id>', methods=["POST"])
def update_handover(handover_id):
    handover = mongo.db.handover
    handover.update( {'_id': ObjectId(handover_id)},  
    {
        'title':request.form.get('title'),
        'first_name':request.form.get('first_name'),
        'surname': request.form.get('surname'),
        'dob': request.form.get('dob'),
        'blood_pressure':request.form.get('blood_pressure'),
        'diabetes':request.form.get('diabetes'),
        'patient_fluids':request.form.get('patient_fluids')
    })
    return redirect(url_for('get_handover'))    

@app.route('/delete_handover/<handover_id>')
def delete_handover(handover_id):
    mongo.db.handover.remove({'_id': ObjectId(handover_id)})
    return redirect(url_for('get_handover'))    

@app.route('/get_sections')
def get_sections():
    return render_template('sections.html',
                           sections=mongo.db.sections.find())

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT','3000')),
            debug=True)