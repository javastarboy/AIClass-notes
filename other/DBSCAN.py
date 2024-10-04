# 接下来，我们将使用DBSCAN算法进行聚类分析。
# DBSCAN算法不需要预先指定聚类个数，能够发现任何形状的聚类。

from sklearn.cluster import DBSCAN
import numpy as np

# 使用DBSCAN进行聚类
dbscan = DBSCAN(eps=0.5, min_samples=5)  # eps和min_samples是DBSCAN的两个关键参数
clusters = dbscan.fit_predict(data_combined_scaled.drop('quality', axis=1))

# 添加聚类结果到数据集中
data_combined_scaled['cluster'] = clusters

# 检查聚类结果
clustered_data_info = data_combined_scaled['cluster'].value_counts()
noise_points = np.sum(np.where(clusters == -1, 1, 0))

clustered_data_info, noise_points
