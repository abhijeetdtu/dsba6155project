import os
import pandas as pd
import pathlib


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance


@singleton
class Model():

    def __init__(self):
        #projectId = "dsba6155p"
        #datasetTable = "nlpdataset.document_entities"
        #__file__ = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\web\\dashapps\\example\\example.py"
        fpath = os.path.join(pathlib.Path(__file__).parent.parent.parent.absolute() , "staticdata")
        dfp = os.path.join(fpath, "outputs_document_entities_export.csv")

        lbp = os.path.join(fpath, "label_descriptions.csv")

        #df = pd.read_gbq(query=f"SELECT * from {projectId}.{datasetTable}",project_id=projectId)
        df = pd.read_csv(dfp , dtype={"count":"int16" , "file" : "category" , "text" : "category" , "label" : "category"})
        df["category"] = df["file"].apply(lambda x: x.split("/")[-1].split("_")[0]).astype("category")

        ldesc = pd.read_csv(lbp , dtype={"label":"category" , "label_description":"category"})
        ldesc.index = ldesc["label"]

        ldesc = ldesc.drop(["label"] , axis=1)
        df = pd.merge(df , ldesc , on="label")

        self.df = df
        self.ldesc = ldesc
