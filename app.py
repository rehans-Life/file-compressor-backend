from flask import Flask,request,send_from_directory
from utils import UPLOAD_COMPRESSED_FILE,UPLOAD_DECOMPRESSED_FILE,UPLOAD_TXT_FILE
import os
from werkzeug.utils import secure_filename
from huffman import huffmanCoding
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_COMPRESSED_FILE'] = UPLOAD_COMPRESSED_FILE
app.config['UPLOAD_DECOMPRESSED_FILE'] = UPLOAD_DECOMPRESSED_FILE
app.config['UPLOAD_TXT_FILE'] = UPLOAD_TXT_FILE
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

@app.after_request
def handle_options(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-Requested-With"

    return response

@app.route('/compress',methods=['GET','POST'])
@cross_origin()
def compress():
    
    if request.method == 'POST':
        
        file = request.files.get('file')
        filename = secure_filename(file.filename)
        path = os.path.join(app.config['UPLOAD_TXT_FILE'], filename)
        file.save(path)
        
        huffmanCoding.path = path
        huffmanCoding.compression()
        
        return {"success":True,"message":'File Successfully Compressed'}
        
    else:
        return {"success":False,"message":'Invalid Method'}

@app.route('/decompress/<path:filename>')
@cross_origin()
def decompress(filename):
    fileName,_ = os.path.splitext(filename)    
    huffmanCoding.decompression(fileName)
        
    return {"success":True,"message":'File Successfully Decompressed'}

@app.route('/download/file/<filename>/<type>')
@cross_origin()
def sendFile(filename,type):
    fileName,_ = os.path.splitext(filename)
    if type == "binary":
        return send_from_directory(app.config['UPLOAD_COMPRESSED_FILE'],path=fileName+'.bin',as_attachment=True)
    else:
        return send_from_directory(app.config['UPLOAD_DECOMPRESSED_FILE'],path=fileName+'_decompressed.txt',as_attachment=True)
        
