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

if __name__ == '__main__':
    app.run(host=os.environ.get('IP', '0.0.0.0'),
            port=int(os.environ.get('PORT','3000')),
            debug=True)