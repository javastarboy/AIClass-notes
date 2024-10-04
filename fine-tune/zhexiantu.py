import json

import matplotlib.pyplot as plt

# 假设您的数据存储在一个名为data的列表中
# data = [
#     {'loss': 0.626, 'learning_rate': 0.00029676043032578116, 'epoch': 0.76},
#     {'loss': 0.4243, 'learning_rate': 0.00029670816123699806, 'epoch': 0.76},
#     # ... 其他数据
#     {'loss': 0.3922, 'learning_rate': 0.00029526740961064514, 'epoch': 0.89}
# ]

"""
data0- 860对数据集：   
  --num_train_epochs 5 \
  --per_device_train_batch_size 2 \
  --learning_rate 3e-4 \
data1- 3000对数据集：   
  --num_train_epochs 10 \
  --per_device_train_batch_size 2 \
  --learning_rate 3e-4 \
  从输出的损失函数值来看，模型的训练过程并不稳定，损失值在震荡，需要降低 learning_rate，减少epoch 数，增大batch_size批次
data2-860对数据集：   
  --num_train_epochs 3 \
  --per_device_train_batch_size 2 \
  --learning_rate 3e-4 \
data3-860对数据集：   
  --num_train_epochs 5 \
  --per_device_train_batch_size 2 \
  --learning_rate 3e-4 \
data4-3000对数据集：   
  --num_train_epochs 5 \
  --per_device_train_batch_size 2 \
  --learning_rate 3e-4 \
data5-860对数据集：   
  --num_train_epochs 5 \
  --per_device_train_batch_size 2 \
  --learning_rate 5e-4 \
data6-860对数据集：   
  --num_train_epochs 3 \
  --per_device_train_batch_size 2 \
  --learning_rate 2e-4 \
  {'train_runtime': 1310.5582, 'train_samples_per_second': 1.93, 'train_steps_per_second': 0.119, 'train_loss': 0.16212441906622516, 'epoch': 2.96}   
"""
filename = 'Statistics/data6.txt'

# 初始化列表以存储数据
data = []

# 读取文本文件并直接将每一行的数据作为一个字典添加到列表中
with open(filename, 'r') as file:
    for line in file:
        # 移除每行末尾的换行符，并直接将其作为字典添加到列表中
        entry = eval(line.strip())
        data.append(entry)

# 提取数据
epochs = [d['epoch'] for d in data]
losses = [d['loss'] for d in data]
learning_rates = [d['learning_rate'] for d in data]

# 绘制损失随训练轮数变化的折线图
plt.figure(figsize=(10, 5))
plt.plot(epochs, losses, label='Loss', marker='o')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss vs Epoch')
plt.legend()
plt.grid(True)
plt.show()

# 绘制学习率随训练轮数变化的折线图
plt.figure(figsize=(10, 5))
plt.plot(epochs, learning_rates, label='Learning Rate', marker='o')
plt.xlabel('Epoch')
plt.ylabel('Learning Rate')
plt.title('Learning Rate vs Epoch')
plt.legend()
plt.grid(True)
plt.show()