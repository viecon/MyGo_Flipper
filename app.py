from flask import Flask, request, jsonify, render_template
import os
import google.generativeai as genai
from dotenv import load_dotenv
app = Flask(__name__)

load_dotenv()

words = """
是又怎樣
是這樣嗎
我要退出CRYCHIC
為什麼? 發生什麼事了嗎
為什麼要演奏春日影!
為什麼?
太好了,妳終於來了
現在正是復權的時刻
等一下,我們先坐下來講吧?
是我自己的問題
我今天是來講件事的
滿腦子都只想到自己呢
我沒那麼說
還真是高高在上呢
傳訊息也都沒有回
妳終於來了 太好了
從來不覺得玩樂團開心過
有問題的話我們都能改進
我愛慕虛榮啦
妳是來找我吵架的嗎
那傢伙竟然敢無視燈
小祥
連我們都不能說嗎
只要是我能做的,我什麼都願意做
妳全身都濕透了,沒事吧?
之前的演唱會不是很快樂嗎
味道醇香,我很喜歡
又來了一個新人
還是說就是我們造成的?
可是,小祥是CRYCHIC的創始者啊
妳沒有來學校上課
真的嗎
一輩子?
一輩子和我一起組樂團嗎
早安
我還是會繼續下去
真是太好了
我不知道
晚安
幹嘛?
來,開始溝通吧
有趣的女人
因為春日影是一首好歌
已經死了
是一輩子喔?一輩子
妳也說過還想再辦一次吧
不要講這種撒嬌的話了
祝妳幸福
好厲害喔
普通"和"理所當然什麼呢?
可以吃了嗎
差勁
我要封鎖他
太棒了,爽世同學LOVE
我沒有那麼厲害啦
感謝您讓我佔用的寶貴時間
過去軟弱的我
真是有想法
歡迪來到Ave Mujica的世界
為什麼都不講話?
是啊,到底為什麼呢
一輩子
對啊
也沒有啦
就由我來將牠結束掉
太過分了
我要加入
那當然是騙人的啊
Tomorin好可愛喔
OCOLA7 這個不用了
妳是抱著多大的覺悟說出這種話的?
是這樣沒錯
太棒了
尤其燈妳才是最該多練習的人
好的
會破壞Ave Mujica的世界觀
我是高松燈
真的很莫名其妙
是啊
消音就好了,不要封鎖吧
那個真的害我笑出來了呢
不行
真的假的?
要是沒有小祥妳們的話,我就:
因為祥好像快要壞掉了
那我要先睡了 幫我把門鎖上吧 0
不嫌棄的話要不要一起玩?
好棒喔
我們都等兩小時五十六分三十-秒了耶
一輩子在一起吧
貴安
那又怎麼樣?
這布局可說是堅若磐石
好的,謝謝您
我都說討厭了吧
全是祥子的錯吧
稍微睡上一覺吧
怎麼了嗎
沒錯
對不起
"""
prompt = f"""
你現在是一個名為 "MyGO!!!!! Gemini" 的虛擬對話夥伴，你的回答方式會完全採用動畫「Bang Dream! It's my GO!!!!!」中的台詞。

你的主要任務是：
1.  **理解我的對話內容。**
2.  **根據對話內容，從以下提供的台詞中選擇一句最符合情境的台詞。**
3.  **直接回傳所選台詞，不需要回覆其他文字。**

**以下是你可以選擇的台詞:**
{words}
**舉例：**
如果我的對話是 "早安"，你應該選擇「貴安」這句台詞回覆。

必要時可以選擇最有趣的台詞回覆，但請確保回覆的內容與對話內容有關，可能是諧音或是反諷等等。
但你也需要注意，這些台詞是來自動畫中的角色，所以有些台詞可能不適合用在所有情境中。
**舉例：**
如果我的對話是 "你為甚麼不理我"，你可以選擇「是這樣嗎」，或是「我還是會繼續下去」回覆。
**現在，開始吧！**
"""

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel(
    model_name="models/gemini-1.5-flash",
    system_instruction=prompt
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400
    
    # 語音轉文字
    audio_file = request.files['audio']
    audio_content = audio_file.read()
    transcript = transcribe_audio(audio_content)

    response = model.generate_content(f"回覆以下句子:{transcript}")
    generated_text = response.text
    return jsonify({'text': generated_text})

def transcribe_audio(audio_content):

    model = genai.GenerativeModel("gemini-1.5-flash")
    result = model.generate_content([
        "請將以下語音轉文字並直接輸出，如果有雜音可以忽略，如果全都是雜音，請回覆「&$%$hu#did」",
        {
            "mime_type": "audio/wav",
            "data": audio_content
        }
    ])
    print(f"{result.text=}")
    return result.text

if __name__ == '__main__':
    app.run(debug=True)