
import sys
import os

def read_pdf(path):
    try:
        import pypdf
    except ImportError:
        print("pypdf not installed. Trying PyPDF2...")
        try:
            import PyPDF2 as pypdf
        except ImportError:
            print("PyPDF2 not installed. Cannot read PDF efficiently.")
            sys.exit(1)

    try:
        reader = pypdf.PdfReader(path)
        print(f"Num Pages: {len(reader.pages)}")
        
        full_text = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            full_text.append(f"--- Page {i+1} ---")
            full_text.append(text)
            
        print("\n".join(full_text))
        
    except Exception as e:
        print(f"Error reading PDF: {e}")

if __name__ == "__main__":
    pdf_path = "/Users/victor/Desktop/CSAS/M3 Challenge 2025/2025 M3 Challenge Paper.pdf"
    if os.path.exists(pdf_path):
        read_pdf(pdf_path)
    else:
        print("File not found.")
