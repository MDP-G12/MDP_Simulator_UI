import config

# see config for verbose level
def verbose( msg, *args, tag='General', lv='normal', pre='' ):
	if (config.verbose[lv] <= config.verboseLv):
		print(pre, '['+tag+']\t', msg, args )

# TODO: logger
# def log(msg):
