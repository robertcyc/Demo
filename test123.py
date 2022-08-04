import subprocess


ret=subprocess.Popen("ipconfig /all",stdout=subprocess.PIPE)
for line in ret.stdout:
    print(line.decode('big5',errors='ignore'))
input("")
    # print(line.decode('gbk', errors='ignore'))




