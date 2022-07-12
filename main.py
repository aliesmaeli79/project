from parsivar import Normalizer , Tokenizer , FindStems
import os
import json
from os.path import exists
from timeit import default_timer

list_stop_words = []
def stop_words():
    stop_words = open("file_project/stop.txt", encoding="utf8")
    stop_words.seek(0)
    for i in stop_words:
        list_stop_words.append(i.replace("\n", ""))

list_len_prefix = []
list_normal_prefix =[]
def normal_prefix():
    normal_prefix = open("file_project/normal_prefix.txt", encoding="utf8")
    for i in normal_prefix:
        list_len_prefix.append(len(i.replace("\n", "")))
        list_normal_prefix.append(i.replace("\n",""))


def elim():
    punc = open("file_project/elim.txt", encoding="utf8")
    result = []
    for i in punc.readlines():
       result.append( i.replace("\n",""))
    return result


def read_document():
    number_dic = os.listdir("document")
    stop_words()
    normal_prefix()
    for doc in range(0, len(number_dic)):
        tokeniz(doc)

dict = {}
def tokeniz(doc):
    list_elim = elim()
    file = open(f"document/{doc}.txt", encoding="utf8")
    text = file.read()
    normal = Normalizer()
    my_tokenizer = Tokenizer()
    text_normal = normal.normalize(text)
    words = my_tokenizer.tokenize_words(text_normal)
    length = len(words)
    for i in range(0, length):
        if (words[i] in list_elim):
            words[i] = words[i].replace(words[i], "")
        else:
            for j in list_elim:
                if j in words[i]:
                    words[i] = words[i].replace(j, "")

    tokens_without_sw = [
        word.replace("\u200c", " ")
        for word in words
        if (not word in list_stop_words) and (word != "")
    ]


    my_stemmer = FindStems()
    tokens_without_suffix = [
       my_stemmer.convert_to_stem(word) for word in tokens_without_sw
    ]

    tokens_without_prefix=[]
    for token in tokens_without_suffix:
        for item in list_normal_prefix:
            if  token.startswith(item):
                token = token.replace(item,"")
        tokens_without_prefix.append(token)

    for word in tokens_without_prefix:
        if word in dict:
            if dict[word].count(doc) > 0:
                continue
            else:
                dict[word].append(doc)
        if word not in dict:
            dict[word] = [doc]

def AND(x, y):
    list1 = []
    i = 0
    j = 0
    while (i <= x.__len__() - 1) & (j <= y.__len__() - 1):
        if (x[i] == y[j]):
            list1.append(x[i])
            i += 1
            j += 1
        elif (x[i] < y[j]):
            i += 1
        else:
            j += 1
    return list1

def OR(x,y):
    list1=[]
    i=0
    j=0
    while (i<=x.__len__()-1) & (j<=y.__len__()-1) :
        if(x[i]==y[j]) :
            list1.append(x[i])
            i+=1
            j+=1
        elif (x[i]<y[j]):
            list1.append(x[i])
            i+=1
        else:
            list1.append(y[j])
            j+=1
    while (i<=x.__len__()-1):
        list1.append(x[i])
        i+=1
    while (j<=y.__len__()-1):
        list1.append(y[j])
        j+=1

    return list1



def write_read():
    if(exists("file_project/tokeniz.txt")==False):
        read_document()
        with open('file_project/tokeniz.txt', 'w' , encoding="unicode_escape") as file:
            file.write(json.dumps(dict))
        dict1 = dict

    elif(exists("file_project/tokeniz.txt")==True):
        with open("file_project/tokeniz.txt","r",encoding="unicode_escape") as file :
            dict1 = json.load(file)
    print(dict1)
    return dict1


def search(query):
    dict = write_read()
    if (query.find("&") != -1):
        try:
            token1 = query[0:query.find("&") - 1]
            token2 = query[query.find("&") + 2:]
            list_id1 = dict[token1]
            list_id2 = dict[token2]
            return (AND(list_id1, list_id2))
        except:
            return 0
    elif (query.find("|") != -1):
        try:
            token1 = query[0:query.find("|") - 1]
            token2 = query[query.find("|") + 2:]
            list_id1 = dict[token1]
            list_id2 = dict[token2]
            return (OR(list_id1, list_id2))
        except:
            return 0
    else:
        try:
            return dict[query]
        except:
            return 0


