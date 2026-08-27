from flask import Flask, render_template, request

# 서버 인스턴스 생성
app = Flask(__name__)

# 엔드포인트 1: 입력화면 (/)
@app.route('/')         # localhost:5000/ 로 요청이 들어오면,
def input_page():       # 이 함수를 실행 하겠다.
    return render_template('in.html')  # in.html 갖다 줘라(응답해라)


# 엔드포인트 2: 출력화면 (/out)
@app.route('/out')
def output_page():
    import os
    from dotenv import load_dotenv
    import requests
    from bs4 import BeautifulSoup
    from openai import OpenAI
    
    # 1. 사용자가 보낸 data를 추출
    urls = request.args.get('urls')
    
    # 2. 링크를 분리한 후에
    if urls:
        urls = [url.strip() for url in urls.splitlines() if url.strip()]
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    
    # 3. 뉴스 기사를 가져와서 내용만 추출 하고
    def extract_news(URL: list):
        news_results = []
        for url in URL:
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            news_results.append(soup.select_one('#dic_area').text.strip())
        return news_results
    
    # 4. GPT에게 넘겨서 댓글을 만들어 달라고 하고
    results =[]
    client = OpenAI(
    api_key = os.getenv('OPENAI_API_KEY')
    )
    sys_msg = '뉴스기사를 읽고 각 기사에 댓글을 달아줘'
    user_msg = extract_news(urls)

    for item in extract_news(urls): 
        gpt_res = client.responses.create(
            model = 'gpt-4.1-mini',
            instructions = sys_msg,
            input = item
        )
        results.append(gpt_res.output_text)
    
    # 5. out.html 에 비벼서 보여준다

    return render_template('out.html', results=results) 


# 서버 실행
app.run(debug=True)