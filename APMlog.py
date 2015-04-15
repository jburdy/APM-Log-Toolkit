#!/usr/bin/env python
import APMlogParserPOC
import APMlogExtender

def getDict(logBinFilePath):
    d = APMlogParserPOC.Parse(logBinFilePath)
    return APMlogExtender.Extend(d)
    
def getJSON(logBinFilePath):
    import json
    return  json.dumps(getDictFromLog(logBinFilePath))
    
    
if __name__ == "__main__":
    d = getDict('testLog/log.bin')
    print d[-20:]
    
    d = getJSON('testLog/log.bin')
    print d[-20:]