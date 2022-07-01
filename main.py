# import unidecode
# import re
# from flashtext import KeywordProcessor
# import pandas as pd
# import sentence_transformers
# pip freeze > requirements.txt


from crypt import methods
from urllib import response
from wsgiref import headers


from requests import request
import requests
from processing import preprocess_text
from LoadDataset import loadDataset
from mergeReply import merge_reply, merge_df
from Models import sentence_embedding 
from utilFunct import check_with_Data
from utility_KB import get_QnA, add_QnA

import os
import time

import copy
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)



#Authentication
# client = QnAMakerClient(endpoint=authoring_endpoint, credentials=CognitiveServicesCredentials(subscription_key))

@app.route("/")
def hello():
    return "hello"

@app.route("/", methods = ['GET'])
def runModel():
    Data_FC = loadDataset('../Final_Code/Data_textual/Data_FC.CSV', 'csv')
    Data_G = loadDataset('../Final_Code/Data_textual/Data_G.CSV', 'csv')

    #Knowledge Base Data
    Data_KB = loadDataset('../Final_Code/Data_textual/KnowledgeBase.xlsx', 'excel')

    Data_FC = merge_reply(Data_FC)
    Data_G = merge_reply(Data_G)

    Data = merge_df(Data_FC, Data_G)
    # generalize question and answer with the help of existing model

    #output from models
    Ques_Sugg = loadDataset('../Final_Code/Data_textual/Question_Suggestion.xlsx', 'excel')

    #Preprocessing Suggestion and question
    Suggestion = []
    Question = []
    for i in Ques_Sugg.index:
        Suggestion.append(preprocess_text(Ques_Sugg.at[i, 'Suggestion'], 1))
        Question.append(preprocess_text(Ques_Sugg.at[i, 'Question'], 1))
    
    Question_KB = []
    for i in Data_KB.index:
        Question_KB.append(preprocess_text(Data_KB.at[i, 'Question'], 1))

    # dimension of embedding vector
    dim = 768

    #Sentence embedding for each Data
    Suggestion_emb = [i.reshape(1, dim) for i in sentence_embedding(Suggestion)]
    Question_emb = [i.reshape(1, dim) for i in sentence_embedding(Question)]
    KB_emb = [i.reshape(1, dim) for i in sentence_embedding(Question_KB)]

    taken_idx, left_idx = check_with_Data(Question_emb, Suggestion_emb, KB_emb, .7, .7, 10)

    KB_copy = copy.deepcopy(Data_KB)

    for i in range(len(taken_idx)):
        KB_copy.loc[len(KB_copy)] = [Ques_Sugg.at[taken_idx[i][0], 'Suggestion'], '', '', '', '', '', '', '', '', '']

    return { "value" :KB_copy.to_dict('records') }



###post request
@app.route("/", methods = ['POST'])
def post_request():
    
    #get data
    Data = pd.DataFrame(request.get_json())
    # Data = loadDataset('../Final_Code/Data_textual/Data_FC.CSV', 'csv')
    
    #Knowledge Base Data
    headers = {
        "Ocp-Apim-Subscription-Key": request.headers["KB_Key"]
    }
    # Data_KB = loadDataset('../Final_Code/Data_textual/KnowledgeBase.xlsx', 'excel')
    Data_KB = pd.DataFrame(get_QnA(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"]))
    
    #merge reply
    Data = merge_reply(Data)
    # print(Data_KB)

    # generalize question and answer with the help of existing model


    #output from models
    # Ques_Sugg = loadDataset('../Final_Code/Data_textual/Question_Suggestion.xlsx', 'excel')
    # Ques_Sugg = Data

    #Preprocessing Suggestion and question
    # Suggestion = []
    # Question = []
    # for i in Ques_Sugg.index:
    #     Suggestion.append(preprocess_text(Ques_Sugg.at[i, 'Suggestion'], 1))
    #     Question.append(preprocess_text(Ques_Sugg.at[i, 'Question'], 1))
    
    # Question_KB = []
    # for i in Data_KB.index:
    #     Question_KB.append(preprocess_text(Data_KB.at[i, 'Question'], 1))

    # # dimension of embedding vector
    # dim = 768

    # #Sentence embedding for each Data
    # Suggestion_emb = [i.reshape(1, dim) for i in sentence_embedding(Suggestion)]
    # Question_emb = [i.reshape(1, dim) for i in sentence_embedding(Question)]
    # KB_emb = [i.reshape(1, dim) for i in sentence_embedding(Question_KB)]

    # taken_idx, left_idx = check_with_Data(Question_emb, Suggestion_emb, KB_emb, .7, .7, 10)

    # KB_copy = copy.deepcopy(Data_KB)

    # for i in range(len(taken_idx)):
    #     KB_copy.loc[len(KB_copy)] = [Ques_Sugg.at[taken_idx[i][0], 'Suggestion'], '', '', '', '', '', '', '', '', '']


    return "HEllo"

if __name__ == "__main__":
    app.run(debug = True)