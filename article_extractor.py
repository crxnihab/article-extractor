import os
import re
import requests
from bs4 import BeautifulSoup
from readability import Document
from fpdf import FPDF

# 📂 Save directory
SAVE_DIR = "/sdcard/ArticleFiles"

# 🔤 Clean file name
def sanitize_filename(name):
    name = re.sub(r'[\\/*?:"<>|]', "", name)  # Remove illegal filename chars
    return name.strip().replace(" ", "_")[:100]  # Limit length

# 📥 Extract article from URL
def extract_article(url):
    try:
        print("🔍 Fetching article...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        doc = Document(response.text)
        title = doc.title()
        html = doc.summary()
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        return title.strip(), text.strip()
    except Exception as e:
        print(f"❌ Failed to extract article: {e}")
        return None, None

# 💾 Save as text file
def save_as_txt(title, content):
    filename = sanitize_filename(title) + ".txt"
    path = os.path.join(SAVE_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ Text saved at: {path}")

# 📄 Save as PDF
def save_as_pdf(title, content):
    filename = sanitize_filename(title) + ".pdf"
    path = os.path.join(SAVE_DIR, filename)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(path)
    print(f"✅ PDF saved at: {path}")

# 🧠 Main logic
def main():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    url = input("🔗 Enter article URL: ").strip()
    title, content = extract_article(url)

    if content:
        choice = input("💾 Save as PDF or TXT? (pdf/txt): ").strip().lower()
        if choice == "pdf":
            save_as_pdf(title, content)
        elif choice == "txt":
            save_as_txt(title, content)
        else:
            print("⚠️ Invalid choice. Please enter 'pdf' or 'txt'.")
    else:
        print("❌ Article extraction failed.")

if __name__ == "__main__":
    main()
