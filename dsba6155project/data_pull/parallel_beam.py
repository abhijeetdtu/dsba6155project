import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText


from dsba6155project.constants import Constants
import os
import re

files = [ os.path.abspath(os.path.join(Constants.DATA_PATH,f)) for f in os.listdir(Constants.DATA_PATH)]

options = PipelineOptions()
pipeline = beam.Pipeline(options=options)

books = pipeline | beam.Create(files)

from collections import defaultdict

import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

wc = defaultdict(int)

def wordClean(word):
    return re.subn("[;,]+" , "" , word)

def wordCount(word):
    wc[word] += 1

def splitLines(line):
    text = nltk.word_tokenize(line.lower().strip("\r\n"))
    filtered_sentence = [w for w in text if not w in stop_words]
    return filtered_sentence


(books
    | "Read Files" >> ReadAllFromText()
    | "Split Lines" >> beam.ParDo(splitLines)
    | "Clean Words" >> beam.ParDo(wordClean)
    | "Count Words" >> beam.ParDo(wordCount)
)


result = pipeline.run()
result.wait_until_finish()

import pandas as pd
df = pd.DataFrame({"word" : list(wc.keys()) , "count" : list(wc.values())})

#df.to_json("./test.json" , orient="records")
#df.sort_values("y" , ascending=False).iloc[:500].to_json("./test.json" , orient="records")
df.to_gbq("nlp.wordcounts" , "dsba6155" , if_exists='append')
