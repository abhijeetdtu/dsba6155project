import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText , WriteToText


from dsba6155project.constants import Constants
import os
import re

files = [ os.path.abspath(os.path.join(Constants.DATA_PATH,f)) for f in os.listdir(Constants.DATA_PATH)]

options = PipelineOptions()
pipelineLoad = beam.Pipeline(options=options)

books = pipelineLoad | beam.Create(files[:2])

import nltk


from sklearn.feature_extraction.text import CountVectorizer

corpus = []
pos_results = (books
    | "Read Files" >> ReadAllFromText()
    | "Add to Corpus" >> beam.ParDo(lambda x: corpus.append(x))
)


results = pipelineLoad.run()
results.wait_until_finish()

corpus = "".join(corpus).split(".")

pipelineClean = beam.Pipeline(options=options)
corpus_beam = pipelineClean | beam.Create(corpus[:1000])

def clean_line(line):
    print(line)
    return [line.strip("\r\n ")]

(corpus_beam
    | beam.ParDo(clean_line)
    | WriteToText("allLines")
)

pipelineClean.run().wait_until_finish()
