#!/usr/bin/env python

from flask import Flask
from flask import render_template
import numpy as np
from sklearn.decomposition import PCA
from sklearn.manifold import MDS
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import scale

app = Flask(__name__)

#Load data set
data1 = pd.read_csv('static/data/Stratified.csv')
data2 = pd.read_csv('static/data/Random.csv')

#convert it to numpy arrays
X = data1.values
Y = data2.values

#Scaling the values
X = scale(X)
Y = scale(Y)

pca = PCA(n_components=11)

print "pca.fit(X)"
pca.fit(X)
var1 = pca.explained_variance_ratio_ * 100
sqr1 = np.array([[elem*elem for elem in inner] for inner in pca.components_[:2,:]])
sqr_x1 = sqr1.sum(axis=0)
val_x1 = np.sqrt(np.abs(sqr_x1))
x1 = np.matmul(pca.components_[:1,:], X.T)
y1 = np.matmul(pca.components_[1:2,:], X.T)

print "pca.fit(Y)"
pca.fit(Y)
var2 = pca.explained_variance_ratio_*100
sqr2 = np.array([[elem*elem for elem in inner] for inner in pca.components_[:2,:]])
sqr_x2 = sqr2.sum(axis=0)
val_x2 = np.sqrt(np.abs(sqr_x2))
x2 = np.matmul(pca.components_[:1,:], Y.T)
y2 = np.matmul(pca.components_[1:2,:], Y.T)

var3 = (var1+var2)/2

