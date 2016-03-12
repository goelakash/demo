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

#Keras imports and declarations
import numpy as np

import keras
from keras.datasets import mnist
from keras.models import *
from keras.layers import core
from keras.layers.core import *
from keras.layers import convolutional
from keras.layers.convolutional import *
from keras.optimizers import *
from keras.utils import np_utils


batch_size = 128
nb_classes = 10
nb_epoch = 5

(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784)
X_test = X_test.reshape(10000, 784)
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train /= 255
X_test /= 255
Y_train = np_utils.to_categorical(y_train, nb_classes)
Y_test = np_utils.to_categorical(y_test, nb_classes)

app = Flask(__name__)
# mongo = PyMongo(app)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)
lst_arr = []

d = {
    'core':
        {
            1 : 'Dense',
            2 : 'Activation',
            3 : 'Dropout'
        },
    'convolutional':
        {
            1 : 'Convolution2D',
            2 : 'MaxPooling2D',
            3 : 'AveragePooling2D'
        }
}


def fill_list():
    for k,v in d.iteritems():
        lst = []
        for ind,val in v.iteritems():
            lst.append((ind,val))
        lst_arr.append(lst)


def train_and_predict(myGraph):
    start = 1
    model = Sequential()
    input_dim = X_train.shape[1]
    optimizer = RMSprop()
    print input_dim
    count = 512
    p_drop=0.5

    while start!=2:
        to = myGraph.edges[start][0]
        start=to
        print to
        layer_name = myGraph.vertices[to]
        if layer_name!='Dense':
            continue
        print layer_name
        layer_type = ''
        for k,v in d.iteritems():
            for num,name in v.iteritems():
                if name==layer_name:
                    module = getattr(keras.layers,k)
                    layer_type = getattr(module,layer_name)
                    break

        model.add(layer_type(count,input_shape=(input_dim,)))
        if layer_name=='Dropout':
            continue
        model.add(Activation('relu'))

    model.add(Dense(nb_classes))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy', optimizer=optimizer)
    model.fit(X_train, Y_train,
          batch_size=batch_size, nb_epoch=nb_epoch,
          show_accuracy=True, verbose=2,
          validation_data=(X_test, Y_test))
    score = model.evaluate(X_test, Y_test,
                       show_accuracy=True, verbose=0)
    print('Test score:', score[0])
    print('Test accuracy:', score[1])
    return score[1]
    return 1


image = None
tuple_list = []
vtype=[]


# Temporary graph class

class dGraph:

    def __init__(self,vList,eList):
        self.vertices = {}
        self.edges = {}
        self.vertices[1] = 'Input'
        self.vertices[2] = 'Output'
        i = 0
        while i<len(vList):
            print "Vertex index:", vList[i]
            print "Layer Type:", i/3+1
            print "Sub-layer:", lst_arr[vList[i+1]-1][vList[i+2]-1][1]
            self.vertices[vList[i]] = lst_arr[vList[i+1]-1][vList[i+2]-1][1]
            i = i+3
        i = 0
        while i<len(eList):
            if eList[i] not in self.edges:
                self.edges[eList[i]] = []
            self.edges[eList[i]].append(eList[i+1])
            i = i+2


class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    # uform = UploadForm
    # global tuple_list,image
    # pipeline_1 = []
    # pipeline_2 = []

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
    return "Accuracy: " + str(train_and_predict(myGraph)*100) + "%\nEpochs: " + str(nb_epoch)



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
