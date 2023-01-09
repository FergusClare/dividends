#!usr/bin/env python3
'''
	Company: VINST, Inc.
	Developer: Fergus W. Clare
	Contact: fergus@vinst.io
	Date: 12/31/2018
	Version: 1.0
	License: Access Restricted, Proprietary
'''

import calendar
from datetime import datetime, timedelta, date
from pytz import timezone

class USActiveTrading (object):

	def __init__(self, year=None):
		'''
			Caller of object has the ability to set a specific year 
			in order to test holiday functions on instantiation. If the 
			caller does not provide a date in integer format, the object
			will calculate the current year and use that for all other
			services in returning data.

			Example usage:
			==============
			>>> markets.USActiveTrading(year=2019)

			*Note: instantiating the class object of USActiveTrading creates the
			following global variables:
			- year (current year unless otherwise provided by caller)
			- timezone: defaults to EST for US markets
			- current_day_EST: '20190101' format for current day in EST
			- current_time_EST: '21:30' format for current time in EST
			- holidays: list of all holidays for the caller provided year (or default)
			- halfdays: list of all halfday sessions closing at 13:00 for the caller provided year (or default)

		'''
		self.tz = timezone('EST')
		if year:
			self.year = year
		else:
			self.year = datetime.now(self.tz).year
		self.month = datetime.strftime(datetime.now(self.tz), '%m')
		self.day = datetime.strftime(datetime.now(self.tz), '%d')
		self.current_day_EST = datetime.strftime(datetime.now(self.tz), '%Y%m%d')
		self.yesterday_EST = datetime.strftime(datetime.now(self.tz) - timedelta(1), '%Y%m%d')
		self.raw_yesterday_EST = datetime.now(self.tz) - timedelta(1)
		self.current_time_EST = datetime.strftime(datetime.now(self.tz), '%H:%M')
		self.weekday_index = datetime.now(self.tz).weekday()
		self.holidays = [ #see https://www.nyse.com/markets/hours-calendars for future holidays
			'{}'.format(self.nyd()), #nyday
			'{}'.format(self.mlk_day()), #mlkday
			'{}'.format(self.presidents_day()), #presday
			'{}'.format(self.good_friday()), #goodfriday
			'{}'.format(self.memorial_day()), #memorialday
			'{}'.format(self.independence()), #independence
			'{}'.format(self.labor_day()), #laborday
			'{}'.format(self.thanksgiving()), #thanksgiving
			'{}'.format(self.christmas()) #christmas
		]
		self.halfdays = self.halfday_sessions()
		self.last_active_day = self.get_last_open()

