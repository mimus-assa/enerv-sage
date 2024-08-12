from docx import Document

class DocumentProcessor:
    def __init__(self, doc_paths):
        """Inicializa la clase con las rutas de los documentos a procesar."""
        self.doc_paths = doc_paths
    
    def replace_text_in_paragraph(self, paragraph, old_text, new_text):
        """Reemplaza el texto manteniendo el formato dentro de un párrafo."""
        for run in paragraph.runs:
            if old_text in run.text:
                run.text = run.text.replace(old_text, new_text)
    
    def replace_text_in_document(self, document, variables):
        """Reemplaza múltiples variables en todo el documento de Word."""
        for paragraph in document.paragraphs:
            for key, value in variables.items():
                self.replace_text_in_paragraph(paragraph, f"${{{key}}}", value)
    
    def save_document(self, document, output_path):
        """Guarda el documento con los cambios realizados."""
        document.save(output_path)
    
    def process_document(self, doc_path, variables, output_path):
        """Método principal para reemplazar texto y guardar el documento."""
        document = Document(doc_path)
        self.replace_text_in_document(document, variables)
        self.save_document(document, output_path)
    
    def process_multiple_documents(self, variables, output_paths):
        """Genera múltiples documentos con las mismas variables pero diferentes rutas de salida."""
        for doc_path, output_path in zip(self.doc_paths, output_paths):
            self.process_document(doc_path, variables, output_path)
