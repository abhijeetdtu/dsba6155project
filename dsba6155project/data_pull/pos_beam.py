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

import nltk

def POS(line):
    text = nltk.word_tokenize(line)
    tags = nltk.pos_tag(text)
    return tags

def CountTags(wordtag):
    word, tag = wordtag

def count_ones(word_ones):
      (word, ones) = word_ones
      return (word, sum(ones))

pos_results = (books
    | "Read Files" >> ReadAllFromText()
    | "POS" >> beam.ParDo(POS)
    | beam.GroupByKey()
    | "Count" >> beam.ParDo(count_ones)
    | 'write words' >> beam.io.WriteToText("Pos_Counts")
)


results = pipeline.run()
results.wait_until_finish()
