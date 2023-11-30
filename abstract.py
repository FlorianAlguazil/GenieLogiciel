
import os
import sys
import re
import string


class extract():
    
    def __init__(self, pdftotext_file):
        self.type = "txt"
        self.fileString = pdftotext_file.read().splitlines() 
        
    def getNextTitle(self, titles):
        nextTitle = False
        last = ""
        for line in self.fileString:
            for title_name in titles:
                if title_name == "":
                    nextTitle = True

                if  len(re.findall("^[IVXL]+\.?\s", line)) and (len(re.findall("\s{}".format(title_name.upper()), line.upper() )) or nextTitle) and (self.type != "arabe" and self.type != "arabePoint"):
                    i = 0
                    for word in line.split():
                        if word[0].isupper() and i >= 1:
                            if re.findall("^[IVXL]+\.$", line.split()[0]) and self.type != "roman": 
                                self.type = "romanPoint"
                            elif re.findall("^[IVXL]+$", line.split()[0]) and self.type != "romanPoint":
                                self.type = "roman"
                            else :
                                continue
                            return self.fileString.index(line)
                        i += 1
                

                if len(re.findall("^[0-9]+\.?[0-9]*\s", line)) and (len(re.findall("\s{}".format(title_name.upper()), line.upper())) or nextTitle) and (self.type != "roman" and self.type != "romanPoint"):
      
                    i = 0
                    for word in line.split():
                        if word[0].isupper() and i >= 1:
                            if re.findall("^[0-9]+\.$", line.split()[0]) and self.type != "arabe": 
                                self.type = "arabePoint"
                            elif re.findall("^[0-9]+$", line.split()[0]) and self.type != "arabePoint":
                                self.type = "arabe"
                            else :
                                continue
                            return self.fileString.index(line)
                        i += 1
                
                if "conclusion".upper() == title_name.upper() or nextTitle:
                    continue
                if len(re.findall("^"+title_name.upper(), line.upper().replace(" ","") )) and self.type == "txt":
                    return self.fileString.index(line)
                    
            
        return -1
     
    def getPreamble(self, input_file_name):
        return input_file_name.replace(' ', '_')              

    def getTitle(self):
        txt = ""
        while txt == "":
            txt = self.fileString.pop(0)
            x = re.findall("[0-9]", txt)
            if len(txt) < 6:
                txt = ""
            if len(x) > 1:
                txt = ""
            x = re.findall("THIS", txt.upper())
            if len(x) > 0:
                txt = ""
        
        return txt+" "+self.fileString.pop(0)

    def getAuthors(self):
        num = self.getNextTitle(["ABSTRACT"])
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
    

    def getAbstract(self):
        num = self.getNextTitle(["INTRODUCTION"])
        if num == -1: 
            num = self.getNextTitle([""])
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

  
    def getIntroduction(self):
        ret = ""
        ret += self.fileString.pop(0)+" "
        num = self.getNextTitle(["work"])
        if num == -1:
            num = self.getNextTitle([""])
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret
   
    def getReference(self):
        num = self.getNextTitle(["REFERENCES"])
        if num == -1:
            num = self.getNextTitle([""])
        ret = ""
        while num < len(self.fileString):
            ret += self.fileString.pop(num)+" "
        return ret

    def getCorps(self):
        num = self.getNextTitle(["conclusion","Discussion"])
        if num == -1: 
            num = self.getNextTitle(["Final"])
            if num == -1:
                num = self.getNextTitle(["Reference"])
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    def getConclusion(self):
        num = self.getNextTitle(["Acknowledgments"])
        if num == -1: 
            num = self.getNextTitle([""])
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    def getDiscussion(self, arg):
        self.type = "txt"
        num = self.getNextTitle(arg)
        ret = ""
        for i in range(num):
            ret += self.fileString.pop(0)+" "
        return ret

    