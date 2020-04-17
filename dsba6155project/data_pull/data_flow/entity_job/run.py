from job.entity_tag_beam import *

if __name__ == '__main__':
    projectid = "dsba6155p"
    datasetid = "nlpdataset"
    tablename = "document_entities"
    ptf ="gs://dsba6155pdatabucket/download/**"
    compute_table_name = f"{projectid}:{datasetid}.{tablename}"

    #os.system("pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_md-2.2.5/en_core_web_md-2.2.5.tar.gz")
    #ptf = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\data\\**"
    SpacyNLP(ptf , compute_table_name)
