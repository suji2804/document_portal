from pathlib import Path
import sys
import fitz
from exception.custom_exception import DocumentPortalException
from logger.custom_logger import CustomLogger


class DataIngestion:
    def __init__(self, base_dir:str="data\\document_compare"):
        self.log = CustomLogger().get_logger(__name__)
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def delete_existing_files(self):
        try:
            if self.base_dir.exists():
                for file in self.base_dir.iterdir():
                    if file.is_file():
                        file.unlink()
                        self.log.info("File deleted", path=str(file))
                self.log.info("Existing files deleted successfully", directory=str(self.base_dir))
        except Exception as e:
            self.log.error(f"Error deleting existing files: {e}")
            raise DocumentPortalException("Error deleting existing files", sys)

    def save_uploaded_files(self, reference_file, actual_file):
        """        Save uploaded files to the base directory."""
        try:
    
            self.delete_existing_files()
            self.log.info("Existing files deleted successfully.")

            ref_path = self.base_dir/ reference_file.name
            act_path = self.base_dir / actual_file.name

            if not reference_file.name.endswith(".pdf") or not actual_file.name.endswith(".pdf"):
                raise ValueError("Only PDF files are allowed.")
                
            with open(ref_path, "wb") as f:
                f.write(reference_file.getbuffer())

            with open(act_path, "wb") as f:
                f.write(actual_file.getbuffer())

            self.log.info("Files saved", reference=str(ref_path), actual=str(act_path))
            return ref_path, act_path
        except Exception as e:
            self.log.error(f"Error saving uploaded files: {e}")
            raise DocumentPortalException("An error occurred while saving uploaded files.", sys)

        

    def read_pdf(self,pdf_path: str) -> str:
        """        Read the content of a PDF file and return it as a string.
        """
        try:
            with fitz.open(pdf_path) as doc:
                if doc.is_encrypted:
                    raise ValueError(f"PDF is encrypted: {pdf_path.name}")
                all_text = []
                for page_num in range(doc.page_count):
                    page=doc.load_page(page_num)
                    text = page.get_text() #type: ignore
                    if text.strip():
                        all_text.append(f"\n --- Page {page_num + 1} --- \n{text}")
                self.log.info("PDF read successfully", file=str(pdf_path), pages=len(all_text))
                return "\n".join(all_text)
        except Exception as e:
            self.log.error(f"Error reading PDF: {e}")
            raise DocumentPortalException("An error occurred while reading the PDF.", sys)
        
    def combine_documents(self) -> str:
        """        Combine the reference and actual document texts into a single string.
        """

        try:
            content_dict = {}
            doc_parts = []

            for filename in sorted(self.base_dir.iterdir()):
                if filename.is_file() and filename.suffix == ".pdf":
                    content_dict[filename.name] = self.read_pdf(filename)
            for name, content in content_dict.items():
                doc_parts.append(f"\n--- {name} ---\n{content}")
            combined_docs = "\n".join(doc_parts)
            self.log.info("Documents combined successfully", parts=len(doc_parts))
            return combined_docs
        except Exception as e:
            self.log.error(f"Error combining documents: {e}")
            raise DocumentPortalException("An error occurred while combining documents.", sys)
