import config

def verbose( msg, tag='General', lv='normal' ):
	if (config.verbose[lv] >= config.verboseLv):
		print('  ['+tag+']\t', msg )

# TODO: logger
# def log(msg):