from flask import Flask,render_template
from flask import request
import base64
import json
from PIL import Image
from torch import var
from yolo import YOLO
from io import BytesIO
#import pymongo
import time
from flask_cors import CORS
#client = pymongo.MongoClient(host="localhost",port=27017)
# from database import *
# from againstspider import *

yolo = YOLO(image=True)


def base64_to_bytes(input_):
	base = input_.split(",")[-1].encode("utf-8")
	return base64.b64decode(base)

def detect_img(yolo,image):
    r_image,result = yolo.detect_image(image)
    return result

app = Flask(__name__)
CORS(app)
@app.route("/recognize",methods=["POST","GET"])
def roc():
	
		if request.method == "POST":
			t= name = request.form["name"]
			# if not eval(request.form["secretsign"]):
			# 	return json.dumps({"status":"failure"},ensure_ascii=False)
			img_bytes = base64_to_bytes(request.form["base64"])
			image = Image.open(BytesIO(img_bytes))
			_,result = yolo.detect_image(image)
			#insert_db(result)
			to_return = {"name":name,
			          	 "result":{"kind":"CPD",
			          		       "flaw":list(result)}}
			return json.dumps(to_return,ensure_ascii=False)
		return json.dumps('',ensure_ascii=False)

@app.route("/index.html")
def main():
	return render_template('index.html')

@app.route("/standard.html")
def standard():
	return render_template("standard.html")

@app.route("/statistics.html")
def statistics():
	return render_template("statistics.html")

@app.route("/datas.html")
def datas():
	return render_template("datas.html")

def insert_db(result):
    struct_time = time.localtime()
    date = time.strftime("%Y-%m-%d", struct_time)
    time_ = time.strftime("%H:%M:%S", struct_time)
    record = {"date":date,"time":time_,"result":result}
    collection.insert_one(record)

if __name__ == "__main__":
	yolo = YOLO(image=True)
	app.run(host='0.0.0.0',port=8080)
