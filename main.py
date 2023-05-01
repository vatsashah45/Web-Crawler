import numpy as np
from sklearn.cluster import KMeans
from indexer import Indexer
from afinn import Afinn
import pandas as pd

numberOfPages = 50

def convertIndex(index: dict[str, list[int]], termIndexMap: dict[str, int]):
    n = len(termIndexMap)
    array = np.zeros([numberOfPages, n], dtype=int)
    for term in index:
        termIndex = termIndexMap[term]
        postingList = index[term]
        for postingId in postingList:
            array[postingId, termIndex] += 1
    return array
        
indexer = Indexer(50)
index, termIndexMap = indexer.build()

X = convertIndex(index, termIndexMap)

kmeans3 = KMeans(n_clusters=3, random_state=0).fit(X)
kmeans6 = KMeans(n_clusters=6, random_state=0).fit(X)

afn = Afinn()

pages = []

for i in range(0, numberOfPages):
    try:
        text = open('pages/' + str(i) + '.txt', 'r').read()
        temp = text.split()
        text = ' '.join(temp)
        pages.append(text)
    except:
        continue

scores = [afn.score(article) for article in pages]
sentiment = ['positive' if score > 0
                        else 'negative' if score < 0
                            else 'neutral'
                                for score in scores]


def printData(pages, scores, sentiment, labels):
    df = pd.DataFrame()
    df['cluster'] = labels
    df['pages'] = pages
    df['scores'] = scores
    df['sentiments'] = sentiment
    print(df)
    map = {}
    for i in range(0, numberOfPages):
        cluster = labels[i]
        if (cluster not in map):
            map[cluster] = {
                "count": 1,
                "totalScore": scores[i],
                "averageScore": scores[i]
            }
        else:
            oldScore = map[cluster]["totalScore"]
            oldCount = map[cluster]["count"]
            
            newScore = oldScore + scores[i]
            newCount = oldCount + 1
            newAverage = newScore/newCount
            map[cluster] = {
                "count": newCount,
                "totalScore": newScore,
                "averageScore": newAverage,
            }
    df1 = pd.DataFrame()
    clusterValues = []
    averageScores = []
    for key in map:
        clusterValues.append(key)
        averageScores.append(map[key]["averageScore"])
    df1["cluster"] = clusterValues
    df1["avg sentiment"] = averageScores
    print(df1)
    return
     
printData(pages, scores, sentiment, kmeans3.labels_)
printData(pages, scores, sentiment, kmeans6.labels_)