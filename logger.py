import config

# see config for verbose level
def verbose( msg, tag='General', lv='normal', pre='' ):
	if (config.verbose[lv] <= config.verboseLv):
		print(pre, '['+tag+']\t', msg )

# TODO: logger
# def log(msg):