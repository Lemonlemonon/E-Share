from flask import Flask, request, send_from_directory, render_template
import os
import qrcode
import socket
import webbrowser
import os, sys

app = Flask(__name__)
UPLOAD_FOLDER = "./upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the upload folder if it doesn't exist

@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if file:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename))

    # Display all files in the upload folder
    files = os.listdir(UPLOAD_FOLDER)
    return render_template('upload.html', files=files)

@app.route('/getQRCode')
def getQRCode():
    hostname = socket.gethostname()
    IPAddr = "http://" + socket.gethostbyname(hostname) + ":8888/upload"
    img = qrcode.make(IPAddr)
    img.save('templates/QRCode.png')
    return send_from_directory("./templates", "QRCode.png", as_attachment=True)

def generate_file_preview(file):
    file_url = f"/download/{file}"
    if file.lower().endswith(('png', 'jpg', 'jpeg', 'gif')):
        return f'<a href="{file_url}"><img src="{file_url}" alt="{file}" style="max-height: 100px; max-width: 100px;"></a>'
    else:
        return f'<a href="{file_url}">{file}</a>'
    
@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)

if __name__ == '__main__':
    url = "http://" + socket.gethostbyname(socket.gethostname()) + ":8888/upload"
    webbrowser.open(url)
    app.run(host="0.0.0.0", port=8888)
    
