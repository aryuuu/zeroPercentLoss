#!/usr/bin/python3

BAR_LENGTH = 65

def print_progress_bar(progress, total, title):
	percentage = "{0:.1f}".format(100 * (progress / total))
	filled_length = BAR_LENGTH * progress // total
	empty_length = BAR_LENGTH - filled_length
	bar = '=' * filled_length + '-' * empty_length + ' ' +percentage + '%' + ' ' + title
	print(bar + '\r', end='')
	
	if (progress == total):
		print()
