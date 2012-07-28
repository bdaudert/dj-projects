#!/usr/bin/python

usage = '''
	JsonDump model_name
        '''

import sys
from django.core import serializers
from my_meta import models

model_name = sys.argv[1]
obj = eval('models.%s' % model_name)

data = serializers.serialize('json', obj.objects.all())
out = open('%s.json' % model_name, 'w')
out.write(data)
out.close()
