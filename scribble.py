

  for ids in identifiers :
      if CIRconvert(ids) == 'Did not work':
          dead_ends.extend(["Y" + ids, "X" + CIRconvert(ids)])
      else:
          results.extend(["Y" + ids, "X" + CIRconvert(ids)])


  ####################################################################################
@app.route('/upload', methods=['POST', 'GET'])
def upload():
    file = request.files['inputFile']

      stream = io.StringIO(file.stream.read().decode("UTF8"))
      csv_input = csv.reader(stream)
      #print("file contents: ", file_contents)
      #print(type(file_contents))

      stream.seek(0)
      indentifiers  = stream.read()

      results = []
      dead_ends = []

      for ids in indentifiers :
          if CIRconvert(ids) == 'Did not work':
              dead_ends.extend(["Y" + ids, "X" + CIRconvert(ids)])
          else:
              results.extend(["Y" + ids, "X" + CIRconvert(ids)])

      results_tagged_names = [i for i in results if i.startswith('Y')]
      results_tagged_SMILES = [i for i in results if i.startswith('X')]

      deadends_tagged_names = [i for i in dead_ends if i.startswith('Y')]
      deadends_tagged_SMILES = [i for i in dead_ends if i.startswith('X')]

      results_data_tuples = list(zip(results_tagged_names,results_tagged_SMILES))
      deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

      deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

      results_df = pd.DataFrame(results_data_tuples, columns=['Names','SMILES'])
      results_df['Names'] = results_df['Names'].str[1:]
      results_df['SMILES'] = results_df['SMILES'].str[1:]

      dead_ends_df = pd.DataFrame(deadends_data_tuples, columns=['Names','SMILES'])
      dead_ends_df['Names'] = dead_ends_df['Names'].str[1:]
      dead_ends_df['SMILES'] = dead_ends_df['SMILES'].str[1:]



      #results_df["Content-Disposition"] = "attachment; filename=export.csv"
      #results_df["Content-Type"] = "text/csv"
      #return results_df

      results = results_df.to_csv(r'results_df.csv')
      return Response(results,
                      mimetype="text/csv",
                      headers={"Content-disposition":
                      "attachment; filename=converted_drugs.csv"})


      #dead_ends_df.to_csv(r'dead_ends_df.csv')

      #return render_template('index.html')





  #@app.route('/uploaded')
  #def upload_file():
  #   return render_template('uploaded.html')

  #@app.route('/uploader', methods = ['GET', 'POST'])
  #def upload_files():
  #   if request.method == 'POST':
  #      f = request.files['file']
  #      f.save(secure_filename(f.filename))
  #      return 'file uploaded successfully'

#############################################################

from flask import Flask, render_template, request, send_file, Response
from werkzeug import secure_filename
from flask_uploads import UploadSet, configure_uploads, DATA, patch_request_class
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField


import numpy as np
import pandas as pd
from urllib.request import urlopen
import csv
import io

def CIRconvert(ids):
    try:
        url = 'http://cactus.nci.nih.gov/chemical/structure/' + ids + '/smiles' #
        ans = urlopen(url).read().decode('utf8')
        return ans
    except:
        return 'Did not work'


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['inputFile']
    #decoded_file = file.read().decode('utf-8')
    #identifiers = [decoded_file]
    #io_string = io.StringIO(decoded_file)
    #identifiers1 = [csv.reader(io_string)]
    #identifiers2 = [identifiers1]
    #print(identifiers2)
    #work_file = csv.reader(io_string)
    #identifiers = [work_file]
        if not file:
            return "No file"

        stream = io.StringIO(file.stream.read().decode("UTF8"))
        csv_input = csv.reader(stream)
    #print("file contents: ", file_contents)
    #print(type(file_contents))

        stream.seek(0)
        indentifiers  = stream.read()

        results = []
        dead_ends = []

        for ids in indentifiers :
            if CIRconvert(ids) == 'Did not work':
                dead_ends.extend(["Y" + ids, "X" + CIRconvert(ids)])
            else:
                results.extend(["Y" + ids, "X" + CIRconvert(ids)])

                results_tagged_names = [i for i in results if i.startswith('Y')]
                results_tagged_SMILES = [i for i in results if i.startswith('X')]

                deadends_tagged_names = [i for i in dead_ends if i.startswith('Y')]
                deadends_tagged_SMILES = [i for i in dead_ends if i.startswith('X')]

                results_data_tuples = list(zip(results_tagged_names,results_tagged_SMILES))
                deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

                deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

                results_df = pd.DataFrame(results_data_tuples, columns=['Names','SMILES'])
                results_df['Names'] = results_df['Names'].str[1:]
                results_df['SMILES'] = results_df['SMILES'].str[1:]

                dead_ends_df = pd.DataFrame(deadends_data_tuples, columns=['Names','SMILES'])
                dead_ends_df['Names'] = dead_ends_df['Names'].str[1:]
                dead_ends_df['SMILES'] = dead_ends_df['SMILES'].str[1:]



    #results_df["Content-Disposition"] = "attachment; filename=export.csv"
    #results_df["Content-Type"] = "text/csv"
    #return results_df

        results = results_df.to_csv(r'results_df.csv')
    return Response(results,
                    mimetype="text/csv",
                    headers={"Content-disposition":
                    "attachment; filename=converted_drugs.csv"})


    #dead_ends_df.to_csv(r'dead_ends_df.csv')

    #return render_template('index.html')

for ids in indentifiers :
    if CIRconvert(ids) == 'Did not work':
        dead_ends.append(["Y" + ids, "X" + CIRconvert(ids)])
    else:
        results.append(["Y" + ids, "X" + CIRconvert(ids)])
    return results

results_tagged_names = [i for i in results if i.startswith('Y')]
results_tagged_SMILES = [i for i in results if i.startswith('X')]

deadends_tagged_names = [i for i in dead_ends if i.startswith('Y')]
deadends_tagged_SMILES = [i for i in dead_ends if i.startswith('X')]

results_data_tuples = list(zip(results_tagged_names,results_tagged_SMILES))

deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))
deadends_data_tuples = list(zip(deadends_tagged_names,deadends_tagged_SMILES))

results_df = pd.DataFrame(results_data_tuples, columns=['Names','SMILES'])
results_df['Names'] = results_df['Names'].str[1:]
results_df['SMILES'] = results_df['SMILES'].str[1:]

dead_ends_df = pd.DataFrame(deadends_data_tuples, columns=['Names','SMILES'])
dead_ends_df['Names'] = dead_ends_df['Names'].str[1:]
dead_ends_df['SMILES'] = dead_ends_df['SMILES'].str[1:]

results_end = results_df

return results




#@app.route('/uploaded')
#def upload_file():
#   return render_template('uploaded.html')

#@app.route('/uploader', methods = ['GET', 'POST'])
#def upload_files():
#   if request.method == 'POST':
#      f = request.files['file']
#      f.save(secure_filename(f.filename))
#      return 'file uploaded successfully'

if __name__ == '__main__':
   app.run(debug = True)
