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
# sorting for pending data points
# finish poi detail
# put title bar on poi detail
# email address constraints with regex in google doc
# handle user input stuff like zip code
# 


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
	print 'entered accept official'
	cursor.execute("UPDATE City_Official SET Approved = TRUE WHERE Username = %s", username)
	conn.commit()
	print username

	return

def reject_official(username):
	print 'entered reject official'

	cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", username)
	conn.commit()
	print username
	return

def accept_dp(poi_name,datetime):
	print 'entered accept datapoint'

	print poi_name
	print datetime
	cursor.execute("UPDATE Data_Point SET Accepted = TRUE WHERE Location_name = %s AND Date_Time = %s",(poi_name, datetime) )
	conn.commit()
	return

def reject_dp(poi_name, datetime):
	print 'entered reject datapoint'

	cursor.execute("UPDATE Data_Point SET Accepted = FALSE WHERE Location_name = %s AND Date_Time = %s",(poi_name, datetime) )
	conn.commit()
	return

def add_datapoint(vpoilocation, vdatetime, vdatatype, vdatavalue):
	"""
	adds a datapoint to the database and returns an error code

	@param array timedate [year, month, day, hour, min, sec] 

	@return int error_code 
	0: success
	"""

	# if time>dt.datetime.now():
	# 	print 'time not valid'
	# 	return
	# 	#error message + print("the time given is not valid, (in the future) (i dunno what to say this correctly)")
	print vdatetime
	execute_string = "select * from Data_Point where Location_Name='{}'".format(vpoilocation) + ' and Date_Time="{}"'.format(vdatetime) 
	# cursor.execute("select * from Data_Point where Location_Name=%s and Date_Time=%s",(vpoilocation,vdatetime))
	cursor.execute(execute_string)
	checkDatapoi= cursor.fetchall()
	print checkDatapoi
	if len(checkDatapoi)==0:
		print vpoilocation
		print vdatetime
		print vdatavalue
		print None
		print vdatatype
		cursor.execute("INSERT INTO Data_Point Values(%s, %s, %s, %s, %s)", (vpoilocation, vdatetime, vdatavalue, None, vdatatype))
		conn.commit()
	else:
		print 'datapoint  with the same location name and date reading already exists'
	#error message + print("data point with the same location name and date reading already exists")

	return 0

def add_poi(vpoilocation, vcity, vstate, vzip):
	"""
	adds a POI to the database

	@return int error_code
	0: success

	"""
	vdateflagged = None
	vzip = int(vzip)
	print vzip
	# print len(vzip)
	print vstate.strip()
	if vpoilocation=="":
		print 'no location'
		return
	#error message + print("all of the fields must be filled")
	if vzip>100000:
		print 'incorrect zip code format'
		return
		#error message + print("please input a correct format of zipcode")

	cursor.execute("SELECT * FROM POI WHERE (City=%s and State=%s) or Location_Name = %s",(vcity,vstate,vpoilocation))
	checkDatapoint = cursor.fetchone() 
	if checkDatapoint:
		cursor.execute("INSERT INTO POI Values(%s, %s, %s, %s, %s, %s)", (vpoilocation, 0, vdateflagged, vzip, vcity, vstate))
		conn.commit()
	else:
		#error message + print("Poi with the same location name of combination of city and state already exists")
		print "POI with same location name of combination of city and state already exists"
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
	Mainview = "SELECT Location_Name, Data_Type, Data_Value, Date_Time FROM Data_Point WHERE Accepted IS NULL"

	cursor.execute(mainview)
	return cursor.fetchall()

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
	if vpoi != "any":
		joincondition.append(" Location_Name = '" + vpoi+"'") 

	if vcity != "any":
		joincondition.append(" city = '" + vcity+"'")

	if vstate != "any":
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
	return list(range(0, 24))
def get_minutes():
	return list(range(0, 60))

