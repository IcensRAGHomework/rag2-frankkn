from langchain.schema import Document  # Import Document class
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

from langchain_text_splitters import RecursiveCharacterTextSplitter
import re

# PDF 文件路徑
q1_pdf = "OpenSourceLicenses.pdf"
q2_pdf = "勞動基準法.pdf"

def hw02_1(q1_pdf):
    # 1. 使用 PyPDFLoader 載入 PDF 文件
    loader = PyPDFLoader(q1_pdf)
    document = loader.load()

    # 2. 使用 CharacterTextSplitter 進行文本切分，設置 chunk_overlap=0
    text_splitter = CharacterTextSplitter(chunk_overlap=0)

    # 3. 將每頁的文本進行分割
    chunks = []
    for i, page in enumerate(document):
        # 使用 text_splitter 進行每一頁的文本切割
        page_chunks = text_splitter.split_text(page.page_content)
        chunks.extend(page_chunks)  # 收集所有的 chunks

    # 4. 取得最後一個 chunk，並返回檔名、頁數與內容
    last_chunk = chunks[-1] if chunks else None
    if last_chunk:
        return Document(
            page_content=last_chunk,
            metadata={"filename": q1_pdf, "page_number": len(document)}
        )
    else:
        return None

def hw02_2(q2_pdf):
    # 1. 讀取 PDF 文本
    loader = PyPDFLoader(q2_pdf)
    documents = loader.load()
    
    # 2. 合併所有頁面的文本
    full_text = "\n".join([doc.page_content for doc in documents])

    # 3. 找出第一章之前的部分（前言）
    # 假設第一章以"第一章"為標識，將第一章之前的部分提取出來
    pre_chapter_pattern = r"^(.*?)(第\s+[一二三四五六七八九十百零]+\s*章)"
    pre_chapter_match = re.match(pre_chapter_pattern, full_text, re.DOTALL)

    # 4. 提取第一章之前的部分作為前言
    pre_chapter_text = pre_chapter_match.group(1).strip() if pre_chapter_match else ""
    full_text_without_intro = full_text[len(pre_chapter_text):]  # 剩餘的部分，不包括前言

    # 5. 章節與條文正則匹配模式（避免 tuple）
    chapter_and_article_pattern = r"(第\s+[一二三四五六七八九十百零]+\s*章|第\s*\d+(-\d+)?\s*條)"
    
    # 6. 使用 re.finditer() 避免 tuple 問題
    matches = [m.group(0) for m in re.finditer(chapter_and_article_pattern + r"[\s\S]*?(?=" + chapter_and_article_pattern + r"|$)", full_text_without_intro)]

    # 7. 合併所有匹配的章節和條文
    combined_sections = [s.strip() for s in matches]

    # 8. 用 RecursiveCharacterTextSplitter 進一步拆分
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # 增大 chunk_size 減少過度拆分
        chunk_overlap=0   # 避免 chunk 重疊造成過多 chunk
    )

    # 9. 逐個段落拆分
    chunks = []
    if pre_chapter_text:  # 如果有前言，先將前言插入為第一個 chunk
        chunks.append(pre_chapter_text)
    
    for section in combined_sections:
        chunks.extend(splitter.split_text(section))

    # 10. 印出所有 chunks 來檢查
    # for i, chunk in enumerate(chunks):
    #     print(f"Chunk {i+1}:\n{chunk}\n")

    print(f"Successfully split into {len(chunks)} chunks.")

    return len(chunks)

if __name__ == '__main__':
    result1 = hw02_1(q1_pdf)
    result2 = hw02_2(q2_pdf)
    print(result1)
    print(result2) # 111