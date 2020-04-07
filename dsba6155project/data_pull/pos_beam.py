import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromText, ReadAllFromText


from dsba6155project.constants import Constants
import os
import re

files = [ os.path.abspath(os.path.join(Constants.DATA_PATH,f)) for f in os.listdir(Constants.DATA_PATH)]

options = PipelineOptions()
pipeline = beam.Pipeline(options=options)

books = pipeline | beam.Create(files[:10])

import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def POS(line):
    text = nltk.word_tokenize(line.lower())
    filtered_sentence = [w for w in text if not w in stop_words]
    tags = nltk.pos_tag(filtered_sentence)
    return tags


def count_ones(word_ones):
    print(word_ones)
    (word, tag) , ones = word_ones
    return ((word, tag) , sum(ones))

pos_results = (books
    | "Read Files" >> ReadAllFromText()
    | "POS" >> beam.ParDo(POS)
    #| "Map" >> beam.ParDo(lambda tag : tag[0] + "-" +tag[1])
    #| "Group" >> beam.GroupByKey()
    #|  beam.combiners.Count.PerElement()
    | "Counting ">> beam.ParDo(count_ones)
    | 'write words' >> beam.io.WriteToText("Pos_Counts")
)


results = pipeline.run()
results.wait_until_finish()
