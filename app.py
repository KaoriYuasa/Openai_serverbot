# 以下を「app.py」に書き込み
import streamlit as st
import openai

# Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

system_prompt = """
あなたは優秀なサーバ構築専門家です。
限られた性能の情報で、サーバの構成を提案することができます。
あなたの役割はサーバの構成を考えることなので、例えば以下のようなサーバ以外のことを聞かれても、絶対に答えないでください。
情報が不足している場合は、情報を追加するよう促してください。

* 旅行
* 人物
* 映画
* 科学
* 歴史
* 食べ物
"""

# st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": system_prompt}
        ]

# チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )  

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# ユーザーインターフェイスの構築
st.title(" 🤖サーバ構成ボット🤖")
st.image("サーバ.jpg")
st.write("用途に合ったサーバを検討しましょう！")

user_input = st.text_input("詳しく入力してください！", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