def get_poi_report(sort_option, order_option):
	mainview = "SELECT *FROM POIREPORT "
	Pendingdatapoints = cursor.execute( mainview + " ORDER BY " + sort_option + " " +order_option) 

	Thereport = cursor.fetchall()
	print Thereport
	return Thereport
	# return [ ['01','02','03','04','05','06','07','08','09','10','11','12'], reversed([1,2,3,4,5,6,7,8,9,10,11,12]) ]

def get_pending_dp():
	mainview = "SELECT Location_Name, Data_Type, Data_Value, Date_Time FROM Data_Point WHERE Accepted IS NULL"

	cursor.execute(mainview)
	return cursor.fetchall()
	# return [list(range(1, 7)), list(reversed(range(1, 7)))]

def get_pending_off():
	cursor.execute("SELECT User.Username, Email, City, State, Title FROM City_Official, User WHERE User_type = 'City Official' AND User.Username = City_Official.Username  AND Approved IS NULL")
	return cursor.fetchall()

	# return [list(range(1, 6)), list(reversed(range(1, 6)))]

def get_poi_detail(vpoilocation, vtype, vminvalue, vmaxvalue, vmindate, vmaxdate):
	"""
	@returns array of length 3 arrays of format [data type, data value, timedate]
	"""
	vjoincondition = ["Location_Name = '"+vpoilocation+"'"]
	if vtype != "All":
	vjoincondition.append("Data_Type = '" vtype+"'")

	if vminvalue!="" and vmaxvalue!="": #FIXME: better error checking
		vjoincondition.append("Data_Value > '" + vminvalue+ "'' AND "+  "Data_Value < '" + vmaxvalue+"'" ) 

	vjoincondition.append("Date_Time > '" + vminvalue+"'")
	vjoincodition.append("Date_Time < '" + vmaxvalue+"'")
	vjoincondition = " AND ".join(vjoincondition)
	vjoincondition = " WHERE " + vjoincondition

	Poidetails = cursor.execute("SELECT Data_Type, Data_Value, Date_Time FROM Data_Point {} ORDER BY Date_Time ".format(vjoincondition) )

	# return [[11,22,33],[66,77,88]]


def flag_poi(poi_name):
	return

def unflag_poi(poi_name):
	return

def get_datatypes():
	return ["Mold", "Air Quality Reading"]

def official_r(f):
	print 'entered reject official for ' +f[1] + "with an f[0] of "+ str(f[0].get())

	# cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", username)
	# conn.commit()
	print f[1]
	if f[0].get():
		cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", f[1])
		conn.commit()
		print "rejected "+f[1]

def official_a(f):
	print 'entered reject official for ' +f[1] + "with an f[0] of "+ str(f[0].get())

	# cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", username)
	# conn.commit()
	print f[1]
	if f[0].get():
		cursor.execute("UPDATE City_Official SET Approved = TRUE WHERE Username = %s", f[1])
		conn.commit()
		print "rejected "+f[1]


def datapoint_r(f):
	print 'entered data point for ' +f[1] + " at " + str(f[2]) +"with an f[0] of "+ str(f[0].get())

	# cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", username)
	# conn.commit()
	print f[1]
	if f[0].get():
		cursor.execute("UPDATE Data_Point SET Accepted = FALSE WHERE Location_name = %s AND Date_Time = %s",(f[1], str(f[2])) )
		conn.commit()
		print "rejected "+f[1]

def datapoint_a(f):
	print 'entered data point for ' +f[1] + " at " + str(f[2]) +"with an f[0] of "+ str(f[0].get())

	# cursor.execute("UPDATE City_Official SET Approved = FALSE WHERE Username = %s", username)
	# conn.commit()
	print f[1]
	if f[0].get():
		cursor.execute("UPDATE Data_Point SET Accepted = TRUE WHERE Location_name = %s AND Date_Time = %s",(f[1], str(f[2]) ))
		conn.commit()
		print "rejected "+f[1]



