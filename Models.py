from sentence_transformers import SentenceTransformer
from transformers import RobertaForQuestionAnswering, RobertaTokenizer, pipeline


def sentence_embedding(Data):
    # Load the pre-trained model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Generate Embeddings
    emb_data = model.encode(Data, show_progress_bar=True)

    return emb_data



# # a) Get predictions
def getAnswer(Data):
    
    model_name = "deepset/roberta-base-squad2"

    # b) Load model & tokenizer
    model = RobertaForQuestionAnswering.from_pretrained(model_name)
    tokenizer = RobertaTokenizer.from_pretrained(model_name, TOKENIZERS_PARALLELISM=True)
    
    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

    for i in Data.index:
        QA_input = {
            'question': Data['Question'][i],
            'context': Data['Answer'][i]
        }

        Data['Answer'][i] = nlp(QA_input)['answer']

    return Data