import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import matplotlib.pyplot as plt
import numpy as np
import pylab as pl
from sklearn.decomposition import PCA

#collect the data from the chosen csv file
#open a text file to write the result of the clusters to it
tweets = pd.read_csv("/Users/jordynbrown/Documents/coronavirus_sample.csv")
file = open("Clusters.txt", "w")

# Extract the collected usernames from all of the tweets
collected_usernames = tweets['username']
# Extract the collected hashtags from all of the tweets
collected_hashtags = tweets['hashtags']
# Extract the collected text from all of the tweets
collected_text = tweets['text']

#Create a vector to transform the names into integer values so that the KMeans can be calculated
#Clusters cannot be created without first vectorising the strings
vectorizer = TfidfVectorizer(stop_words='english')
# Vectorise usernames
vect_username = vectorizer.fit_transform(collected_usernames)
# Vectorise hashtags
vect_hashtags = vectorizer.fit_transform(collected_hashtags)
# Vectorise text 
vect_text = vectorizer.fit_transform(collected_text)

k = 8


# Cluster the usernames from the vector
kmeans_username = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_username.fit(vect_username)

# Print top 10 usernames per cluster
print("Top usernames per cluster:")
file.write("Top usernames per cluster:\n")
order_centroids = kmeans_username.cluster_centers_.argsort()[:, ::-1]
terms_username = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_username[ind])
        file.write(' %s' % terms_username[ind])
        file.write("\n")



# Cluster the hashtags from the vector
kmeans_hashtags = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_hashtags.fit(vect_hashtags)

# Print top 10 hashtags per cluster
print("Top hashtags per cluster:")
file.write("\nTop hashtags per cluster:\n")
order_centroids = kmeans_hashtags.cluster_centers_.argsort()[:, ::-1]
terms_hashtags = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_hashtags[ind])
        file.write(' %s' % terms_hashtags[ind])
        file.write("\n")

print("\n")


# Cluster the text from the vector
kmeans_text = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1)
kmeans_text.fit(vect_text)



# Print top 10 text per cluster
print("Top text per cluster:")
file.write("\nTop text per cluster:\n")
order_centroids = kmeans_text.cluster_centers_.argsort()[:, ::-1]
terms_text = vectorizer.get_feature_names()
for i in range(k):
    print ("Cluster %d:" % i)
    file.write("Cluster %d:" % i)
    file.write("\n")
    for ind in order_centroids[i, :10]:
        print (' %s' % terms_text[ind])
        file.write(' %s' % terms_text[ind])
        file.write("\n")

file.close()