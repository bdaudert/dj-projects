#!/use/bin/python
import sys
#from django.core import serializers
import json
import os

usage = '''
        JsonMod.py model_name
        '''

model_name = '%s' % sys.argv[1]
file_name = '%s.json' % model_name
out_file_name ='New%s' % file_name

if os.path.isfile(out_file_name):
    os.remove(out_file_name)

in_file = open(file_name, 'r')
data =  json.loads(in_file.read())
in_file.close()


out_file = open (out_file_name, 'a')
#print data[0]
#print data[0]['fields']
i_d = 0

for i, dat in enumerate(data):
    i_d+=1
    ucan_id = dat['pk']

    dat['fields']['ucan_station_id'] = ucan_id
    dat['pk'] = i_d


data_out = json.dumps(data)
out_file.write(data_out)
out_file.close()
