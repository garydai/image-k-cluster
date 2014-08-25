#!/usr/bin/env python
#coding:utf-8
import os
import random
import math
from PIL import Image

class Center(object):
    def __init__(self, vector):
        self.vector = vector
        self.objects = []
class Vector(object):
    """单个数据记录的向量表示"""
    def __init__(self):
        # 由于当前向量比较稀疏，所以使用字典而非数组来表示
     #   self.words = {}
        self.x = -1
        self.y = -1
        self.z = -1
      #  self.label = label
    
    def addToNearestCenter(self, centers):
        nearest = centers[0]
        print '------'
        print nearest.vector.x, nearest.vector.y, nearest.vector.z

        d = self.distance(centers[0].vector)
        for center in centers[1:]:
            new_d = self.distance(center.vector)
            if new_d < d:
                d = new_d
                nearest = center
        print nearest.vector.x, nearest.vector.y, nearest.vector.z
        print '---------------'
        nearest.objects.append(self)
    """
        计算两个向量之间的欧几里得距离,注意数据维度上的值非常稀疏.
    """
    def distance(self, vector):
        square_sum = 0.0
        square_sum = (float)(self.x - vector.x)* (self.x - vector.x) \
        + (self.y - vector.y)* (self.y - vector.y) +\
            (self.z - vector.z)* (self.z - vector.z) 
        result = math.sqrt(square_sum)
        return result

class KMeans(object):
    """ 准备数据，把新闻数据向量化"""
    def __init__(self, file_name):

        self.vectors = []

        self.centers = []
        self.map = {}

        # 上一次中心点的损失
        self.last_cost = 0.0
        # 从指定目录加载文件
        f = open(file_name, 'r')
        img = Image.open("a.png")
        sequence = img.getdata()
        #for color in sequence:
         #   print color

        print 123, sequence[0][0]
        #while 1:
        for color in sequence:

         #   line = f.readline()
          #  if not line:
          #      break
          #  words = line.split()

            v = Vector()
            v.x = int(color[0])
            v.y = int(color[1])
            v.z = int(color[2])

            self.vectors.append(v)
            self.map[(v.x << 16)+ (v.y <<8 ) + v.z] = 1
        print self.vectors[0].x
        print self.vectors[0].y
        print self.vectors[0].z
    """ 分配初始中心点,计算初始损失，并开始聚类 """
    def start(self, class_num):
        # 从现有的所有文章中，随机选出class_num个点作为初始聚类中心
        #while 1:
          #  vector = random.sample(self.vectors)
        for m in random.sample(self.map, class_num):
            v = Vector()
            v.x =m>>16
            v.y = (m&0x00ff00)>>8
            v.z = m &0x0000ff
            c = Center(v)
            print 1
            print c.vector.x
            print c.vector.y
            print c.vector.z
            self.centers.append(c)


        # 初始划分，并计算初始损失
        print 'init center points'
        self.split()
        self.locateCenter()
        self.last_cost = self.costFunction()
        print 'start optimization'
        # 开始进行优化，不断的进行三步操作：划分、重新定位中心点、最小化损失
        i = 0
        while True:
            i += 1
            print '第 ',i,' 次优化:'
            self.split()
            self.locateCenter()
            current_cost = self.costFunction()
            print '损失降低(上一次 - 当前)：',self.last_cost,' - ',current_cost,' = ',(self.last_cost - current_cost)
            if self.last_cost - current_cost  <= 1:
                break
            else:
                self.last_cost = current_cost
        # 迭代优化损失函数，当损失函数与上一次损失相差非常小的时候，停止优化
        count = 0
        for center in self.centers:
            count += 1
            print '第', count, '组:'
            print center.vector.x, center.vector.y, center.vector.z
          #  for vector in center.objects:
           #     print vector.x, vector.y, vector.z
            print '---------------------------------------'
    """
        根据每个聚类的中心点，计算每个对象与这些中心的距离，根据最小距离重新划分每个对象所属的分类
    """
    def split(self):
        print '划分对象... Objects : ', len(self.vectors)
        # 先清空上一次中心点表里的对象数据，需要重新划分
        for center in self.centers:
            center.objects = []
        # 遍历所有文件并分配向量到最近的中心点区域
        for vector in self.vectors:
            vector.addToNearestCenter(self.centers)
    """ 重新获得划分对象后的中心点 """
    def locateCenter(self):
        # 遍历中心点，使用每个中心点所包含的文件重新求中心点
        count = 0
        for center in self.centers:
            count += 1
            print '计算第 ', count, ' 类的新中心点...'
            files_count = float(len(center.objects))
            # 新的中心点，格式为 {word1:0,word2:5...}
            new_center = {}
            # 遍历所有该中心包含的文件
            x = 0.0
            y = 0.0
            z = 0.0
            for vector in center.objects:
                x += vector.x
                y += vector.y
                z += vector.z
            x /= len(center.objects)
            y /= len(center.objects)
            z /= len(center.objects)

            # 中心点对象
            center.vector = Vector()
            center.vector.x = x
            center.vector.y = y
            center.vector.z = z

    """ 损失函数 """
    def costFunction(self):
        print '开始计算损失函数'
        total_cost = 0.0
        count = 0
        for center in self.centers:
            count += 1
            print '计算第 ', count, ' 类的损失 objects : ', len(center.objects)
            for vector in center.objects:
                # 求距离平方作为损失
                total_cost += math.pow(vector.distance(center.vector),2)
        print '本轮损失为：',total_cost
        return total_cost
if __name__ == '__main__':
    km = KMeans('color.txt')
    km.start(5)