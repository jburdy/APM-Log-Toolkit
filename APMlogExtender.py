#!/usr/bin/env python
 
import APMlogParserPOC
from datetime import datetime, timedelta
from dateutil import tz
 
tick = '0'
dt = 0
 
# http://copter.ardupilot.com/wiki/common-diagnosing-problems-using-logs/#unexpected_errors_including_failsafes
def printERR(msg):
    global tick, dt
    print dt, tick, 'ERR -',
    if msg[1][0] == 'Subsys=5':
        print 'Throttle failsafe :',
        if msg[1][1] == 'ECode=1': print 'throttle dropped below FS_THR_VALUE meaning likely loss of contact between RX/TX',
        if msg[1][1] == 'ECode=0': print 'RX/TX contact likely restored',
    if msg[1][0] == 'Subsys=11':
        print 'GPS :',
        if msg[1][1] == 'ECode=0': print 'GPS Glitch cleared',
        if msg[1][1] == 'ECode=2': print 'GPS Glitch',
    if msg[1][0] == 'Subsys=16':
        print 'EKF/InertialNav Check :',
        if msg[1][1] == 'ECode=0': print 'Bad Variance cleared',
        if msg[1][1] == 'ECode=2': print 'Bad Variance',
    if msg[1][0] == 'Subsys=17':
        print 'EKF/InertialNav Failsafe :',
        if msg[1][1] == 'ECode=2': print 'EKF Failsafe triggered',
    print '-', msg[1]
 
def printMODE(msg):
    global tick, dt
    print dt, tick, 'Mode -',
    if msg[1][0] == 'Mode=0': print 'Stabilize',
    if msg[1][0] == 'Mode=1': print 'Acro',
    if msg[1][0] == 'Mode=2': print 'AltHold',
    if msg[1][0] == 'Mode=3': print 'Auto',
    if msg[1][0] == 'Mode=4': print 'Guided',
    if msg[1][0] == 'Mode=5': print 'PosHold',
    if msg[1][0] == 'Mode=6': print 'RTL',
    if msg[1][0] == 'Mode=7': print 'Circle',
    if msg[1][0] == 'Mode=8': print 'Position',
    if msg[1][0] == 'Mode=9': print 'Land',
    if msg[1][0] == 'Mode=10': print 'OF_Loiter',
    print '-', msg[1]
 
# http://ardupilot.com/forum/viewtopic.php?f=80&t=11945
def parseGPSDate(GPSweek, GPSms):
    return datetime(1980, 1, 6) + timedelta(weeks=GPSweek, hours=2, seconds=(GPSms/1000)-16)
 
def getValInt(v):
    return int(v.split('=')[1])
     
def printMsg(msg):
    global tick
    global dt
    if msg[0] == 'ERR': printERR(msg)
    if msg[0] == 'MODE': printMODE(msg)
    if msg[0] == 'CURR': tick = str(float(msg[1][0].split('=')[1])/60000.0)[:6]
    if msg[0] == 'GPS': dt = parseGPSDate(getValInt(msg[1][2]), getValInt(msg[1][1]))
    #print msg
 
 
 
p = APMlogParserPOC.SDLog2Parser()
p.setDebugOut(True)
p.setCorrectErrors(True)
d = p.process('testLog/log.bin')
 
 
 
for i in d:
    printMsg(i)