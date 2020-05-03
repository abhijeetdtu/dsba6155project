import requests
import re


def getResults(numPages , queryText):
    offset = 10
    results = []
    url = "https://uncc.primo.exlibrisgroup.com/primaws/rest/pub/pnxs?blendFacetsSeparately=false&disableCache=false&getMore=0&inst=01UNCC_INST&lang=en&limit=10&multiFacets=facet_rtype,include,articles&newspapersActive=false&newspapersSearch=false&offset={OFFSET}&pcAvailability=false&q=any,contains,{QUERY}&qExclude=&qInclude=&refEntryActive=false&rtaLinks=true&scope=MyInst_and_CI&skipDelivery=Y&sort=rank&tab=Everything&vid=01UNCC_INST:01UNCC_INST"

    for iteration in range(0,numPages*offset,offset):
        query = url.format(**{"QUERY" : queryText, "OFFSET" : iteration})
        print(query)
        data = requests.get(query)

        js = data.json()
        for doc in js["docs"]:
            display = doc["pnx"]["display"]
            if "ispartof" not in display:
                continue
            p = display["ispartof"][0]
            title = display["title"][0]
            nums = re.findall("\d{4}" , p)
            nums = [n for n in nums if int(n) > 1900 and int(n) < 2020]
            n = -1 if len(nums) == 0 else nums[0]
            results.append((title, p, n , queryText))

    return results

r1 = getResults(5,"rule+based+systems")
r2 = getResults(5,"machine+learning+systems")
r3 = getResults(5,"expert+systems")

import pandas as pd

df = pd.DataFrame(r1+r2+r3)
df.columns = ["title" , "Journal" , "Year" , "Query"]
df["Year"] = df["Year"].astype("int32")
df.head()

df.groupby("Query").agg(median_year = ("Year" , "median"))
