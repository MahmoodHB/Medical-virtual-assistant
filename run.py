from flask import Flask, render_template, request
from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
import os
from chatterbot.trainers import ListTrainer
import nltk 
from nltk.collocations import * 
from collections import Counter
import operator
import pandas as pd
import re
from numpy.random import choice
import numpy as np
import sys
from nltk import ngrams
from gensim.models import Phrases
import gensim.models.keyedvectors as word2vec
from nltk import trigrams
import string
import array
import numba
from numba import jit

finalscore = 0
score = 0
response1 = 1
response2 = 0
finalresponse = '請問有摸到乳房腫塊嗎？'
tryresponse1 = 1
t = '上1題'
filenumber=int(os.listdir('saved_conversations')[-1])
filenumber=filenumber+1
file= open('saved_conversations/'+str(filenumber),"w+")
file.write('bot : 1,0 請問有摸到乳房腫塊嗎？\n')
file.close()

app = Flask(__name__)


english_bot = ChatBot('Bot',
             storage_adapter='chatterbot.storage.SQLStorageAdapter',
             logic_adapters=[
   {
       'import_path': 'chatterbot.logic.BestMatch'
   },
   
],
trainer='chatterbot.trainers.ListTrainer')
english_bot.set_trainer(ListTrainer)
trigrams = nltk.collocations.TrigramAssocMeasures()

a = np.zeros((19,10))
array = []
array.append(str(0))
array.append(str(0))
#@jit
def getresponse(ans) :
    return str(english_bot.get_response(ans))
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/get")


def get_bot_response():
    global finalscore
    global response1
    global response2
    global finalresponse
    global tryresponse1
    global score
    global up
    up = 0
    userText = request.args.get('msg')
    userText = userText.replace('一','1')
    userText = userText.replace('二','2')
    userText = userText.replace('兩','2')
    userText = userText.replace('三','3')
    userText = userText.replace('四','4')
    userText = userText.replace('五','5')
    userText = userText.replace('六','6')
    userText = userText.replace('七','7')
    userText = userText.replace('八','8')
    userText = userText.replace('九','9')
    userText = userText.replace('十','10')
    userText = userText.replace('姊','姐')
    answerText = str(response1)+str(response2)+str(userText)
    tryresponse1 = str(response1)
    tryresponse2 = str(response2)
    orgfinalresponse = finalresponse
    
    result = str.find(userText,t)!=-1
    try :
        if result == True : 
            up = up + 1
            nowup = up + 2
            if tryresponse2 != str(0) :
                tryresponse2 = str(int(tryresponse2)-1) 
                response2 = tryresponse2
                nowresponse = "第"+tryresponse1+"."+tryresponse2+"題"
                nowresponse = getresponse(nowresponse)
                finalscore = finalscore - a[int(response1)-1][int(response2)]
                a[int(response1)-1][int(response2)] = 0
                array.append(tryresponse2)
                appendfile= open('saved_conversations/'+str(filenumber),"a")
                appendfile.write('user : '+userText+'\n')
                appendfile.write('目前總分數 : '+str(finalscore)+'\n')
                appendfile.write('-----------------------------------------'+ '\n')
                appendfile.write('問題 : '+nowresponse+'\n')
                appendfile.close()
                finalresponse = nowresponse
                return nowresponse
            else :
                tryresponse1 = str(int(tryresponse1)-1) 
                response1 = tryresponse1
                if array[-nowup] == str(0) :
                    tryresponse2 = array[-nowup]
                    nowresponse = "第"+tryresponse1+"."+tryresponse2+"題"
                    nowresponse = getresponse(nowresponse)
                    finalscore = finalscore - a[int(response1)-1][int(response2)]
                    a[int(response1)-1][int(response2)] = 0
                    array.append(tryresponse2)
                    appendfile= open('saved_conversations/'+str(filenumber),"a")
                    appendfile.write('user : '+userText+'\n')
                    appendfile.write('目前總分數 : '+str(finalscore)+'\n')
                    appendfile.write('-----------------------------------------'+ '\n')
                    appendfile.write('問題 : '+nowresponse+'\n')
                    appendfile.close()
                    finalresponse = nowresponse
                    return nowresponse
                else : 
                    tryresponse2 = array[-nowup]
                    response2 = tryresponse2
                    nowresponse = "第"+tryresponse1+"."+tryresponse2+"題"
                    nowresponse = getresponse(nowresponse)
                    finalscore = finalscore - a[int(response1)-2][int(response2)]
                    a[int(response1)-2][int(response2)] = 0
                    array.append(tryresponse2)
                    appendfile= open('saved_conversations/'+str(filenumber),"a")
                    appendfile.write('user : '+userText+'\n')
                    appendfile.write('目前總分數 : '+str(finalscore)+'\n')
                    appendfile.write('-----------------------------------------'+ '\n')
                    appendfile.write('問題 : '+nowresponse+'\n')
                    appendfile.close()
                    finalresponse = nowresponse
                    return nowresponse
        else :
            up = 0 
            response = getresponse(answerText)
            finalresponse , response1 , response2 , nowscore = response.split(',')
            if response1 == tryresponse1 and response2 <= tryresponse2 :
                print ("geterror")
                response1 = tryresponse1
                response2 = tryresponse2
                finalresponse = orgfinalresponse
                outresponse = '請再回答更精確一些，' + orgfinalresponse
                return outresponse
            elif str(response1) == str(tryresponse1) or str(response1) == str(int(tryresponse1)+1) : 
                score = nowscore
                finalscore=finalscore+int(score)
                array.append(response2)
                if response2 == str(0) and array[-2] == str(0) :
                    a[int(response1)-2][int(response2)] = score
                elif response2 == str(0) and array[-2] != str(0) : 
                    a[int(response1)-2][int(array[-2])] = score
                else : 
                    a[int(response1)-1][int(array[-2])] = score   
                appendfile=os.listdir('saved_conversations')[-1]
                appendfile= open('saved_conversations/'+str(filenumber),"a")
                appendfile.write('user : '+userText+'\n')
                appendfile.write('本題分數 : '+nowscore+'\n')
                appendfile.write('目前總分數 : '+str(finalscore)+'\n')
                appendfile.write('-----------------------------------------'+ '\n')
                appendfile.write('問題 : '+finalresponse+'\n')
                appendfile.close()
                print (response)
                if response1 == str(20) :
                    finalresponse = '您的總分是' + str(finalscore)
                return finalresponse
            else :
                print ("geterror")
                response1 = tryresponse1
                response2 = tryresponse2
                finalresponse = orgfinalresponse
                outresponse = '請再回答更精確一些，' + orgfinalresponse
                return outresponse
    except ValueError :
            print ("ValueError")
            outresponse = '請再回答更精確一些，' + orgfinalresponse
            return outresponse

if __name__ == "__main__":
    app.run("0.0.0.0", debug=False)



