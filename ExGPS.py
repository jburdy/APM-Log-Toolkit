#!/usr/bin/env python
import APMlog

# https://kml-samples.googlecode.com/svn/trunk/interactive/index.html
# http://gis.stackexchange.com/questions/130910/google-earth-plugin-deprecated-which-alternatives
# https://developers.google.com/maps/
# http://cesiumjs.org/ - http://d3js.org/ - http://kartograph.org/
# http://www.gpsvisualizer.com/

d = APMlog.getDict('testLog/log.bin')

print 'type, latitude, longitude, alt'
for i in filter(lambda x: x[0]=='GPS', d)[-50:]:
    print 'T', ',', i[1]['Lat'], ',', i[1]['Lng'], ',', i[1]['RelAlt']