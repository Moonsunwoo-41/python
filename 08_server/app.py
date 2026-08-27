from flask import Flask, render_template, request

# 서버 인스턴스 생성
app = Flask(__name__) 

# 엔드포인트 1: 입력화면 (/in)
@app.route('/')
def input_page():
    return render_template('in.html')

# 엔드포인트 2: 출력화면 (/out)
@app.route('/out')
def output_page():
    urls = request.form.get('urls')
    urls = urls.split('\n')
    urls = list(map(lambda url: url.strip(), urls))
    
    results =[]

    return render_template('out.html', results = results)

# 서버 실행
app.run(debug=True) 