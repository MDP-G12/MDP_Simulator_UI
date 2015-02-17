import config

# see config for verbose level
# return true if verbosed
def verbose( msg, *args, tag='General', lv='normal', pre='' ):
	if (config.verbose[lv] <= config.verboseLv):
		print(pre, '['+tag+']\t', msg, args )
		return True
	return False

# TODO: logger
# def log(msg):
