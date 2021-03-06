import os
import json
from urllib import response
import requests

# Function to be operated on KB

#Function to download KB
def get_QnA(headers, KB_ID, KB_END_POINT):
    url = "{}/qnamaker/v4.0/knowledgebases/{}/Test/qna".format(KB_END_POINT, KB_ID)
    # print(url)
    response = requests.request("GET", 
            url, 
            headers = headers)

    return json.loads(response.text)['qnaDocuments']

#Function to add list of question
def add_QnA(data, headers, KB_ID, KB_END_POINT):
    
    qnaList = []
    for i in data.index:
        qnaList.append({
            "id": i,
            "answer": data['Answer'][i],
            "source": "Team Channel",
            "questions": [
                data['Question'][i]
            ],
            "metadata": []
        })
    
    body = {
                "add": {
                    "qnaList": qnaList
                }
            }

    url = "{}/qnamaker/v4.0/knowledgebases/{}".format(KB_END_POINT, KB_ID)    
    response = requests.request("PATCH", 
                    url, 
                    headers = headers,
                    json=body)


# Delete data for given index.
def delete_QnA(Ids, headers, KB_ID, KB_END_POINT):

    body = {
            "delete": {
                "ids": Ids
                },
    }

    url = "{}/qnamaker/v4.0/knowledgebases/{}".format(KB_END_POINT, KB_ID)    
    response = requests.request("PATCH", 
                    url, 
                    headers = headers,
                    json=body)


# Function to Publish KB.
def publish_kb(headers, KB_ID, KB_END_POINT):
    url = "{}/qnamaker/v4.0/knowledgebases/{}".format(KB_END_POINT, KB_ID)
    response = requests.request("POST",
                    url, 
                    headers = headers)