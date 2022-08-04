with open ('ipCfg.txt','r') as f:
    ipAddr=[]
    for line in f.readlines():
        ipAddr.append(line.rstrip())
    print (ipAddr)