print "Plotting PCA Scree Plot"
plt.figure(1, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
ax.set_xlim(0, 12)
ax.plot(range(1,12),var2, 'ro-', linewidth=2, alpha=0.75, label='Random', markersize=5)
ax.plot(range(1,12),var1, 'bo-', linewidth=2, alpha=0.75, label='Stratified', markersize=5)
ax.plot(range(1,12),var3, 'go-', linewidth=0, alpha=0.5, markevery=[1], markersize=20, markeredgewidth=3, fillstyle='none')
ax.annotate("Intrinsic Dimentionality", (2.2, 13))

plt.title('PCA Scree Plot')
plt.xticks(np.arange(0,12,1))
plt.xlabel('Principal Components')
plt.ylabel('Explained Variance(%)')
plt.legend()
plt.savefig("static/images/ScreePlot.png", dpi=300)

print "Plotting PCA Loading Stratified"
plt.figure(10, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
ax.bar(np.arange(11), val_x1, 0.6, color='b')

labels=['Month', 'DayofMonth', 'DayOfWeek', 'DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime', 'UniqueCarrier', 'FlightNum', 'TaxiIn', 'TaxiOut']
x=np.arange(0,12,1)
plt.title('PCA Loadings - Stratified')
plt.xticks(x, labels, rotation='vertical')
plt.tight_layout()
plt.savefig("static/images/PCA_Loading_Stratified.png", dpi=300)

print "Plotting PCA Loading Random"
plt.figure(11, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
ax.bar(np.arange(11), val_x2, 0.6, color='b')

plt.title('PCA Loadings - Random')
plt.xticks(x, labels, rotation='vertical')
plt.tight_layout()
plt.savefig("static/images/PCA_Loading_Random.png", dpi=300)

print "Plotting PCA Scatter Plot Stratified"
plt.figure(2, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
ax.plot(x1, y1, 'o', markersize=8, color='blue', alpha=0.5)
plt.title('PCA Scatter Plot Stratified')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.xticks(np.arange(-4,6,1))
plt.savefig("static/images/ScatterPlot_Stratified.png", dpi=300)

print "Plotting PCA Scatter Plot Random"
plt.figure(3, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
ax.plot(x2, y2, 'o', markersize=8, color='blue', alpha=0.5)
plt.title('PCA Scatter Plot Random')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.xticks(np.arange(-4,6,1))
plt.savefig("static/images/ScatterPlot_Random.png", dpi=300)

mds = MDS(n_components=2, dissimilarity="euclidean")
results = mds.fit(X)
coordsX = results.embedding_

print "Plotting MDS Scatter Plot Euclidean - Stratified"
plt.figure(4, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
plt.scatter(
    coordsX[:, 0], coordsX[:, 1], marker = 'o', color='blue'
    )
plt.title('MDS Scatter Plot Euclidean - Stratified')
plt.savefig("static/images/MDS_Stratified_Euclidean.png", dpi=300)

results = mds.fit(Y)
coordsY = results.embedding_

print "Plotting MDS Scatter Plot Euclidean - Random"
plt.figure(5, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
plt.scatter(
    coordsY[:, 0], coordsY[:, 1], marker = 'o', color='blue'
    )
plt.title('MDS Scatter Plot Euclidean - Random')
plt.savefig("static/images/MDS_Random_Euclidean.png", dpi=300)

mds = MDS(n_components=2, dissimilarity="precomputed")
results = mds.fit(np.corrcoef(X))
coords = results.embedding_

print "Plotting MDS Scatter Plot Correlation Distance - Stratified"
plt.figure(6, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
plt.scatter(
    coords[:, 0], coords[:, 1], marker = 'o', color='blue'
    )
plt.title('MDS Scatter Plot Correlation Distance - Stratified')
plt.savefig("static/images/MDS_Stratified_Correlation.png", dpi=300)

results = mds.fit(np.corrcoef(Y))
coords = results.embedding_

print "Plotting MDS Scatter Plot Correlation Distance - Random"
plt.figure(7, figsize=(12,6))
ax=plt.subplot(111, facecolor='lightgray')
plt.scatter(
    coords[:, 0], coords[:, 1], marker = 'o', color='blue'
    )
plt.title('MDS Scatter Plot Correlation Distance - Random')
plt.savefig("static/images/MDS_Random_Correlation.png", dpi=300)

X_uniq = X[:, 7:8]
X_taxiIn = X[:, 9:10]
X_crsarr = X[:,6:7]
print "Plotting Scatter Plot - Random"
print "UniqueCarrier-UniqueCarrier"
plt.figure(8, figsize=(12,6))
ax=plt.subplot(337, facecolor='lightgray')
plt.scatter(X_uniq, X_uniq, marker='o', color='blue')
ax.annotate("Unique Carrier", (0.5, -1.65))

print "UniqueCarrier-TaxiIn"
ax=plt.subplot(334, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
plt.scatter(X_uniq, X_taxiIn, marker='o', color='blue')

print "UniqueCarrier-CRSArr"
ax=plt.subplot(331, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
plt.scatter(X_uniq, X_crsarr, marker='o', color='blue')

print "TaxiIn-UniqueCarrier"
ax=plt.subplot(338, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_taxiIn, X_uniq, marker='o', color='blue')

print "TaxiIn-TaxiIn"
ax=plt.subplot(335, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_taxiIn, X_taxiIn, marker='o', color='blue')
ax.annotate("Taxi In", (6.5, -1))

print "TaxiIn-CRSArr"
ax=plt.subplot(332, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_taxiIn, X_crsarr, marker='o', color='blue')

print "CRSArr-UniqueCarrier"
ax=plt.subplot(339, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_crsarr, X_uniq, marker='o', color='blue')

print "CRSArr-TaxiIn"
ax=plt.subplot(336, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_crsarr, X_taxiIn, marker='o', color='blue')

print "CRSArr-CRSArr"
ax=plt.subplot(333, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(X_crsarr, X_crsarr, marker='o', color='blue')
ax.annotate("CRSArr Time", (0.6, -2.8))

plt.tight_layout()
plt.savefig("static/images/ScatterPlotMatrix-Random.png", dpi=300)

Y_uniq = Y[:,7:8]
Y_crsdep = Y[:,4:5]
Y_deptime = Y[:,3:4]
print "Plotting Scatter Plot - Stratified"
print "UniqueCarrier-UniqueCarrier"
plt.figure(9, figsize=(12,6))
ax=plt.subplot(337, facecolor='lightgray')
plt.scatter(Y_uniq, Y_uniq, marker='o', color='blue')
ax.annotate("Unique Carrier", (0.4, -1.65))

print "UniqueCarrier-CRSDep"
ax=plt.subplot(334, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
plt.scatter(Y_uniq, Y_crsdep, marker='o', color='blue')

print "UniqueCarrier-DepTime"
ax=plt.subplot(331, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
plt.scatter(Y_uniq, Y_deptime, marker='o', color='blue')

print "CRSDep-UniqueCarrier"
ax=plt.subplot(338, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_crsdep, Y_uniq, marker='o', color='blue')

print "CRSDep-CRSDep"
ax=plt.subplot(335, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_crsdep, Y_crsdep, marker='o', color='blue')
ax.annotate("CRSDep Time", (0.8, -2.5))

print "CRSDep-DepTime"
ax=plt.subplot(332, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_crsdep, Y_deptime, marker='o', color='blue')

print "DepTime-UniqueCarrier"
ax=plt.subplot(339, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_deptime, Y_uniq, marker='o', color='blue')

print "DepTime-CRSDep"
ax=plt.subplot(336, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_deptime, Y_crsdep, marker='o', color='blue')

print "DepTime-DepTime"
ax=plt.subplot(333, facecolor='lightgray')
frame = plt.gca()
frame.axes.get_xaxis().set_visible(False)
frame.axes.get_yaxis().set_visible(False)
plt.scatter(Y_deptime, Y_deptime, marker='o', color='blue')
ax.annotate("Dep Time", (1.3, -2.5))

plt.tight_layout()
plt.savefig("static/images/ScatterPlotMatrix-Stratified.png", dpi=300)


print "Starting Server"
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
