#!/usr/bin/env python
 
import APMlogParserPOC
from datetime import datetime, timedelta
from dateutil import tz
 
tick = '0'
dt = 0
 
# https://github.com/diydrones/ardupilot/tree/master/ArduCopter
# https://github.com/diydrones/ardupilot/blob/master/ArduCopter/defines.h
# http://copter.ardupilot.com/wiki/common-diagnosing-problems-using-logs/#unexpected_errors_including_failsafes
refErrors = {
5:{
	'Subsys': 'Throttle failsafe',
	'ECode':{
		1:'throttle dropped below FS_THR_VALUE meaning likely loss of contact between RX/TX',
		0:'RX/TX contact likely restored'}},
11:{
	'Subsys': 'GPS',
	'ECode':{
		2:'GPS Glitch',
		0:'GPS Glitch cleared'}},
16:{
	'Subsys': 'EKF/InertialNav Check',
	'ECode':{
		2:'Bad Variance',
		0:'Bad Variance cleared'}},
17:{
	'Subsys': 'EKF/InertialNav Failsafe',
	'ECode':{
		2:'EKF Failsafe triggered',
		0:'?????????????????????????????',
		1:'?????????????????????????????'}}
}

def printERR(msg):
    global tick, dt
    print dt, tick, '- ERR -',
    try:
        print refErrors[msg['Subsys']]['Subsys'],
        print refErrors[msg['Subsys']]['ECode'][msg['ECode']]
    except:
        print '\n***************', msg, refErrors[msg['Subsys']]
 
refModeName = {0: 'Stabilize', 1: 'Acro', 2: 'AltHold', 3: 'Auto', 4: 'Guided', 5: 'PosHold', 6: 'RTL', 7: 'Circle', 8: 'Position', 9: 'Land', 10: 'OF_Loiter'}

def printMODE(msg):
    global tick, dt
    print dt, tick, '- Mode -',
    print refModeName[msg['Mode']],
    print '-', msg
 
# http://ardupilot.com/forum/viewtopic.php?f=80&t=11945
def parseGPSDate(GPSweek, GPSms):
    return datetime(1980, 1, 6) + timedelta(weeks=GPSweek, hours=2, seconds=(GPSms/1000)-16)
     
def printMsg(msg):
    global tick
    global dt
    if msg[0] == 'ERR': printERR(msg[1])
    if msg[0] == 'MODE': printMODE(msg[1])
    if msg[0] == 'CURR': tick = str(float(msg[1]['TimeMS'])/60000.0)[:6]
    if msg[0] == 'GPS': dt = parseGPSDate(msg[1]['Week'], msg[1]['TimeMS'])
    #print msg
 
 
 
def ExtendWithDate(logData):
    cursDate = None
    for i in logData:
        if i[0] == 'GPS':
            d = parseGPSDate(i[1]['Week'], i[1]['TimeMS'])
            if not cursDate: cursDate = d
            i[1]['DateTime'] = str(d)
    for i in logData: # estimation date autre evenements
        if i[0] == 'GPS': cursDate = i[1]['DateTime']
        else: i[1]['DateTime'] = cursDate
        
    return logData   

def ExtendWithErrText(logData):
    pass
 

def Extend(logData):
    return ExtendWithDate(logData)

if __name__ == "__main__":


    import APMlogParserPOC
    d = APMlogParserPOC.Parse('testLog/log.bin')
    
    for i in d:
        printMsg(i)
    
