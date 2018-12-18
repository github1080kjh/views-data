from django.test import TestCase

# Create your tests here.
from static import imgs
import os


# import matplotlib.pyplot as plt
# import numpy as np
#
# fig = plt.figure(1)        # 创建了一个figure对象;
#
# #figure对象的add_axes()可以在其中创建一个axes对象,
# # add_axes()的参数为一个形如[left, bottom, width, height]的列表,取值范围在0与1之间;
# ax = fig.add_axes([0.1, 0.5, 0.8, 0.5]) # 我们把它放在了figure图形的上半部分，对应参数分别为：left, bottom, width, height;
# ax.set_xlabel('time')     #用axes对象的set_xlabel函数来设置它的xlabel
#
# line =ax.plot(range(5))[0]  #用axes对象的plot()进行绘图,它返回一个Line2D的对象;
# line.set_color('r')             # 再调用Line2D的对象的set_color函数设置color的属性;
# plt.show()

import matplotlib.pyplot as plt

labels = ['Frogs', 'Hogs', 'Dogs', 'Logs']
sizes = [70, 10, 15, 5]
explode = (0, 0, 0.1, 0)  # 0.1表示将Hogs那一块凸显出来
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
# startangle表示饼图的起始角度
BASEDIR = os.path.dirname(os.getcwd())
result_dir = os.path.join(BASEDIR, 'static\imgs\data.png')
print(result_dir)
plt.savefig(result_dir)