#############################################
#		SETTER METHODS FOR HOLIDAYS			#
#############################################
		
	def nyd(self, day_only=False):
		'''
			Returns the 01 as the first day in January.  Since this
			day is always a holiday, it's location within the week
			is immaterial to trading except for the caluclation of last_session
			which will automatically adjust active trading if the session falls
			on a Friday or Monday.

			Example usage:
			==============
			>>> markets.ActiveTrading().nyd(day_only=True)
			>>> 01 #for 2019
			>>> markets.ActiveTrading().nyd()
			>>> 20190101 #for 2019
		'''
		return '01' if day_only==True else '{}0101'.format(self.year)

	def mlk_day(self, day_only=False):
		'''
			Calculates the third Monday in January for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().mlkday()
			>>> 21 #for 2019
		'''
		weeks = calendar.monthcalendar(self.year, 1)
		third_week = lambda weeks: weeks[3] if weeks[0][0] == 0 else weeks[2]
		return third_week(weeks)[0] if day_only==True else '{}01{}'.format(self.year, third_week(weeks)[0])

	def presidents_day(self, day_only=False):
		'''
			Calculates the third Monday in February for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().mlkday()
			>>> 21 #for 2019
		'''
		weeks = calendar.monthcalendar(self.year, 2)
		third_week = lambda weeks: weeks[3] if weeks[0][0] == 0 else weeks[2]
		return third_week(weeks)[0] if day_only==True else '{}02{}'.format(self.year, third_week(weeks)[0])

	def good_friday(self, day_only=False):
		'''
			Calculates Easter using Bucher's Algorithm and then deducts two days
			to return Good Friday for the given year set on markets.ActiveTrading
			instantiation.

			Special thanks to Martin Diers for providing this sample of Bucher's Algorithm
		'''
		# see source code here: http://code.activestate.com/recipes/576517-calculate-easter-western-given-a-year/
		a = self.year % 19
		b = self.year // 100
		c = self.year % 100
		d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
		e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
		f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
		month = f // 31
		day = f % 31 + 1
		return datetime.strftime(date(self.year, month, day)-timedelta(2), '%d') if day_only==True else '{}04{}'.format(self.year, datetime.strftime(date(self.year, month, day)-timedelta(2), '%d'))    
		
	def memorial_day(self, day_only=False):
		'''
			Calculates the last Monday in May for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().memorial_day()
			>>> 27 #for 2019
		'''
		weeks = calendar.monthcalendar(self.year, 5)
		return max(weeks)[0] if day_only==True else '{}05{}'.format(self.year, max(weeks)[0]) # since monday is always the first day of the week, there will not be any instaces where max monday == 0

	def independence(self, day_only=False):
		return '04' if day_only==True else '{}0704'.format(self.year)

	def labor_day(self, day_only=False):
		'''
			Calculates the first Monday in September for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().labor_day()
			>>> 2 #for 2019
		'''
		weeks = calendar.monthcalendar(self.year, 9)
		first_week = lambda weeks: weeks[1] if weeks[0][0] == 0 else weeks[0]
		return first_week(weeks)[0] if day_only==True else '{}090{}'.format(self.year, first_week(weeks)[0])
	
	def thanksgiving(self, day_only=False):
		'''
			Calculates the fourth Thursday in November for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().thanksgiving()
			>>> 28 #for 2019
		'''
		weeks = calendar.monthcalendar(self.year, 11) #get all dates of the month of November in list format
		fourth_thurs = lambda weeks: weeks[4][3] if weeks[0][3] == 0 else weeks[3][3] #return day format as dd for the fourth thursday in the month
		thanks_index = lambda weeks: 4 if weeks [0][3] == 0 else 3 #return the index of the day in the week for thanksgiving day
		return weeks[thanks_index(weeks)].index(forth_thurs) if day_only==True else '{}11{}'.format(self.year, fourth_thurs(weeks)) #always the fourth Thursday in November 

	def christmas(self, day_only=False):
		'''
			Calculates the 25 or 23 of December for the current year
			and returns the day of the month as 'dd' to the caller.

			Example usage:
			==============
			>>> markets.ActiveTrading().christmas()
			>>> 25 #for 2019
			>>> 24 #for 2021		
		'''
		# if 25th falls on a Saturday, set preceeding Friday as holiday
		weeks = calendar.monthcalendar(self.year, 12)
		x = [25 in i for i in weeks] # find the week with Christmas day
		holiday_week = weeks[x.index(True)] # find the week index in range
		if 5 >= holiday_week.index(25): # if the day of the week < Saturday
			return '25' if day_only==True else '{}12{}'.format(self.year, 25) # return Christmas day
		else: # if the day of the week >= Saturday
			return '24' if day_only==True else '{}12{}'.format(self.year, 24) # return Christmas eve day

