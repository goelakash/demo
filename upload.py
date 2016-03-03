import os
import imghdr
from flask import Flask, render_template
from flask.ext.bootstrap import Bootstrap
from flask.ext.wtf import Form
from wtforms import FileField, SubmitField, SelectField, ValidationError
import cv2
from subprocess import call

app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)

FILE_EXT = ["jpg","jpeg","png"]

lst=[]

def fill_list():
    count = 0
    for file in os.listdir(os.path.join(app.static_folder, "scripts")):
        if file[-2:]=='py':
            lst.append((count,file[:-3]))
            count+=1

class PipelineForm(Form):
    select_op = SelectField('Apply Operation',coerce=int,choices=lst)
    submit = SubmitField('Submit')


class UploadForm(Form):
    image_file = FileField('Image file')
    submit = SubmitField('Submit')

image = None
pipeline = []

@app.route('/', methods=['GET', 'POST'])
def index():
    global image,pipeline

    uform = UploadForm()
    pform = PipelineForm()

    if pform.validate_on_submit():
        operation = pform.select_op.data
        op = lst[operation][1]
        pipeline.append(op)

        file_location = os.path.join(app.static_folder, image)
        script_location = os.path.join(app.static_folder, "scripts/"+pipeline[-1]+".py")
        print file_location, script_location
        call(["python",script_location,file_location])


    if uform.validate_on_submit():
        if hasattr(uform.image_file.data,'filename'):
            pipeline = []
            image = 'temp/' + uform.image_file.data.filename
            uform.image_file.data.save(os.path.join(app.static_folder, image))

    return render_template('index.html', uform=uform, pform=pform, image=image, pipeline = pipeline)


if __name__ == '__main__':
    fill_list()
    app.run(debug=True)
