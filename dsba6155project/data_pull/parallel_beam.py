import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText


from dsba6155project.constants import Constants
import os
import re

files = [ os.path.abspath(os.path.join(Constants.DATA_PATH,f)) for f in os.listdir(Constants.DATA_PATH)]

options = PipelineOptions()
pipeline = beam.Pipeline(options=options)

books = pipeline | beam.Create(files[:3])

from collections import defaultdict


wc = defaultdict(int)

def wordClean(word):
    return re.subn("[;,]+" , "" , word)

def wordCount(word):
    wc[word] += 1

def splitLines(line):
    return line.lower().strip("\r\n").split(" ")


(books
    | "Read Files" >> ReadAllFromText()
    | "Split Lines" >> beam.ParDo(splitLines)
    | "Clean Words" >> beam.ParDo(wordClean)
    | "Count Words" >> beam.ParDo(wordCount)
)


result = pipeline.run()
result.wait_until_finish()

import pandas as pd
df = pd.DataFrame({"words" : list(wc.keys()) , "counts" : list(wc.values())})

df.sort_values("counts" , ascending=False).iloc[50:100]
