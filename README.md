
![Religions](https://user-images.githubusercontent.com/6872080/77272080-b6696780-6c86-11ea-898e-c4ad6011ff11.png)
#  Overfitters Anonymous

| Abhijeet | Kevin|Janani|Mansi|Riddhi
|---|---|---|---|---|



1. **Research question**:  
   - Distinctions between Pre-abrahamic vs Abrahamic religions
   - Geography/Demographics by religion
   - What do different religious books agree/disagree on?
   - Evolution of themes in the texts over time/ change of tone / language / concepts
   - Leverage text analytics/ word vectors to search for similar ideas in different books, compare and contrast them

- **Audience**: Theologians, Anthropologists, Religious scholars, Researchers, Curious people, &c.


2.  **Domain and Data**:

  * **Data**:
    Religious texts will be downloaded from the Project Gutenberg website. Project Gutenberg is an online archive of books that are free to download and distribute.
    * Project Gutenberg
      - https://www.gutenberg.org/ebooks/10
      - http://www.gutenberg.org/ebooks/2800
      - http://www.gutenberg.org/ebooks/3283
      - http://www.gutenberg.org/ebooks/35895
      - http://www.gutenberg.org/ebooks/17
      - http://www.gutenberg.org/ebooks/2680
    * World Religion Data:
      - https://data.world/cow/world-religion-data
      - https://data.world/ian/world-religious-populations
   
    * **Architecture**
      <img src="./dsba6155project/web/static/images/architecture_svg.svg">
      - Access has been given to Dr Thompson as a reader to the project- dsba6155 in gcp
      - Cloud Functions - We have the [Python Script](https://github.com/abhijeetdtu/dsba6155project/blob/master/dsba6155project/data_pull/gutenberg.py) ready that pulls books from project gutenberg. It needs to be hooked to cloud functions
      - Cloud Storage - **kbs_bookstore** - stores the intermediate books downloaded from Project Gutenberg
      - App Engine - **default**- App Service is hosting the Frontend of the project
      - **Bigquery** 
         - This has a dataset - nlp so far with only one table - wordcounts - which was populated using - [Apache Beam](https://github.com/abhijeetdtu/dsba6155project/blob/master/dsba6155project/data_pull/parallel_beam.py)
         
         
    a) **Preprocessing**
      - Creating Corpus
        - Cleaning
        - Tokenization
        - Lemmatization
        - TF/IDF
      - Word To Vector Embeddings

    b) **Size of data**
      - Very high dimensional text analysis
      - Depends on number of books we end up incorporating/ingesting

    c)  **Tentative Plan for Analysis on GCP**

      1. **EDA and Preprocessing**
           - Use Apache Beam to Scrape Data
           - Google Storage Bucket for staging data
           - Data Studio for EDA/Visualization/Reporting

      2.  **Dashboard for User group, Dashboard for Data Engineers**
           - Data Studio Dashboard - User Group
               - We are planning to build an GCP App Engine web frontend hosted [here](https://dsba6155.appspot.com/)
               - We are going to use Python Dash and Google Data studio to embed dashboards in the web app to provide seamless storytelling
           - Datalab Jupyter Notebook & Data Studio Dashboard - Data Engineers

      3.  **GCP further processing - ML**
         - Google AI platform and Google Datalab to create notebooks to perform analytics, data mining, text processing.

      4. **Evaluation of results**
         - We might use cluster evaluation methods such as ‘within cluster MSE’ to evaluate the fitness of the clusters of topics/themes.

      5.  **Steps for production model**
        - Word to Vector conversions
            -   Pymagnitude
            -   Scipy
            -   Gensim
            -   Google BERT
        
           - Model to find similar concepts and themes
           - Flask API as an interface between model and webapp
           - Webapp to enable easy search and exploration of similar concepts across religions

      6. **Final Dashboard for User Group**
           - An interactive app that presents the insights that we have gained.
           - One of the interactions the user will be able to do with the dashboard is input keywords they want to search for in the texts to get an insight into what opinion each religion holds.
           - Maybe, a separate web app(Google App Engine)/R-shiny app to enable interactive exploration.

* **Research Papers**
  - https://arxiv.org/pdf/1912.10847.pdf
  - [Designing Cloud Architectures](https://docs.huihoo.com/amazon/aws/whitepapers/AWS-Cloud-Architectures.pdf)
  - [Text Mining In Cloud](https://link.springer.com/article/10.1007/s10586-017-0909-1)
  - Helper Blogs
      - [Cloud NLP](https://medium.com/google-cloud/sentiment-analysis-using-google-cloud-machine-learning-552be9b9c39b)
