# -*- coding: utf-8 -*-
"""
Nefeli Lefa
PRPA, Práctica 1
Consumer-Producers
"""

from multiprocessing import Process, Semaphore, Value, Manager
import random
import math

N=3  #Producers
m=3  #Number of products that can produce each producer

def produce(i,sem_list, sem_full, sem_empty ,values):
    
    for j in range(m):
        sem_empty.acquire() #after the first time, wait until the consumer consumes an item
        sem_list.acquire() 
        val0=random.randint(1, 10)
        val=random.randint(11, 20)
        
        if values.value==-2: #first round
            values.value=val0
                
        else:
            values.value+=val #create values in ascending order
            
        sem_list.release()    
        print(f"Producer {i} produced: { values.value} \n")
        sem_full.release() #signal for the consumer
    
    #exits for loop, when m items have been producted and stops producing  
    sem_empty.acquire() 
    values.value=-1 
    sem_full.release()
  
    
def consume(sem_list, sem_full, sem_empty, values, result):
    
    for i in range(N):
        sem_full[i].acquire() #wait until every producer has produced
        
    while flag(values): 
        m=math.inf #compare with something big
        
        for k in range (N): #find the minimum value
            v=values[k].value
            if v < m and v!=-1:
                m=v
                p=k
                
        print(f"Consumer consumed item {m} from producer {p}.  \n ")       
        result.append(m)
        sem_empty[p].release() #signal to producer p to produce an item
        sem_full[p].acquire()  #wait until the producer p has produced an item
        
    return result
    
def flag(values): #if all producers have stopped, flag-> False, thus the consumer will stop consuming
    
    flag=False
    for j in values:
        if j.value !=-1:
            flag=True
    return flag
    
  
def main():
     
     sem_list=[Semaphore(1) for i in range(N)] 
    
     sem_full_list=[Semaphore(0) for i in range(N)]
     
     sem_empty_list=[Semaphore(1) for i in range(N)]
     
     values=[Value('i',-2) for i in range(N)]
     
     manager=Manager()
     
     result=manager.list()
     
     p=[Process(target=produce, args=(i, sem_list[i], sem_full_list[i], sem_empty_list[i], values[i])) for i in range(N)]
        
     c=Process(target=consume, args=(sem_list, sem_full_list, sem_empty_list, values, result))
         
     for k in p:
         k.start()
         
     c.start()
     
     for k in p:
         k.join()
         
     c.join()
    
     print(result)
     print(f'End')                  
    
if __name__=='__main__':
    main()