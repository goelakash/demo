import os
import time
import imghdr
from flask import Flask, render_template, make_response, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import Form
# from flask_pymongo import PyMongo
from wtforms import FileField, TextField, SubmitField, SelectField, ValidationError, widgets
from wtforms.validators import Required
from subprocess import call

app = Flask(__name__)
# mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)

lst=[]

def fill_list():
    count = 0
    for file in os.listdir(os.path.join(app.static_folder, "scripts")):
        if file[-2:]=='py':
            lst.append((count,file[:-3]))
            count+=1

class PipelineForm(Form):
    width = TextField('Width')
    height = TextField('Height')
    submit = SubmitField('Final Submit')

class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

image = None
tuple_list = []

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if pform.validate_on_submit():
        global tuple_list,image
        pipeline_1 = []
        #get the pipeline operations
        for a,b in tuple_list:
            pipeline_1.append(a)

        val = request.files['file']
        #conver val to pipeline_2


        if pipeline_1 != pipeline_2:
            i = 0;
            min_len = min(len(pipeline_1),len(pipeline_2))
            while i<min_len:
                if pipeline_1[i]!=pipeline_2[i]:
                    break
                i=i+1

            if i<len(pipeline_1):
                tuple_list = tuple_list[:i]

            while i<len(pipeline_2):
                op = lst[pipeline_2[i]]

                input_location = os.path.join(app.static_folder, tuple_list[i-1][1])
                script_location = os.path.join(app.static_folder, "scripts/"+op+".py")

                print input_location, script_location

                ext = input_location[input_location.rfind('.')+1:]
                timestamp = int(time.time())
                output_location = input_location[:input_location.index('_')+1]+str(timestamp)+"."+ext

                print output_location

                call(["python",script_location,input_location,output_location])
                #get image from db
                #do the operation of pipeline_2[i]
                #store the image at (image_ID with i) location

                # tuple_list.append((pipeline_2[i]),new_img)

                i=i+1
            image = tuple_list[-1][1]


        # if image != None:
            # file_location = os.path.join(app.static_folder, image)
            # script_location = os.path.join(app.static_folder, "scripts/"+pipeline[-1]+".py")
            # print file_location, script_location
            # call(["python",script_location,file_location])
        # else:
        #     pipeline_1=pipeline_2=[]


@app.route('/', methods=['GET', 'POST'])
def index():
    global image,tuple_list
    # pipeline = []

    uform = UploadForm()
    pform = PipelineForm()

    if uform.validate_on_submit():
        if hasattr(uform.image_file.data,'filename'):
            tuple_list = []
            for file in os.listdir(app.static_folder+"/temp"):
                os.remove(app.static_folder+"/temp/"+file)
            image = 'temp/' + uform.image_file.data.filename
            uform.image_file.data.save(os.path.join(app.static_folder, image))

    return render_template('index.html', uform=uform, pform=pform, image=image, tuple_list = tuple_list, lst=lst)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

if __name__ == '__main__':
    fill_list()
    app.run(debug=True)
