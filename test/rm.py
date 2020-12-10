import shutil
import os
if not os.path.exists('./output/'):
	print 'a'
else:
	shutil.rmtree('output')
