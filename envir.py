import os
import random,time

while True:
    dat1=random.randint(1,1000)
    os.environ['Dat1']=str(dat1)
    print (os.environ.get('Dat1'))
    time.sleep(1)