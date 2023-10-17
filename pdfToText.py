import os
import subprocess
import sys

def convert_pdfs_to_text(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for pdf_file in os.listdir(input_folder):
        if pdf_file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, pdf_file)
            txt_file = os.path.splitext(pdf_file)[0] + ".txt"
            txt_path = os.path.join(output_folder, txt_file)

            # Utilisation de pdftotext pour convertir le PDF en texte
            subprocess.call(["pdftotext", pdf_path, txt_path])

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_to_text.py input_folder output_folder")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]

    if not os.path.exists(input_folder):
        print(f"Le dossier d'entrée '{input_folder}' n'existe pas.")
        sys.exit(1)

    convert_pdfs_to_text(input_folder, output_folder)
    print("Conversion terminée.")
