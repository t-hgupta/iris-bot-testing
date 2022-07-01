from sentence_transformers import SentenceTransformer

def sentence_embedding(Data):
    # Load the pre-trained model
    model = SentenceTransformer('all-mpnet-base-v2')

    # Generate Embeddings
    emb_data = model.encode(Data, show_progress_bar=True)

    return emb_data