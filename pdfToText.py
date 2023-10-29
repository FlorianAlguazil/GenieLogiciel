#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import abstract

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="chemin vers le dossier contenant les pdfs")
    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path + "_output"):
        os.makedirs(path + "_output")
    elif os.listdir(path + "_output"):
        for file in os.listdir(path + "_output"):
            os.remove(path + "_output/" + file)

    for file in os.listdir(path):
        if file.endswith(".pdf"):
            print("Processing file: " + file)
            pdf_file = Path(path + "/" + file)
            txt_file = Path(path + "_output/" + file + ".txt")
            if not txt_file.is_file():
                subprocess.call(["pdftotext", "-raw", pdf_file, txt_file])
                print ("fichier temporaire crée: " + str(txt_file))
            else:
                print("Fichier déjà existant: " + str(txt_file))
        
            pdftotext_file = open(txt_file, 'r')
            output_file = open(path+'_output/'+str(Path(os.path.basename(pdf_file)).stem)+'.txt', 'w+')
        
            output_file.write(os.path.basename(pdf_file).replace(' ', '_') + '\n')
    
            title = pdftotext_file.readline().strip()+pdftotext_file.readline().strip()
            output_file.write(title + '\n')

            output_file.write(abstract.readAbstract(pdftotext_file))

            pdftotext_file.close()
            output_file.close()
            os.remove(txt_file)
            
main()
