import pandas as pd
import json

# function to join array of string
def reply_to_paragraph(Reply):
    return " ".join(Reply)

def merge_reply(Data):
    
    #initialize Output variable to store merged reply
    Output = pd.DataFrame(columns=['Question', 'Reply'])

    for i in Data.index:
        # Initialize Reply
        Reply = Data.at[i, 'Reply']
        
        # check for type of varible if string convert to list
        if(isinstance(Reply, str)):
            Reply = json.loads(Reply)

        # replies are in reverse order.
        Reply.reverse()
        Reply = reply_to_paragraph(Reply)

        Question = Data.at[i, 'Question']
        
        # if Question or reply is empty then change the value to pd.NA
        if(Reply == '' or Question == '' ):
            Question = pd.NA

        # add question and reply to Output Variable
        Output.loc[len(Output.index)] = [Question, Reply]

    #drop row with Nan
    Output = Output.dropna(how='any')

    return Output

# Function to merge DataFrame having same columns.
def merge_df(data1, data2):

    # Initialize data to store output
    data = pd.DataFrame(columns=data1.columns)
    
    idx = 0
    # Add data1 into data
    for i in data1.index:
        data.loc[idx] = [data1['Question'][i], data1['Reply'][i]]
        idx += 1

    # Add data2 into data
    for i in data2.index:
        data.loc[idx] = [data2['Question'][i], data2['Reply'][i]]
        idx += 1
    
    return data