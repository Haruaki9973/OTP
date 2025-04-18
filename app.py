from flask import Flask, render_template, request, redirect, url_for
import secrets
import datetime

app = Flask(__name__)

# ワンタイムパスワードの保存場所（シンプルな実装）
otp_code = None
otp_expire = None

@app.route("/")
def home():
    return "<a href='/generate'>ワンタイムパスワードを発行</a>"

# OTP発行
@app.route("/generate")
def generate():
    global otp_code, otp_expire
    otp_code = str(secrets.randbelow(1000000)).zfill(6)
    otp_expire = datetime.datetime.now() + datetime.timedelta(minutes=5)
    return f"<h1>OTP発行：{otp_code}</h1><a href='/otp'>→ 入力画面へ</a>"


# 入力フォーム表示
@app.route("/otp")
def otp_input():
    return render_template("otp_input.html")

# OTP確認
@app.route("/verify", methods=["POST"])
def verify():
    global otp_code, otp_expire
    user_code = request.form["otp"]
    now = datetime.datetime.now()

    if otp_code is None or now > otp_expire:
        result = "期限切れ、またはコードが存在しません。"
    elif user_code == otp_code:
        result = "認証成功！"
    else:
        result = "認証失敗。コードが違います。"

    return render_template("otp_result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
