from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt

X, y = make_blobs(n_samples=300, centers=4, cluster_std=0.60, random_state=0)
kmeans = KMeans(n_clusters=4)
kmeans.fit(X)
labels = kmeans.labels_
cluster_centers = kmeans.cluster_centers_

print("Cluster Centers: \n", cluster_centers)

plt.scatter(X[:,0], X[:,1], c=labels, cmap='rainbow')
plt.scatter(cluster_centers[:,0], cluster_centers[:,1], marker='*', c='black', s=300)
plt.title("K-Means Clustering")
plt.xlabel("Feature 1")
plt.ylabel("Feature 2")
plt.show()
plt.savefig("kMeansResult.png")