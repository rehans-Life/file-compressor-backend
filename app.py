from flask import Flask,request,send_from_directory
from utils import UPLOAD_COMPRESSED_FILE,UPLOAD_DECOMPRESSED_FILE,UPLOAD_TXT_FILE
import os
from werkzeug.utils import secure_filename
from huffman import huffmanCoding
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

app.config['UPLOAD_COMPRESSED_FILE'] = UPLOAD_COMPRESSED_FILE
app.config['UPLOAD_DECOMPRESSED_FILE'] = UPLOAD_DECOMPRESSED_FILE
app.config['UPLOAD_TXT_FILE'] = UPLOAD_TXT_FILE

@app.route('/compress',methods=['GET','POST'])
def compress():
    
    if request.method == 'POST':
        
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_TXT_FILE'], filename)
        file.save(path)
        
        huffmanCoding.path = path
        huffmanCoding.compression()
        
        return json.dumps({"success":True,"message":'File Successfully Compressed'})
        
    else:
        return json.dumps({"success":False,"message":'Invalid Method'})

@app.route('/decompress/<path:filename>')
def decompress(filename):
    fileName,_ = os.path.splitext(filename)    
    huffmanCoding.decompression(fileName)
        
    return json.dumps({"success":True,"message":'File Successfully Decompressed'})

@app.route('/download/file/<filename>/<type>')
def sendFile(filename,type):
    fileName,_ = os.path.splitext(filename)
    if type == "binary":
        return send_from_directory(app.config['UPLOAD_COMPRESSED_FILE'],path=fileName+'.bin',as_attachment=True)
    else:
        return send_from_directory(app.config['UPLOAD_DECOMPRESSED_FILE'],path=fileName+'_decompressed.txt',as_attachment=True)
        
