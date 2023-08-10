from flask import Flask, render_template, request, jsonify
app = Flask(__name__)
from bson.objectid import ObjectId

# 파이몽고 연결하기
from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.z6pz5so.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    userInt_receive = request.cookies.get('userInt')
    return render_template('index.html')

@app.route('/login')
def loginPage():
    return render_template('login.html')


# 몽고DB에 닉네임, 이메일, 비밀번호 데이터 넣기
@app.route("/login", methods=["POST"])
def login():
    # userInt = 0
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']
    # todoMemo_receive = request.form['todoMemo_give']
    # done_receive = request.form['done_give']
    # date_receive = request.form['date_give']
    
    doc = {
        # 'userInt': userInt,
        'id': id_receive,
        'pw': pw_receive,
        'nickname' : nick_receive,
        # 'todoList': [{'todoMemo' : todoMemo_receive,
        #                 'done' : done_receive,
        #                 'date' : date_receive}],
        
    }
    # userInt += 1 

    # id, 암호화된pw을 가지고 해당 유저를 찾습니다.
    result = db.todo.find_one({'id': id_receive, 'pw': pw_receive, 'nickname': nick_receive})

    # 찾으면 JWT 토큰을 만들어 발급합니다.
    if result is not None:

        # token을 줍니다.
        return jsonify({'result': 'success', 'userNickname': result['nickname']})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})



#userInt 가져오기
@app.route("/userInt", methods=["GET"])
def userInt():
    userNickname_receive = request.cookies.get('userNickname')
    userinfo = db.todo.find_one({'nickname': userNickname_receive}, {'_id': 0})

    
    return jsonify({'result': userinfo, 'userNickname':userNickname_receive})





if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)

