
#Load libraries
from flask import Flask, render_template, request, send_file, Response, make_response, flash
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class, UploadNotAllowed

import numpy as np
import pandas as pd
from urllib.request import urlopen
import csv
import io

#Define the convert function which calls on API
def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles' #
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'

#Initialize App
app = Flask(__name__)

#configuration
csv_file = UploadSet('files', ('csv',))
#Route for home page
@app.route('/')
def index():
    return render_template('index.html')

#Route for upload function execution
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    print(request.method)
    print(request)
    print(request.files)
#ensure that there is a file
    if request.method in ['POST', 'GET'] and 'csv_data':
        try:
            file = request.files['inputFile']
        except UploadNotAllowed:
            flash('Only CSV files can be uploaded, please correct', 'error')

#convert file into pandas DF and then to list
    identifiers = pd.read_csv(file, names=["Drugs"])
    identifiers = list(identifiers.Drugs)

#create empty lists to populate with convert function
    results = []
    dead_ends = []

#convert file elements to SMILES and append appropriate lists
    for ids in identifiers :
        if CIRconvert(ids) == 'Did not work':
            dead_ends.extend(["Y" + ids, "X" + CIRconvert(ids)])
        else:
            results.extend(["Y" + ids, "X" + CIRconvert(ids)])

#Tag, divide, and sort elements
    results_tagged_names = [i for i in results if i.startswith('Y')]
    results_tagged_SMILES = [i for i in results if i.startswith('X')]

    deadends_tagged_names = [i for i in dead_ends if i.startswith('Y')]
    deadends_tagged_SMILES = [i for i in dead_ends if i.startswith('X')]

    results_data_tuples = list(zip(results_tagged_names,results_tagged_SMILES))
    deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

    deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

#remove tags
    results_df = pd.DataFrame(results_data_tuples, columns=['Names','SMILES'])
    results_df['Names'] = results_df['Names'].str[1:]
    results_df['SMILES'] = results_df['SMILES'].str[1:]

    dead_ends_df = pd.DataFrame(deadends_data_tuples, columns=['Names','SMILES'])
    dead_ends_df['Names'] = dead_ends_df['Names'].str[1:]
    dead_ends_df['SMILES'] = dead_ends_df['SMILES'].str[1:]
    dead_ends_df.rename(index=str, columns={"Names": "Bad Names", "SMILES": "No SMILES"})
    #results_df = pd.concat([results_df, placeholder, dead_ends_df], axis=1)

#convert pandas DF back to csv and allow for download
    result_csv = make_response(results_df.to_csv())
    result_csv.headers["Content-Disposition"] = "attachment; filename=converted_drugs.csv"
    result_csv.headers["Content-Type"] = "text/csv"

    return result_csv

    #return render_template('simple.html',  tables=[results_df.to_html(classes='data', header="true")])

#Run this spicy boi
if __name__ == '__main__':
   app.run(debug = True)
