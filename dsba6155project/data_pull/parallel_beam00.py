import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText


from dsba6155project.constants import Constants
import os
import re


from collections import defaultdict

import numpy as np
from scipy.sparse import vstack
from sklearn.decomposition import IncrementalPCA
from sklearn.feature_extraction.text import HashingVectorizer
vectorizer = HashingVectorizer(n_features=20000 ,strip_accents='unicode'
                            , stop_words="english" , norm=None)


class Hashing(beam.DoFn):
    def process(self,doc):
        #print(doc)
        filen , doc = doc
        vector = np.sum(np.abs(vectorizer.fit_transform(doc)) , axis=0).tolist()[0]
        vector = [str(v) for v in vector]
        return [ filen +"," + ",".join(vector)]

class StackingFn(beam.CombineFn):
  def create_accumulator(self):
    return ""

  def add_input(self, arr, input):
    return arr + "\n" + input

  def merge_accumulators(self, accumulators):
    return  "\n".join(accumulators)

  def extract_output(self, arr):
    return arr

import json
import pandas as pd
from sklearn.decomposition import IncrementalPCA
from apache_beam.io.filesystems import FileSystems
from apache_beam.io.textio import ReadFromTextWithFilename , WriteToText


def GetSchema():
    return "book:STRING, "+", ".join([f"W{i}:FLOAT64" for i in range(NCOMPONENTS)])

def RunPCA(X):
    from io import StringIO
    sdata = StringIO(X)
    X = pd.read_csv(sdata , header=None)
    ipca = IncrementalPCA(n_components=NCOMPONENTS, batch_size=50)
    comp = ipca.fit_transform(X.drop([X.columns[0]] , axis=1))
    df = pd.DataFrame(comp,columns=[f"W{i}" for i in range(comp.shape[1])])
    df["book"] = X.iloc[:,0]
    js = json.loads(df.to_json(orient="records"))
    print(js[0])
    return js
    #for i,r in enumerate(comp):
    #    yield X.iloc[i , 0] + "," +",".join([str(v) for v in r])

def BuildPipeline(pathToFiles , compute_table_name):
    raw_output = "output-raw"
    final_output = "output-final"
    options = PipelineOptions()
    #pathToFiles= "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    pipeline = beam.Pipeline(options=options)
    vectors = (pipeline
        | "Read Files" >> ReadFromTextWithFilename(pathToFiles)
        | "Group by File" >> beam.GroupByKey()
        | "Hashing Vectors" >> beam.ParDo(Hashing())
        | "Stack Em UP" >> beam.CombineGlobally(StackingFn())
        | beam.ParDo(RunPCA)
        | "Write CSV to biqquery" >> beam.io.WriteToBigQuery(
            table=compute_table_name,
            schema=GetSchema(),
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            # create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
        #| "Write to file" >> WriteToText(raw_output)
        #|
        #| "Save" >> beam.ParDo(Save())
    )
    return pipeline



def RunPipeline(pathToFiles , compute_table_name):
    pipeline = BuildPipeline(pathToFiles , compute_table_name)
    result = pipeline.run()
    result.wait_until_finish()

#df.to_gbq("nlp.wordcounts" , "dsba6155" , if_exists='append')

if __name__ == "__main__":
    #pathToFiles= "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    projectid = "dsba6155p"
    datasetid = "nlpdataset"
    tablename = "document_vectors"
    NCOMPONENTS = 100
    pathToFiles ="gs://dsba6155pdatabucket/download/**"
    compute_table_name = f"{projectid}:{datasetid}.{tablename}"
    RunPipeline(pathToFiles,compute_table_name)
    #GenerateSchema()
