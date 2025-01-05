import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

def summarize_text(text):
    """テキスト全体の要約を生成"""
    if len(text) > 2000:
        # テキストが長すぎる場合は分割して処理
        return summarize_text_in_chunks(text)
    prompt = f"以下の文章を簡潔に要約してください。文が途切れないようにしてください:\n{text[:2000]}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"].strip()

def summarize_text_in_chunks(text):
    """テキストを分割して要約を生成"""
    chunks = [text[i:i+2000] for i in range(0, len(text), 2000)]
    summaries = [summarize_text(chunk) for chunk in chunks]
    return " ".join(summaries)


def summarize_paper(text, section=None):
    """論文特化の要約生成（セクション指定可能）"""
    if section:
        prompt = f"以下の論文から、'{section}'セクションを要約してください:\n{text[:2000]}"
    else:
        prompt = f"以下の論文を要約してください:\n{text[:2000]}"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"].strip()

def answer_question(question, context):
    """質問応答機能"""
    prompt = f"以下の内容を元に質問に答えてください:\n\n内容:\n{context[:2000]}\n\n質問:\n{question}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # GPTモデルを指定
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response["choices"][0]["message"]["content"].strip()
