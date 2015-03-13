import config
import time

# see config for verbose level
# return true if verbosed
def verbose( msg, *args, tag='General', lv='normal', pre='' ):
	ret = (config.verbose[lv] <= config.verboseLv)
	if (tag != None) :
		tag = '['+tag+']\t'
	else:
		tag = '\t'
	if ret:
		print(pre, tag, msg, *args)
		# log(config.log_path, pre, tag, msg, *args)
	log(config.log_path_full, pre, tag, msg, *args)
	return ret


def log(path, *args):
	f = open(path, 'a')
	f.write( time.ctime() + ';' )
	for i in args:
		f.write(' ' + str(i))
	f.write('\n')
