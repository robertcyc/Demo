import logging,time
import os

class pyLogger:
    def __init__(self,loggerName):
        self.loggerName=loggerName
        self.dateFormat='[%Y-%m-%d %H:%M:%S] '
        self.logName =time.strftime("%Y-%m-%d")+str(".log")
        logging.basicConfig(level=logging.DEBUG,
                            filename=self.logName,
                            filemode='a',
                            datefmt=self.dateFormat,
                            format='%(asctime)s%(name)s/%(levelname)s: %(message)s')
        self.logger=logging.getLogger(self.loggerName)

# ++++++++ TEST ZONE +++++++++++++
#sts=pyLogger("test")
#sts.logger.error("it is an error123")

# print(logging.NOTSET)   # 0
# print(logging.DEBUG)    # 10
# print(logging.INFO)     # 20
# print(logging.WARNING)  # 30
# print(logging.ERROR)    # 40
# print(logging.CRITICAL) # 50
#+++++++++++++++++++++++++++++
# print(logging.getLevelName(0))    # NOTSET
# print(logging.getLevelName(10))   # DEBUG
# print(logging.getLevelName(20))   # INFO
# print(logging.getLevelName(30))   # WARNING
# print(logging.getLevelName(40))   # ERROR
# print(logging.getLevelName(50))   # CRITICAL



