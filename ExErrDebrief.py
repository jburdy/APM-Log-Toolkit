#!/usr/bin/env python
import APMlog

# https://kml-samples.googlecode.com/svn/trunk/interactive/index.html
# http://gis.stackexchange.com/questions/130910/google-earth-plugin-deprecated-which-alternatives
# https://developers.google.com/maps/
# http://cesiumjs.org/ - http://d3js.org/ - http://kartograph.org/
# http://www.gpsvisualizer.com/

d = APMlog.getDict('testLog/log.bin')

for err in filter(lambda x: x[0]=='ERR', d)[-50:]:
    print err
    