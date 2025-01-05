import openai
import pdfplumber
from PIL import Image
from pdf2image import convert_from_path # type: ignore
import io
import os
import tempfile

openai.api_key = os.environ['OPENAI_API_KEY']

def extract_text_from_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        with pdfplumber.open(tmp_file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        
        os.remove(tmp_file_path)
        return text
    except Exception as e:
        print(f"テキスト抽出エラー: {e}")
        return ""

def summarize_text(text):
    """openai APIを使用してテキストを要約"""
    prompt = f"以下の文章を要約してください:\n{text[:2000]}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=300
    )
    return response["choices"][0]["message"]["content"].strip()

def extract_images_from_pdf(file):
    """pdfplumberを使用してPDFから画像を抽出"""
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        images = []
        with pdfplumber.open(tmp_file_path) as pdf:
            for page in pdf.pages:
                if hasattr(page, "images"):  # ページに画像が含まれている場合のみ処理
                    for img in page.images:
                        try:
                            if "stream" in img:
                                image_data = img["stream"].get_data()
                                image = Image.open(io.BytesIO(image_data))
                                images.append(image)
                        except Exception as e:
                            print(f"画像抽出エラー: {e}")
        
        os.remove(tmp_file_path)
        return images
    except Exception as e:
        print(f"画像抽出エラー: {e}")
        return []

def render_pdf_page_as_image(file):
    """pdf2imageを使用してPDFページ全体を画像としてレンダリング"""
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        images = convert_from_path(tmp_file_path, dpi=300)  # DPIを設定して高解像度でレンダリング
        
        os.remove(tmp_file_path)
        return images
    except Exception as e:
        print(f"ページレンダリングエラー: {e}")
        return []

def extract_all_images_from_pdf(file):
    """pdfplumberとpdf2imageの両方を使用してPDFからすべての画像を抽出"""
    images = extract_images_from_pdf(file)
    rendered_images = render_pdf_page_as_image(file)
    return images + rendered_images

def extract_tables_from_pdf(file):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file.read())
            tmp_file_path = tmp_file.name
        
        tables = []
        with pdfplumber.open(tmp_file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    tables.append(table)
        
        os.remove(tmp_file_path)
        return tables
    except Exception as e:
        print(f"テーブル抽出エラー: {e}")
        return []

# Example usage
if __name__ == "__main__":
    file_path = "path/to/your/file.pdf"
    text = extract_text_from_pdf(file_path)
    summary = summarize_text(text)
    print(summary)
