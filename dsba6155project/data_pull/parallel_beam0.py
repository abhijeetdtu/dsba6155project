import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText


from dsba6155project.constants import Constants
import os
import re


from collections import defaultdict

import numpy as np
from scipy.sparse import vstack
from sklearn.feature_extraction.text import HashingVectorizer
vectorizer = HashingVectorizer(n_features=20000 ,strip_accents='unicode'
                            , stop_words="english" , norm=None)



class PerformIncrementalPCA(beam.DoFn):

    def process(self,elem):
        ipca = IncrementalPCA(n_components=n_components, batch_size=10)
        X_ipca = ipca.fit_transform(X)

class ReadBooks(beam.DoFn):

    def process(self,elem):
        return ReadFromTextWithFilename(elem)

class Hashing(beam.DoFn):
    def process(self,doc):
        #print(doc)
        filen , doc = doc
        vector = np.sum(np.abs(vectorizer.fit_transform(doc)) , axis=0).tolist()[0]
        vector = [str(v) for v in vector]
        return [filen + "," + ",".join(vector)]


def npsum(values):
    print(values)
    return np.sum(values , axis=0)


def stacking(values):
    if len(values) == 0:
        return

    print(values)
    f,mat = values

    stack.append(mat)
    return stack

class Save(beam.DoFn):
    def process(self,mtx):
        global dtm
        dtm = mtx
        return mtx

dtm = None

from apache_beam.io.filesystems import FileSystems
from apache_beam.io.textio import ReadFromTextWithFilename , WriteToText
#fnames = os.listdir(Constants.DATA_PATH)
#files = [ os.path.abspath(os.path.join(Constants.DATA_PATH,f)) for f in fnames]
#keyedFiles = list(zip(fnames , files))


#books = pipeline
stack = []
#path = FileSystems.match("C:/Users/Abhijeet/Documents/GitHub/dsba6155project/dsba6155project/data/hinduism_A History of Indian Philosophy Volume 1.txt")


def GenerateSchema():
    import pandas as pd
    df = pd.read_csv("output-00000-of-00001")
    with open("biqschema", "w") as f:
        f.write( "book:STRING,"+",".join([f"{i}:INTEGER" for i in range(df.shape[1])]) )

def GetSchema():
    return open("./biqschema", "r").read()

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
        # | "Write CSV to biqquery" >> beam.io.WriteToBigQuery(
        #     table=compute_table_name,
        #     schema=GetSchema()
        # )
        | "Write to file" >> WriteToText(raw_output)
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
    pathToFiles= "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    projectid = "dsba6155p"
    datasetid = "nlpdataset"
    tablename = "word_count_table"
    #pathToFiles ="gs://dsba6155pdatabucket/download/**"
    compute_table_name = f"{projectid}:{datasetid}.{tablename}"
    RunPipeline(pathToFiles,compute_table_name)
    #GenerateSchema()
