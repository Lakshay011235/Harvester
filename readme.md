# **Solution for Blackcoffer :Test Assignment (Data Extraction and NLP)**
## **Setup**

---

### **Install Python Virtual Environment**

\
Open a terminal in this directory

Run the following command to install virtual environment

    python -m venv VirtualEnv

Activate the environment before proceeding to next step

    VirtualEnv\Scripts\activate

---

### **Install dependencies**

\
In terminal, run command

    pip install -r requirements.txt

---

## **Running the code** 

---

### **First Run**

---

For first time users, __uncomment__ the spider code in main.py

This process will take time, hence the files are already extracted and saved.

> NOTE:: Run these command to extract data using spider 
>
>> import subprocess
>>
>> project_path="dataExtraction"
>>
>> subprocess.Popen(["scrapy","crawl","harvester","-o","harvestedfiles.json"],shell=True, cwd=project_path)
 
OR

> In terminal run commands
>
>      cd dataExtraction
>
>      scrapy crawl harvester -o harvestedfiles.json
>
>      cd ..

---

## **Normal Run**

\
Run the following command:

    python main.py

---

## **About**

\
As per the instructions in **Objective.docx**, the data extraction is done from the urls in **Input.xlsx**  using Scrapy library in Python

The code is dynamic and will handle errors like bad_url and any new url in **Input.xlsx** will get handled by first run commands.

Please note that running spider will take about 5 mins to complete and is not advised to use

Text Analysis is done using both given stopwords and nltk provided stopwords

Sentiment analysis is performed from given stopwords as provided

While the readability analysis is done from raw text as per need

All the code uses **python only**.

You can view the anaylsis in **Output Data Structure.xlsx**

---

### Additional Support

.json file is also created for data that has been extracted from urls

Directory StopWords and Input.xlsx are dynamically binded to support any new files and links respectively

Spider also has a pipeline interface to store data into a database

---

## **Contact**

### Name: Lakshay Sharma
### Phone: 7011829824
### Email: lakshayegyu@gmail.com

---