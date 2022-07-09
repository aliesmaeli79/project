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

dict = {}

def read_document():
    number_dic = os.listdir("document")
    stop_words()
    normal_prefix()
    print(list_normal_prefix)
    for doc in range(0, len(number_dic)):
        tokeniz(doc)
    print(dict)

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
    tokens_without_prefix = [
       my_stemmer.convert_to_stem(word) for word in tokens_without_sw
    ]

    # tokens_normal = []
    # for item in list_normal_prefix:
    #     for token in tokens_without_prefix:
    #         if  token.find(item)!=-1:
    #             token.replace(item,"")
    #         else:
    #             tokens_normal.append(token)

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

if __name__ == '__main__':
    start = default_timer()
    read_document()
    end = default_timer()
    print(end-start)
    # if(exists("file_project/tokeniz.txt")==False):
    #     read_document()
    #     with open('file_project/tokeniz.txt', 'w') as file:
    #         file.write(json.dumps(dict))
    # elif(exists("file_project/tokeniz.txt")==True):
    #     file_token = open("file_project/tokeniz.txt","r",encoding="utf8")
    #     dict1 = file_token.read()
    #     print(dict1)
    while (1):
        query = input("Enter query :")
        if (query.find("&")!=-1):
            try:
                token1 = query[0:query.find("&") - 1]
                token2 = query[query.find("&") + 2:]
                list_id1 = dict[token1]
                list_id2 = dict[token2]
                print(AND(list_id1, list_id2))
            except:
                print("سند مورد نظر یافت نشد")
        elif(query.find("|")!=-1):
            try:
                token1 = query[0:query.find("|") - 1]
                token2 = query[query.find("|") + 2:]
                list_id1 = dict[token1]
                list_id2 = dict[token2]
                print(OR(list_id1, list_id2))
            except:
                print("سند مورد نظر یافت نشد")
        else:
            try:
                print(dict[query])
            except:
                print("سند مورد نظر یافت نشد")