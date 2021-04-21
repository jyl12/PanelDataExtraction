'''
Database module 
Write semantic objects to a csv file to log outputs

'''

import csv
import datetime
from DataCollation.SemanticOutputMap import SemanticMap
import numpy as np

"""function to make header rows as a new csv file
input a list of the semantic object"""

def define_log(SOs):

    try:
        
        with open('log.csv','w') as f:
            w = csv.writer(f, delimiter = ',')
            w.writerow(['Time'] + [semanticObj.meaning for semanticObj in SOs])

    except IOError:

        with open('log.csv','w+') as f:
            w = csv.writer(f, delimiter = ',')
            w.writerow(['Time'] + [semanticObj.meaning for semanticObj in SOs])
        
def define_log_validation(SOs):

    with open('log.csv','w+') as f:
        w = csv.writer(f, delimiter = ',')
        w.writerow(['Time'] + [semanticObj.meaning for semanticObj in SOs])
 
    with open('validation.csv','w+') as f:
        w = csv.writer(f, delimiter = ',')
        w.writerow(['Time'] +['DM']+['AM']+['GL']+['RL']+['SL'])
     
"""
function to append new data to log.csv file
input a list of the semantic object
"""
def write_to_log(SOs):

    with open('log.csv','a') as f:
        w = csv.writer(f, delimiter = ',')
        w.writerow([datetime.datetime.now()] + [semanticObj.value for semanticObj in SOs])
 
def write_to_log_validation(SOs,data):
    time=datetime.datetime.now()
    with open('log.csv','a') as f:
        w = csv.writer(f, delimiter = ',')
        w.writerow([time] +[semanticObj.value for semanticObj in SOs])
 
    with open('validation.csv','a') as f:
        w = csv.writer(f, delimiter = ',')
        w.writerow([time] +[x for x in data] )
 
def read_from_validation():
    with open('validation.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data
 
def read_from_log():
    with open('log.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))
    return data
#     with open('log.csv') as f:
#         r = csv.reader(f, delimiter = ',')
#         line_count = 0
#         data=np.array([])
#         for row in r:
#             if line_count == 0:
#                 name=", ".join(row)
#                 #print(name)
#                 line_count += 1
#             else:
#                 print(row)
#                 data[line_count]=row
#                 line_count += 1
#         #print(f'Processed {line_count} lines.')
#     return name,data

     
if __name__ == '__main__':
    
    # test module
    semantic_objects = SemanticMap()  #a list of semantic objects
    for i in semantic_objects:
        semantic_objects[i].values = 12
    #print(semantic_objects)
    
    define_log(semantic_objects.values())
    
    for i in range(10):
        write_to_log(semantic_objects.values())