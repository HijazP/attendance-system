from flask import Flask, render_template, Response, request
from flask_mysqldb import MySQL
import cv2
from datetime import date, datetime
import os, sys
import numpy as np
from threading import Thread
import fnmatch, time
import keras.utils as image
import tensorflow
from tensorflow import keras
from keras import models
from pipeline.pipeline import new_data

global rec_frame, out, capture, upload_folder, allowed_extensions
capture=0

# Membuat direktori untuk menyimpan foto hasil presensi
try:
    os.mkdir('./static')
except OSError as error:
    pass

# Muat model
model = models.load_model('./model/Model_Face_Recognition.h5', compile=False)

# Inisiasi aplikasi Flask
app = Flask(__name__, template_folder='./templates')

# Koneksi ke basis data
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'pegawai'
 
mysql = MySQL(app)

camera = cv2.VideoCapture(0)
 
# Membangkitkan kamera secara frame by frame
def gen_frames():
    global out, capture, rec_frame, result
    while True:
        success, frame = camera.read() 
        if success:
            if(capture):
                capture=0

                # Menyimpan foto ke direktori 'static'
                p = os.path.sep.join(['static', data])
                cv2.imwrite(p, frame)

                # Panggil salah satu data 
                test_image=image.load_img('./static/'+data,target_size=(150, 150))
                test_image=image.img_to_array(test_image)

                # Prediksi kelas
                test_image=np.expand_dims(test_image,axis=0)
                test_image=test_image / 255.0
                prediction = model.predict(test_image)
                result = np.argmax(prediction)
                print(data)
                print(result)

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

            # Membangkitkan data baru
            data = "presensi_{}.jpg".format(str(now).replace(":",'.').replace(" ",'_'))

            capture=1
            time.sleep(1)

            id_pegawai=result
            nama_pegawai="face"+str(id_pegawai)

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO presensi(id_pegawai, tanggal_presensi, waktu_presensi, berhasil_presensi) VALUES(%s,%s,%s,%s) ''',(id_pegawai,tanggal_presensi,waktu_presensi,1))
            mysql.connection.commit()
            cursor.close()

            pegawai = {
                'id_pegawai': id_pegawai,
                'nama_pegawai': nama_pegawai,
                'tanggal_presensi': tanggal_presensi,
                'waktu_presensi': waktu_presensi,
                'data': data
            }

            return render_template('presensi.html', **pegawai)

        if request.form.get('presensi-ulang') == 'Presensi Ulang':
            # Menghapus foto di direktori 'static'
            os.remove('./static/'+data)
            data=''
            return render_template('index.html')

        if request.form.get('new_data') == 'Pegawai Baru':
            return render_template('pegawai-baru.html')

        if request.form.get('halaman-presensi') == 'Halaman Presensi':
            return render_template('index.html')

        if request.form.get('submit_pegawai_baru') == 'Submit Pegawai Baru':
            next = len(os.listdir('./model/Face Images/Final Training Images/'))+1
            train_folder = './model/Face Images/Final Training Images/'+'face'+str(next)
            test_folder = './model/Face Images/Final Testing Images/'+'face'+str(next)
            os.mkdir(train_folder)
            os.mkdir(test_folder)
            app.config['train_folder'] = train_folder
            app.config['test_folder'] = test_folder
            nama = request.form['nama']
            divisi = request.form['divisi']
            jabatan = request.form['jabatan']

            cursor = mysql.connection.cursor()
            cursor.execute(''' INSERT INTO biodata(id_pegawai, nama_pegawai, divisi_pegawai, jabatan_pegawai) VALUES(%s,%s,%s,%s) ''',(next,nama,divisi,jabatan))
            mysql.connection.commit()
            cursor.close()

            files = request.files.getlist("file")
            for idx, file in enumerate(files):
                if idx < 5:
                    file.save(os.path.join(app.config['train_folder'], file.filename))
                else:
                    file.save(os.path.join(app.config['test_folder'], file.filename))
            new_data()
            return render_template('sukses.html')
                          
    elif request.method=='GET':
        return render_template('index.html')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
    
camera.release()
cv2.destroyAllWindows()