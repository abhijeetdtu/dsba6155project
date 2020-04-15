import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io import ReadFromTextWithFilename

import logging
import pathlib
import spacy
import os


from apache_beam.coders.coders import Coder


def SpacyNLP(nlp,pathToFiles , biqTable):


    class ISOCoder(Coder):
        """A coder used for reading and writing strings as ISO-8859-1."""

        def encode(self, value):
            return value.encode('iso-8859-1')

        def decode(self, value):
            return value.decode('iso-8859-1')

        def is_deterministic(self):
            return True

    #nlp = spacy.load("en_core_web_md")

    def getPathToRequirementsFile():
        #return os.path.abspath(os.path.join(pathlib.Path(__file__).parent.absolute() , "requirements.txt"))
        return os.path.abspath(os.path.join(pathlib.Path(__file__).parent.absolute() , "setup.py"))

    def _tag(elem):
        #nlp = spacy.load("en_core_web_md")
        filen , sent = elem
        doc = nlp(sent)
        for ent in doc.ents:
            yield ( "*".join((filen ,  ent.label_ , ent.text)), 1)

    def _count(elem):
        #print(elem)
        filen_tag_text_label , counts = elem
        filen , label  , text = filen_tag_text_label.split("*")
        return [{"file" : filen ,"label":label,"text" : text , "count":sum(counts)}]

    def getSchema():
        return "file:STRING, label:STRING, text:STRING, count:FLOAT64"


    pipe = beam.Pipeline(options=PipelineOptions([
        #'--direct_num_workers', '2',
        "--runner", "DataFlowRunner",
        "--project", "dsba6155p",
        "--region" , "us-east1",
        "--temp_location", "gs://dsba6155pdatabucket/dataflow_temp_location/",
        #"--save_main_session" , "True"
        #"--requirements_file", self.getPathToRequirementsFile()
        "--setup_file" , getPathToRequirementsFile()
        ]))
    (
        pipe
        | "Read Files" >> ReadFromTextWithFilename(pathToFiles, coder=ISOCoder())
        | "Entity Tag Lines" >> beam.ParDo(_tag)
        | "Group By Key" >> beam.GroupByKey()
        #| "Map to Ones" >> beam.Map(lambda x: (x , len(set(x[1]))))
        #| "Group By File and Type" >> beam.GroupByKey()
        | "Count" >> beam.ParDo(_count)
        #| "Write to File" >> beam.io.WriteToText("outputf")
        | "Write CSV to biqquery" >> beam.io.WriteToBigQuery(
            table=biqTable,
            schema=getSchema(),
            write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
            # create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED
        )
    )
    rs = pipe.run()
    rs.wait_until_finish()


if __name__ == "__main__":


    logging.basicConfig(level=logging.DEBUG)

    nlp = spacy.load("en_core_web_md")
    projectid = "dsba6155p"
    datasetid = "nlpdataset"
    tablename = "document_entities"
    ptf ="gs://dsba6155pdatabucket/download/**"
    compute_table_name = f"{projectid}:{datasetid}.{tablename}"


    #os.system("python -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz")
    #ptf = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    SpacyNLP(nlp,ptf , compute_table_name)
