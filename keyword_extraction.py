import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

def extract_keywords(text):
    prompt = f"以下の文章からキーワードを抽出してください:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    keywords = response["choices"][0]["message"]["content"].strip()
    return keywords.split(", ")

# Example usage
if __name__ == "__main__":
    text = "OpenAI APIを使用してキーワードを抽出する方法について説明します。"
    keywords = extract_keywords(text)
    print(keywords)
