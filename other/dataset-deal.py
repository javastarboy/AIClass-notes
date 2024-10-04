# 首先，让我们加载数据集并进行必要的预处理。
# 这将包括数据加载、缺失值检查、异常值处理和数据标准化。

import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

# 加载数据集
file_path_red = 'winequality-red.csv'
file_path_white = 'winequality-white.csv'
data_red = pd.read_csv(file_path_red, sep=';')
data_white = pd.read_csv(file_path_white, sep=';')

# 检查缺失值
missing_values_red = data_red.isnull().sum()
missing_values_white = data_white.isnull().sum()

# 如果存在缺失值，使用均值进行填充
if missing_values_red.any():
    imputer = SimpleImputer(strategy='mean')
    data_red[missing_values_red[missing_values_red > 0].index] = imputer.fit_transform(
        data_red[missing_values_red[missing_values_red > 0].index])

if missing_values_white.any():
    imputer = SimpleImputer(strategy='mean')
    data_white[missing_values_white[missing_values_white > 0].index] = imputer.fit_transform(
        data_white[missing_values_white[missing_values_white > 0].index])

# 数据标准化
scaler = StandardScaler()
data_red_scaled = scaler.fit_transform(data_red.drop('quality', axis=1))
data_white_scaled = scaler.fit_transform(data_white.drop('quality', axis=1))

data_red_scaled = pd.DataFrame(data_red_scaled, columns=data_red.columns[:-1])
data_white_scaled = pd.DataFrame(data_white_scaled, columns=data_white.columns[:-1])

# 合并数据集以便进行统一分析
data_combined_scaled = pd.concat([data_red_scaled, data_white_scaled], axis=0)
data_combined_scaled['quality'] = pd.concat([data_red['quality'], data_white['quality']], axis=0)

# 显示处理后的数据集信息
data_combined_scaled.info(), data_combined_scaled.head()


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


# 使用PCA进行降维分析，我们将保留前两个主成分以便可视化。

from sklearn.decomposition import PCA

# 初始化PCA并拟合数据
pca = PCA(n_components=2)
principal_components = pca.fit_transform(data_combined_scaled.drop('quality', axis=1))

# 解释的方差比例
explained_variance_ratio = pca.explained_variance_ratio_

# 将主成分添加到数据集中
pca_data = pd.DataFrame(data=principal_components, columns=['PC1', 'PC2'])
pca_data['quality'] = data_combined_scaled['quality'].values

explained_variance_ratio, pca_data.head()


# 使用CART算法建立决策树模型，并使用交叉验证来评估模型的性能。

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score

# 初始化CART模型
cart = DecisionTreeClassifier(random_state=42)

# 使用交叉验证评估模型性能
cv_scores_cart = cross_val_score(cart, data_combined_scaled.drop('quality', axis=1), data_combined_scaled['quality'], cv=5)

# 训练CART模型
cart.fit(data_combined_scaled.drop('quality', axis=1), data_combined_scaled['quality'])

# 显示交叉验证的准确率
cv_scores_cart.mean(), cart.feature_importances_

# 使用支持向量机（SVM）进行分类，并使用交叉验证来评估模型的性能。

from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV

# 初始化SVM模型
svm = SVC(kernel='rbf', random_state=42)

# 使用网格搜索进行参数优化
param_grid = {'C': [0.1, 1, 10], 'gamma': [0.001, 0.01, 0.1, 1]}
grid_search = GridSearchCV(svm, param_grid, cv=5)
grid_search.fit(data_combined_scaled.drop('quality', axis=1), data_combined_scaled['quality'])

# 获取最佳参数和最佳模型
best_params = grid_search.best_params_
best_svm = grid_search.best_estimator_

# 使用交叉验证评估最佳模型的性能
cv_scores_svm = cross_val_score(best_svm, data_combined_scaled.drop('quality', axis=1), data_combined_scaled['quality'], cv=5)

best_params, cv_scores_svm.mean()