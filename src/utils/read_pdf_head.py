
import sys
import os

def read_pdf_head(path, pages=5):
    try:
        import pypdf
    except ImportError:
        import PyPDF2 as pypdf

    try:
        reader = pypdf.PdfReader(path)
        
        full_text = []
        for i in range(min(pages, len(reader.pages))):
            text = page = reader.pages[i].extract_text()
            full_text.append(f"--- Page {i+1} ---")
            full_text.append(text)
            
        print("\n".join(full_text))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    pdf_path = "/Users/victor/Desktop/CSAS/R Modeling/Curling.pdf"
    read_pdf_head(pdf_path)
