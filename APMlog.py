#!/usr/bin/env python
import APMlogParserPOC
import APMlogExtender

def getDict(logBinFilePath):
    d = APMlogParserPOC.Parse(logBinFilePath)
    return APMlogExtender.Extend(d)
    
def getJSON(logBinFilePath):
    import json
    return  json.dumps(getDict(logBinFilePath))

class APMlog:
    
    def __init__(self, logPath):
        self.data = APMlogExtender.Extend(APMlogParserPOC.Parse(logPath))
        self.logStartAt = self.data[0][1]['DateTime']
        self.logStopAt = self.data[-1][1]['DateTime']
        
    def __repr__(self):
        return "Start @ %s and stop @ %s" % (self.logStartAt, self.logStopAt)
        
    def getEvent(self, evType):
        return filter(lambda x: x[0] == evType, self.data)
    
    def getMax(self, evType, cat):
        tmp = None
        for i in self.getEvent(evType):
            if i[1][cat] > tmp: tmp = i[1][cat]
        return tmp
    
    def getMaxSpeed(self):
        return self.getMax('GPS', 'Spd')
    
    def getMaxRelAlt(self):
        return self.getMax('GPS', 'RelAlt')
        
    
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        apmLog = APMlog(sys.argv[1])
    else:
        apmLog = APMlog('testLog/log.bin')
        
    print apmLog
    print apmLog.logStartAt
    print apmLog.getMaxSpeed()
    print apmLog.getMaxRelAlt()
    print apmLog.getEvent('ERR')