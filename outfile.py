import os
import re
from bs4 import BeautifulSoup
import nltk
from pyvi import ViTokenizer, ViPosTagger # thư viện NLP tiếng Việt
import gensim # thư viện NLP
# nltk.download('stopwords')
nltk.download('punkt')
# from nltk.tokenize import word_tokenize, sent_tokenize #import hàm xử lý tách từ,tách câu
# from nltk.corpus import stopwords #import tập hư từ
from nltk.stem import PorterStemmer
ps = PorterStemmer()
# from string import punctuation #import tập dấu câu từ thư viện string
# my_stopwords = set(stopwords.words('english') + list(punctuation))
stop_words = open('vietnamese_stopwords.txt',encoding="utf8")
a=stop_words.read()
my_stopwords = a
# print(my_stopwords)

#Hàm trả về type của file
def getTypeOfFile(path):
    return path[-3:]
# Hàm đọc đường dẫn file                
def readLinkFile(path):   
    list_path=[]
    for root, dirs, files in os.walk(path):
        for file in files:
            list_path.append(root+"/"+file)
    return list_path
            
# Hàm đọc file
def readFile(list_path):
    read_files = []
    i=0
    for i in range (len(list_path)):
        read_file=open(list_path[i], "r" ,encoding="utf8")
        a=read_file.readlines()
        a = ' '.join(a)
        read_files.append(a)            
    return read_files

#lấy du liệu từ file


#Hàm lấy tên file
def getNameTxtFile(path):
    if getTypeOfFile(path) == "txt":
        arrSplit = path.split('/')
        nameTxtFile = arrSplit[len(arrSplit)-1]
        return nameTxtFile[:-4]
#Hàm xóa thẻ html
def clean_html(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()
#Hàm loại bỏ các ký tự đạc biệt
def remove_special_character(text):
    
    #Thay thế các ký tự đặc biệt bằng ''
    string  = re.sub('[^\w\s]','',text)
    #xóa ký tự \n
    string = string.replace("nn", "")
    #Xử lí các khoảng trắng thừa ở giữa chuỗi
    string = re.sub('\s',' ',string)
    #Xử lý khoảng trắng thừa ở đầu và cuối câu
    string = string.strip() 
    return string
# Hàm xóa trùng
def remove_duplicates(text):
    return list(set(text))
#Tách câu tách từ, loại bỏ hư từ
def filterTexts(txtArr):
    res = []
    for i in range(len(txtArr)):
        # text_cleaned = clean_html(txtArr[i])
        # #Tách câu
        # sents  = sent_tokenize(text_cleaned)
        # #Loại bỏ ký tự đặc biệt
        # sents_cleaned = [remove_special_character(s) for s in sents]
        # #Nối các câu lại thành text
        # text_sents_join = ''.join(sents_cleaned)
        # #Tách từ
        # words = word_tokenize(text_sents_join)
        # #Đưa về dạng chữ thường
        # words = [word.lower() for word in words]
        # #Loại bỏ hư từ
        # words = [word for word in words if word not in my_stopwords]
        # words = [ps.stem(word) for word in words]
        # words = remove_duplicates(words)
        # words = ' '.join(words) 
       
        # res.append(words)
        #vietnamese
        #tách từ trong tiếng việt
        lines = ViTokenizer.tokenize(txtArr[i])  
        lines = lines.replace('\ n', ' ')
        #Xư lí các ký tự đặc biệt
        lines = gensim.utils.simple_preprocess(lines)
        #Loại bỏ stop word
        lines = [line for line in lines if line not in my_stopwords]
        #Xóa trùng
        # lines = remove_duplicates(lines)
        lines = '\n'.join(lines)         
        res.append(lines)
    return res
#Ghi ra file txt
def writeFile(txtArrAfter, outputName, path):
    f = open(path + "/" + outputName + "_word.txt", 'w',encoding="utf8")
    f.write(str(txtArrAfter))
    f.close()
#main   
def main():
    i_path = input('Nhập đường dẫn folder:')
    list_path = readLinkFile(i_path)
    o_path = input('Nhập đường dẫn folder muốn xuất ra:')
    
    for i in range(len(list_path)):
        read_files = readFile(list_path)
        name_file = getNameTxtFile(list_path[i])
        files_filted = filterTexts(read_files)
        writeFile(files_filted[i], str(name_file), o_path)
    print('Đã xuất file !')

    
if __name__ == "__main__":
    main()
    
    
