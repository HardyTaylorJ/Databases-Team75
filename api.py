from Tkinter import*
#from tkinter import messagebox
import base64
import pymysql as sql
import os
from datetime import date
from datetime import datetime
import datetime
conn = sql.connect(host = "academic-mysql.cc.gatech.edu",
                        passwd = "XzXVaWnA",
                        user = "cs4400_75",
                        db = "cs4400_75") 
cursor = conn.cursor()
active_user = None

## todo: 
# add datapoint
# add poi
# get pending data points
# get pending city officials
# accept pending city officials
# reject pending city officials
# accept pending data points
# reject pending data points
# flag


def login(username, password):
	""" 
	verifies username password combination and returns user type

	@return string
	"Official"
	"Scientist"
	"Admin"
	"Invalid"
	"""
	# try:
	# conn = sql.connect(host = "academic-mysql.cc.gatech.edu",
 #                        passwd = "XzXVaWnA",
 #                        user = "cs4400_75",
 #                        db = "cs4400_75") 
	cursor =  conn.cursor()
	statement = "SELECT * FROM User WHERE USERNAME=%s and PASSWORD=%s"
	cursor.execute(statement, (username, password))
	user = cursor.fetchone()
	print user
	if user == None:
		return "Invalid"
	print user[3]
	active_user = username
	return user[3]
	# except:
	# 	print "Error","Connection Error"
	# return "Official" #Fixme: change this

def logout(): #FIXME is this needed?
	active_user = None
	return

def add_user(username,  email, pwd, confpwd, user_type, type_args):
	""" 
	registers user in the database

	@return int error_code: FIXME: maybe not the best way to do this
	0: no error
	1: duplicate username
	2: duplicate email
	"""

	print type_args[0]
	print type_args[1]

	if confpwd == pwd:
		users = cursor.execute("SELECT * FROM User WHERE Username = %s",(username))
		# users = cursor.fetchone()
		if users == 0:
			cursor.execute("INSERT INTO User VALUES (%s, %s, %s, %s)", (username, email, pwd, user_type))
			conn.commit()
			if user_type == "City Official":
				cursor.execute("INSERT INTO City_Official VALUES (%s, %s, %s, %s, %s)",(username, None, type_args[2], type_args[0], type_args[1]))
				conn.commit()
		else:
			print "User already exists"
	else:
		print "passwords dont match"
		#window + print("passwords do not match")
	

	return 0

def accept_official(username):
	return

def reject_official(username):
	return

def accept_dp(datetime):
	return

def reject_dp(datetime):
	return

def add_datapoint(loc_name, time_date, data_type, data_val):
	"""
	adds a datapoint to the database and returns an error code

	@param array timedate [year, month, day, hour, min, sec] 

	@return int error_code 
	0: success
	"""
	return 0

def add_poi(loc_name, city, state, zip_code):
	"""
	adds a POI to the database

	@return int error_code
	0: success

	"""
	return 0

def get_cities(): #fixme: does this need to deend on state
	"""
	returns list of valid cities in the database

	@return array city_list
	"""
	cursor.execute("select Distinct City from City_State")
	cities = cursor.fetchall()


	return [x[0] for x in cities]
	# return ["Atlanta", "Macon", "Savanna"]


def get_states():
	"""
	returns list of valid states in the database

	@return array state_list
	"""
	# return ["GA", "TN", "NY"]
	cursor.execute("select Distinct State from City_State")
	states = cursor.fetchall()

	return [x[0] for x in states]

def get_poi_names():
	"""
	returns a list of POI names

	@return array poi_names
	"""
	# return ["Little 5 Points", "Georgia Tech", "Macon Mall"]
	cursor.execute('select Distinct Location_Name from POI')
	pois = cursor.fetchall()
	return [x[0] for x in pois]

def get_pending_datapoints():
	return

def get_pending_officials():
	return

def get_poi(vpoi,vcity,vstate,vzip,vflagged,sdate,edate):
	"""
	@param array filters 
	pending
	location_name
	city
	state
	zip
	flagged
	date_flagged_start
	date_flagged_end
	"""
	# for k in filters

	joincondition  = []
	if vpoi != "None":
		joincondition.append(" Location_Name = '" + vpoi+"'") 

	if vcity != "None":
		joincondition.append(" city = '" + vcity+"'")

	if vstate != "default":
		joincondition.append(" state = '" + vstate+"'")

	if vzip != "": #say 00000
		joincondition.append(" zip = '" + vzip+"'")

	if vflagged == 1:
		joincondition.append(" flag = 1")
		if sdate != None:
			sdatestring ='Date_flagged>"{}"'.format(sdate) 
			joincondition.append(sdatestring)

		if edate != None:
			edatestring = 'Date_flagged<"{}"'.format(edate) 
			joincondition.append(edatestring)
	else:
		joincondition.append(" flag = 0")



	joincondition = " AND ".join(joincondition) 		
	
	mainsqlquery = "SELECT Location_Name, City, State,  ZIP, Flag, Date_flagged FROM POI"

	if bool(joincondition): 
		x = mainsqlquery + " WHERE " + joincondition
		print x
		cursor.execute(x)
		result = cursor.fetchall()
		print result
		return result
	else:
		cursor.execute(mainsqlquery)
		return cursor.fetchall()


	# return [["GT", "1", "2", "3", "4", "5"],["TECH", "a", "b", "c", "d", "e"],["GATECH", "q", "w", "e", "r", "t"]]#FIXME: remove this

def get_datapoints(filters):
	"""
	@param dictionary filters 
	pending
	location_name
	city
	state
	zip
	flagged
	date_flagged_start
	date_flagged_end
	"""
	# for k in filters.keys

def get_years():
	return list(reversed(range(1900, 2018)))


def get_months():
	# return ['01','02','03','04','05','06','07','08','09','10','11','12']
	return list(range(1,13))

def get_days(month):
	return list(range(1, 32))

def get_hours():
	return list(range(1, 25))
def get_minutes():
	return list(range(1, 61))

def get_poi_report(sort_option, order_option):
	mainview = "SELECT *FROM POIREPORT "
	Pendingdatapoints = cursor.execute( mainview + " ORDER BY " + sort_option + " " +order_option) 

	Thereport = cursor.fetchall()
	print Thereport
	return Thereport
	# return [ ['01','02','03','04','05','06','07','08','09','10','11','12'], reversed([1,2,3,4,5,6,7,8,9,10,11,12]) ]

def get_pending_dp():
	return [list(range(1, 7)), list(reversed(range(1, 7)))]

def get_pending_off():
	return [list(range(1, 6)), list(reversed(range(1, 6)))]

def get_poi_detail(data_type, data_min, data_max, timedate_start, timedate_end):
	"""
	@returns array of length 3 arrays of format [data type, data value, timedate]
	"""
	return [[11,22,33][66,77,88]]


def flag_poi(poi_name):
	return

def unflag_poi(poi_name):
	return