import heapq
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity

def k_nearest_points(point, Data, k):
    #initialize heap
    k_nn = []
    heapq.heapify(k_nn)

    for i in range(len(Data)):
        if(len(k_nn) < k):
            heapq.heappush(k_nn, (-euclidean_distances(point, Data[i]), i))
        else:
            heapq.heappushpop(k_nn, (-euclidean_distances(point, Data[i]), i))
    return k_nn



def max_Score(point, Data, k_nn):
    max_score = 0
    idx = 0
    for i in k_nn:
        sim_score = cosine_similarity(point, Data[i[1]])
        if(sim_score[0][0] > max_score):
            max_score = sim_score[0][0]
    return max_score, idx



def check_with_Data(Question_emb, Suggestion_emb, kb_emb, th, th_sugg, k):
    taken_idx = []
    left_idx = []
    # kb_emb = copy.deepcopy(KB_emb)
    # k = 10
    # th = 0.7
    # th_sugg = 0.7

    for i in range(len(Suggestion_emb)):
        
        #ignore suggestion with less score
        if(cosine_similarity(Question_emb[i], Suggestion_emb[i]) < th_sugg):
            continue

        k_nn = k_nearest_points(Suggestion_emb[i], kb_emb, k)
        max_score, idx = max_Score(Suggestion_emb[i], kb_emb, k_nn)
        
        # print(max_score)
        if(max_score >= th):
                left_idx.append((i, idx))
        else:
            taken_idx.append((i, idx))
            kb_emb.append(Suggestion_emb[i])
        
    return taken_idx, left_idx