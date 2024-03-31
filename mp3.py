from flask import Flask, render_template, request, redirect, url_for, jsonify
import subprocess
import os

app = Flask(__name__, static_url_path='/static')
UPLOAD_FOLDER = 'uploads'

if not os.path.exists(UPLOAD_FOLDER):
os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def index():
mp3_files = os.listdir(UPLOAD_FOLDER)
return render_template('index.html', mp3_files=mp3_files)

@app.route('/upload', methods=['POST'])
def upload():
if 'mp3_file' not in request.files:
return redirect(request.url)

mp3_file = request.files['mp3_file']
if mp3_file.filename == '':
return redirect(request.url)

filename = os.path.join(UPLOAD_FOLDER, mp3_file.filename)
count = 1
while os.path.exists(filename):
base, ext = os.path.splitext(mp3_file.filename)
filename = os.path.join(UPLOAD_FOLDER, f"{base}_{count}{ext}")
count += 1

mp3_file.save(filename)
return redirect(url_for('index'))

@app.route('/play/<filename>')
def play(filename):
try:
filepath = os.path.join(UPLOAD_FOLDER, filename)
subprocess.Popen(['cvlc', filepath])
except Exception as e:
return f'Error: {str(e)}'

return 'Playing {filename}'

@app.route('/list_files')
def list_files():
mp3_files = os.listdir(UPLOAD_FOLDER)
print("MP3 Files:",mp3_files)
return jsonify({"files": mp3_files})

if __name__ == '__main__':
app.run(host='192.168.140.12', port=5000, debug=True)