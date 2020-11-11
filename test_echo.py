import numpy as np
import csv
from Heart_EJ900_fast import EJ900
from Echo_EJ_format_v2 import EJ_format

import time
"""
filename = 'C:/Users/SunhoChoi/Desktop/CDM/dataset_2017_sample.csv'
reader = csv.reader(open(filename, 'r', encoding='cp949'))
lines=[]

for line in reader:
    lines.append(line)

data_ = np.array(lines, dtype='U')
Code_EJ900 = data_[data_[:,0]=="EJ900",6]


aa = EJ900(data=Code_EJ900, path='C:/Users/SunhoChoi/Desktop/CDM/EJ900_2017_sam.csv')

"""
start = time.time() #삼성병원 정보 추가한 것
#filename = 'C:/Users/SunhoChoi/Desktop/CDM/Echo_Sample_Data_de-identified.csv'
#filename = 'C:/Users/SunhoChoi/Desktop/CDM/190827_2003_2018_input.csv'
filename = 'C:/Users/SunhoChoi/Desktop/CDM/삼성_단순-심장초음파-200909.csv'
aa = EJ_format()

aa.data_load(filename=filename)
aa.Start(path='삼성심초음파', format='New')

print("time :", time.time()-start)