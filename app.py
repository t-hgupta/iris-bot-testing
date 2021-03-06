# pip freeze > requirements.txt


from processing import preprocess_text
from LoadDataset import loadDataset
from mergeReply import merge_reply, merge_df
from Models import sentence_embedding, getAnswer 
from utilFunct import check_with_Data
from utility_KB import get_QnA, add_QnA, delete_QnA, publish_kb

import os
import time

import requests
import copy
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)



os.environ["TOKENIZERS_PARALLELISM"] = "false"


@app.route("/")
def hello():
    return "Hey, It's working"

# Get request for offline data
@app.route("/run", methods = ['GET'])
def runModel():
    Data_FC = loadDataset('../Data_textual/Data_FC.CSV', 'csv')
    Data_G = loadDataset('../Data_textual/Data_G.CSV', 'csv')

    #Knowledge Base Data
    Data_KB = loadDataset('../Data_textual/KnowledgeBase.xlsx', 'excel')

    Data_FC = merge_reply(Data_FC)
    Data_G = merge_reply(Data_G)

    Data = merge_df(Data_FC, Data_G)
    # generalize question and answer with the help of existing model

    #output from models
    Ques_Sugg = loadDataset('../Data_textual/Question_Suggestion.xlsx', 'excel')

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

    Data_taken = pd.DataFrame(columns=['Question', 'Answer'])
    for i in range(len(taken_idx)):
        Data_taken.loc[i] = [Ques_Sugg.at[taken_idx[i][0], 'Suggestion'], Ques_Sugg.at[taken_idx[i][0], 'Reply']]
    
    #Generate Answers
    # Data_taken = getAnswer(Data_taken)

    # Add Data to KB
    # headers = {
    #     "Ocp-Apim-Subscription-Key": request.headers["KB_Key"]
    # }
    # add_QnA(Data_taken, headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])

    # publish_kb(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])

    return { "Added" :Data_taken.to_dict('records') }


###post request

#######################-----POST request to add file with Question and Answer-------##################

@app.route("/addFile", methods = ['POST'])
def addFile():
    headers = {
        "Ocp-Apim-Subscription-Key": request.headers["KB_Key"]
    }
    
    # get all data of KB
    Data_KB = pd.DataFrame(get_QnA(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"]))

    # Add iris Bot KB data
    add_QnA(Data_KB, headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])

    publish_kb(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])
    
    return 'Added file Data in knowledge Base'



#######################-----POST request to update team channel Data-------##################

@app.route("/teamData", methods = ['POST'])
def teamData():
    
    #get data
    Data = pd.DataFrame(request.get_json())
    # Data = loadDataset('../Data_textual/Data_FC.CSV', 'csv')
    
    #Knowledge Base Data
    headers = {
        "Ocp-Apim-Subscription-Key": request.headers["KB_Key"]
    }
    # Data_KB = loadDataset('../Data_textual/KnowledgeBase.xlsx', 'excel')
    Data_KB = pd.DataFrame(get_QnA(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"]))
    print(Data_KB.columns)
    #merge reply
    Data = merge_reply(Data)

    # prepare data for deepask api
    Data_DAA = pd.DataFrame(columns=['Paragraph'])
    for i in Data_DAA.index:
        Data_DAA.loc[i] = preprocess_text(' '.join([Data.at[i, 'Question'], Data.at[i, 'Reply']]), 0)

    # generalize question and answer with the help of existing model


    #output from models
    Ques_Sugg = loadDataset('../Data_textual/Question_Suggestion.xlsx', 'excel')
    # Ques_Sugg = Data

    #Preprocessing Suggestion and question
    Suggestion = []
    Question = []
    for i in Ques_Sugg.index:
        Suggestion.append(preprocess_text(Ques_Sugg.at[i, 'Suggestion'], 1))
        Question.append(preprocess_text(Ques_Sugg.at[i, 'Question'], 1))
    
    Question_KB = []
    for i in Data_KB.index:
        Question_KB.append(preprocess_text(Data_KB.at[i, 'questions'], 1))

    #dimension of embedding vector
    dim = 768

    #Sentence embedding for each Data
    Suggestion_emb = [i.reshape(1, dim) for i in sentence_embedding(Suggestion)]
    Question_emb = [i.reshape(1, dim) for i in sentence_embedding(Question)]
    KB_emb = [i.reshape(1, dim) for i in sentence_embedding(Question_KB)]

    taken_idx, left_idx = check_with_Data(Question_emb, Suggestion_emb, KB_emb, .7, .7, 10)

    Data_taken = pd.DataFrame(columns=['Question', 'Answer'])
    for i in range(len(taken_idx)):
        Data_taken.loc[i] = [Ques_Sugg.at[taken_idx[i][0], 'Suggestion'], Ques_Sugg.at[taken_idx[i][0], 'Reply']]
    
    #Generate Answers
    # Data_taken = getAnswer(Data_taken)

    # print(Data_taken)
    add_QnA(Data_taken, headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])

    publish_kb(headers, request.headers["KB_ID"], request.headers["KB_END_POINT"])

    return "Data is updated"

#######################-----POST request for new Message on team channel-------##################

@app.route("/newMessage", methods = ['POST'])
def newMessage():
    
    #get data
    Data = pd.DataFrame(request.get_json())
    # Data = loadDataset('../Data_textual/Data_FC.CSV', 'csv')

    #merge reply
    Data = merge_reply(Data)

    # prepare data for deepask api
    Data_DAA = pd.DataFrame(columns=['Paragraph'])
    for i in Data_DAA.index:
        Data_DAA.loc[i] = preprocess_text(' '.join([Data.at[i, 'Question'], Data.at[i, 'Reply']]), 0)

    # generalize question and answer with the help of existing model


    # Seach for most similar question in Knowledge Base.
    
    # if similar refer to iris bot.

    # else add to Database
    # Create Database of unanswered question and new question
    # columns = ["messageId", "Question", "Answer" , "isAnswered", "isSent"]
    
    return "new message added"



#######################-----POST request to check unanswered questions-------##################

@app.route('/checkQuestions', methods=['POST'])
def checkQuestions():
    # Retrieve all tha unaswered questions

    # if isAnswered 1 then update to Knowledge Base

    # else check isSent if 1 then continue

    #else send the questions to SME and mark it 1.

    return "checked"



#######################-----POST request to update unanswered questions-------##################

@app.route('/updateAnswer', methods=['POST'])
def updateAnswer():

    # Request body contains index, questions and answers

    # add it to storage

    return "updated"


if __name__ == "__main__":
    app.run(debug = True)