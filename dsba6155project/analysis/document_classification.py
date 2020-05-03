import os
import pathlib

def _getDataPath():
    try:
        __file__
        p = os.path.join(pathlib.Path(__file__).parent.parent.absolute())
    except:
        p =  os.path.join(pathlib.Path(".").absolute() , "dsba6155project")

    return os.path.join(p, "data" , "outputs_document_entities_export.csv")

dfpath = _getDataPath()


import numpy as np
import pandas as pd

df = pd.read_csv(dfpath)
df["label"].unique()
df = df[~df["label"].isin(["CARDINAL" , "QUANTITY" , "TIME" , "PERCENT" ,"DATE" ,"LAW" , "ORDINAL"])]
df["category"] = df.iloc[:,0].apply(lambda x: x.split("/")[-1].split("_")[0])
df["category"] = df["category"].replace("jews" , "jewish")

df

df = df[df["text"].str.match("^[xvi]{2,5}$") == False]
# to_exclude = ["A Short History of the World"
#             , "Plant Lore Legends and Lyrics"
#             ,"The Ballad of the White Horse"
#             ,"Nicolo Paganini His Life and Work"
#             ,"Political and Literary essays 19081913"
#             ,"The Canterbury Tales and Other Poems"
#             ]
#
# df.shape
# df[df["file"].str.contains("|".join(to_exclude))]
#df["file"].apply(lambda x: x.split("/")[-1]).unique()

distinctBooks = df["file"].unique()
bybook = df.groupby(["file" , "text"]).agg(totcount = ("count" , "sum")).unstack().reset_index()
bybook.columns = bybook.columns.droplevel(0)

toDrop = list(bybook.isna().sum()[bybook.isna().sum() > len(distinctBooks)*0.8].index)
bybook = bybook.drop(toDrop , axis=1)

bybook = bybook.fillna(0)


#bybook["rowsum"] = bybook.iloc[:,1:].apply(lambda x: np.sum(x) , axis=1)
#bybook.iloc[:,1:] = bybook.iloc[:,1:].apply(lambda x : x/bybook.iloc[:,-1])
#bybook

bybook["rowsum"] = bybook.iloc[: , 1:-2].apply(lambda x : np.sum(x), axis=1)
bybook.iloc[: , 1:-2] =  bybook.iloc[: , 1:-2].apply(lambda x : x / bybook["rowsum"] )

bybook["category"] = bybook.iloc[:,0].apply(lambda x : x.split("/")[-1].split("_")[0])


#bybook[bybook.mean() > 1]
#mdf = bybook.drop(["rowsum"] , axis=1)
mdf = bybook
X = mdf.iloc[: , 1:].drop(["rowsum","category"] , axis=1)
#X = X.fillna(X.mean())
y = mdf["category"]

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

clf = RandomForestClassifier()
np.mean(cross_val_score(clf,X,y, scoring="accuracy" , cv=10))

# X = X_transdf.drop(["cat"] , axis=1)
# y = X_transdf["cat"]

clf.fit(X,y)

featureimpdf = pd.DataFrame({"imp" : clf.feature_importances_ , "col" : X.columns})
featureimpdf = featureimpdf.sort_values("imp" , ascending=False).head(100)
featureimpdf["col"] = pd.Categorical(featureimpdf["col"], categories=featureimpdf["col"].values)
ggplot(featureimpdf , aes(x="col" , y="imp")) + geom_col() + coord_flip() + theme(text = element_text(size=5))


from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

Xclust = StandardScaler().fit_transform(X)
kmeansmodel = KMeans(n_clusters=7)
kmeansmodel.fit(X)

preds = kmeansmodel.predict(X)

X["pred_cat"] = preds
X["cat"] = y
X[["pred_cat" , "cat"]]

clusterplotdf = X.groupby(["pred_cat" , "cat"]).agg("count").reset_index().iloc[:,0:3]
#clusterplotdf["comp_0"] = clusterplotdf["comp_0"].astype("category")
#clusterplotdf["comp_o_norm"] = clusterplotdf[["pred_cat" , "comp_0"]].groupby("pred_cat").transform(lambda x : (x-x.mean())/x.std())
clusterplotdf.columns = ["pred_cat" , "cat" , "count"]

ggplot(clusterplotdf , aes(x="pred_cat" , y="cat" , fill="count")) + geom_tile()
from sklearn.metrics import confusion_matrix


clf = RandomForestClassifier()
cross_val_score(clf,X,y, scoring="accuracy" , cv=10)

from keras.wrappers.scikit_learn import KerasClassifier


from keras import Sequential
from keras.layers import Dense

def build_model(colnum,y_unique):
    model = Sequential()
    model.add(Dense(units=colnum , activation="relu"))
    model.add(Dense(units=int(colnum/2) , activation="relu"))
    model.add(Dense(units=y_unique))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


clf = KerasClassifier(build_fn =build_model , colnum=X.shape[1] , y_unique=len(y.unique()))


from sklearn.model_selection import StratifiedKFold

#skf = StratifiedKFold(n_splits=5)
cross_val_score(clf,X,y, scoring="accuracy" , cv=10)
