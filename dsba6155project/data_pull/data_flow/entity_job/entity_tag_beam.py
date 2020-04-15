import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromTextWithFilename

import logging
import pathlib
import spacy
import os


logging.basicConfig(level=logging.INFO)

class SpacyNLP():
    nlp = spacy.load("en_core_web_md")

    def getPathToRequirementsFile(self):
        return os.path.abspath(os.path.join(pathlib.Path(__file__).parent.absolute() , "setup.py"))

    @staticmethod
    def _tag(elem):
        filen , sent = elem
        doc = SpacyNLP.nlp(sent)
        for ent in doc.ents:
            yield ( "*".join((filen ,  ent.label_ , ent.text)), 1)

    @staticmethod
    def _count(elem):
        filen_tag_text_label , counts = elem
        filen , label  , text = filen_tag_text_label.split("*")
        return [{"file" : filen ,"label":label,"text" : text , "count":sum(counts)}]

    def getSchema(self):
        return "file:STRING, label:STRING, text:STRING, count:FLOAT64"

    def __init__(self , pathToFiles, biqTable):
        self.magURL = "http://magnitude.plasticity.ai/glove/light/glove-lemmatized.6B.200d.magnitude"

        self.pipe = beam.Pipeline(options=PipelineOptions([
            '--direct_num_workers', '2',
            "--runner", "DataFlowRunner",
            "--project", "dsba6155p",
            "--region" , "us-east1",
            "--temp_location", "gs://dsba6155pdatabucket/dataflow_temp_location/",
            "--setup_file" , self.getPathToRequirementsFile()
            ]))
        (
            self.pipe
            | "Read Files" >> ReadFromTextWithFilename(pathToFiles)
            | "Entity Tag Lines" >> beam.ParDo(SpacyNLP._tag)
            | "Group By Key" >> beam.GroupByKey()
            #| "Map to Ones" >> beam.Map(lambda x: (x , len(set(x[1]))))
            #| "Group By File and Type" >> beam.GroupByKey()
            | "Count" >> beam.ParDo(SpacyNLP._count)
            #| "Write to File" >> beam.io.WriteToText("outputf")
            | "Write CSV to biqquery" >> beam.io.WriteToBigQuery(
                table=biqTable,
                schema=self.getSchema(),
                write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                # create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
            )
        )
        rs = self.pipe.run()
        rs.wait_until_finish()


if __name__ == "__main__":
    projectid = "dsba6155p"
    datasetid = "nlpdataset"
    tablename = "document_entities"
    ptf ="gs://dsba6155pdatabucket/download/**"
    compute_table_name = f"{projectid}:{datasetid}.{tablename}"
    #ptf = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    SpacyNLP(ptf , compute_table_name)
