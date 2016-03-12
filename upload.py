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
lst_arr=[]

d ={
    'core':
        {
            1:'Dense',
            2:'Activation',
            3:'Dropout'
        },
    'convolutional':
        {
            1:'Convolution2D',
            2:'MaxPooling2D',
            3:'AveragePooling2D'
        }
}

def fill_list():
    for k,v in d.iteritems():
        lst = []
        for ind,val in v.iteritems():
            lst.append((ind,val))
        lst_arr.append(lst)

class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

image = None
tuple_list = []
vtype=[]


# Temporary graph class

class dGraph:

    def __init__(self,vList,eList):
        self.vertices={}
        self.edges={}
        self.vertices[1]='Input'
        self.vertices[2]='Output'
        i=0
        while i<len(vList):
            print "Vertex index:", vList[i]
            print "Layer Type:", i/3+1
            print "Sub-layer:", lst_arr[vList[i+1]-1][vList[i+2]-1][1]
            self.vertices[vList[i]] = lst_arr[vList[i+1]-1][vList[i+2]-1][1]
            i=i+3
        i=0
        while i<len(eList):
            if eList[i] not in self.edges:
                self.edges[eList[i]]=[]
            self.edges[eList[i]].append(eList[i+1])
            i=i+2


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
    vertices = vertices[6:]
    print vertices
    print edges
    myGraph = dGraph(vertices,edges)
    for k,v in myGraph.vertices.iteritems():
        print k,v
    for k,v in myGraph.edges.iteritems():
        print k,v
    return "Success"

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
    return render_template('index.html', cnt=0, uform=uform, image=image,
        lst_arr=lst_arr, plumb="jsPlumb-2.0.7.js",app="app.js",app_css="app.css")

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
    print lst_arr
    app.run(debug=True)
