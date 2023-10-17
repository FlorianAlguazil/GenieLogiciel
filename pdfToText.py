import os
import subprocess
import sys
import time

def convert_pdfs_to_text(input_folder):
    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_file)
            txt_file = os.path.splitext(pdf_file)[0] + ".txt"
            txt_path = os.path.join(input_folder, "text_files", txt_file)

            # Crée un sous-dossier "text_files" dans le dossier d'entrée si nécessaire
            text_files_folder = os.path.join(input_folder, "text_files")
            if not os.path.exists(text_files_folder):
                os.makedirs(text_files_folder)

            # Utilisez pdftotext pour convertir le PDF en texte
            subprocess.call(["pdftotext", pdf_path, txt_path])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pdf_to_text.py input_folder")
        sys.exit(1)

    input_folder = sys.argv[1]

    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        sys.exit(1)

    start_time = time.time()

    convert_pdfs_to_text(input_folder)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Conversion terminée en {elapsed_time:.2f} secondes.")


