from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import func, case
import random
import datetime


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# SQLiteデータベースの設定
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ユーザーモデル
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

# 問題解答結果モデル
class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(200), nullable=False)
    user_answer = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    time_taken = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
# アカウント作成
@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json()
    username = data.get('username')

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Account created successfully", "user_id": new_user.id}), 201

# アカウントログイン
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')

    user = User.query.filter_by(username=username).first()

    if user:
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    else:
        return jsonify({"message": "Account not found"}), 404

# 問題生成
@app.route('/generate', methods=['POST'])
def generate_question():
    data = request.get_json()
    mode = data.get('mode')
    
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    
    if mode == 'multiplication':
        question = f"{a} × {b} = ?"
        correct_answer = a * b
    else:  # division
        product = a * b
        question = f"{product} ÷ {a} = ?"
        correct_answer = b

    return jsonify({
        'question': question,
        'correct_answer': correct_answer
    })

# 解答チェックと結果の保存
@app.route('/check', methods=['POST'])
def check_answer():
    data = request.get_json()
    user_id = data.get('user_id')
    user_answer = int(data.get('userAnswer'))
    correct_answer = int(data.get('correctAnswer'))
    question = data.get('question')
    time_taken = float(data.get('time_taken'))

    is_correct = user_answer == correct_answer

    # 結果をデータベースに保存
    new_result = QuizResult(
        user_id=user_id,
        question=question,
        correct_answer=str(correct_answer),
        user_answer=str(user_answer),
        is_correct=is_correct,
        time_taken=time_taken
    )
    db.session.add(new_result)
    db.session.commit()

    return jsonify({
        'result': is_correct,
        'correct_answer': correct_answer
    })

# 日ごとの正解率と解答時間を取得
@app.route('/get_statistics', methods=['GET'])
def get_statistics():
    # 日ごとに掛け算と割り算モードを区別
    stats = db.session.query(
        func.date(QuizResult.created_at).label('date'),
        case(
            [(QuizResult.question.contains('×'), 'multiplication')],
            else_='division'
        ).label('mode'),
        func.avg(case([(QuizResult.is_correct == True, 1)], else_=0)).label('average_correct_rate'),
        func.avg(QuizResult.time_taken).label('average_time_taken')
    ).group_by(func.date(QuizResult.created_at), case([(QuizResult.question.contains('×'), 'multiplication')], else_='division')).all()

    results = []
    for stat in stats:
        results.append({
            'date': stat.date.strftime('%Y-%m-%d'),
            'mode': stat.mode,
            'average_correct_rate': round(stat.average_correct_rate * 100, 2),  # 正解率をパーセンテージで返す
            'average_time_taken': round(stat.average_time_taken, 2)  # 秒単位で返す
        })
    return jsonify(results)

# アプリ起動時にデータベースを初期化
if __name__ == '__main__':
    # デバッグモードが有効で再起動が行われるのを防ぐ
    if not app.debug or os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        with app.app_context():
            db.create_all()  # データベースのテーブルを作成

    app.run(host='0.0.0.0', port=5000)
