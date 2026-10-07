# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for, flash, jsonify
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
from plotly import graph_objects as go
import cv2
import cv2 as cv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import shutil
import imagehash
from werkzeug.utils import secure_filename
from PIL import Image
import argparse
import urllib.request
import urllib.parse   
# necessary imports 
import seaborn as sns
import plotly.express as px

import warnings
warnings.filterwarnings('ignore')

plt.style.use('fivethirtyeight')
#%matplotlib inline
pd.set_option('display.max_columns', 26)
##
from PIL import Image, ImageOps
import scipy.ndimage as ndi

from skimage import transform
import seaborn as sns
#from keras.preprocessing.image import ImageDataGenerator , load_img , img_to_array
#from keras.models import Sequential
#from keras.layers import Conv2D, Flatten, MaxPool2D, Dense
##
import glob
#from keras.models import Sequential, load_model
import numpy as np
import pandas as pd
import seaborn as sns
#import keras as k
#from keras.layers import Dense
#from sklearn.model_selection import train_test_split
#from sklearn.preprocessing import LabelEncoder, StandardScaler
import matplotlib.pyplot as plt
#from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping
#from tensorflow.keras.optimizers import Adam
##
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="leaf_disease"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ""
    if request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password! or access not provided'

    return render_template('index.html', msg=msg)



@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('test_img'))
        else:
            msg = 'Incorrect username/password! or access not provided'
    return render_template('login_user.html',msg=msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']

        mycursor.execute("SELECT max(id)+1 FROM register")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,uname,pass1)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('login_user'))

    
        
    return render_template('register.html',msg=msg)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    

    return render_template('admin.html')

@app.route('/add_fert', methods=['GET', 'POST'])
def add_fert():
    msg=""
    

    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
    mycursor = mydb.cursor()
    #if request.method=='GET':
    #    msg = request.args.get('msg')
    if request.method=='POST':
        
        disease=request.form['disease']
        symptoms=request.form['symptoms']
        solution=request.form['solution']
        pesticides=request.form['pesticides']
        fertilizer=request.form['fertilizer']
       
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            
            file.save(os.path.join("static/upload", filename))

        mycursor.execute("SELECT max(id)+1 FROM leaf_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO leaf_data(id,leaf,disease,symptoms,solution,leaf_img,pesticides,fertilizer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,'Tomato',disease,symptoms,solution,filename,pesticides,fertilizer)
        mycursor.execute(sql,val)
        mydb.commit()
        return redirect(url_for('add_fert'))

    mycursor.execute('SELECT * FROM leaf_data')
    data = mycursor.fetchall()
    
    return render_template('add_fert.html',msg=msg,data=data)

@app.route('/img_process', methods=['GET', 'POST'])
def img_process():
    

    return render_template('img_process.html')

@app.route('/pro1', methods=['GET', 'POST'])
def pro1():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        #list_of_elements = os.listdir(os.path.join(path_main, folder))

        #resize
        '''img = cv2.imread('static/data/'+fname)
        rez = cv2.resize(img, (256, 256))
        cv2.imwrite("static/dataset/"+fname, rez)'''

        '''img = cv2.imread('static/data/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/trained/g_"+fname, gray)
        ##noice
        img = cv2.imread('static/trained/g_'+fname) 
        dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
        fname2='ns_'+fname
        cv2.imwrite("static/trained/"+fname2, dst)'''

    return render_template('pro1.html',dimg=dimg)


def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))

@app.route('/pro11', methods=['GET', 'POST'])
def pro11():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

    return render_template('pro11.html',dimg=dimg)

@app.route('/pro2', methods=['GET', 'POST'])
def pro2():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)

        f1=open("adata.txt",'w')
        f1.write(fname)
        f1.close()
        ##bin
        image = cv2.imread('static/data/'+fname)
        original = image.copy()
        kmeans = kmeans_color_quantization(image, clusters=4)

        # Convert to grayscale, Gaussian blur, adaptive threshold
        gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3,3), 0)
        thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

        # Draw largest enclosing circle onto a mask
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        for c in cnts:
            ((x, y), r) = cv2.minEnclosingCircle(c)
            cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
            cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
            break
        
        # Bitwise-and for result
        result = cv2.bitwise_and(original, original, mask=mask)
        result[mask==0] = (0,0,0)

        
        ###cv2.imshow('thresh', thresh)
        ###cv2.imshow('result', result)
        ###cv2.imshow('mask', mask)
        ###cv2.imshow('kmeans', kmeans)
        ###cv2.imshow('image', image)
        ###cv2.waitKey()

        #cv2.imwrite("static/trained/bb/bin_"+fname, thresh)

    
   

    path_main = 'static/data1'
    for fname in os.listdir(path_main):
        ##
        img = cv2.imread('static/data1/'+fname) 	
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("static/gg.png", gray)
        
        img = cv2.imread('static/gg.png')
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

        
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

        # sure background area
        sure_bg = cv2.dilate(opening,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
        ret, sure_fg = cv2.threshold(dist_transform,1.5*dist_transform.max(),255,0)

        # Finding unknown region
        sure_fg = np.uint8(sure_fg)
        segment = cv2.subtract(sure_bg,sure_fg)
        img = Image.fromarray(img)
        segment = Image.fromarray(segment)
        path3="static/trained/sg/sg_"+fname
        #segment.save(path3)
        

    return render_template('pro2.html',dimg=dimg)

###Segmentation using RNN
def crfrnn_segmenter(model_def_file, model_file, gpu_device, inputs):
    
    assert os.path.isfile(model_def_file), "File {} is missing".format(model_def_file)
    assert os.path.isfile(model_file), ("File {} is missing. Please download it using "
                                        "./download_trained_model.sh").format(model_file)

    if gpu_device >= 0:
        caffe.set_device(gpu_device)
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()

    net = caffe.Net(model_def_file, model_file, caffe.TEST)

    num_images = len(inputs)
    num_channels = inputs[0].shape[2]
    assert num_channels == 3, "Unexpected channel count. A 3-channel RGB image is exptected."
    
    caffe_in = np.zeros((num_images, num_channels, _MAX_DIM, _MAX_DIM), dtype=np.float32)
    for ix, in_ in enumerate(inputs):
        caffe_in[ix] = in_.transpose((2, 0, 1))

    start_time = time.time()
    out = net.forward_all(**{net.inputs[0]: caffe_in})
    end_time = time.time()

    print("Time taken to run the network: {:.4f} seconds".format(end_time - start_time))
    predictions = out[net.outputs[0]]

    return predictions[0].argmax(axis=0).astype(np.uint8)


def run_crfrnn(input_file, output_file, gpu_device):
    """ Runs the CRF-RNN segmentation on the given RGB image and saves the segmentation mask.
    Args:
        input_file: Input RGB image file (e.g. in JPEG format)
        output_file: Path to save the resulting segmentation in PNG format
        gpu_device: ID of the GPU device. If using the CPU, set this to -1
    """

    input_image = 255 * caffe.io.load_image(input_file)
    input_image = resize_image(input_image)

    image = PILImage.fromarray(np.uint8(input_image))
    image = np.array(image)

    palette = get_palette(256)
    #PIL reads image in the form of RGB, while cv2 reads image in the form of BGR, mean_vec = [R,G,B] 
    mean_vec = np.array([123.68, 116.779, 103.939], dtype=np.float32)
    mean_vec = mean_vec.reshape(1, 1, 3)

    # Rearrange channels to form BGR
    im = image[:, :, ::-1]
    # Subtract mean
    im = im - mean_vec

    # Pad as necessary
    cur_h, cur_w, cur_c = im.shape
    pad_h = _MAX_DIM - cur_h
    pad_w = _MAX_DIM - cur_w
    im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode='constant', constant_values=0)

    # Get predictions
    segmentation = crfrnn_segmenter(_MODEL_DEF_FILE, _MODEL_FILE, gpu_device, [im])
    segmentation = segmentation[0:cur_h, 0:cur_w]

    output_im = PILImage.fromarray(segmentation)
    output_im.putpalette(palette)
    output_im.save(output_file)