#############################################
#				GETTER METHODS				#
#############################################

	def is_holiday(self, date=None):
		if date:
			return True if date in self.holidays else False
		else:
			return True if self.current_day_EST in self.holidays else False

	def is_post_market(self):
		# 4PM to 8PM EST
		if '16:00' <= self.current_time_EST <= '20:00':
			return True
		elif self.is_holiday():
			return False
		else:
			return False

	def is_pre_market(self):
		# 4AM - 9:30AM EST
		if '04:00' <= self.current_time_EST <= '09:30':
			return True
		elif self.is_holiday():
			return False
		else:
			return False

	def is_open(self, date=None):
		'''
			Creates a list of Boolean values and then returns False if False
			exists in the list or True if there are no falsey values.  To generate
			the Boolean list, this function checks to see if the index of the 
			weekday in the given week is less than Saturday, if it is not a holiday
			and if the the current eastern time is greater than 4AM and less than 1PM EST
			on a specified holiday.

			Accepted optional parameters are date which can be in either string or datetime
			format. Function intelligently returns BOOL regardless of date type.

			Example Usage:
			==============
			>>> #Assuming the current date is not a holiday or weekend
			>>> markets.USActiveTrading().is_open()
			>>> True
		'''

		if isinstance(date, datetime) == True:
		# if a raw date has been provided by the caller
		#set all values in the list to truthy.  If false in list, market is not open.
			x = [
				date.weekday() < 5, # check to see if the date was during the work week
				self.is_holiday(date=datetime.strftime(date, '%Y%m%d')) == False, # check to see if the date was a holiday
			]
			return False if False in x else True # if any value is False in x, return False, otherwise is_open() returns True
		elif isinstance(date, str) == True: # if a string was provided as the optional data param to the function
			
			# requires str to be formated as %Y%m%d
			date = datetime.strptime(date, '%Y%m%d')
			x = [
				date.weekday() < 5, # check to see if the date was during the work week
				self.is_holiday(date) == False, # check to see if the date was a holiday
			]
			return False if False in x else True # if any value is False in x, return False, otherwise is_open() returns True			
		else:
			x = [
				self.weekday_index < 5,
				self.is_holiday() == False,
				'04:00' < self.current_time_EST < '20:00',
				(self.current_day_EST in self.halfday_sessions()) and ('04:00' < self.current_time_EST < '13:00')
			]
			return False if False in x else True

	def next_open(self, date):
		'''
			Function provides the next market open date when the date provided to the 
			function is not open.  Relies on the self.is_open() to determine market 
			availability.

			Intelligently checks if date provided is datetime or string and returns
			the next market open date as a string regardless of format date is delivered to function
			in.

			Example usage:
			>>> from markets import USActiveTrading
			>>> from datetime import datetime
			>>> opm = USActiveTrading()
			>>> date = '20210807' (market is not open on this day)
			>>> opm.next_open(date)
			'20210809'
			>>> new_date = datetime.strptime(date, '%Y%m%d')
			>>> new_date
			datetime.datetime(2021, 8, 7, 0, 0)
			>>> opm.next_open(new_date)
			'20210809'
		'''
		if isinstance(date, datetime) == True: # if the date provided is in datetime format
			if self.is_open(date) == False: # if date provided is not an active trading day
				return self.next_open(date + timedelta(days=1)) # increment the day by 1 and call recursively
			else: # if the date provided is active trading day
				return datetime.strftime(date, '%Y-%m%-d') # return the day as a string object
		elif isinstance(date, str) == True: # if the date parameter is passed as a string
			if self.is_open(date) == False: # if the date is not an active trading day
				# convert string to datetime object
				return self.next_open(datetime.strftime(datetime.strptime(date, '%Y%m%d') + timedelta(days=1), '%Y%m%d'))
			else: # if the market is active on the day provided
				date = '-'.join([date[:4], date[4:6], date[6:]])
				return date

	def is_closed(self):
		'''
			Returns a boolean value to indicate if the market is closed.  This
			function calls self.is_open() and returns False self.is_open() returns True or True
			if self.is_open() returns False.

			See self.is_open() for more information and example usage.
		'''
		return False if self.is_open() == True else True

	def weekday_of_holiday(self, month, day):
		'''
			Returns the day of the week from 0-6 for the user
			provided month and day of the current year.

			This data is helpful in determining if certain holidays
			like Indepedence, Thanksgiving and Christmas Days will
			be open for half day trading sessions. 

			See the is_halfday_session() for more information.

			Example usage:
			==============
			>>> markets.ActiveTrading().is_off_holiday(12,25)
			>>> 1 #Tuesday is Christmas for 2018
			>>> markets.ActiveTrading().is_off_holiday(1,1)
			>>> 0 #Monday is New Years for 2018	
		'''
		weeks = calendar.monthcalendar(self.year, month) #set weeks to the calendar month provided for the current year during class instantiation
		for week in weeks: #loop through each week in the weeks list
			if day in week: #if the day provided by the caller is in the list of the week
				day_of_week = weeks[weeks.index(week)].index(int(day)) #set the day of the week as 0-6 to the day of the week.
				return day_of_week #return the day of the week to the caller
			else:
				pass

	def halfday_sessions(self):
		'''
			Returns a list of celebrated halfdays to the caller based on the NYSE
			calendar for 2018 through 2021 holidays. See this page for additional details:
			https://www.nyse.com/markets/hours-calendars.

			If an actual holiday falls within an active work week, the markets are open a halfday.
			If the observed holiday falls on a Saturday, the markets will be closed the preceeding Friday.
			If the observed holiday falls on a Sunday, the markets will be closed the following Monday.


			Example usage:
			==============
			>>> markets.ActiveTrading().halfday_sessions()
			>>> ['20190704', '20191128', '20191225'] #for Independence, Thanksgiving and Christmas days in 2019
		'''
		halfs=['{}'.format(self.thanksgiving())] #set the new halfdays list adding thanksgiving which always occurs on a thursday
		ind = self.weekday_of_holiday(7,int(self.independence(day_only=True))) #get the month and day for independence day (celebrated)
		christmas = self.weekday_of_holiday(12, int(self.christmas(day_only=True))) #get the month and day for Christmas day (celebrated)
		if 4 > ind > 0: #if independence day does not fall on a Friday
			halfs.append(self.independence()) #add independence day to the halfdays list
		if christmas < 5 and self.christmas(day_only=True) == '25': #if Christmas is a Saturday and the date of observance is the 25th
			halfs.append(self.christmas()) #add Christmas to the halfdays observed list
		return halfs #return the list of halfdays

	def get_last_month_number(self):
		calendar_months = list(range(1,13)) #set a range of month numbers 1-12
		if int(self.month) - 1 < calendar_months[0]:
			return calendar_months[-1]
		else:
			return int(self.month)

	def get_next_month_number(self):
		calendar_months = list(range(1,13)) #set a range of month numbers 1-12
		if int(self.month) + 1 > calendar_months[11]:
			return calendar_months[0]
		else:
			return int(self.month)	

	def get_week_index(self, month):
		for week in month: #loop through the month
			if int(self.day) in week: #if today's day is in the week
				return month.index(week) #get the week in the month that contains today	

	def recursion(self, raw_yesterday):
		yesterday = raw_yesterday
		x = self.is_open(yesterday)
		while x == False: # while yesterday wasn't open
			yesterday = yesterday - timedelta(1)
			x = self.is_open(yesterday) # check and see if the day before yesterday was open
		return datetime.strftime(yesterday, "%Y%m%d")

	def get_last_open(self):

		month = calendar.monthcalendar(self.year, int(self.month)) #[[0, 1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12, 13], [14, 15, 16, 17, 18, 19, 20], [21, 22, 23, 24, 25, 26, 27], [28, 29, 30, 31, 0, 0, 0]]
		w_index = self.get_week_index(month)

		'''
			if the index of the week is in the first two weeks of the month
			and the Thursday before the current date is in the previous month,
			set the month to the previous month and the w_index to the 
			index of the week containing the prior Thursday from the prior month.
		'''
		if w_index <= 1 and month[w_index][3] == 0:
			month = calendar.monthcalendar(self.year, self.get_last_month_number())
			w_index = self.get_week_index(month)

		#CALC OF LAST DAY WHEN CURRENT DAY IS MONDAY
		if self.weekday_index == 0 and self.is_open() == False: #if today is Monday and the markets are not open
			date_data = '{}{}{}'.format(
				self.year, 
				self.month, 
				month[w_index-1][3] if len(list(str(month[w_index][3]))) > 1 else '0{}'.format(month[w_index][3])) 
			return self.recursion(datetime.strptime(date_data, '%Y%m%d')) #return Thursday
		elif self.weekday_index == 0 and self.is_open() == True:
			date_data = datetime.strftime(datetime.now(self.tz) - timedelta(3), '%Y%m%d') 
			return self.recursion(datetime.strptime(date_data, '%Y%m%d')) #return Friday
		#CALC OF LAST DAY WHEN CURRENT DAY IS SAT OR SUN
		elif self.weekday_index in [5, 6]:
			date_data = datetime.strftime(datetime.now(self.tz) - timedelta(2), '%Y%m%d') if self.weekday_index == 5 else datetime.strftime(datetime.now(self.tz) - timedelta(3), '%Y%m%d') 
			return self.recursion(datetime.strptime(date_data, '%Y%m%d')) #return Thursday
		elif 0 < self.weekday_index < 5:
			return self.recursion(self.raw_yesterday_EST) 
		'''
			+---------------+---------------+-----------+---------------+
			| Day of week	| weekday_index	| is_open	| get_last_open	|
			+---------------+---------------+-----------+---------------+
			| Monday		| 0				| False		| Thursday		| # based on open hours
			+---------------+---------------+-----------+---------------+
			| Monday		| 0				| True		| Friday		|
			+---------------+---------------+-----------+---------------+
			| Tuesday		| 1				| True		| Monday		|
			+---------------+---------------+-----------+---------------+
			| Wednesday		| 2				| True		| Tuesday		|
			+---------------+---------------+-----------+---------------+
			| Thursday		| 3				| True		| Wednesday		|
			+---------------+---------------+-----------+---------------+
			| Friday		| 4				| True		| Thursday		|
			+---------------+---------------+-----------+---------------+
			| Saturday		| 5				| False		| Thursday		|
			+---------------+---------------+-----------+---------------+
			| Sunday		| 6				| False		| Thursday		|
			+---------------+---------------+-----------+---------------+
		'''




