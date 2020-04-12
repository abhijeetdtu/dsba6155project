import pandas as pd
df = pd.read_csv("output-00000-of-00001" ,header=None)
df.shape

df.loc[:,0] = df.loc[:,0].str.split("\\").apply(lambda x : x[-1])
#df[0]

#df[0]
from plotnine import *
from sklearn.decomposition import PCA

pcam = PCA()
t = pcam.fit_transform(df.iloc[:,1:])

pcam.n_components_
pcar = pd.DataFrame({"explained" : np.cumsum(pcam.explained_variance_ratio_) , "comp":np.arange(0,pcam.n_components_ , 1)})

ggplot(pcar , aes(x="comp" , y="explained")) + geom_line()


pcaf = PCA(n_components=32)
t = pcaf.fit_transform(df.iloc[:,1:])

ftdf = pd.DataFrame(t)
ftdf["book"] = df[0]

from sklearn.metrics import pairwise_distances


def plot(metric , df):
    dists = pairwise_distances(df.drop(["book"] , axis=1).values , metric=metric)

    tdf = pd.DataFrame(dists , columns=df["book"].values , index=df["book"].values)
    tdf = pd.melt(tdf.reset_index(),id_vars='index')
    tdf["religion"] = tdf["index"].str.split("_").apply(lambda x:x[0])
    #dists[24,8:20]
    p = ggplot(tdf[tdf["religion"] == "fantasy"] , aes(x="index" , y="variable" , fill="value")) +geom_tile()
    print(metric)
    #df.to_json("./test.json" , orient="records")
    #df.sort_values("y" , ascending=False).iloc[:500].to_json("./test.json" , orient="records")
    return p

plts = [plot(m , ftdf) for m in  ['braycurtis', 'canberra', 'chebyshev', 'correlation', 'hamming', 'jaccard', 'kulsinski', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean', 'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule']]

print(plts[1])
for p in plts:
    print(p)


dists = pairwise_distances(df.drop([0] , axis=1).values , metric="canberra")
tdf = pd.DataFrame(dists , columns=df["book"].values , index=df["book"].values)
