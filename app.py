from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.epsmx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta



@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    # 기록하기 API 완성
    bucket_receive = request.form['bucket_give']

    # 숫자 설정 = 전체 리스트 들고 오기 > len(전체 리스트 받아온 변수)
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num' : count,
        'bucket' : bucket_receive,
        'done' : 0
    }

    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # client에서 서버로 숫자로 넘겨줘도 다 문자 받음
    num_receive = request.form['num_give']
    #                           숫자로 바꿔줘야 됨
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})

    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    # 보여주기 API
    # 전체 리스트 들고와서
    bucket_list = list(db.bucket.find({}, {'_id': False}))
    # 내려주기
    return jsonify({'buckets': bucket_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)