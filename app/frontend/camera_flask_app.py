from flask import Flask, render_template, Response, request
from flask_mysqldb import MySQL
import cv2
from datetime import date, datetime
import os, sys
import numpy as np
from threading import Thread
import fnmatch, time

global capture, rec_frame, out
capture=0

#make shots directory to save pics
try:
    os.mkdir('./static')
except OSError as error:
    pass

#Load pretrained face detection model    
net = cv2.dnn.readNetFromCaffe('./saved_model/deploy.prototxt.txt', './saved_model/res10_300x300_ssd_iter_140000.caffemodel')

# Muat model
model = load_model('/model/Model_Face_Recognition.h5')

#instatiate flask app  
app = Flask(__name__, template_folder='./templates')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pegawai'
 
mysql = MySQL(app)

camera = cv2.VideoCapture(0)

def record(out):
    global rec_frame
    while(rec):
        time.sleep(0.05)
        out.write(rec_frame)


def detect_face(frame):
    global net
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
        (300, 300), (104.0, 177.0, 123.0))   
    net.setInput(blob)
    detections = net.forward()
    confidence = detections[0, 0, 0, 2]

    if confidence < 0.5:            
            return frame           

    box = detections[0, 0, 0, 3:7] * np.array([w, h, w, h])
    (startX, startY, endX, endY) = box.astype("int")
    try:
        frame=frame[startY:endY, startX:endX]
        (h, w) = frame.shape[:2]
        r = 480 / float(h)
        dim = ( int(w * r), 480)
        frame=cv2.resize(frame,dim)
    except Exception as e:
        pass
    return frame
 

def gen_frames():  # generate frame by frame from camera
    global out, capture, rec_frame, result
    while True:
        success, frame = camera.read() 
        if success:
            if(capture):
                capture=0
                frame= detect_face(frame)
                p = os.path.sep.join(['static', data])
                cv2.imwrite(p, frame)

                # Panggil salah satu data 
                test_image=image.load_img(data,target_size=(150, 150))
                test_image=image.img_to_array(test_image)

                # Prediksi kelas
                test_image=np.expand_dims(test_image,axis=0)
                result=model.predict(test_image,verbose=0)

                check=True
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass


@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/requests',methods=['POST','GET'])
def tasks():
    global switch,camera,data,check,id_pegawai
    if request.method == 'POST':
        if request.form.get('click') == 'Presensi':
            global capture
            today = date.today()
            tanggal_presensi = today.strftime("%Y-%m-%d")
            now = datetime.now()
            waktu_presensi = now.strftime("%H:%M:%S")
            data = "presensi_{}.png".format(str(now).replace(":",'.').replace(" ",'_'))
            check=False
            capture=1
            while(check!=False):
                pass
            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO presensi(id_pegawai, tanggal_presensi, waktu_presensi, berhasil_presensi) VALUES(%s,%s,%s,%s) ''',(id_pegawai,tanggal_presensi,waktu_presensi,1))
            mysql.connection.commit()
            cursor.close()
            pegawai = {
                'id_pegawai': id_pegawai,
                'tanggal_presensi': tanggal_presensi,
                'waktu_presensi': waktu_presensi,
                'data': data
            }
            return render_template('absen.html', **pegawai)

        if request.form.get('presensi-ulang') == 'Presensi Ulang':
            os.remove('./static/'+data)
            data=''
            return render_template('index.html')
                          
    elif request.method=='GET':
        return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()