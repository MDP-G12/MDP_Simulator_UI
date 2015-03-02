import config

# see config for verbose level
# return true if verbosed
def verbose( msg, *args, tag='General', lv='normal', pre='' ):
	if (config.verbose[lv] <= config.verboseLv):
		if (tag != None) :
			tag = '['+tag+']\t'
		else:
			tag = '\t'
		print(pre, tag, msg, *args)
		# log(pre, tag, msg, *args)
		return True
	return False

# TODO: logger
def log(*args):
	print(*args)