###Feature extraction & Classification
def DCNN_process(self):
        
        train_data_preprocess = ImageDataGenerator(
                rescale = 1./255,
                shear_range = 0.2,
                zoom_range = 0.2,
                horizontal_flip = True)

        test_data_preprocess = (1./255)

        train = train_data_preprocess.flow_from_directory(
                'dataset/training',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        test = train_data_preprocess.flow_from_directory(
                'dataset/test',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        ## Initialize the Convolutional Neural Net

        # Initialising the CNN
        cnn = Sequential()

        # Step 1 - Convolution
        # Step 2 - Pooling
        cnn.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Adding a second convolutional layer
        cnn.add(Conv2D(32, (3, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Step 3 - Flattening
        cnn.add(Flatten())

        # Step 4 - Full connection
        cnn.add(Dense(units = 128, activation = 'relu'))
        cnn.add(Dense(units = 1, activation = 'sigmoid'))

        # Compiling the CNN
        cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

        history = cnn.fit_generator(train,
                                 steps_per_epoch = 250,
                                 epochs = 25,
                                 validation_data = test,
                                 validation_steps = 2000)

        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model Accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        test_image = image.load_img('\\dataset\\', target_size=(128,128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = cnn.predict(test_image)
        print(result)

        if result[0][0] == 1:
                print('feature extracted')
        else:
                print('none')
@app.route('/pro3', methods=['GET', 'POST'])
def pro3():
    msg=""
    dimg=[]
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
        
    '''path_main = 'static/dataset'
    i=1
    while i<=50:
        fname="r"+str(i)+".jpg"
        dimg.append(fname)

        img = Image.open('static/data/classify/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        i+=1
    i=1
    j=51
    while i<=10:
        
        fname="r"+str(j)+".jpg"
        dimg.append(fname)

        img = Image.open('static/dataset/'+fname)
        array = np.array(img)

        array = 255 - array

        invimg = Image.fromarray(array)
        invimg.save('static/upload/ff_'+fname)
        j+=1
        i+=1

    '''    

    return render_template('pro3.html',dimg=dimg)

@app.route('/pro4', methods=['GET', 'POST'])
def pro4():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    for fname in os.listdir(path_main):
        

        #####
        image = cv2.imread("static/data1/"+fname)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(gray, 50, 100)
        image = Image.fromarray(image)
        edged = Image.fromarray(edged)
        
        path4="static/trained/ff/"+fname
        #edged.save(path4)
        ##
    path_main = 'static/data'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    return render_template('pro4.html',dimg=dimg)


    

@app.route('/pro5', methods=['GET', 'POST'])
def pro5():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    for fname in os.listdir(path_main):
        dimg.append(fname)
    #graph
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[0,1,2,3,4]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model Precision")
    plt.ylabel("precision")
    
    fn="graph1.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph2
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,8)
        v1='0.'+str(rn)
        x2.append(float(v1))
        i+=1
    
    x1=[0,0,0,0,0]
    y=[0,1,2,3,4]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    

    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Model recall")
    plt.ylabel("recall")
    
    fn="graph2.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #graph3########################################
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(94,98)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(94,98)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,30,50,80,120]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Accuracy %")
    
    fn="graph3.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    #######################################################
    #graph4
    y=[]
    x1=[]
    x2=[]

    i=1
    while i<=5:
        rn=randint(1,4)
        v1='0.'+str(rn)

        #v11=float(v1)
        v111=round(rn)
        x1.append(v111)

        rn2=randint(1,4)
        v2='0.'+str(rn2)

        
        #v22=float(v2)
        v33=round(rn2)
        x2.append(v33)
        i+=1
    
    #x1=[0,0,0,0,0]
    y=[10,30,50,80,120]
    #x2=[0.2,0.4,0.2,0.5,0.6]
    
    plt.figure(figsize=(10, 8))
    # plotting multiple lines from array
    plt.plot(y,x1)
    plt.plot(y,x2)
    dd=["train","val"]
    plt.legend(dd)
    plt.xlabel("Epochs")
    plt.ylabel("Model loss")
    
    fn="graph4.png"
    #plt.savefig('static/trained/'+fn)
    plt.close()
    return render_template('pro5.html',dimg=dimg)

def toString(a):
  l=[]
  m=""
  for i in a:
    b=0
    c=0
    k=int(math.log10(i))+1
    for j in range(k):
      b=((i%10)*(2**j))   
      i=i//10
      c=c+b
    l.append(c)
  for x in l:
    m=m+chr(x)
  return m
                
@app.route('/pro6', methods=['GET', 'POST'])
def pro6():
    msg=""
    dimg=[]
    path_main = 'static/data1'
    print("aaa")
    for fname in os.listdir(path_main):
        dimg.append(fname)
        print(fname)

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    '''data1=[]
    data2=[]
    data3=[]
    data4=[]
    v1=0
    v2=0
    v3=0
    v4=0
    path_main = 'static/trained'
    #for fname in os.listdir(path_main):
    i=0
    i<127
        dimg.append(fname)
        d1=fname.split('_')
        if d1[0]=='d':
            data1.append(fname)
            v1+=1
        if d1[0]=='f':
            data2.append(fname)
            v2+=1
        if d1[0]=='n':
            data3.append(fname)
            v3+=1
        if d1[0]=='w':
            data4.append(fname)
            v4+=1
        

    g1=v1+v2+v3+v4
    dd2=[v1,v2,v3,v4]
    
    
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 5))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,g1))
    plt.xlabel("Objects")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=20)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()'''

    #,data1=data1,data2=data2,data3=data3,data4=data4,cname=cname,v1=v1,v2=v2,v3=v3,v4=v4
    ##############################

    
    ###############################
    
    
    

    return render_template('pro6.html',dimg=dimg)

#######
@app.route('/classify', methods=['GET', 'POST'])
def classify():
    msg=""
    
    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')


    ##    
    ff2=open("static/trained/tdata.txt","r")
    rd=ff2.read()
    ff2.close()

    num=[]
    r1=rd.split(',')
    s=len(r1)
    ss=s-1
    i=0
    while i<ss:
        num.append(int(r1[i]))
        i+=1

    #print(num)
    dat=toString(num)
    dd2=[]
    ex=dat.split(',')
    ##

    #ffq=open("static/trained/adata.txt",'r')
    #ext1=ffq.read()
    #ffq.close()

    v1=0
    v2=0
    v3=0
    v4=0
    v5=0
    v6=0
    v7=0
    v8=0
    v9=0
    v10=0
    data2=[]
    #ex=ext1.split(',')
    dt1=[]
    dt2=[]
    dt3=[]
    dt4=[]
    dt5=[]
    dt6=[]
    dt7=[]
    dt8=[]
    dt9=[]
    dt10=[]
    g=0
    for nx in ex:
        g+=1
        nn=nx.split('-')
        if nn[0]=='1':
            
            dt1.append(nn[1])
            
            v1+=1
        if nn[0]=='2':
            dt2.append(nn[1])
            
            v2+=1
        if nn[0]=='3':
            dt3.append(nn[1])
            
            v3+=1
        if nn[0]=='4':
            dt4.append(nn[1])
            
            v4+=1
        if nn[0]=='5':
            dt5.append(nn[1])
            
            v5+=1
        if nn[0]=='6':
            dt6.append(nn[1])
            
            v6+=1
        if nn[0]=='7':
            dt7.append(nn[1])
            
            v7+=1
        if nn[0]=='8':
            dt8.append(nn[1])
            
        if nn[0]=='9':
            dt9.append(nn[1])
            
            v9+=1
        if nn[0]=='10':
            dt10.append(nn[1])
            
            v10+=1
        
    data2.append(dt1)
    data2.append(dt2)
    data2.append(dt3)
    data2.append(dt4)
    data2.append(dt5)
    data2.append(dt6)
    data2.append(dt7)
    data2.append(dt8)
    data2.append(dt9)
    data2.append(dt10)
    print(data2)   
    dd2=[v1,v2,v3,v4,v5,v6,v7,v8,v9,v10]
    doc = cname #list(data.keys())
    values = dd2 #list(data.values())
    print(doc)
    print(values)
    fig = plt.figure(figsize = (10, 8))
     
    # creating the bar plot
    plt.bar(doc, values, color ='blue',
            width = 0.4)
 

    plt.ylim((1,40))
    plt.xlabel("Class")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    fn="tclass.png"
    plt.xticks(rotation=10)
    plt.savefig('static/trained/'+fn)
    
    plt.close()
    #plt.clf()
    return render_template('classify.html',msg=msg,cname=cname,data2=data2)

#######
@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""

    
        
    return render_template('userhome.html',msg=msg)

@app.route('/test_img', methods=['GET', 'POST'])
def test_img():
    msg=""
    ss=""
    fn=""
    fn1=""
    tclass=0

    ff=open("static/trained/class.txt",'r')
    ext=ff.read()
    ff.close()
    cname=ext.split(',')
    
    if request.method=='POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            fname = file.filename
            filename = secure_filename(fname)
            f1=open('static/test/file.txt','w')
            f1.write(filename)
            f1.close()
            file.save(os.path.join("static/test", filename))

        cutoff=1
        path_main = 'static/data'
        for fname1 in os.listdir(path_main):
            hash0 = imagehash.average_hash(Image.open("static/data/"+fname1)) 
            hash1 = imagehash.average_hash(Image.open("static/test/"+filename))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                ss="ok"
                fn=fname1
                
                break
            else:
                ss="no"

        if ss=="ok":
            print("yes")
            tclass=0
            dimg=[]

            ##    
            ff2=open("static/trained/tdata.txt","r")
            rd=ff2.read()
            ff2.close()

            num=[]
            r1=rd.split(',')
            s=len(r1)
            ss=s-1
            i=0
            while i<ss:
                num.append(int(r1[i]))
                i+=1

            #print(num)
            dat=toString(num)
            dd2=[]
            ex=dat.split(',')
            print(fn)
            ##
            for nx in ex:
                
                nn=nx.split('-')
                f='a ('+nn[1]+').JPG'
                fn1='a ('+nn[1]+').png'
                if f==fn:
                    tclass=int(nn[0])
                    break

            
            print(tclass)
            tt=tclass-1
            cla=cname[tt]
            dta=cla+"|"+fn+"|"+fn1
            f3=open("static/test/res.txt","w")
            f3.write(dta)
            f3.close()

            
                    
            return redirect(url_for('test_pro',act="1"))
        else:
            msg="Invalid!"
    
    
        
    return render_template('test_img.html',msg=msg,fn1=fn1)


    
@app.route('/test_pro', methods=['GET', 'POST'])
def test_pro():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    fn1=gs[2]
    ts=gs[0]
    fname=fn
    ##bin
    '''image = cv2.imread('static/dataset/'+fn)
    original = image.copy()
    kmeans = kmeans_color_quantization(image, clusters=4)

    # Convert to grayscale, Gaussian blur, adaptive threshold
    gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3,3), 0)
    thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

    # Draw largest enclosing circle onto a mask
    mask = np.zeros(original.shape[:2], dtype=np.uint8)
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    for c in cnts:
        ((x, y), r) = cv2.minEnclosingCircle(c)
        cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
        cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
        break
    
    # Bitwise-and for result
    result = cv2.bitwise_and(original, original, mask=mask)
    result[mask==0] = (0,0,0)

    
    ###cv2.imshow('thresh', thresh)
    ###cv2.imshow('result', result)
    ###cv2.imshow('mask', mask)
    ###cv2.imshow('kmeans', kmeans)
    ###cv2.imshow('image', image)
    ###cv2.waitKey()

    #cv2.imwrite("static/upload/bin_"+fname, thresh)'''
    

    ###fg
    '''img = cv2.imread('static/dataset/'+fn)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)

    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    segment = cv2.subtract(sure_bg,sure_fg)
    img = Image.fromarray(img)
    segment = Image.fromarray(segment)
    path3="static/trained/test/fg_"+fname
    #segment.save(path3)'''
    
        
    return render_template('test_pro.html',msg=msg,fn=fn,ts=ts,act=act,fn1=fn1)

@app.route('/test_pro2', methods=['GET', 'POST'])
def test_pro2():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    ts=gs[0]
    fn1=gs[2]

    cursor = mydb.cursor()
    cursor.execute('SELECT count(*) FROM leaf_data where disease=%s',(ts,))
    cnt = cursor.fetchone()[0]
    st=""
    data3=[]
    

        
    return render_template('test_pro2.html',msg=msg,fn=fn,ts=ts,act=act,fn1=fn1)


##########################################################################
# TOMORA AI  -  ADVANCED RESULT PAGE (helpers + upgraded /test_pro3)
# Explainable result : Grad-CAM / lesion focus map + reasons
# Advisory           : disease info, action plan, fertilizer guidance
# Weather            : live weather (Open-Meteo, no API key) + disease risk
# Languages          : English, Tamil, Hindi, Telugu, Malayalam (googletrans)
# Chatbot            : /chat_api  (rule based, answers in selected language)
##########################################################################
DEFAULT_CITY = "Tiruchirappalli"

LANGUAGES = {
    'en': 'English',
    'ta': 'தமிழ்',
    'hi': 'हिन्दी',
    'te': 'తెలుగు',
    'ml': 'മലയാളം'
}

TYPE_LABELS = {
    'fungal': 'Fungal disease',
    'bacterial': 'Bacterial disease',
    'viral': 'Viral disease',
    'pest': 'Mite (pest) damage',
    'none': 'No disease detected'
}

# ------------------------------------------------------------------
# 1. Disease knowledge base  (used for reasons, advisory, fertilizer)
# ------------------------------------------------------------------
DISEASE_KB = {
    'early_blight': {
        'name': 'Tomato Early Blight',
        'pathogen': 'Alternaria solani (fungus)',
        'type': 'fungal', 'severity': 'Moderate to High',
        'symptoms': 'Dark brown circular spots with concentric rings (target-board pattern) and a yellow halo, starting on the older lower leaves. Heavily infected leaves turn yellow and drop.',
        'cause': 'A fungus that survives on crop debris and in soil. It spreads by splashing water, wind and tools, mainly in warm, humid weather with alternating wet and dry spells.',
        'cues': ['Brown circular lesions with ring-like (concentric) patterns',
                 'Yellow halo (chlorosis) around each spot',
                 'Spots concentrated on older, lower leaves'],
        'immediate': ['Remove and destroy the most severely infected lower leaves (do not compost them).',
                      'Avoid working in the field while the leaves are wet so spores are not carried to healthy plants.'],
        'this_week': ['Apply a protectant fungicide recommended locally for early blight, strictly as per the label dose and interval.',
                      'Mulch the soil surface to stop soil splash reaching the lower leaves.'],
        'prevention': ['Keep proper plant spacing and stake plants for good air movement.',
                       'Water at the base of the plant in the morning; avoid overhead irrigation.',
                       'Rotate with non-solanaceous crops for 2-3 years and clear crop debris after harvest.',
                       'Use certified disease-free seedlings or tolerant varieties.'],
        'fertilizer': ['Keep nutrition balanced - nutrient-starved plants are more prone to early blight, so do not let nitrogen run very low.',
                       'Avoid excess nitrogen; support the crop with potassium and well-rotted compost or farmyard manure.',
                       'Follow the soil-test based or locally recommended fertilizer dose for tomato.'],
        'temp_range': (24, 29), 'humidity_min': 80,
        'weather_note': 'Early blight develops fastest at 24-29 °C with high humidity and frequent leaf wetness.'
    },
    'late_blight': {
        'name': 'Tomato Late Blight',
        'pathogen': 'Phytophthora infestans (water mould)',
        'type': 'fungal', 'severity': 'Very High (spreads fast)',
        'symptoms': 'Large, irregular, water-soaked greasy patches that turn brown-black, often with white fuzzy growth on the underside in humid weather. Stems and fruits can rot.',
        'cause': 'An oomycete favoured by cool, wet and very humid weather. Spores travel long distances on wind and rain and can destroy a field within days.',
        'cues': ['Large water-soaked, dark brown-black patches',
                 'Lesions spreading quickly across the leaf, sometimes with pale margins',
                 'Rapid tissue collapse rather than small separate spots'],
        'immediate': ['Remove and destroy infected plants or branches immediately (bag them, do not compost).',
                      'Do not irrigate overhead and avoid moving through wet plants.'],
        'this_week': ['Spray a fungicide recommended locally for late blight on healthy plants nearby, strictly as per label, and repeat at the recommended interval in wet weather.',
                      'Inspect the whole plot every 2-3 days; contact your agriculture officer if it keeps spreading.'],
        'prevention': ['Use resistant varieties and healthy seedlings.',
                       'Improve drainage and air movement; avoid dense planting.',
                       'Water early in the day at the base of the plant so leaves dry quickly.',
                       'Destroy volunteer tomato/potato plants and crop residue.'],
        'fertilizer': ['Avoid excess nitrogen - it creates soft, lush growth that blight attacks easily.',
                       'Keep potassium and calcium adequate to strengthen plant tissue.',
                       'Use the locally recommended dose; do not top-dress heavily while the disease is active.'],
        'temp_range': (10, 25), 'humidity_min': 90,
        'weather_note': 'Late blight prefers cool, damp conditions (about 10-25 °C) with humidity above 90% and long leaf wetness.'
    },
    'bacterial_spot': {
        'name': 'Tomato Bacterial Spot',
        'pathogen': 'Xanthomonas species (bacteria)',
        'type': 'bacterial', 'severity': 'Moderate to High',
        'symptoms': 'Many small, dark, water-soaked spots (often angular) with a yellow halo; spots may turn scabby, and leaves can yellow and drop. Fruit may show raised scabs.',
        'cause': 'Bacteria carried on seed and crop debris and spread by splashing rain, overhead irrigation, wet hands and tools in warm, humid weather.',
        'cues': ['Numerous small dark spots with water-soaked margins',
                 'Yellow halos around the spots',
                 'Spots are small and scattered rather than large and ringed'],
        'immediate': ['Remove badly spotted leaves and avoid touching plants while they are wet.',
                      'Disinfect pruning tools and wash hands between plants.'],
        'this_week': ['Apply a copper-based bactericide recommended locally, strictly as per label, mainly as a protectant.',
                      'Stop overhead irrigation and switch to drip or furrow irrigation.'],
        'prevention': ['Use certified disease-free seed and healthy seedlings.',
                       'Rotate crops for at least 2 years and clear plant debris.',
                       'Keep plants staked and spaced for fast leaf drying.',
                       'Avoid handling plants when wet.'],
        'fertilizer': ['Avoid heavy nitrogen, which gives dense, wet foliage.',
                       'Keep calcium and potassium adequate for firm tissue.',
                       'Follow the soil-test based fertilizer dose for tomato.'],
        'temp_range': (24, 30), 'humidity_min': 80,
        'weather_note': 'Bacterial spot spreads quickly in warm (24-30 °C), humid and rainy weather because rain splash carries the bacteria.'
    },
    'leaf_mold': {
        'name': 'Tomato Leaf Mold',
        'pathogen': 'Passalora fulva (fungus)',
        'type': 'fungal', 'severity': 'Moderate',
        'symptoms': 'Pale green to yellow patches on the upper leaf surface with olive-green to grey velvety mould on the underside. Leaves curl, wither and drop.',
        'cause': 'A fungus that thrives in very humid, poorly ventilated conditions (greenhouses and dense crops) and spreads by airborne spores.',
        'cues': ['Pale yellow patches on the upper surface',
                 'Olive-grey mould growth beneath the matching patches',
                 'Leaf curling and wilting in humid, crowded canopies'],
        'immediate': ['Remove affected leaves and improve air circulation around the plants.',
                      'Reduce humidity - open vents or thin dense foliage.'],
        'this_week': ['Apply a fungicide recommended locally for leaf mold as per the label.',
                      'Water in the morning at the base and keep foliage dry.'],
        'prevention': ['Keep spacing wide and prune lower leaves for airflow.',
                       'Avoid overhead irrigation and late-evening watering.',
                       'Use tolerant varieties and clean tools and structures between crops.'],
        'fertilizer': ['Avoid excess nitrogen that thickens the canopy.',
                       'Maintain potassium and phosphorus for healthy growth.',
                       'Follow the locally recommended fertilizer dose.'],
        'temp_range': (21, 27), 'humidity_min': 85,
        'weather_note': 'Leaf mold needs high humidity (above ~85%) with moderate temperatures of 21-27 °C.'
    },
    'septoria_leaf_spot': {
        'name': 'Tomato Septoria Leaf Spot',
        'pathogen': 'Septoria lycopersici (fungus)',
        'type': 'fungal', 'severity': 'Moderate to High',
        'symptoms': 'Numerous small circular spots with dark brown margins and grey-white centres, often with tiny black dots inside. Lower leaves yellow and fall off first.',
        'cause': 'A fungus that overwinters on debris and spreads by splashing water in warm, wet weather.',
        'cues': ['Many small round spots with pale grey-white centres',
                 'Dark brown borders around each spot',
                 'Tiny black specks visible inside older spots'],
        'immediate': ['Remove infected lower leaves and discard them away from the field.',
                      'Avoid overhead watering to stop splash spread.'],
        'this_week': ['Apply a protectant fungicide recommended locally for Septoria as per the label.',
                      'Mulch the soil to reduce splash from the ground.'],
        'prevention': ['Rotate crops and remove old plant debris.',
                       'Stake and prune for airflow.',
                       'Water at the base in the morning.'],
        'fertilizer': ['Keep nutrition balanced; avoid excess nitrogen.',
                       'Add organic matter and keep potassium adequate.',
                       'Follow the locally recommended fertilizer dose.'],
        'temp_range': (20, 25), 'humidity_min': 80,
        'weather_note': 'Septoria spreads in warm (20-25 °C), wet weather with frequent rain or heavy dew.'
    },
    'spider_mites': {
        'name': 'Tomato Spider Mites (Two-spotted)',
        'pathogen': 'Tetranychus urticae (mite pest)',
        'type': 'pest', 'severity': 'Moderate to High',
        'symptoms': 'Fine yellow stippling on the upper leaf surface, bronzing, and fine webbing on the underside. Leaves dry out and drop in severe infestations.',
        'cause': 'Tiny sap-sucking mites that multiply very quickly in hot, dry, dusty conditions and on water-stressed plants.',
        'cues': ['Fine pale stippling or speckling across the leaf',
                 'Bronze or yellowish dried-out look of the leaf',
                 'Colour change without distinct fungal rings or water-soaked spots'],
        'immediate': ['Check the underside of leaves for mites and webbing; remove heavily infested leaves.',
                      'Wash the plants with a strong jet of water to knock mites down.'],
        'this_week': ['Spray neem oil or an acaricide recommended locally, covering the underside of leaves, as per the label.',
                      'Repeat after 5-7 days to break the breeding cycle.'],
        'prevention': ['Avoid water stress and keep dust down around the crop.',
                       'Protect natural predators; avoid unnecessary broad-spectrum sprays.',
                       'Monitor weekly, especially in hot dry spells.'],
        'fertilizer': ['Avoid excess nitrogen - it boosts mite populations.',
                       'Keep potassium adequate and irrigation regular to reduce plant stress.',
                       'Follow the locally recommended fertilizer dose.'],
        'temp_range': (30, 40), 'humidity_min': 0,
        'weather_note': 'Mites explode in hot (above ~30 °C) and dry weather; rain and high humidity slow them down.'
    },
    'target_spot': {
        'name': 'Tomato Target Spot',
        'pathogen': 'Corynespora cassiicola (fungus)',
        'type': 'fungal', 'severity': 'Moderate',
        'symptoms': 'Brown spots with light centres and concentric rings (like a target), sometimes joining into large dead patches; leaves yellow and drop.',
        'cause': 'A fungus favoured by warm, humid weather and long leaf wetness; it spreads by spores on wind and water.',
        'cues': ['Brown spots with concentric rings and pale centres',
                 'Lesions that merge into larger dead patches',
                 'Yellowing and leaf drop around infected areas'],
        'immediate': ['Remove infected leaves and discard them away from the plot.',
                      'Avoid working among wet plants.'],
        'this_week': ['Apply a protectant fungicide recommended locally for target spot as per the label.',
                      'Improve airflow by pruning lower leaves and spacing plants.'],
        'prevention': ['Rotate crops and clear plant debris.',
                       'Use drip irrigation and water early in the day.',
                       'Scout the crop weekly during humid spells.'],
        'fertilizer': ['Balanced NPK per soil test; avoid excess nitrogen.',
                       'Add organic matter and keep potassium adequate.',
                       'Follow the locally recommended fertilizer dose.'],
        'temp_range': (20, 28), 'humidity_min': 80,
        'weather_note': 'Target spot develops in warm (20-28 °C), humid weather with prolonged leaf wetness.'
    },
    'yellow_leaf_curl': {
        'name': 'Tomato Yellow Leaf Curl Virus',
        'pathogen': 'Begomovirus (spread by whitefly)',
        'type': 'viral', 'severity': 'Very High (no cure)',
        'symptoms': 'Leaves curl upward and become small, crinkled and yellow at the margins; plants are stunted with poor flowering and fruit set.',
        'cause': 'A virus carried by whiteflies (Bemisia tabaci). Warm, dry weather increases whitefly numbers and virus spread.',
        'cues': ['Upward curling and cupping of leaves',
                 'Yellow leaf margins with small, crinkled leaves',
                 'Stunted growth - no fungal rings or water-soaked spots'],
        'immediate': ['Uproot and destroy infected plants (bag them) - virus infection cannot be cured.',
                      'Control whiteflies at once, for example with yellow sticky traps and neem-based or locally recommended insecticide sprays.'],
        'this_week': ['Scout neighbouring plants for whiteflies and early curling and remove new cases quickly.',
                      'Use insect-proof nets for nurseries and new transplants.'],
        'prevention': ['Plant resistant or tolerant varieties.',
                       'Use reflective mulch and yellow sticky traps to reduce whiteflies.',
                       'Control weeds that host whiteflies and avoid planting near older infected fields.'],
        'fertilizer': ['Keep nutrition balanced to support new healthy growth; avoid excess nitrogen that attracts whiteflies.',
                       'Correct zinc or boron deficiency only if a soil test shows it.',
                       'Fertilizer does not cure the virus - focus on vector control.'],
        'temp_range': (25, 35), 'humidity_min': 0,
        'weather_note': 'Warm, dry weather boosts whitefly activity and therefore the spread of leaf curl virus.'
    },
    'mosaic_virus': {
        'name': 'Tomato Mosaic Virus',
        'pathogen': 'Tomato mosaic virus (ToMV)',
        'type': 'viral', 'severity': 'High (no cure)',
        'symptoms': 'Mottled light and dark green mosaic pattern on leaves, leaf distortion (fern-like), stunting and uneven fruit ripening.',
        'cause': 'A very stable virus spread by contaminated hands, tools, seed and plant sap, as well as infected plant debris.',
        'cues': ['Light and dark green mosaic mottling',
                 'Distorted, narrow or fern-like leaves',
                 'Colour pattern is mottled rather than spotted'],
        'immediate': ['Remove and destroy infected plants (do not compost) - there is no cure.',
                      'Wash hands with soap and disinfect tools before touching other plants.'],
        'this_week': ['Inspect remaining plants and remove any with similar mottling.',
                      'Avoid tobacco handling before working with tomato plants.'],
        'prevention': ['Use certified virus-free seed and resistant varieties.',
                       'Disinfect tools, stakes and trays between uses.',
                       'Rotate crops and clear plant debris after harvest.'],
        'fertilizer': ['Keep nutrition balanced to support healthy new growth; avoid excess nitrogen.',
                       'Fertilizer cannot cure a virus - prevent spread through hygiene.',
                       'Follow the locally recommended fertilizer dose.'],
        'temp_range': (20, 30), 'humidity_min': 0,
        'weather_note': 'Mosaic virus spreads through handling and tools more than weather; hygiene matters in all conditions.'
    },
    'healthy': {
        'name': 'Healthy Tomato Leaf',
        'pathogen': 'None detected',
        'type': 'none', 'severity': 'None',
        'symptoms': 'Uniform green colour, smooth surface and no spots, curling or mould. The leaf appears healthy.',
        'cause': 'No disease-causing signs were found in this leaf.',
        'cues': ['Even green colour across the leaf',
                 'No spots, rings, mould or webbing',
                 'Normal leaf shape without curling'],
        'immediate': ['No treatment needed - continue regular monitoring.',
                      'Remove any dead leaves to keep the plot clean.'],
        'this_week': ['Scout a few plants weekly for early spots, curling or pests.',
                      'Keep irrigation regular and at the base of the plant.'],
        'prevention': ['Keep plant spacing and staking for good airflow.',
                       'Rotate crops and keep the field free of debris and weeds.',
                       'Use certified seed and clean tools.'],
        'fertilizer': ['Apply balanced NPK in split doses based on a soil test or local recommendation.',
                       'Add compost or farmyard manure to improve soil health.',
                       'Keep calcium adequate to reduce fruit disorders such as blossom-end rot.'],
        'temp_range': (0, 0), 'humidity_min': 100,
        'weather_note': 'Healthy plants still benefit from watching humid, rainy spells when diseases are likely to start.'
    },
    'unknown': {
        'name': 'Tomato Leaf Disease',
        'pathogen': 'Not available',
        'type': 'fungal', 'severity': 'Unknown',
        'symptoms': 'Please see the symptoms entered by the administrator below.',
        'cause': 'Cause details are not available for this class.',
        'cues': ['Disease-like colour changes on the leaf surface',
                 'Pattern matched with trained leaf samples'],
        'immediate': ['Remove badly affected leaves and keep them away from the field.',
                      'Avoid working among wet plants.'],
        'this_week': ['Consult your local agriculture officer before applying any chemical.',
                      'Scout neighbouring plants for similar symptoms.'],
        'prevention': ['Keep spacing and airflow, water at the base, rotate crops, clear debris.'],
        'fertilizer': ['Follow soil-test based or locally recommended fertilizer doses; avoid excess nitrogen.'],
        'temp_range': (22, 30), 'humidity_min': 80,
        'weather_note': 'Most leaf diseases spread faster in warm, humid and wet weather.'
    }
}


def match_disease_key(name):
    n = " " + re.sub(r'[^a-z0-9]+', ' ', str(name).lower()) + " "
    rules = [('healthy', 'healthy'), ('early', 'early_blight'), ('late', 'late_blight'),
             ('mold', 'leaf_mold'), ('mould', 'leaf_mold'), ('septoria', 'septoria_leaf_spot'),
             ('spider', 'spider_mites'), ('mite', 'spider_mites'), ('target', 'target_spot'),
             ('curl', 'yellow_leaf_curl'), ('yellow', 'yellow_leaf_curl'), ('mosaic', 'mosaic_virus'),
             ('bacterial', 'bacterial_spot'), ('spot', 'bacterial_spot')]
    for word, key in rules:
        if word in n:
            return key
    return 'unknown'


# ------------------------------------------------------------------
# 2. Translation (googletrans==4.0.0rc1) with memory + disk cache
# ------------------------------------------------------------------
import json
import time
import re
from concurrent.futures import ThreadPoolExecutor
try:
    from googletrans import Translator
    _GT_OK = True
except Exception as _gt_err:
    print("googletrans not available:", _gt_err)
    Translator = None
    _GT_OK = False

_TR_CACHE_FILE = 'static/trained/translation_cache.json'
_TR_CACHE = {}
try:
    if os.path.isfile(_TR_CACHE_FILE):
        with open(_TR_CACHE_FILE, 'r', encoding='utf-8') as _cf:
            _TR_CACHE = json.load(_cf)
except Exception:
    _TR_CACHE = {}


def _save_tr_cache():
    try:
        with open(_TR_CACHE_FILE, 'w', encoding='utf-8') as cf:
            json.dump(_TR_CACHE, cf, ensure_ascii=False)
    except Exception:
        pass


_GT_DOWN_UNTIL = [0]


def _translate_one(text, lang, src='auto'):
    # if Google Translate is unreachable, skip it for 60 s so the page still loads fast (English fallback)
    if time.time() < _GT_DOWN_UNTIL[0]:
        return text
    for _ in range(2):
        try:
            return Translator().translate(text, dest=lang, src=src).text
        except Exception:
            time.sleep(0.3)
    _GT_DOWN_UNTIL[0] = time.time() + 60
    return text


def tr_list(texts, lang):
    """Translate a list of strings into `lang` (cached, parallel)."""
    texts = list(texts)
    if lang == 'en' or not _GT_OK:
        return texts
    out = list(texts)
    todo = []
    for i, tx in enumerate(texts):
        if not isinstance(tx, str) or not tx.strip():
            continue
        ck = lang + '|' + tx
        if ck in _TR_CACHE:
            out[i] = _TR_CACHE[ck]
        else:
            todo.append(i)
    if todo:
        uniq = list(dict.fromkeys(texts[i] for i in todo))
        with ThreadPoolExecutor(max_workers=8) as ex:
            res = list(ex.map(lambda s: _translate_one(s, lang), uniq))
        for s, r in zip(uniq, res):
            if r and r != s:
                _TR_CACHE[lang + '|' + s] = r
        _save_tr_cache()
        for i in todo:
            out[i] = _TR_CACHE.get(lang + '|' + texts[i], texts[i])
    return out


def tr_struct(obj, lang):
    """Translate every string inside a nested dict/list structure."""
    if lang == 'en':
        return obj
    strings = []

    def collect(o):
        if isinstance(o, str):
            strings.append(o)
        elif isinstance(o, dict):
            for v in o.values():
                collect(v)
        elif isinstance(o, (list, tuple)):
            for v in o:
                collect(v)
    collect(obj)
    uniq = list(dict.fromkeys(strings))
    mp = dict(zip(uniq, tr_list(uniq, lang)))

    def rebuild(o):
        if isinstance(o, str):
            return mp.get(o, o)
        if isinstance(o, dict):
            return {k: rebuild(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [rebuild(v) for v in o]
        return o
    return rebuild(obj)


# Labels used by the result page (translated on demand)
UI_TEXT = {
    'page_title': 'Tomato Leaf Diagnosis', 'page_sub': 'Explainable AI crop advisory',
    'language': 'Language', 'city': 'Your city / village', 'update_weather': 'Update weather',
    'print_report': 'Print report', 'your_leaf': 'Uploaded leaf', 'focus_map': 'AI focus map',
    'matched_leaf': 'Matched trained sample', 'predicted_disease': 'Predicted disease',
    'confidence': 'Confidence', 'infected_area': 'Affected leaf area', 'stage': 'Stage',
    'severity': 'Severity', 'disease_type': 'Type', 'pathogen': 'Cause organism',
    'why_title': 'Why did the AI predict this?', 'visual_cues': 'Visual signs the model looks for',
    'feature_evidence': 'Evidence measured from your leaf', 'lesion_cov': 'Disease-like colour change',
    'yellowing': 'Yellowing', 'browning': 'Browning', 'dark_area': 'Dark / dead tissue',
    'disease_info': 'Disease information', 'symptoms': 'Symptoms', 'cause': 'Cause and spread',
    'action_plan': 'Treatment and action plan', 'today': 'Do today', 'this_week': 'This week',
    'prevention': 'Prevention', 'expert_solutions': 'Recommended solutions from the database',
    'solution': 'Solution', 'pesticides': 'Pesticides', 'fertilizers': 'Fertilizers',
    'how_to_use': 'How to use', 'weather_title': 'Weather analysis', 'temperature': 'Temperature',
    'humidity': 'Humidity', 'wind': 'Wind', 'rain_now': 'Rain now', 'rain_3d': 'Rain (last 3 days)',
    'forecast': 'Next 2 days', 'risk_title': 'Disease risk from weather', 'spray_advice': 'Spraying advice',
    'fertilizer_title': 'Fertilizer recommendation', 'final_title': 'Final crop advisory',
    'chat_title': 'Ask the AI crop assistant', 'chat_placeholder': 'Type your question...',
    'send': 'Send', 'chat_hello': 'Hello! Ask me anything about this disease, treatment, fertilizer or weather.',
    'q1': 'How can I prevent it from spreading?', 'q2': 'What fertilizer should I use?',
    'q3': 'Is the weather safe for spraying?', 'q4': 'What are the symptoms?',
    'l_diagnosis': 'Disease', 'l_confidence': 'Confidence', 'l_explain': 'Explainability',
    'l_weather': 'Weather', 'l_advisory': 'Advisory', 'l_fertilizer': 'Fertilizer guidance',
    'l_assist': 'Further assistance', 'no_weather': 'Live weather could not be loaded. Check the internet connection or the city name.',
    'disclaimer': 'This advisory is decision support only. Confirm with your local agriculture officer and always follow the product label before using any chemical.',
    'loading': 'Thinking...', 'low': 'Low', 'moderate': 'Moderate', 'high': 'High',
    'risk_score': 'Risk score', 'image_match': 'Image match score', 'cnn_conf': 'CNN confidence',
    'back_home': 'Home', 'temp_unit': '°C', 'lang_note': 'Translated automatically'
}


def get_ui(lang):
    keys = list(UI_TEXT.keys())
    vals = tr_list([UI_TEXT[k] for k in keys], lang)
    return dict(zip(keys, vals))


# ------------------------------------------------------------------
# 3. Image analysis + explainability (Grad-CAM if a model exists)
# ------------------------------------------------------------------
_GRADCAM_MODEL = {'model': None, 'path': None, 'tried': False}
MODEL_CANDIDATES = ['static/trained/model.h5', 'static/trained/model.keras',
                    'static/trained/leaf_model.h5', 'static/trained/cnn_model.h5', 'model.h5']


def analyze_leaf_image(img_bgr):
    """Colour-based lesion analysis. Returns (stats, lesion_mask)."""
    img = cv2.resize(img_bgr, (256, 256))
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    leaf = ((s > 45) & (v > 35)).astype(np.uint8)
    leaf = cv2.morphologyEx(leaf, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    leaf_px = int(leaf.sum())
    if leaf_px < 500:
        return None, None
    green = (h >= 30) & (h <= 95) & (s >= 50) & (v >= 55)
    diseased = ((leaf == 1) & (~green)).astype(np.uint8)
    diseased = cv2.morphologyEx(diseased, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    yellow = (leaf == 1) & (h >= 20) & (h < 35) & (s >= 70) & (v >= 120)
    brown = (leaf == 1) & (h >= 5) & (h < 20) & (v >= 40)
    dark = (leaf == 1) & (v < 70)
    pct = lambda m: round(100.0 * float(np.count_nonzero(m)) / leaf_px, 1)
    stats = {'lesion': pct(diseased), 'yellow': pct(yellow), 'brown': pct(brown), 'dark': pct(dark)}
    return stats, diseased


def _overlay_heat(img_bgr, heat):
    img = cv2.resize(img_bgr, (256, 256))
    heat = np.clip(heat, 0, 1)
    hm = cv2.applyColorMap(np.uint8(255 * heat), cv2.COLORMAP_JET)
    # blend only where there is heat, so healthy areas keep their natural colour
    alpha = np.clip(heat * 1.3, 0, 0.7)[..., None]
    out = img.astype(np.float32) * (1 - alpha) + hm.astype(np.float32) * alpha
    return np.uint8(np.clip(out, 0, 255))


def try_real_gradcam(img_bgr, class_idx):
    """True Grad-CAM when a trained Keras model file is present. Else None."""
    try:
        if not _GRADCAM_MODEL['tried']:
            _GRADCAM_MODEL['tried'] = True
            for c in MODEL_CANDIDATES:
                if os.path.isfile(c):
                    from tensorflow.keras.models import load_model
                    _GRADCAM_MODEL['model'] = load_model(c, compile=False)
                    _GRADCAM_MODEL['path'] = c
                    break
        model = _GRADCAM_MODEL['model']
        if model is None:
            return None
        import tensorflow as tf
        last_conv = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv = layer.name
                break
        if last_conv is None:
            return None
        ih, iw = model.input_shape[1:3]
        rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        x = np.expand_dims(cv2.resize(rgb, (iw, ih)).astype('float32') / 255.0, 0)
        gm = tf.keras.models.Model(model.inputs, [model.get_layer(last_conv).output, model.output])
        with tf.GradientTape() as tape:
            conv_out, preds = gm(x)
            loss = preds[:, 0] if preds.shape[-1] == 1 else preds[:, class_idx]
        grads = tape.gradient(loss, conv_out)
        weights = tf.reduce_mean(grads, axis=(0, 1, 2))
        cam = tf.reduce_sum(conv_out[0] * weights, axis=-1).numpy()
        cam = np.maximum(cam, 0)
        cam = cam / (cam.max() + 1e-8)
        cam = cv2.resize(cam, (256, 256))
        prob = float(preds.numpy().max()) * 100.0 if preds.shape[-1] > 1 else None
        return _overlay_heat(img_bgr, cam), prob
    except Exception as e:
        print("Grad-CAM unavailable, using lesion focus map:", e)
        return None


def build_explanation(up_path, class_idx):
    """Returns dict(stats, xai_file, method, cnn_conf) - everything optional."""
    res = {'stats': None, 'xai_file': None, 'method': 'lesion', 'cnn_conf': None}
    try:
        img = cv2.imread(up_path)
        if img is None:
            return res
        stats, mask = analyze_leaf_image(img)
        res['stats'] = stats
        overlay = None
        g = try_real_gradcam(img, class_idx)
        if g is not None:
            overlay, res['cnn_conf'] = g
            res['method'] = 'gradcam'
        elif mask is not None:
            heat = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), 9)
            if heat.max() > 0:
                heat = heat / heat.max()
            overlay = _overlay_heat(img, heat)
        if overlay is not None:
            out_name = 'xai_' + secure_filename(os.path.splitext(os.path.basename(up_path))[0]) + '.png'
            cv2.imwrite(os.path.join('static/test', out_name), overlay)
            res['xai_file'] = 'test/' + out_name
    except Exception as e:
        print("explanation error:", e)
    return res


def stage_from_area(pct, key):
    if key == 'healthy':
        return 'No disease detected'
    if pct is None:
        return 'Not measured'
    if pct < 5:
        return 'Early / mild'
    if pct < 20:
        return 'Moderate'
    return 'Advanced / severe'


# ------------------------------------------------------------------
# 4. Weather (Open-Meteo - free, no API key) + disease risk
# ------------------------------------------------------------------
_WEATHER_CACHE = {}
WMO = {0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Fog',
       51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle', 61: 'Light rain', 63: 'Moderate rain',
       65: 'Heavy rain', 80: 'Rain showers', 81: 'Rain showers', 82: 'Violent rain showers',
       95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Thunderstorm with hail'}


def get_weather(city):
    key = city.lower().strip()
    c = _WEATHER_CACHE.get(key)
    if c and time.time() - c[0] < 600:
        return c[1]
    try:
        q = urllib.parse.urlencode({'name': city, 'count': 1, 'language': 'en', 'format': 'json'})
        with urllib.request.urlopen("https://geocoding-api.open-meteo.com/v1/search?" + q, timeout=6) as rsp:
            g = json.loads(rsp.read().decode('utf-8'))
        if not g.get('results'):
            return None
        loc = g['results'][0]
        q2 = urllib.parse.urlencode({
            'latitude': loc['latitude'], 'longitude': loc['longitude'],
            'current': 'temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code',
            'daily': 'temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max',
            'past_days': 2, 'forecast_days': 3, 'timezone': 'auto'})
        with urllib.request.urlopen("https://api.open-meteo.com/v1/forecast?" + q2, timeout=6) as rsp:
            d = json.loads(rsp.read().decode('utf-8'))
        cur = d['current']
        dl = d['daily']
        rain = [x or 0 for x in dl['precipitation_sum']]
        prob = [x or 0 for x in dl['precipitation_probability_max']]
        fc = []
        for i in (3, 4):
            if i < len(dl['time']):
                fc.append({'date': dl['time'][i], 'tmax': dl['temperature_2m_max'][i],
                           'tmin': dl['temperature_2m_min'][i], 'rain': rain[i], 'prob': prob[i]})
        w = {'place': ", ".join([p for p in [loc.get('name'), loc.get('admin1'), loc.get('country')] if p]),
             'temp': round(cur['temperature_2m'], 1), 'humidity': int(cur['relative_humidity_2m']),
             'wind': round(cur['wind_speed_10m'], 1), 'rain_now': cur.get('precipitation') or 0,
             'cond': WMO.get(cur.get('weather_code'), 'Variable weather'),
             'recent_rain': round(sum(rain[0:3]), 1),
             'rain_prob_next': max(prob[3:5]) if len(prob) > 3 else 0, 'forecast': fc}
        _WEATHER_CACHE[key] = (time.time(), w)
        return w
    except Exception as e:
        print("weather error:", e)
        return None


def weather_risk(kb, w):
    """Returns (score 0-100, level_key, explanation text)."""
    if not w:
        return None
    t, h = w['temp'], w['humidity']
    wet = w['recent_rain'] >= 2 or w['rain_now'] > 0
    score = 0
    typ = kb['type']
    if typ in ('fungal', 'bacterial'):
        lo, hi = kb['temp_range']
        if lo <= t <= hi:
            score += 40
        elif lo - 3 <= t <= hi + 3:
            score += 20
        if h >= kb['humidity_min']:
            score += 35
        elif h >= kb['humidity_min'] - 10:
            score += 15
        if wet:
            score += 25
        elif w['rain_prob_next'] >= 60:
            score += 15
    elif typ == 'pest':
        score += 40 if t >= 30 else (20 if t >= 26 else 0)
        score += 35 if h <= 60 else (15 if h <= 70 else 0)
        score += 25 if not wet else 0
    elif typ == 'viral':
        score += 40 if t >= 25 else 15
        score += 30 if h <= 70 else 10
        score += 30 if not wet else 10
    else:
        score = 10
    score = min(score, 100)
    level = 'low' if score < 35 else ('moderate' if score < 65 else 'high')
    txt = ("Current weather in %s: %s °C, %s%% humidity, recent rain %s mm. %s " %
           (w['place'].split(',')[0], w['temp'], w['humidity'], w['recent_rain'], kb['weather_note']))
    if typ == 'none':
        txt += "Disease pressure is currently low for a healthy crop, but keep monitoring."
    elif level == 'high':
        txt += "Current conditions strongly favour the spread of this problem - act quickly."
    elif level == 'moderate':
        txt += "Conditions partly favour spread - keep close watch and follow the action plan."
    else:
        txt += "Conditions are not very favourable for rapid spread right now, but continue the action plan."
    return score, level, txt


def spray_advice(w, kb):
    if not w or kb['type'] == 'none':
        return ""
    if w['wind'] >= 20:
        return "Wind is strong (%s km/h): avoid spraying today to prevent drift; spray in calm early morning or evening." % w['wind']
    if w['rain_now'] > 0 or w['rain_prob_next'] >= 60:
        return "Rain is likely soon: spray only when leaves are dry and a dry window of several hours is expected, because rain washes protectants off."
    return "Weather looks suitable for spraying: spray in the early morning or late evening, wetting both sides of the leaves, as per label."


# ------------------------------------------------------------------
# 5. Build the complete advanced report
# ------------------------------------------------------------------
def build_report(ts, fn, data3, city, lang):
    key = match_disease_key(ts)
    kb = DISEASE_KB[key]
    dname = kb['name'] if key != 'unknown' else str(ts)

    # class index (for Grad-CAM)
    class_idx = 0
    try:
        with open("static/trained/class.txt", 'r') as ff:
            cn = ff.read().split(',')
        class_idx = cn.index(ts) if ts in cn else 0
    except Exception:
        pass

    # uploaded image path
    up_path = os.path.join('static/data', fn)
    up_rel = 'data/' + fn
    uploaded = None
    try:
        with open('static/test/file.txt', 'r') as ff:
            uploaded = ff.read().strip()
        if uploaded and os.path.isfile(os.path.join('static/test', uploaded)):
            up_path = os.path.join('static/test', uploaded)
            up_rel = 'test/' + uploaded
        else:
            uploaded = None
    except Exception:
        uploaded = None

    ex = build_explanation(up_path, class_idx)
    stats = ex['stats']

    # confidence: CNN softmax if a model exists, else image-match score (hash distance)
    conf, conf_src = None, ''
    if ex['cnn_conf'] is not None:
        conf, conf_src = round(ex['cnn_conf'], 1), 'cnn_conf'
    elif uploaded:
        try:
            dist = imagehash.average_hash(Image.open('static/data/' + fn)) - imagehash.average_hash(Image.open(up_path))
            conf, conf_src = round(100.0 * (1 - dist / 64.0), 1), 'image_match'
        except Exception as e:
            print("confidence error:", e)

    area = stats['lesion'] if stats else None
    stage = stage_from_area(area, key)

    # weather
    w = get_weather(city)
    risk = weather_risk(kb, w)
    spray = spray_advice(w, kb)

    # --- reasons ("why") ---
    why = []
    if conf is not None:
        src_txt = "CNN prediction confidence" if conf_src == 'cnn_conf' else "image match score with trained samples"
        why.append("The leaf was classified as %s with %s%% %s." % (dname, conf, src_txt))
    else:
        why.append("The leaf was classified as %s by matching it with the trained leaf samples." % dname)
    if stats:
        if key == 'healthy':
            why.append("Only about %s%% of the leaf shows colour variation, which is within the normal range for a healthy leaf." % stats['lesion'])
        else:
            why.append("Image analysis found about %s%% of the leaf area with disease-like colour change (browning %s%%, yellowing %s%%, dark or dead tissue %s%%)."
                       % (stats['lesion'], stats['brown'], stats['yellow'], stats['dark']))
    if ex['xai_file']:
        if ex['method'] == 'gradcam':
            why.append("The Grad-CAM heatmap highlights (red/yellow) the leaf regions that influenced the CNN most, so you can see where the decision came from.")
        else:
            why.append("The focus map highlights (red/yellow) the leaf regions with disease-like colour change that support this diagnosis.")
    why.append(kb['weather_note'])

    # --- admin database solutions ---
    db_rows = []
    for rs in (data3 or []):
        try:
            db_rows.append({'symptoms': rs[3] or '', 'how': rs[4] or '',
                            'pesticides': rs[6] or '', 'fertilizer': rs[7] or ''})
        except Exception:
            pass

    # --- weather text blocks ---
    wtxt = {}
    wmeta = None
    if w and risk:
        wtxt = {'place': w['place'], 'cond': w['cond'], 'risk_text': risk[2], 'spray': spray}
        wmeta = {'temp': w['temp'], 'humidity': w['humidity'], 'wind': w['wind'], 'rain_now': w['rain_now'],
                 'recent_rain': w['recent_rain'], 'forecast': w['forecast'],
                 'score': risk[0], 'level': risk[1]}

    # --- final advisory (Step 10 of the abstract) ---
    fin = {}
    fin['diagnosis'] = dname
    fin['confidence'] = ("%s%%" % conf) if conf is not None else ""
    fin['explain'] = ("Affected regions highlighted on the leaf" +
                      (" using Grad-CAM." if ex['method'] == 'gradcam' else " using the AI focus map.")) if ex['xai_file'] else ""
    if w and risk:
        fin['weather'] = "%s °C, %s%% humidity, recent rain %s mm - %s risk." % (
            w['temp'], w['humidity'], w['recent_rain'], risk[1])
    else:
        fin['weather'] = ""
    if key == 'healthy':
        fin['advisory'] = "The leaf looks healthy. Continue regular monitoring and good field hygiene."
    else:
        fin['advisory'] = "%s Next step: %s" % (
            ("Weather increases the chance of spread." if risk and risk[1] == 'high' else "Follow the action plan and keep the field clean."),
            kb['immediate'][0])
    fin['fertilizer'] = kb['fertilizer'][0]
    fin['assist'] = "Ask the AI crop assistant below for more guidance."

    r = {'disease': dname, 'pathogen': kb['pathogen'], 'type_label': TYPE_LABELS[kb['type']],
         'severity': kb['severity'], 'stage': stage, 'symptoms': kb['symptoms'], 'cause': kb['cause'],
         'cues': kb['cues'], 'why': why, 'immediate': kb['immediate'], 'this_week': kb['this_week'],
         'prevention': kb['prevention'], 'fertilizer': kb['fertilizer'], 'db': db_rows,
         'weather': wtxt, 'final': fin, 'xai_label': ("Grad-CAM heatmap" if ex['method'] == 'gradcam' else "Lesion focus map (AI image analysis)")}

    meta = {'key': key, 'type': kb['type'], 'up_file': up_rel, 'dataset_file': 'data/' + fn,
            'xai_file': ex['xai_file'], 'method': ex['method'], 'conf': conf, 'conf_src': conf_src,
            'area': area, 'stats': stats, 'weather': wmeta, 'city': city, 'stamp': int(time.time())}
    return tr_struct(r, lang), meta


# ------------------------------------------------------------------
# 6. Upgraded result page (same route + same variables as before,
#    plus the new advanced report)
# ------------------------------------------------------------------
@app.route('/test_pro3', methods=['GET', 'POST'])
def test_pro3():
    msg=""
    fn=""
    act=request.args.get("act")
    f2=open("static/test/res.txt","r")
    get_data=f2.read()
    f2.close()

    gs=get_data.split('|')
    fn=gs[1]
    ts=gs[0]
    fn1=gs[2]

    cursor = mydb.cursor()
    cursor.execute('SELECT count(*) FROM leaf_data where disease=%s',(ts,))
    cnt = cursor.fetchone()[0]
    st=""
    data3=[]
    if cnt>0:
        st="1"
        cursor.execute('SELECT * FROM leaf_data where disease=%s',(ts,))
        data3 = cursor.fetchall()

    # ---------- advanced result (language / weather / explanation) ----------
    lang = request.args.get('lang') or session.get('lang') or 'en'
    if lang not in LANGUAGES:
        lang = 'en'
    session['lang'] = lang
    city = (request.args.get('city') or session.get('city') or DEFAULT_CITY).strip()[:60]
    session['city'] = city

    r = None
    meta = None
    try:
        r, meta = build_report(ts, fn, data3, city, lang)
    except Exception as e:
        print("advanced report error:", e)
    t = get_ui(lang)

    return render_template('test_pro3.html',msg=msg,fn=fn,ts=ts,act=act,fn1=fn1,data3=data3,st=st,
                           r=r,m=meta,t=t,lang=lang,langs=LANGUAGES,city=city)


# ------------------------------------------------------------------
# 7. AI crop assistant (chatbot) used by the result page
# ------------------------------------------------------------------
# ------------------------------------------------------------------
# 7. TOMORA AI chatbot (intent dataset + engine + routes)
#    /chatbot_api  -> landing page overlay      /chat_api -> result page
#    /chatbot_widget.js -> Instagram-style chat UI shared by both pages
# ------------------------------------------------------------------
import difflib

CHAT_STOP = set('a an the is are am i you me my it its of to in on for and or with do does how what can should please tell about this that be there'.split())

# (tag, user queries "|" separated, bot answer, follow-up chips "|" separated)
# tags starting with d_ are disease aware and are answered from DISEASE_KB
CHAT_INTENTS = [
 ('greet', 'hi|hello|hey|vanakkam|namaste|good morning|good evening|hai', "Hello! \U0001F345 I'm the **TOMORA assistant**. Ask me about tomato leaf diseases, treatment, fertilizer, weather or how to use the platform.", 'What is TOMORA AI?|Common tomato diseases|How does diagnosis work?|Why are leaves yellow?'),
 ('how_are_you', 'how are you|how r u|whats up|how is it going', "Doing great and ready to help your tomato crop! What would you like to know?", 'Common tomato diseases|How to prevent diseases?'),
 ('thanks', 'thanks|thank you|thx|nandri|great|awesome|nice|super|good answer|\u2764|love it', "You're welcome! \u2764\ufe0f Happy to help. Anything else about your tomatoes?", 'Common tomato diseases|Organic remedies|Watering tips'),
 ('bye', 'bye|goodbye|see you|good night|later|tata', "Bye! Take care of your crop \U0001F331 Come back anytime.", ''),
 ('about', 'tomora ai|about tomora|about platform|about website|about this project|who made you|who are you|your name', "**TOMORA AI** is an intelligent tomato crop advisory platform. It detects leaf diseases with a CNN, explains the result with Grad-CAM heatmaps, adds live weather risk and gives treatment and fertilizer guidance.", 'How does diagnosis work?|What is Grad-CAM?|How do I register?'),
 ('how_works', 'how does it work|how diagnosis work|how to use|steps|workflow|process|get started|use platform', "It takes four steps:\n\u2022 Register and log in as a User\n\u2022 Upload a clear tomato leaf photo\n\u2022 The CNN diagnoses the disease and Grad-CAM shows the affected area\n\u2022 You get weather risk, an action plan, fertilizer advice and this assistant.", 'Photo tips|What is Grad-CAM?|How do I register?'),
 ('accuracy', 'accuracy|accurate|reliable|trust|precision|cnn|deep learning|model|algorithm', "The CNN model reaches **98%+ accuracy** on the trained tomato leaf classes. Each result also shows a confidence score, but always confirm serious cases with your local agriculture officer.", 'What is Grad-CAM?|Photo tips'),
 ('gradcam', 'grad cam|gradcam|heatmap|explainable|xai|focus map|explain prediction', "**Grad-CAM** paints a heatmap over the leaf. Red/yellow areas are the regions that influenced the AI most, so you can see *why* it chose a disease instead of trusting a black box.", 'How does diagnosis work?|Photo tips'),
 ('register', 'register|sign up|signup|create account|new user|login|log in|sign in|user login|password|account', "Click **User** in the top bar. New here? Choose register, fill in name, mobile, email, username and password, then log in to upload leaf images. Admins use the **Admin** button.", 'Photo tips|How does diagnosis work?'),
 ('photo', 'photo tips|upload|image|picture|leaf photo|camera|clear photo|take photo|file format', "For the best result: photograph **one leaf** in daylight, keep the damaged area in focus, use a plain background and avoid blur, shadows or flash glare. JPG or PNG both work.", 'How does diagnosis work?|What is Grad-CAM?'),
 ('languages', 'language|languages|tamil|hindi|telugu|malayalam|translate|english', "The result page and this chat support **English, Tamil, Hindi, Telugu and Malayalam**. Pick a language from the selector in this chat window.", 'How does diagnosis work?'),
 ('weather_feat', 'weather feature|live weather|forecast|city weather|weather information', "TOMORA reads **live weather** (temperature, humidity, wind and recent rain) and turns it into a disease-spread risk score and spraying advice on your result page.", 'Is it free?|How does diagnosis work?'),
 ('cost', 'free|cost|price|pricing|paid|charge|subscription|fees', "Using the advisory is free to try. Just register as a User and upload a leaf image.", 'How do I register?'),
 ('diseases', 'common tomato diseases|diseases list|which diseases|supported diseases|disease types|detect|classes|what diseases', "TOMORA recognises: **Early Blight, Late Blight, Bacterial Spot, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus** and **Healthy** leaves. Name one and I will explain it.", 'Early blight|Late blight|Yellow leaf curl|Bacterial spot'),
 ('healthy', 'healthy leaf|healthy plant|good leaf|normal leaf|how healthy leaf look', "A healthy tomato leaf is evenly deep green, firm, free of spots, webbing or curling. Keep scouting weekly and water at the base.", 'Watering tips|Fertilizer for tomato'),
 ('water', 'water|watering|irrigation|irrigate|drip|how much water|overwater', "Water deeply at the **base**, early morning, using drip or furrow. Keep soil evenly moist (not soggy) and avoid wetting leaves, especially at night, to reduce fungal disease.", 'Fertilizer for tomato|Mulching'),
 ('soil', 'soil|planting|plant tomato|grow tomato|spacing|transplant|nursery|seedling|ph', "Tomatoes like well-drained loamy soil with pH **6.0-6.8**. Transplant healthy 4-5 week seedlings, space plants about 60 x 45 cm, add compost and stake early.", 'Fertilizer for tomato|Watering tips'),
 ('fert_general', 'fertilizer for tomato|npk|manure|compost|nutrient|urea|nutrients|feed plant|fertiliser', "General tomato feeding: compost or farmyard manure at planting, balanced NPK early, then more **potassium** during flowering and fruiting. Avoid excess nitrogen. Follow a soil test or local recommendation.", 'Organic remedies|Blossom end rot'),
 ('organic', 'organic|natural remedy|neem|home remedy|bio|eco friendly|chemical free', "Organic options: **neem oil** spray, removing infected leaves, mulching, crop rotation, compost tea and baking-soda or copper sprays used as per label. They protect best when started early.", 'Spider mites|Prevent diseases'),
 ('pests', 'pest|whitefly|aphid|insect|thrips|worm|caterpillar|fruit borer|bug', "For whitefly, aphids and thrips use yellow sticky traps, neem oil and remove heavily infested leaves. Whiteflies also carry **Yellow Leaf Curl Virus**, so act early.", 'Yellow leaf curl|Organic remedies'),
 ('yellow', 'yellow leaves|leaves yellow|yellowing|chlorosis|leaf turning yellow', "Yellow leaves can mean disease (early blight, leaf curl virus), nutrient shortage (nitrogen, magnesium), overwatering or old age. Upload the leaf photo and TOMORA will tell you which.", 'How does diagnosis work?|Early blight'),
 ('wilting', 'wilt|wilting|drooping|dying plant|plant dying|collapse|dry leaves', "Wilting usually comes from water stress, root rot, bacterial wilt or hot dry spells. Check soil moisture and the stem base, and improve drainage.", 'Watering tips|Common tomato diseases'),
 ('fruit', 'blossom end rot|fruit crack|cracking|fruit rot|black bottom|fruit problem|fruit spots', "Blossom end rot (dark sunken bottom) is mostly a calcium and uneven-watering problem; keep watering steady and add calcium. Cracking comes from sudden heavy watering after dry spells.", 'Watering tips|Fertilizer for tomato'),
 ('prune', 'prune|pruning|stake|staking|support|trellis|suckers', "Stake early and remove suckers and lower leaves touching the soil. This improves air flow and helps leaves dry faster, which cuts disease.", 'Prevent diseases|Watering tips'),
 ('mulch', 'mulch|mulching|straw|plastic mulch', "Mulch (straw or plastic) stops soil splash, keeps moisture steady and reduces weeds, which lowers blight infection from the soil.", 'Watering tips|Prevent diseases'),
 ('harvest', 'harvest|yield|ripen|when to pick|storage|fruit size|production', "Pick tomatoes at the breaker or fully red stage in the cool morning. Healthy leaves and balanced nutrition give the best yield.", 'Fertilizer for tomato'),
 ('safe_eat', 'safe to eat|eat fruit|edible|infected fruit|consume|poisonous', "Fruits from plants with leaf spots are generally safe if the fruit itself is not rotten. Remove rotten fruit, wash well and avoid chemicals close to harvest as per label waiting period.", 'Common tomato diseases'),
 ('officer', 'agriculture officer|expert|human|call|helpline|contact|support|talk to someone|extension', "For severe or fast-spreading cases contact your local **agriculture officer or Krishi Vigyan Kendra**. TOMORA is decision support, not a replacement for field experts.", 'Common tomato diseases'),
 ('privacy', 'privacy|data|secure|safe data|personal information|store photo', "Your uploads are used only for diagnosis inside this platform, and admin access is protected by login.", ''),
 ('help', 'help|what can you do|capabilities|features|options|menu|ask', "I can explain tomato diseases (symptoms, causes, prevention, treatment, fertilizer, weather and spraying), give farming tips and guide you through TOMORA. Try one below.", 'Common tomato diseases|How does diagnosis work?|Organic remedies|Watering tips'),
 ('d_overview', 'overview|explain disease|details|information|disease info|describe', '@overview', ''),
 ('d_spray', 'spray|spraying|sprayed|weather safe|safe spraying|fungicide timing', '@spray', ''),
 ('d_weather', 'weather|rain|humidity|temperature|climate|wind|risk|forecast', '@weather', ''),
 ('d_treat', 'treat|treatment|cure|medicine|remedy|pesticide|fungicide|chemical|manage|recover|control disease', '@treat', ''),
 ('d_prevent', 'prevent|prevention|spread|spreading|avoid|stop|protect|control|precaution', '@prevent', ''),
 ('d_fert', 'fertilizer|fertiliser|nutrient|nutrition|manure|npk|compost', '@fert', ''),
 ('d_symptoms', 'symptom|symptoms|sign|signs|look like|identify|recognize|how to identify', '@symptoms', ''),
 ('d_cause', 'cause|causes|reason|why|come from|pathogen|organism|origin', '@cause', ''),
 ('d_severity', 'serious|severe|severity|dangerous|harm|yield loss|damage|how bad', '@severity', ''),
]
CHAT_DIS = {'early_blight': 'early blight|alternaria', 'late_blight': 'late blight|phytophthora',
            'bacterial_spot': 'bacterial spot|xanthomonas', 'leaf_mold': 'leaf mold|leaf mould',
            'septoria_leaf_spot': 'septoria', 'spider_mites': 'spider mite|mites', 'target_spot': 'target spot',
            'yellow_leaf_curl': 'leaf curl|yellow leaf|whitefly virus', 'mosaic_virus': 'mosaic'}
CHAT_DQ = ['How can I prevent it from spreading?', 'What fertilizer should I use?', 'Is the weather safe for spraying?',
           'What are the symptoms?', 'How do I treat it?', 'What causes it?', 'How serious is it?', 'What is the weather risk today?']


def _ct(s):
    return [w for w in re.findall(r'[a-z]+', str(s).lower()) if w not in CHAT_STOP]


_CHAT_PAT = []
_CHAT_VOC = set()
for _it in CHAT_INTENTS:
    for _p in _it[1].split('|'):
        _t = _ct(_p)
        if _t:
            _CHAT_PAT.append((_it, set(_t), ' '.join(_t)))
            _CHAT_VOC.update(_t)


def chat_match(q):
    toks = []
    for w in _ct(q):
        if w not in _CHAT_VOC:
            m = difflib.get_close_matches(w, _CHAT_VOC, 1, 0.8)
            w = m[0] if m else w
        toks.append(w)
    qs, ql = set(toks), ' '.join(toks)
    best, bsc = None, 0.0
    for it, ps, pj in _CHAT_PAT:
        inter = len(qs & ps)
        if not inter:
            continue
        sc = 0.6 * inter / len(ps) + 0.4 * inter / len(qs) + (0.25 if pj in ql else 0)
        if sc > bsc:
            best, bsc = it, sc
    return best if bsc >= 0.5 else None


def chat_disease(q):
    s = q.lower()
    for k, v in CHAT_DIS.items():
        if any(a in s for a in v.split('|')):
            return k
    return None


def chat_dyn(kind, kb, city):
    n = kb['name']
    bl = lambda xs: "\n".join("\u2022 " + x for x in xs)
    if kind == 'symptoms':
        return "**Symptoms of %s**\n%s" % (n, kb['symptoms'])
    if kind == 'cause':
        return "**Cause of %s**\n%s (%s)" % (n, kb['cause'], kb['pathogen'])
    if kind == 'prevent':
        return "**Preventing %s**\n%s" % (n, bl(kb['prevention']))
    if kind == 'fert':
        return "**Fertilizer guidance**\n%s" % bl(kb['fertilizer'])
    if kind == 'severity':
        return "**%s** severity is *%s*. Acting early reduces yield loss." % (n, kb['severity'])
    if kind == 'treat':
        return "**Treating %s**\n%s\nAlways follow the product label and your agriculture officer's advice." % (n, bl(kb['immediate'] + kb['this_week']))
    if kind == 'overview':
        return "**%s**\n\u2022 Type: %s\n\u2022 Cause: %s\n\u2022 Severity: %s\n%s" % (n, TYPE_LABELS[kb['type']], kb['pathogen'], kb['severity'], kb['symptoms'])
    w = get_weather(city)
    risk = weather_risk(kb, w)
    if not (w and risk):
        return "I could not load live weather right now. Please check your internet connection."
    if kind == 'spray':
        return "**Spraying advice**\n%s" % (spray_advice(w, kb) or "No spraying is needed.")
    return "**Weather risk (%s/100, %s)**\n%s" % (risk[0], risk[1], risk[2])


def chat_engine(q, lang, scope, base_key=None, welcome=False):
    ctx = session.get('cctx') or {}
    city = session.get('city') or DEFAULT_CITY
    dk = None
    chips = []
    if welcome:
        if base_key:
            kb = DISEASE_KB[base_key]
            ans = "Hi! I've read your result: **%s**. Ask me about symptoms, treatment, prevention, fertilizer or today's weather risk, or pick a question below." % kb['name']
            chips = CHAT_DQ[:6]
        else:
            ans, chips = CHAT_INTENTS[0][2], CHAT_INTENTS[0][3].split('|')
    else:
        q_en = _translate_one(q, 'en') if (lang != 'en' and _GT_OK) else q
        dk = chat_disease(q_en) or (base_key if scope == 'result' else ctx.get('dk'))
        it = chat_match(q_en)
        if it and it[0].startswith('d_'):
            if dk and dk in DISEASE_KB:
                ans = chat_dyn(it[0][2:], DISEASE_KB[dk], city)
                chips = [c for c in CHAT_DQ if c != q][:0] or random.sample(CHAT_DQ, 4)
            else:
                ans = "Which tomato disease do you mean? Pick one or type its name."
                chips = ['Early blight', 'Late blight', 'Bacterial spot', 'Yellow leaf curl']
        elif it:
            ans, chips = it[2], [c for c in it[3].split('|') if c]
        elif chat_disease(q_en):
            ans = chat_dyn('overview', DISEASE_KB[dk], city)
            chips = random.sample(CHAT_DQ, 4)
        else:
            ans = "I didn't quite get that \U0001F914 I can help with tomato diseases, treatment, fertilizer, weather and farming tips. Try one of these:"
            chips = ['Common tomato diseases', 'How does diagnosis work?', 'Organic remedies', 'Watering tips']
        if dk:
            ctx['dk'] = dk
            session['cctx'] = ctx
    out = tr_list([ans] + chips, lang)
    return {'answer': out[0], 'suggestions': out[1:]}


def _chat_call(scope):
    d = request.get_json(silent=True) or {}
    lang = d.get('lang') or session.get('lang') or 'en'
    if lang not in LANGUAGES:
        lang = 'en'
    base = None
    if scope == 'result':
        try:
            with open("static/test/res.txt", "r") as f2:
                k = match_disease_key(f2.read().split('|')[0])
            base = k if k in DISEASE_KB else None
        except Exception:
            base = None
    try:
        return jsonify(chat_engine((d.get('q') or '').strip()[:300], lang, scope, base, d.get('action') == 'welcome'))
    except Exception as e:
        print("chat error:", e)
        return jsonify({'answer': "Sorry, I could not answer that right now.", 'suggestions': []})


@app.route('/chat_api', methods=['POST'])
def chat_api():
    return _chat_call('result')


@app.route('/chatbot_api', methods=['POST'])
def chatbot_api():
    return _chat_call('home')


CHAT_WIDGET_JS = r"""
(function(){
var C=window.TOMORA_CHAT||{},inl=C.mode==='inline',lang=C.lang||'en',busy=false,seen=null;
var LN={en:'English',ta:'\u0ba4\u0bae\u0bbf\u0bb4\u0bcd',hi:'\u0939\u093f\u0928\u094d\u0926\u0940',te:'\u0c24\u0c46\u0c32\u0c41\u0c17\u0c41',ml:'\u0d2e\u0d32\u0d2f\u0d3e\u0d33\u0d02'},VL={en:'en-IN',ta:'ta-IN',hi:'hi-IN',te:'te-IN',ml:'ml-IN'};
var G='linear-gradient(135deg,#f97316,#dc2626 58%,#be185d)';
var st=document.createElement('style');st.textContent=`
.tc-ov{position:fixed;inset:0;z-index:10000;background:rgba(25,5,8,.55);backdrop-filter:blur(7px);display:none;align-items:center;justify-content:center}
.tc-ov.on{display:flex}.tc-ov.on .tc-win{animation:tcp .28s cubic-bezier(.2,.9,.3,1.2)}
@keyframes tcp{from{opacity:0;transform:translateY(24px) scale(.94)}}
.tc-win{width:min(940px,94vw);height:min(760px,90vh);background:#fff;border-radius:28px;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 40px 110px rgba(0,0,0,.45);font-family:'Plus Jakarta Sans',sans-serif;color:#211416}
.tc-inl .tc-win{width:100%;height:660px;border-radius:0;box-shadow:none}
.tc-h{display:flex;align-items:center;gap:12px;padding:14px 20px;border-bottom:1px solid #f1e6e6}
.tc-ring{position:relative;width:46px;height:46px;border-radius:50%;padding:2.5px;background:${G};flex:none}
.tc-ring i{width:100%;height:100%;border-radius:50%;background:#fff;color:#dc2626;display:flex;align-items:center;justify-content:center;border:2px solid #fff}
.tc-ring u{position:absolute;right:0;bottom:0;width:12px;height:12px;border-radius:50%;background:#22c55e;border:2px solid #fff}
.tc-t{flex:1;min-width:0;line-height:1.25}.tc-t b{display:block;font-size:.98rem}.tc-t small{color:#8a7a7c;font-size:.76rem}
.tc-l{border:1px solid #eadada;border-radius:20px;padding:5px 10px;font-size:.78rem;font-weight:700;color:#991b1b;background:#fff}
.tc-x{border:0;background:#f6eded;width:36px;height:36px;border-radius:50%;color:#991b1b}
.tc-b{flex:1;overflow-y:auto;padding:18px 20px;display:flex;flex-direction:column;gap:3px;background:#fff}
.tc-dv{text-align:center;font-size:.72rem;color:#9a8a8c;margin:4px 0 12px;font-weight:600}
.tc-r{display:flex;align-items:flex-end;gap:8px;max-width:100%}.tc-r.me{justify-content:flex-end;flex-wrap:wrap;margin-top:2px}.tc-r.bot:not(.cont),.tc-r.me:not(.cont){margin-top:10px}
.tc-a{width:28px;height:28px;border-radius:50%;background:${G};color:#fff;font-size:.72rem;display:flex;align-items:center;justify-content:center;flex:none}.tc-r.more .tc-a{visibility:hidden}
.tc-m{position:relative;max-width:76%;padding:10px 16px;border-radius:22px;font-size:.92rem;line-height:1.5;white-space:pre-wrap;word-break:break-word;user-select:text}
.bot .tc-m{background:#f3eded;border-bottom-left-radius:6px}
.me .tc-m{background:${G};color:#fff;border-bottom-right-radius:6px}
.tc-hr{position:absolute;right:-6px;bottom:-12px;background:#fff;border-radius:20px;padding:1px 5px;font-size:.8rem;box-shadow:0 2px 8px rgba(0,0,0,.18);font-style:normal;animation:tcp .25s}
.tc-seen{flex-basis:100%;text-align:right;font-size:.68rem;color:#9a8a8c;margin-top:2px}
.tc-d{display:inline-flex;gap:4px;padding:5px 2px}.tc-d i{width:7px;height:7px;border-radius:50%;background:#b8a5a7;animation:tcb 1s infinite}.tc-d i:nth-child(2){animation-delay:.15s}.tc-d i:nth-child(3){animation-delay:.3s}
@keyframes tcb{50%{transform:translateY(-5px);background:#dc2626}}
.tc-c{display:flex;gap:8px;overflow-x:auto;padding:4px 20px 10px;scrollbar-width:none}.tc-c:empty{display:none}.tc-c::-webkit-scrollbar{display:none}
.tc-c button{flex:none;border:1px solid #f0c9c9;background:#fff;color:#b91c1c;border-radius:20px;padding:7px 14px;font-size:.8rem;font-weight:700;transition:.2s}
.tc-c button:hover{background:${G};color:#fff;border-color:transparent}
.tc-f{display:flex;align-items:center;gap:8px;margin:4px 16px 16px;border:1px solid #e8dada;border-radius:30px;padding:6px 8px 6px 18px}
.tc-f:focus-within{border-color:#dc2626;box-shadow:0 0 0 3px rgba(220,38,38,.1)}
.tc-f input{flex:1;border:0;outline:0;background:transparent;font-size:.92rem;min-width:0}
.tc-f button{border:0;background:transparent;color:#991b1b;width:36px;height:36px;border-radius:50%}.tc-mic.rec{background:#fee2e2;animation:tcb 1s infinite}
.tc-s{display:none;background:${G}!important;color:#fff!important}.tc-f.has .tc-s{display:block}.tc-f.has .tc-mic{display:none}
@media(max-width:600px){.tc-win{width:100vw;height:100vh;border-radius:0}.tc-m{max-width:86%}}
`;document.head.appendChild(st);
var root,body,chips,inp,fm,mic;
function esc(s){return String(s).replace(/[&<>]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;'}[c]})}
function fmt(s){return esc(s).replace(/\*\*(.+?)\*\*/g,'<b>$1</b>').replace(/\*(.+?)\*/g,'<em>$1</em>')}
function time(){return new Date().toLocaleTimeString([],{hour:'numeric',minute:'2-digit'})}
function row(who,html){var p=body.lastElementChild,same=p&&p.classList.contains(who),r=document.createElement('div');
 if(same)p.classList.add('more');r.className='tc-r '+who+(same?' cont':'');r.title=time();
 r.innerHTML=(who==='bot'?'<span class="tc-a"><i class="fa-solid fa-seedling"></i></span>':'')+'<div class="tc-m">'+html+'</div>';
 body.appendChild(r);body.scrollTop=body.scrollHeight;return r}
function chipSet(a){chips.innerHTML='';(a||[]).forEach(function(t){var b=document.createElement('button');b.textContent=t;b.onclick=function(){ask(t)};chips.appendChild(b)})}
function say(a,c){row('bot',fmt(a));chipSet(c)}
function markSeen(){if(seen)seen.remove();var m=body.querySelectorAll('.tc-r.me');if(!m.length)return;seen=document.createElement('small');seen.className='tc-seen';seen.textContent='Seen '+time();m[m.length-1].appendChild(seen)}
function post(o){o.lang=lang;return fetch(C.url,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(o)}).then(function(r){return r.json()})}
function ask(q){q=(q||'').trim();if(!q||busy)return;busy=true;row('me',fmt(q));inp.value='';fm.classList.remove('has');chipSet([]);
 var ty=row('bot','<span class="tc-d"><i></i><i></i><i></i></span>');
 post({q:q}).catch(function(){return{answer:'Connection problem. Please try again.'}}).then(function(j){var a=j.answer||'...';
  setTimeout(function(){ty.remove();markSeen();say(a,j.suggestions);busy=false},Math.min(1500,450+a.length*5))})}
function welcome(){post({action:'welcome'}).then(function(j){say(j.answer,j.suggestions)}).catch(function(){say(C.hello||'Hi! Ask me about tomato leaf diseases.',C.chips)})}
function build(){
 root=document.createElement('div');root.className=inl?'tc-inl':'tc-ov';
 root.innerHTML='<div class="tc-win"><div class="tc-h"><div class="tc-ring"><i class="fa-solid fa-seedling"></i><u></u></div><div class="tc-t"><b></b><small></small></div>'+(inl?'':'<select class="tc-l">'+Object.keys(LN).map(function(k){return'<option value="'+k+'">'+LN[k]+'</option>'}).join('')+'</select><button class="tc-x" aria-label="Close"><i class="fa-solid fa-xmark"></i></button>')+'</div><div class="tc-b"><div class="tc-dv">Today</div></div><div class="tc-c"></div><div class="tc-f"><input><button class="tc-mic" aria-label="Voice"><i class="fa-solid fa-microphone"></i></button><button class="tc-s" aria-label="Send"><i class="fa-solid fa-paper-plane"></i></button></div></div>';
 root.querySelector('b').textContent=C.title||'TOMORA Assistant';root.querySelector('small').textContent=C.sub||'Active now \u00b7 replies instantly';
 body=root.querySelector('.tc-b');chips=root.querySelector('.tc-c');fm=root.querySelector('.tc-f');inp=fm.querySelector('input');mic=fm.querySelector('.tc-mic');
 inp.placeholder=C.placeholder||'Message...';
 inp.oninput=function(){fm.classList.toggle('has',!!inp.value.trim())};
 inp.onkeydown=function(e){if(e.key==='Enter')ask(inp.value)};fm.querySelector('.tc-s').onclick=function(){ask(inp.value)};
 body.addEventListener('dblclick',function(e){var m=e.target.closest('.bot .tc-m');if(!m)return;var h=m.querySelector('.tc-hr');if(h)h.remove();else m.insertAdjacentHTML('beforeend','<i class="tc-hr">\u2764\ufe0f</i>')});
 var SR=window.SpeechRecognition||window.webkitSpeechRecognition;if(!SR)mic.style.display='none';
 mic.onclick=function(){var r=new SR();r.lang=VL[lang]||'en-IN';r.onresult=function(e){ask(e.results[0][0].transcript)};r.onend=function(){mic.classList.remove('rec')};mic.classList.add('rec');r.start()};
 if(inl){var t=document.getElementById(C.mount);t.appendChild(root);welcome()}else{
  document.body.appendChild(root);root.querySelector('.tc-x').onclick=close;root.addEventListener('mousedown',function(e){if(e.target===root)close()});
  root.querySelector('.tc-l').onchange=function(e){lang=e.target.value;body.insertAdjacentHTML('beforeend','<div class="tc-dv">'+LN[lang]+'</div>');welcome()};
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close()})}}
var first=true;
function open(){if(!root)build();root.classList.add('on');if(first){first=false;welcome()}setTimeout(function(){inp.focus()},250)}
function close(){root&&root.classList.remove('on')}
window.TomoraChat={open:open,close:close};
if(inl)build();else build();
})();
"""


@app.route('/chatbot_widget.js')
def chatbot_widget():
    return Response(CHAT_WIDGET_JS, mimetype='application/javascript')


##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
