import os
import time
import imghdr
from flask import Flask, render_template, make_response, redirect, url_for, request, jsonify, json
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

class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

image = None
tuple_list = []

@app.route('/apply', methods=['GET', 'POST'])
def apply():
    uform = UploadForm
    global tuple_list,image
    pipeline_1 = []
    pipeline_2 = []

    vertices = request.form.get('vertices').split(',')
    edges = request.form.get('edges').split(',')
    if u'' in vertices:
        vertices.remove(u'')
    if u'' in edges:
        edges.remove(u'')
    for i in xrange(len(vertices)):
        vertices[i] = int(vertices[i])
    for i in xrange(len(edges)):
        edges[i] = int(edges[i])
    print vertices
    print edges
    # print l, type(l)
    # pipeline_2 = [-1]
    # for _ in l:
    #     pipeline_2.append(int(_))

    # for a,b in tuple_list:
    #     pipeline_1.append(a)

    # print pipeline_1
    # print pipeline_2

    # if pipeline_1 != pipeline_2:
    #     i = 1;
    #     min_len = min(len(pipeline_1),len(pipeline_2))
    #     while i<min_len:
    #         if pipeline_1[i]!=pipeline_2[i]:
    #             break
    #         i=i+1

    #     if i<len(pipeline_1):
    #         j = i
    #         while j<len(pipeline_1):
    #             print "Deleting "+tuple_list[j][1]
    #             os.remove(tuple_list[j][1])
    #             j=j+1
    #         tuple_list = tuple_list[:i]
    #         if i==0:
    #             print "Emptying tuple_list"

    #     while i<len(pipeline_2):
    #         op = lst[pipeline_2[i]][1]
    #         print op
    #         print len(tuple_list)

    #         input_location = os.path.join(app.static_folder, tuple_list[i-1][1])
    #         script_location = os.path.join(app.static_folder, "scripts/"+op+".py")

    #         print "Before: "+input_location

    #         name, ext = os.path.splitext(input_location)
    #         name = name[:name.rfind("_")]
    #         timestamp = time.time()
    #         output_location = name+"_"+str(timestamp)+ext

    #         print "After: "+output_location

    #         call(["python",script_location,input_location,output_location])

    #         tuple_list.append((pipeline_2[i],output_location))

    #         i=i+1

    #     image = tuple_list[-1][1]
    # print "/static/temp/"+image.split("/")[-1]
    return jsonify(result = "/static/temp/"+image.split("/")[-1])


@app.route('/', methods=['GET', 'POST'])
def index():
    global image,tuple_list

    uform = UploadForm()
    print "Redirect successful"

    try:
        if uform.validate_on_submit():
            if hasattr(uform.image_file.data,'filename'):
                for file in os.listdir(app.static_folder+"/temp"):
                    os.remove(app.static_folder+"/temp/"+file)
                fname = uform.image_file.data.filename
                name, ext = os.path.splitext(fname)
                image = 'temp/' + name+"_"+str(time.time())+ext
                tuple_list = [(-1,image)]
                uform.image_file.data.save(os.path.join(app.static_folder, image))
                print "No Exceptions"
    except e:
        print "Exception happened"
        print type(e)
    return render_template('index.html', uform=uform, image=image, lst=lst, plumb="jsPlumb-2.0.7.js",app="app.js",app_css="app.css")

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
