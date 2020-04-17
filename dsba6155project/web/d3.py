import requests
import json
import pandas as pd
import pathlib
import os

class D3:

    def getGroup(self,date):
        breakpoints  =[1700 ,1860 , [1861,1865] , [1914,1918] , [1939,1945] ,[1960,1980],[1990,2000],2002]
        num = 0
        valName =""
        retVal = None
        for k ,j in enumerate(breakpoints):
            l = -1
            valName = str(j)

            if type(j) == list:
                valName = "_".join([str(ji) for ji in j])
                j,l = j
                num += 1
                if date < j:
                    valName = f"< {j}-{l}"
                    retVal= num
                    break
                if date < l:
                    valName = f"{j}-{l}"
                    retVal= num+1
                    break
            elif date < j:
                valName = f"< {j}"
                retVal= num
                break

            num += 1
        #print((num,valName))
        return (retVal,valName)

    def getData(self):
        data = requests.get("http://www.thearda.com/timeline/json/tlRank1to2JsonFeed.js?_=1586741122479")
        js = data.text.replace("TLonJSONPLoad(" , "").replace(")" , "")
        js = json.loads(js)
        nodes = []
        links = []
        groups = {

        }
        for i,j in enumerate(js):
            if 'startDate' in j:

                j["year"] = int(j["startDate"].split("-")[0])
                j["id"] = j["title"] + " - " + str(j["year"])
                j["group"],j["groupName"] = self.getGroup(j["year"] )
                totalLinks = 0
                for k,l in enumerate(js):
                    if k > i and 'startDate' in l:
                        l["year"] = int(l["startDate"].split("-")[0])
                        l["id"] = l["title"] + " - " + str(l["year"])
                        l["group"],l["groupName"] = self.getGroup(l["year"] )

                        dist = abs(int(l["startDate"].split("-")[0]) - int(j["startDate"].split("-")[0]))
                        if dist < 10:
                            totalLinks += 1
                            links.append({"source" : j["id"] , "target" : l["id"] , "value" : dist})
                j["totalLinks"] = totalLinks
                nodes.append(j)
        return {"nodes" : nodes , "links":links}


class D3BookData:

    def getData(self , labelFilter):
        labelFilter = "PERSON"
        #__file__ = "C:\\Users\\Abhijeet\\Documents\\GitHub\\dsba6155project\\dsba6155project\\web\\d3.py"
        path = os.path.join(pathlib.Path(__file__).parent.absolute() , "staticdata" , "outputs_document_entities_export.csv")
        df = pd.read_csv(path)
        df = df[df["label"] == labelFilter]
        df = df[df["count"] > 50]
        df["category"] = df["file"].apply(lambda x: x.split("/")[-1].split("_")[0])
        return json.loads(df[["text" , "count" , "category"]].to_json(orient="records"))
