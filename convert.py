#!/usr/bin/python

import os
import subprocess
import argparse
from pathlib import Path

import abstract

def main():    
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to the directory containing the pdf files")
    parser.add_argument("-x", "--xml", action="store_true",  help="output file will be in xml format")
    parser.add_argument("-t", "--txt", action="store_true", help="output file will be in txt format")

    args = parser.parse_args()

    path = args.path
    if args.xml and args.txt:
        print("Error: cannot specify both xml and txt output")
        exit(1)
    elif args.xml:
        createFiles(path, "xml", False, args)
    elif args.txt:
        createFiles(path, "txt", False, args)
    else:
        print("Error: no output format specified")
        exit(1)
        

def SanitizeOutputDirectory(path):
    if not os.path.exists(path):
        os.makedirs(path)
    elif os.listdir(path):
        for file in os.listdir(path):
            os.remove(path+"/"+file)

def generateTempFiles(inputPath, outputPath, files):
    for file in files:
        if file.endswith(".pdf"):
            pdf_file = Path(inputPath + "/" + file)
            txt_file = Path(outputPath+ "/" + file + ".txt")
            if not txt_file.is_file():
                subprocess.call(["pdftotext", "-raw", pdf_file, txt_file])
                print("Created temporary text file: " + str(txt_file))
            else:
                print("File already exists: " + str(txt_file))
    return

def cleanTempFiles(path):
    for file in os.listdir(path):
        if file.endswith(".pdf.txt"):
            os.remove(path+"/"+file)

def createFiles(inputPath, format, xmlplus, args):

    print("Please select the files you want to parse:")
    i = 0
    for file in os.listdir(inputPath):
        if file.endswith(".pdf"):
            print(str(i)+'. '+file)
            i += 1
    print("Enter the number of the files you want to parse, separated by a space:")
    filesIndexes = input().split()
    files = []
    i = 0
    for file in os.listdir(inputPath):
        if file.endswith(".pdf"):
            if str(i) in filesIndexes:
                files.append(file)
            i += 1

    outputPath = inputPath + "_" + format.upper()
    SanitizeOutputDirectory(outputPath)
    generateTempFiles(inputPath, outputPath, files)
    if format == "xml":
        generateXMLFiles(outputPath, xmlplus)
    elif format == "txt":
        generateTXTFiles(outputPath, xmlplus)
    cleanTempFiles(outputPath)
    exit(0)

def generateTXTFiles(outputPath, xmlplus):
    for file in os.listdir(outputPath):
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')

        input_file_name = Path(os.path.basename(file)).stem

        output_file = open(outputPath+"/"+Path(input_file_name).stem+".txt", 'w+')
        
        extracter = abstract.extract(pdftotext_file)
        output_file.write("Préamble :\n\t" + extracter.getPreamble(input_file_name))
        output_file.write("\nTitre :\n\t"+ extracter.getTitle())
        output_file.write("\nAuteurs :\n\t" + extracter.getAuthors())
        output_file.write("\nAbstract :\n\t"+extracter.getAbstract())
        output_file.write("\nIntroduction :\n\t"+extracter.getIntroduction())

        pdftotext_file.close()
        output_file.close()
    
    return

def generateXMLFiles(outputPath, xmlplus):
    for file in os.listdir(outputPath):
        if not file.endswith(".pdf.txt"):
            continue
        else:
            pdftotext_file = open(outputPath+"/"+file, 'r')
        input_file_name = Path(os.path.basename(file)).stem
        output_file = open(outputPath+"/"+Path(input_file_name).stem+".xml", 'w+')

        extracter = abstract.extract(pdftotext_file)
        output_file.write('<article>\n')
        output_file.write("\t<preamble>" + extracter.getPreamble(input_file_name) + '</preamble>\n')
        output_file.write("\t<title>"+ extracter.getTitle() + '</title>\n')
        output_file.write("\t<auteur>" + extracter.getAuthors() + '</auteur>\n')
        output_file.write("\t<abstract>"+extracter.getAbstract()+"</abstract>\n")
        output_file.write("\t<introduction>"+extracter.getIntroduction()+"</introduction>\n")
        output_file.write('</article>')

        pdftotext_file.close()
        output_file.close()
    
    return

main()




