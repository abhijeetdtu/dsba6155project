import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromTextWithFilename

import logging
import pathlib
import spacy
import os


logging.basicConfig(level=logging.INFO)


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
      self.nlp = spacy.load("en_core_web_md")

class TagDoFn(beam.DoFn):

    def process(self,elem):
        nlp = Model().nlp
        filen , sent = elem
        doc = nlp(sent.lower())
        for ent in doc.ents:
            yield ( "_ESC_VAL_".join((filen ,  ent.label_ , ent.text)), 1)

class SpacyNLP():

    def getPathToRequirementsFile(self):
        return os.path.abspath(os.path.join(pathlib.Path(__file__).parent.parent.absolute() , "setup.py"))

    @staticmethod
    def _tag(elem):
        import spacy
        nlp = spacy.load("en_core_web_md")
        #nlp = spacy.load("/tmp/spacy_model")
        filen , sent = elem
        doc = nlp(sent.lower())
        for ent in doc.ents:
            yield ( "_ESC_VAL_".join((filen ,  ent.label_ , ent.text)), 1)

    @staticmethod
    def _count(elem):
        filen_tag_text_label , counts = elem
        filen , label  , text = filen_tag_text_label.split("_ESC_VAL_")
        return [{"file" : filen ,"label":label,"text" : text , "count":sum(counts)}]

    def getSchema(self):
        return "file:STRING, label:STRING, text:STRING, count:FLOAT64"

    def __init__(self , pathToFiles, biqTable):
        self.pipe = beam.Pipeline(options=PipelineOptions([
            #'--direct_num_workers', '2',
            "--runner", "DataFlowRunner",
            "--project", "dsba6155p",
            "--region" , "us-east1",
            "--temp_location", "gs://dsba6155pdatabucket/dataflow_temp_location/",
            "--setup_file" , self.getPathToRequirementsFile(),
            # Cloud Data Flow Specs
            "--disk_size_gb", "20",
            "--use_public_ips","false",
            "--worker_machine_type","custom-8-7424",
            "--max_num_workers" , "10"
            ]))
        (
            self.pipe
            | "Read Files" >> ReadFromTextWithFilename(pathToFiles)
            | "Entity Tag Lines" >> beam.ParDo(TagDoFn())
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


# if __name__ == "__main__":
#     projectid = "dsba6155p"
#     datasetid = "nlpdataset"
#     tablename = "document_entities"
#     ptf ="gs://dsba6155pdatabucket/download/hindu**"
#     compute_table_name = f"{projectid}:{datasetid}.{tablename}"
#
#     #os.system("pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz")
#     #ptf = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
#     SpacyNLP(ptf , compute_table_name)
