import pymongo

client = pymongo.MongoClient("mongodb+srv://flavouredwaffles:VE24bVpDgPKOnpFr@cluster-hh.4k34p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster-hh")
db = client.sample_mflix
collection = db.movies

from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embedding(text):
    return model.encode(text)


# for i in collection.find({'plot' : {'$exists': True}}).limit(50):
#     print(i['title'])
#     i['plot_embed'] = get_embedding(i['plot']).tolist()
#     collection.replace_one({'_id': i['_id']}, i)



QUERY = "romance and love"

rez = collection.aggregate([
    
   { "$vectorSearch": {
            "queryVector" :get_embedding(QUERY).tolist(),
            "path": "plot_embed",
            "numCandidates": 10,
            "limit" : 4,
            "index" : "sem_search"

    }}
])


for idx, i in enumerate(rez):
    print(f"{idx}) Movie name: {i['title']},   Movie plot: {i['plot']}\n")