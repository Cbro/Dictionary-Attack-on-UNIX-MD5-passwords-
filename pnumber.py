#!/usr/bin/python

# Year
for yr in range(0, 100):
	if yr < 10:
		yr_str = '0' + str(yr)
	else:
		yr_str = str(yr)
		
	# Month
	for mon in range (1,13):
		if mon < 10:
			mon_str = '0' + str(mon)
		else:
			mon_str = str(mon)
		
		# Day
		for day in range (1,32):
			if day < 10:
				day_str = '0' + str(day)
			else:
				day_str = str(day)
			
			# YYMMDD
			print yr_str + mon_str + day_str
				