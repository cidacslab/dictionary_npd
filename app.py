from flask import Flask, request, render_template
import os
import sys
import json
import pandas as pd
from pymongo import MongoClient

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates/')

app = Flask(__name__, template_folder=template_path)
# app.config['MONGO_DBNAME'] = 'dictionaryDB'
# app.config["MONGO_URI"] = "mongodb://localhost:27017/dictionaryDB"

# mongo = PyMongo(app)

client = MongoClient('mongodb://localhost:27017/')
db = client.dictionaryDB
def pymongo_python_sys():
        if sys.version_info.major == 2:
                app.config['MONGO_DBNAME'] = 'dictionaryDB'
                app.config["MONGO_URI"] = "mongodb://localhost:27017/dictionaryDB"
                mongo = PyMongo(app)
        else:
                client = MongoClient('mongodb://localhost:27017/')
                mongo = client.dictionaryDB
        return mongo

# mongo = pymongo_python_sys()
@app.route('/')
def index():
        return render_template('index.html')

@app.route('/dictionary')
def dictionary():
        #dicttionarys = db.collection_names(include_system_collections=False) #Incluir select para buscar todos os dicionarios no banco.
        return render_template('dictionary.html')

@app.route('/teste', methods=['POST']) 
def teste():
        nameDictionary = str(request.form.get('nameDictionary'))
        variables = str(request.form.get('result'))

        variables  = variables.replace("'",'"').replace('-,','-').split('-')

        for var in variables:
                if var is not '':
                        try:
                                var = var.replace(",}","}")
                                var = json.loads(var)
                        except:
                                return "erro"
                        collection = db[nameDictionary]
                        collection.insert(var)    
        return render_template('index.html')


@app.route('/to_csv', methods=['POST'])
def pandas_to_csv():

        nameDictionary = str(request.form.get('nameDictionary'))
        
        collection = db[nameDictionary]
        df = pd.DataFrame(list(collection.find()))
        df = df[['variable','categories_std','type']]
        df.to_csv('/dictionary/name.csv',index=False)

@app.route("/search")
def search():

        # nameDictionary = str(request.form.get('nameDictionary'))
        # collection = db[nameDictionary]
        # list(db.hans.find())
        return render_template('dictionary.html')
