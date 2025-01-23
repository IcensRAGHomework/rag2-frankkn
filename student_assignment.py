from langchain.schema import Document  # Import Document class
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter

# PDF 文件路徑
q1_pdf = "OpenSourceLicenses.pdf"

def hw02_1(q1_pdf):
    # 1. 使用 PyPDFLoader 載入 PDF 文件
    loader = PyPDFLoader(q1_pdf)
    document = loader.load()

    # 2. 使用 CharacterTextSplitter 進行文本切分，設置 chunk_overlap=0
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    # 3. 將每頁的文本進行分割
    chunks = []
    for i, page in enumerate(document):
        # 使用 text_splitter 進行每一頁的文本切割
        page_chunks = text_splitter.split_text(page.page_content)
        chunks.extend(page_chunks)  # 收集所有的 chunks

    # 4. 取得最後一個 chunk，並返回檔名、頁數與內容
    last_chunk = chunks[-1] if chunks else None
    if last_chunk:
        # 返回 Document 類型
        return Document(
            page_content=last_chunk,
            metadata={"filename": q1_pdf, "page_number": len(document)}
        )
    else:
        return None

if __name__ == '__main__':
    result = hw02_1(q1_pdf)
    print(result)
