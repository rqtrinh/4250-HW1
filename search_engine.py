#-------------------------------------------------------------------------
# AUTHOR: Ryan Trinh
# FILENAME: search_engine.py
# SPECIFICATION: Read csv files and determine which documents to retreive calcuatre df-idf/recall/precision
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#importing some Python libraries
import csv
import math

documents = []
labels = []
query = "cats and dogs"

#reading the data in a csv file
with open('collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            labels.append(row[1])

print(documents)
# print(labels)

#Conduct stopword removal.
#--> add your Python code here
stopWords = {'I', 'and', 'She', 'They', 'her', 'their'}
for i in range(len(documents)):
  for word in stopWords:
      documents[i] = documents[i].replace(word, "")
  #Remove white spaces from front and back of string
  documents[i] = " ".join(documents[i].split())

#stopword removal query
for word in stopWords:
    query = query.replace(word, "")
#Remove white spaces from front and back of string
query = " ".join(query.split())  
print(query)



#Conduct stemming.
#--> add your Python code here
steeming = {
  "cats": "cat",
  "dogs": "dog",
  "loves": "love",
}

for i in range(len(documents)):
    for key in steeming.keys():
        if key in documents[i]:
          documents[i] = documents[i].replace(key, steeming[key])
print(documents)

for key in steeming.keys():
    if key in query:
      query = query.replace(key, steeming[key])
print("Query:", query)


#Identify the index terms.
#--> add your Python code here
terms = []
for document in documents:
    for word in document.split():
        if word not in terms:
            terms.append(word)
print(terms)

query_weights = []
#Query weights
for word in terms:
    if word in query:
        query_weights.append(1)
    else:
        query_weights.append(0)
print("Query weights:", query_weights)

#Build the tf-idf term weights matrix.
#--> add your Python code here
docMatrix = []

terms_idf = []
for i in range(len(terms)):
    #Calculate df for term
    df = 0
    for document in documents:
        if terms[i] in document:
            df += 1
    #Calculate idf for term 
    print("length", len(documents))
    print("df", df)

    idf = math.log10(len(documents)/df)
    terms_idf.append(idf)

for document in documents:
    total_words = len(document.split())
    document_tf_idf = []

    for i in range(len(terms)):
        terms_doc = document.count(terms[i])
        tf = terms_doc/total_words
        document_tf_idf.append(tf*terms_idf[i])
    docMatrix.append(document_tf_idf)

print(docMatrix)


#Calculate the document scores (ranking) using document weigths (tf-idf) calculated before and query weights (binary - have or not the term).
#--> add your Python code here
docScores = []
for tf_idf_scores in docMatrix:
    docScore = 0
    for i in range(len(tf_idf_scores)):
        docScore += query_weights[i] * tf_idf_scores[i]
    docScores.append(round(docScore,2))

print(docScores)
#Calculate and print the precision and recall of the model by considering that the search engine will return all documents with scores >= 0.1.
#--> add your Python code here
a = 0
b = 0 
c = 0 
d = 0

print(labels)
for i in range(len(docScores)):
    if docScores[i] >= 0.1 and labels[i] == " R":
        a += 1
    elif docScores[i] >= 0.1 and labels[i] == " I":
        b += 1
    elif docScores[i] < 0.1 and labels[i] == " R":
        c += 1
    else:
        d += 1

print("Recall", a/(a+c) * 100)
print("Precision", a/(a+b) * 100)