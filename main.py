import Tkinter as tk
from Tkinter import *
import api
import tktable
import datetime
# from Tkinter import ttk
LARGE_FONT=("Verdana", 12)

## TODO
# pending data points
# pending city officials
# fix datetime

class TKMain (tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # All frames (pages) must be included in this list
        for F in (LoginPage, RegisterPage, SciPortalPage, AddDPPage, AddPOIPage, OffPortalPage, AdminPortalPage, ViewPOIPage, POIReportPage, PDPPage, POPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky=N+E+S+W)
        self.show_frame(LoginPage)


    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()


class PageTemplate(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent)

class LoginPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Login", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10, sticky=N+E+S+W)

        uname_label = tk.Label(self, text="Username").grid(row=1, column=0, pady = 20)
        pwd_label = tk.Label(self, text="Password").grid(row=2, column=0, pady = 20)

        uname_entry = tk.Entry(self)
        uname_entry.grid(row=1, column=1, pady = 20, padx= 20)
        pwd_entry = tk.Entry(self)
        pwd_entry.grid(row=2, column=1, pady = 20, padx= 20)


        reg_button = tk.Button(self, text="Register", command=lambda :self.register(controller))
        reg_button.grid(row=4, column=0, padx = 20, pady = 10)

        login_button = tk.Button(self, text="Login", command=lambda :self.login(controller, uname_entry.get(), pwd_entry.get()))
        login_button.grid(row=4, column=1, padx = 20, sticky="E")

        # table = tktable.Table(parent, 
        #     rows = 5,
        #     cols = 5
        # )
        # table.grid(row=5)



    def login(self, controller, uname, pwd):
        user_type  = api.login(uname, pwd)
        #check login creds
        #
        if user_type == "Invalid":
            return
        #   create popup window sayig its invalid
        #
        if user_type == "Admin":
            controller.show_frame(AdminPortalPage)

        #   go to admin portal
        #
        if user_type == "City Official":
            controller.show_frame(OffPortalPage)
        #   go to city official portal
        #
        if user_type == "City Scientist":
            controller.show_frame(SciPortalPage)
        #   go to city scientist portal


        # controller.show_frame(SciPortalPage)

        # controller.show_frame(OffPortalPage)
        # controller.show_frame(AdminPortalPage)


    def register(self, controller):
        controller.show_frame(RegisterPage)

class RegisterPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Register", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        uname_label = tk.Label(self, text="Username").grid(row=1, column=0, pady = 5)
        email_label = tk.Label(self, text="Email").grid(row=2, column=0, pady = 5)
        pwd_label = tk.Label(self, text="Password").grid(row=3, column=0, pady = 5)
        cpwd_label = tk.Label(self, text="Confirm Password").grid(row=4, column=0, pady = 5)
        type_label = tk.Label(self, text="User Type").grid(row=5, column=0, pady = 5)

        uname_entry = tk.Entry(self)
        uname_entry.grid(row=1, column=1, pady = 5, padx= 20)
        email_entry = tk.Entry(self)
        email_entry.grid(row=2, column=1, pady = 5, padx= 20)
        pwd_entry = tk.Entry(self)
        pwd_entry.grid(row=3, column=1, pady = 5, padx= 20)
        cpwd_entry = tk.Entry(self)
        cpwd_entry.grid(row=4, column=1, pady = 5, padx= 20)

        #variable in the dropdown
        type_var = StringVar(self)
        type_var.set("City Official") #FIXME: get from db?
        #set trace on var
        # observer_name = trace_variable("w", callback)

        #dropdown box
        type_option = OptionMenu(self, type_var, "City Official", "City Scientist").grid(row=5, column=1, padx = 20, pady = 10, sticky = "W")

        #TODO: add section that depends on user type


        officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        officials_frame.grid(row = 6, columnspan=2, padx = 20)

        officials_title = tk.Label(officials_frame, text="Fill out this form if you chose city official").grid(row=0, column=0, pady = 5, columnspan=2)
        city_label = tk.Label(officials_frame, text="City").grid(row=1, column=0, pady = 5)
        state_label = tk.Label(officials_frame, text="State").grid(row=2, column=0, pady = 5)
        title_label = tk.Label(officials_frame, text="Title").grid(row=3, column=0, pady = 5)

        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (officials_frame, city_var) + tuple(city_options))
        city_dropdown.grid(row=1, column=1, padx = 20, pady = 5, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (officials_frame, state_var) + tuple(state_options))
        state_dropdown.grid(row=2, column=1, padx = 20, pady = 5, sticky="W")


        title_entry = tk.Entry(officials_frame)
        title_entry.grid(row=3, column=1, pady = 5, padx=20)

        city_official_info = (city_var.get(), state_var.get(), title_entry.get())
        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller, uname_entry.get(),  email_entry.get(),  pwd_entry.get(), cpwd_entry.get(), type_var.get(), (city_var.get(), state_var.get(), title_entry.get())))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def submit(self, controller, username, email, pwd, cpwd, user_type, type_args): #FIXME: probably need to pass an array with values to register with
        api.add_user(username, email, pwd, cpwd, user_type, type_args) #FIXME: error handling

        controller.show_frame(LoginPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(LoginPage)

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()

class SciPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        add_dp_button = tk.Button(self, text="Add Data Point", command=lambda :self.add_dp(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        add_poi_button = tk.Button(self, text="Add POI", command=lambda :self.add_poi(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")


    def add_dp(self, controller):
        controller.show_frame(AddDPPage)

    def add_poi(self, controller):
        controller.show_frame(AddPOIPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)



class AddDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add Data Point", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5, sticky="E")
        timedate_label = tk.Label(self, text="Time and Date of Data Reading").grid(row=2, column=0, pady = 5, sticky="E")
        datatype_label = tk.Label(self, text="Data Type").grid(row=4, column=0, pady = 5, sticky="E")
        dataval_label = tk.Label(self, text="Data Value").grid(row=5, column=0, pady = 5, sticky="E")

        timedate_entry = tk.Entry(self)
        timedate_entry.grid(row=2, column=1, pady = 5, padx= 20, sticky="W")
        dataval_entry = tk.Entry(self)
        dataval_entry.grid(row=5, column=1, pady = 5, padx= 20, sticky="W")


        ## location option menu
        #variable in the dropdown
        loc_options = self.get_loc_options()
        locname_var = StringVar(self)
        locname_var.set(loc_options[0])

        loc_dropdown = apply(OptionMenu, (self, locname_var) + tuple(loc_options))
        loc_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")

        # datetime options
        date_frame = tk.Frame(self)
        date_frame.grid(row=2, column=1, pady = 5, sticky="W", padx = 20)

        #month
        month_options = self.get_month_options()
        month_var = StringVar(self)
        month_var.set(month_options[0])

        month_dropdown = apply(OptionMenu, (date_frame, month_var) + tuple(month_options))
        month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        day_var = StringVar(self)
        day_var.set(day_options[0])

        day_dropdown = apply(OptionMenu, (date_frame, day_var) + tuple(day_options))
        day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(date_frame, text="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        year_var = StringVar(self)
        year_var.set(year_options[0])

        year_dropdown = apply(OptionMenu, (date_frame, year_var) + tuple(year_options))
        year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")

        # dateto_label = tk.Label(self, text="to").grid(row=7, column=1, pady = 0)

        ##time stuff
        time_frame = tk.Frame(self)
        time_frame.grid(row=3, column=1, pady = 5, sticky="W", padx = 20)
        #hour
        hour_options = self.get_hour_options()
        hour_var = StringVar(self)
        hour_var.set(month_options[0])

        hour_dropdown = apply(OptionMenu, (time_frame, hour_var) + tuple(hour_options))
        hour_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(time_frame, text=":").grid(row=0, column=1, sticky = 'E')

        #minute
        minute_options = self.get_minute_options()
        minute_var = StringVar(self)
        minute_var.set(day_options[0])

        minute_dropdown = apply(OptionMenu, (time_frame, minute_var) + tuple(minute_options))
        minute_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        # slash_label2 = tk.Label(time_frame, text ="/").grid(row=0, column=3,sticky = 'E')


        ## datatype option menu
        datatype_options = self.get_datatype_options()
        datatype_var = StringVar(self)
        datatype_var.set(datatype_options[0])
        datatype_dropdown = apply(OptionMenu, (self, datatype_var) + tuple(datatype_options))
        datatype_dropdown.grid(row=4, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller, locname_var.get(), datetime.datetime(int(year_var.get()), int(month_var.get()), int(day_var.get()), hour=int(hour_var.get()), minute=int(minute_var.get())), datatype_var.get(), dataval_entry.get()))
        sub_button.grid(row=8, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def get_hour_options(self):
        return api.get_hours()

    def get_minute_options(self):
        return api.get_minutes()


    def get_year_options(self):
        return api.get_years()

    def get_month_options(self):
        return api.get_months()

    def get_day_options(self):
        return api.get_days("1")

    def submit(self, controller, loc_name, time_date, data_type, data_val): #FIXME: probably need to pass an array with values to register with
        api.add_datapoint(loc_name, time_date, data_type, data_val)
        controller.show_frame(SciPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(SciPortalPage)

    def get_loc_options(self): #FIXME: get these from database
        return api.get_poi_names()

    def get_datatype_options(self): #FIXME: get these from database
        return api.get_datatypes()

class AddPOIPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add a New Location", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        city_label = tk.Label(self, text="City").grid(row=2, column=0, pady = 5)
        state_label = tk.Label(self, text="State").grid(row=3, column=0, pady = 5)
        zip_label = tk.Label(self, text="Zip Code").grid(row=4, column=0, pady = 5)

        locn_entry = tk.Entry(self)
        locn_entry.grid(row=1, column=1, pady = 5, padx= 20)
        zip_entry = tk.Entry(self)
        zip_entry.grid(row=4, column=1, pady = 5, padx= 20)

        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options))
        city_dropdown.grid(row=2, column=1, padx = 20, pady = 10, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options))
        state_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller, locn_entry.get(), city_var.get(), state_var.get(), zip_entry.get()))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

    def submit(self, controller, loc_name, city, state, zip_code): #FIXME: probably need to pass an array with values to register with
        api.add_poi(loc_name, city, state, zip_code)
        controller.show_frame(SciPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(SciPortalPage)

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()



class OffPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        fs_poi_button = tk.Button(self, text="Filter/Search POI", command=lambda :self.fs_poi(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        poi_report_button = tk.Button(self, text="POI Report", command=lambda :self.poi_report(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")

        sdetail_button = tk.Button(self, text="test poidetail", command=lambda :self.detail_window(parent, controller)).grid(row=4, column=0, padx = 20, pady = 10, sticky="W")


    def fs_poi(self, controller):
        controller.show_frame(ViewPOIPage)




    def poi_report(self, controller):
        controller.show_frame(POIReportPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)

# class POIDetail()
class POIDetail(PageTemplate):
    def __init__(self, parent, controller, poi_name, poi_timedate   ):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="POI Details", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10, padx=20)

        type_label = tk.Label(self, text="Data Type").grid(row=1, column=0, pady = 5, sticky = 'E')
        dval_label = tk.Label(self, text="Data Value").grid(row=2, column=0, pady = 5, sticky = 'E')


         ## datatype option menu
        datatype_options = self.get_datatype_options()
        datatype_var = StringVar(self)
        datatype_var.set(datatype_options[0])
        datatype_dropdown = apply(OptionMenu, (self, datatype_var) + tuple(datatype_options))
        datatype_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")

        ## data value range
        dval_frame = tk.Frame(self)
        dval_frame.grid(row=2, column=1, pady = 5, sticky="W", padx = 20)

        min_dval_entry = tk.Entry(dval_frame)
        min_dval_entry.grid(row=0, column=0, pady = 5, padx= 5, sticky="W")

        dval_to_label = tk.Label(dval_frame, text="to").grid(row=0, column=1, pady = 5)

        max_dval_entry = tk.Entry(dval_frame)
        max_dval_entry.grid(row=0, column=2, pady = 5, padx= 5, sticky="W") 




        ## date chooser stuff
        dateflag_label = tk.Label(self, text="Date Flagged").grid(row=3, column=0, pady = 5, sticky="E")
        date_frame = tk.Frame(self)
        date_frame.grid(row=3, column=1, pady = 5, sticky="W", padx = 20)

        #month
        month_options = self.get_month_options()
        month_var = StringVar(self)
        month_var.set(month_options[0])

        month_dropdown = apply(OptionMenu, (date_frame, month_var) + tuple(month_options))
        month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        day_var = StringVar(self)
        day_var.set(day_options[0])

        day_dropdown = apply(OptionMenu, (date_frame, day_var) + tuple(day_options))
        day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(date_frame, text="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        year_var = StringVar(self)
        year_var.set(year_options[0])

        year_dropdown = apply(OptionMenu, (date_frame, year_var) + tuple(year_options))
        year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")


        ## time
        time_frame = tk.Frame(self)
        time_frame.grid(row=4, column=1, pady = 5, sticky="W", padx = 20)
        #hour
        hour_options = self.get_hour_options()
        hour_var = StringVar(self)
        hour_var.set(month_options[0])

        hour_dropdown = apply(OptionMenu, (time_frame, hour_var) + tuple(hour_options))
        hour_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(time_frame, text=":").grid(row=0, column=1, sticky = 'E')
                #minute
        minute_options = self.get_minute_options()
        minute_var = StringVar(self)
        minute_var.set(day_options[0])

        minute_dropdown = apply(OptionMenu, (time_frame, minute_var) + tuple(minute_options))
        minute_dropdown.grid(row=0, column=2, padx = 1, sticky="W")


        dateto_label = tk.Label(self, text="to").grid(row=5, column=1, pady = 0)

        ##end date stuff
        end_date_frame = tk.Frame(self)
        end_date_frame.grid(row=6, column=1, pady = 5, sticky="W", padx = 20)
        #month
        month_options = self.get_month_options()
        end_month_var = StringVar(self)
        end_month_var.set(month_options[0])

        end_month_dropdown = apply(OptionMenu, (end_date_frame, end_month_var) + tuple(month_options))
        end_month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(end_date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        end_day_var = StringVar(self)
        end_day_var.set(day_options[0])

        end_day_dropdown = apply(OptionMenu, (end_date_frame, end_day_var) + tuple(day_options))
        end_day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(end_date_frame, text ="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        end_year_var = StringVar(self)
        end_year_var.set(year_options[0])

        end_year_dropdown = apply(OptionMenu, (end_date_frame, end_year_var) + tuple(year_options))
        end_year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")

        end_time_frame = tk.Frame(self)
        end_time_frame.grid(row=7, column=1, pady = 5, sticky="W", padx = 20)
        #hour
        hour_options = self.get_hour_options()
        end_hour_var = StringVar(self)
        end_hour_var.set(month_options[0])

        end_hour_dropdown = apply(OptionMenu, (end_time_frame, end_hour_var) + tuple(hour_options))
        end_hour_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(end_time_frame, text=":").grid(row=0, column=1, sticky = 'E')

        #minute
        minute_options = self.get_minute_options()
        end_minute_var = StringVar(self)
        end_minute_var.set(day_options[0])

        end_minute_dropdown = apply(OptionMenu, (end_time_frame, end_minute_var) + tuple(minute_options))
        end_minute_dropdown.grid(row=0, column=2, padx = 1, sticky="W")



        # zip_entry = tk.Entry(self)
        # zip_entry.grid(row=4, column=1, pady = 5, padx= 20, sticky="W")

        # flag_var = IntVar()
        # flag_check = Checkbutton(self, variable=flag_var)
        # flag_check.grid(row=5, column=1, pady = 5, sticky="W", padx = 20)

        # ## loc option menu
        # loc_options = ('None',) + tuple(self.get_loc_options())
        # loc_var = StringVar(self)
        # loc_var.set(loc_options[0])

        # loc_dropdown = apply(OptionMenu, (self, loc_var) + tuple(loc_options))
        # loc_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")



        # ## city option menu
        # city_options = self.get_city_options()
        # city_var = StringVar(self)
        # city_var.set(city_options[0])

        # city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options))
        # city_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        # ## state option menu
        # state_options = self.get_state_options()
        # state_var = StringVar(self)
        # state_var.set(state_options[0])
        # state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options))
        # state_dropdown.grid(row=2, column=1, padx = 20, pady = 10, sticky="W")

    def get_hour_options(self):
        return api.get_hours()

    def get_minute_options(self):
        return api.get_minutes()

    def get_datatype_options(self):
        return api.get_datatypes()



    def apply_filter(self, controller, table, location,city,state,zipc,flag,sdate,edate): #FIXME: probably need to pass an array with values to filter with
        titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *titles)
        table.see(idx)
        filtered_poi = api.get_poi(location,city,state,zipc,flag,sdate,edate)
        for r in filtered_poi:
            self.add_new_data(r, table)

    def add_new_data(self, row, table):
        #table.config(state='normal')
        table.insert_rows('end', 1)
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *row)
        table.see(idx)
        #table.config(state='disabled')


    def reset_filter(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def get_loc_options(self):
        return api.get_poi_names()

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()

    def get_year_options(self):
        return api.get_years()

    def get_month_options(self):
        return api.get_months()

    def get_day_options(self):
        return api.get_days("1")

class POIReportPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="POI Report", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # # table goes here
        #         ##table stuff
        # table_frame = tk.Frame(self)
        # table_frame.grid(row=2,column=0, columnspan=2, padx=0,pady=5)
        # numrows, numcols = 0, 11

        # var = tktable.ArrayVar(table_frame)
        # for y in range(numrows):
        #     for x in range(numcols):
        #         index = "%i,%i" % (y, x)
        #         var[index] = index

        # table = tktable.Table(table_frame, 
        #     rows = numrows,
        #     cols = numcols,
        #     state='normal',
        #     titlerows=1,
        #     titlecols=0,
        #     colwidth=10,
        #     height=10,
        #     roworigin=-1,
        #     colorigin=-1,
        #     selectmode='extended',
        #     selecttype='row',
        #     rowstretch='all',
        #     colstretch='last',
        #     # browsecmd=browsecmd,
        #     flashmode='on',
        #     variable=var,
        #     usecommand=0
        # )
        # scroll = Scrollbar(table_frame, orient='vertical', command=table.yview_scroll)
        # table.config(yscrollcommand=scroll.set)
        # scroll.pack(side='right', fill='y')
        # table.pack(expand=1, fill='y')
        
        # # table.grid(row=0, column=0)
        # # scroll.grid(row=0, column=1)
        # titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        # r = table.index('end').split(',')[0]
        # print r
        # index = r + ",-1"
        # table.set("row", "-1,-1", "Results")

        # filters = []

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10, columnspan = 2)

                        ## sort option menu
        sort_options = ['POI_Location', 'City', 'State', 'Mold_Min', 'Mold_Avg', 'Mold_Max', 'Aq_min', 'Aq_Avg', 'Aq_Max', 'total_data_points', 'Flagged']
        sort_var = StringVar(self)
        sort_var.set(sort_options[0])

        sort_dropdown = apply(OptionMenu, (self, sort_var) + tuple(sort_options))
        sort_dropdown.grid(row=1, column=0, padx = 20, pady = 10, sticky="W")

                        ## order option menu
        order_options = ("ASC", "DESC")
        order_var = StringVar(self)
        order_var.set(order_options[0])

        order_dropdown = apply(OptionMenu, (self, order_var) + tuple(order_options))
        order_dropdown.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")

        self.cell_frames, self.table_frame = self.build_table("POI_Location","ASC")


        apply_button = tk.Button(self, text="Sort", command=lambda :self.apply_filter(sort_var.get(), order_var.get()))
        apply_button.grid(row=1, column=1, padx = 20, pady = 10, sticky="E")

    def build_table(self, sort_option, order_option):
        table_frame = tk.Frame(self)
        table_frame.grid(row=10,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6

        titles = ['POI_Location', 'City', 'State', 'Mold_Min', 'Mold_Avg', 'Mold_Max', 'Aq_min', 'Aq_Avg', 'Aq_Max', 'total_data_points', 'Flagged']
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        report = api.get_poi_report(sort_option, order_option)

        for i in range(0,len(report)):
            cell_frames.append(self.add_row(table_frame, i+1, report[i], "white"))

        return cell_frames, table_frame

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        a_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        a_frame.grid(row=r, column=0,sticky=N+S+E+W)
        a_label = tk.Label(a_frame, bg = bg_color, text=row[0])
        a_label.grid(row=0, column=0, pady = 5, padx = 5)
        # a_button = tk.Button(self, text="...", command=lambda :self.detail_window(row[0]))
        # a_button.grid(row=0, column=1, padx = 5, pady = 5, sticky="E")



        b_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        b_frame.grid(row=r, column=1,sticky=N+S+E+W)
        b_label = tk.Label(b_frame, bg = bg_color, text=row[1])
        b_label.grid(row=0, column=0, pady = 5, padx = 5)

        c_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        c_frame.grid(row=r, column=2,sticky=N+S+E+W)
        c_label = tk.Label(c_frame, bg = bg_color, text=row[2])
        c_label.grid(row=0, column=0, pady = 5, padx = 5)

        d_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        d_frame.grid(row=r, column=3,sticky=N+S+E+W)
        d_label = tk.Label(d_frame, bg = bg_color, text=row[3])
        d_label.grid(row=0, column=0, pady = 5, padx = 5)

        e_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        e_frame.grid(row=r, column=4,sticky=N+S+E+W)
        e_label = tk.Label(e_frame, bg = bg_color, text=row[4])
        e_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        f_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        f_frame.grid(row=r, column=5,sticky=N+S+E+W)
        f_label = tk.Label(f_frame, bg = bg_color, text=row[5])
        f_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        g_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        g_frame.grid(row=r, column=6,sticky=N+S+E+W)
        g_label = tk.Label(g_frame, bg = bg_color, text=row[6])
        g_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        h_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        h_frame.grid(row=r, column=7,sticky=N+S+E+W)
        h_label = tk.Label(h_frame, bg = bg_color, text=row[7])
        h_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        i_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        i_frame.grid(row=r, column=8,sticky=N+S+E+W)
        i_label = tk.Label(i_frame, bg = bg_color, text=row[8])
        i_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        j_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        j_frame.grid(row=r, column=9,sticky=N+S+E+W)
        j_label = tk.Label(j_frame, bg = bg_color, text=row[9])
        j_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        k_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        k_frame.grid(row=r, column=10,sticky=N+S+E+W)
        k_label = tk.Label(k_frame, bg = bg_color, text=row[10])
        k_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        # l_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        # l_frame.grid(row=r, column=5,sticky=N+S+E+W)
        # l_label = tk.Label(l_frame, bg = bg_color, text=row[5])
        # l_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        a_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        a_frame.grid(row=r, column=0,sticky=N+S+E+W)
        a_label = tk.Label(a_frame, bg = bg_color, text=row[0])
        a_label.grid(row=0, column=0, pady = 5, padx = 5)

        b_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        b_frame.grid(row=r, column=1,sticky=N+S+E+W)
        b_label = tk.Label(b_frame, bg = bg_color, text=row[1])
        b_label.grid(row=0, column=0, pady = 5, padx = 5)

        c_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        c_frame.grid(row=r, column=2,sticky=N+S+E+W)
        c_label = tk.Label(c_frame, bg = bg_color, text=row[2])
        c_label.grid(row=0, column=0, pady = 5, padx = 5)

        d_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        d_frame.grid(row=r, column=3,sticky=N+S+E+W)
        d_label = tk.Label(d_frame, bg = bg_color, text=row[3])
        d_label.grid(row=0, column=0, pady = 5, padx = 5)

        e_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        e_frame.grid(row=r, column=4,sticky=N+S+E+W)
        e_label = tk.Label(e_frame, bg = bg_color, text=row[4])
        e_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        f_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        f_frame.grid(row=r, column=5,sticky=N+S+E+W)
        f_label = tk.Label(f_frame, bg = bg_color, text=row[5])
        f_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        g_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        g_frame.grid(row=r, column=6,sticky=N+S+E+W)
        g_label = tk.Label(g_frame, bg = bg_color, text=row[6])
        g_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        h_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        h_frame.grid(row=r, column=7,sticky=N+S+E+W)
        h_label = tk.Label(h_frame, bg = bg_color, text=row[7])
        h_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        i_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        i_frame.grid(row=r, column=8,sticky=N+S+E+W)
        i_label = tk.Label(i_frame, bg = bg_color, text=row[8])
        i_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        j_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        j_frame.grid(row=r, column=9,sticky=N+S+E+W)
        j_label = tk.Label(j_frame, bg = bg_color, text=row[9])
        j_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        k_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        k_frame.grid(row=r, column=10,sticky=N+S+E+W)
        k_label = tk.Label(k_frame, bg = bg_color, text=row[10])
        k_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        # l_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        # l_frame.grid(row=r, column=5,sticky=N+S+E+W)
        # l_label = tk.Label(l_frame, bg = bg_color, text=row[5])
        # l_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)


    def apply_filter(self, sort_option, order_option): #FIXME: probably need to pass an array with values to filter with
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames, self.table_frame = self.build_table(sort_option, order_option)

    def add_new_data(self, row, table):
        #table.config(state='normal')
        table.insert_rows('end', 1)
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *row)
        table.see(idx)
        #table.config(state='disabled')


    def back(self, controller):
        controller.show_frame(OffPortalPage)

class ViewPOIPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="View POI", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10, padx=20)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5, sticky = 'E')
        city_label = tk.Label(self, text="City").grid(row=2, column=0, pady = 5, sticky = 'E')
        state_label = tk.Label(self, text="State").grid(row=3, column=0, pady = 5, sticky = 'E')
        zip_label = tk.Label(self, text="Zip Code").grid(row=4, column=0, pady = 5, sticky = 'E')
        flag_label = tk.Label(self, text="Flagged").grid(row=5, column=0, pady = 5, sticky = 'E')

        ## date chooser stuff
        dateflag_label = tk.Label(self, text="Date Flagged").grid(row=6, column=0, pady = 5, sticky="E")
        date_frame = tk.Frame(self)
        date_frame.grid(row=6, column=1, pady = 5, sticky="W", padx = 20)

        #month
        month_options = self.get_month_options()
        month_var = StringVar(self)
        month_var.set(month_options[0])

        month_dropdown = apply(OptionMenu, (date_frame, month_var) + tuple(month_options))
        month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        day_var = StringVar(self)
        day_var.set(day_options[0])

        day_dropdown = apply(OptionMenu, (date_frame, day_var) + tuple(day_options))
        day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(date_frame, text="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        year_var = StringVar(self)
        year_var.set(year_options[0])

        year_dropdown = apply(OptionMenu, (date_frame, year_var) + tuple(year_options))
        year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")

        dateto_label = tk.Label(self, text="to").grid(row=7, column=1, pady = 0)

        ##end date stuff
        end_date_frame = tk.Frame(self)
        end_date_frame.grid(row=8, column=1, pady = 5, sticky="W", padx = 20)
        #month
        month_options = self.get_month_options()
        end_month_var = StringVar(self)
        end_month_var.set(month_options[0])

        end_month_dropdown = apply(OptionMenu, (end_date_frame, end_month_var) + tuple(month_options))
        end_month_dropdown.grid(row=0, column=0, padx = 1, sticky="W")
        slash_label1 = tk.Label(end_date_frame, text="/").grid(row=0, column=1, sticky = 'E')

        #day
        day_options = self.get_day_options()
        end_day_var = StringVar(self)
        end_day_var.set(day_options[0])

        end_day_dropdown = apply(OptionMenu, (end_date_frame, end_day_var) + tuple(day_options))
        end_day_dropdown.grid(row=0, column=2, padx = 1, sticky="W")
        slash_label2 = tk.Label(end_date_frame, text ="/").grid(row=0, column=3,sticky = 'E')

        #year
        year_options = self.get_year_options()
        end_year_var = StringVar(self)
        end_year_var.set(year_options[0])

        end_year_dropdown = apply(OptionMenu, (end_date_frame, end_year_var) + tuple(year_options))
        end_year_dropdown.grid(row=0, column=4, padx = 1, sticky="W")



        zip_entry = tk.Entry(self)
        zip_entry.grid(row=4, column=1, pady = 5, padx= 20, sticky="W")

        flag_var = IntVar()
        flag_check = Checkbutton(self, variable=flag_var)
        flag_check.grid(row=5, column=1, pady = 5, sticky="W", padx = 20)

        ## loc option menu
        loc_options = ('any',) + tuple(self.get_loc_options())
        loc_var = StringVar(self)
        loc_var.set(loc_options[0])

        loc_dropdown = apply(OptionMenu, (self, loc_var) + tuple(loc_options))
        loc_dropdown.grid(row=1, column=1, padx = 20, pady = 10, sticky="W")



        ## city option menu
        city_options = ('any',) + tuple(self.get_city_options())
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options))
        city_dropdown.grid(row=2, column=1, padx = 20, pady = 10, sticky="W")

        ## state option menu
        state_options = ('any',) + tuple(self.get_state_options())
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options))
        state_dropdown.grid(row=3, column=1, padx = 20, pady = 10, sticky="W")





        # ##table stuff
        # table_frame = tk.Frame(self)
        # table_frame.grid(row=10,column=0, columnspan=2, padx=0,pady=5)
        # numrows, numcols = 0, 6

        # var = tktable.ArrayVar(table_frame)
        # for y in range(numrows):
        #     for x in range(numcols):
        #         index = "%i,%i" % (y, x)
        #         var[index] = index

        # table = tktable.Table(table_frame, 
        #     rows = numrows,
        #     cols = numcols,
        #     state='normal',
        #     titlerows=1,
        #     titlecols=0,
        #     colwidth=10,
        #     height=10,
        #     roworigin=-1,
        #     colorigin=-1,
        #     selectmode='extended',
        #     selecttype='row',
        #     rowstretch='all',
        #     colstretch='last',
        #     # browsecmd=browsecmd,
        #     flashmode='on',
        #     variable=var,
        #     usecommand=0
        # )
        # scroll = Scrollbar(table_frame, orient='vertical', command=table.yview_scroll)
        # table.config(yscrollcommand=scroll.set)
        # scroll.pack(side='right', fill='y')
        # table.pack(expand=1, fill='y')
        
        # # table.grid(row=0, column=0)
        # # scroll.grid(row=0, column=1)
        # titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        # r = table.index('end').split(',')[0]
        # print r
        # index = r + ",-1"
        # table.set("row", "-1,-1", "Results")

        # #         ## sort option menu
        # # sort_options = self.get_loc_options()
        # # sort_var = StringVar(self)
        # # sort_var.set(sort_options[0])

        # # sort_dropdown = apply(OptionMenu, (self, sort_var) + tuple(sort_options))
        # # sort_dropdown.grid(row=20, column=0, padx = 20, pady = 10, sticky="W")

        # #                 ## order option menu
        # # order_options = ('None',) + tuple(self.get_loc_options())
        # # order_var = StringVar(self)
        # # order_var.set(order_options[0])

        # # order_dropdown = apply(OptionMenu, (self, order_var) + tuple(order_options))
        # # order_dropdown.grid(row=20, column=1, padx = 20, pady = 10, sticky="W")

        # filters = []

        

        self.cell_frames, self.table_frame = self.build_table("any","any","any","",0,"","" )


        apply_button = tk.Button(self, text="Apply Filter", command=lambda :self.apply_filter(controller, loc_var.get(), city_var.get(), state_var.get(), zip_entry.get(), flag_var.get(), datetime.date(int(year_var.get()), int(month_var.get()), int(day_var.get())), datetime.date(int(end_year_var.get()), int(end_month_var.get()), int(end_day_var.get()))))
        apply_button.grid(row=9, column=1, padx = 20, pady = 10, sticky="E")

        reset_button = tk.Button(self, text="Reset Filter", command=lambda :self.reset_filter(controller))
        reset_button.grid(row=9, column=0, padx = 20, pady = 10, sticky="W")

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=11, column=0, padx = 20, pady = 10, sticky="W")

    def build_table(self, location,city,state,zipc,flag,sdate,edate):
        table_frame = tk.Frame(self)
        table_frame.grid(row=10,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6

        titles = ["Location Name", "City", "State", "Zip code", "Flagged?", "Date Flagged"]
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        pending_data_points = api.get_poi(location,city,state,zipc,flag,sdate,edate)

        for i in range(0,len(pending_data_points)):
            cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))

        return cell_frames, table_frame

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        a_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        a_frame.grid(row=r, column=0,sticky=N+S+E+W)
        a_label = tk.Label(a_frame, bg = bg_color, text=row[0])
        a_label.grid(row=0, column=0, pady = 5, padx = 5)
        a_button = tk.Button(a_frame, text="...", command=lambda :self.detail_window(row[0]))
        a_button.grid(row=0, column=1, padx = 5, pady = 5, sticky="E")

        b_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        b_frame.grid(row=r, column=1,sticky=N+S+E+W)
        b_label = tk.Label(b_frame, bg = bg_color, text=row[1])
        b_label.grid(row=0, column=0, pady = 5, padx = 5)

        c_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        c_frame.grid(row=r, column=2,sticky=N+S+E+W)
        c_label = tk.Label(c_frame, bg = bg_color, text=row[2])
        c_label.grid(row=0, column=0, pady = 5, padx = 5)

        d_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        d_frame.grid(row=r, column=3,sticky=N+S+E+W)
        d_label = tk.Label(d_frame, bg = bg_color, text=row[3])
        d_label.grid(row=0, column=0, pady = 5, padx = 5)

        e_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        e_frame.grid(row=r, column=4,sticky=N+S+E+W)
        e_label = tk.Label(e_frame, bg = bg_color, text=row[4])
        e_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        f_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        f_frame.grid(row=r, column=5,sticky=N+S+E+W)
        f_label = tk.Label(f_frame, bg = bg_color, text=row[5])
        f_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        # return (flag_var, row[0],row[3]) #returns flag variable and datetime


        # return row_ref
    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        r = 0
        a_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        a_frame.grid(row=r, column=0,sticky=N+S+E+W)
        a_label = tk.Label(a_frame, bg = bg_color, text=row[0])
        a_label.grid(row=0, column=0, pady = 5, padx = 5)

        b_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        b_frame.grid(row=r, column=1,sticky=N+S+E+W)
        b_label = tk.Label(b_frame, bg = bg_color, text=row[1])
        b_label.grid(row=0, column=0, pady = 5, padx = 5)

        c_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        c_frame.grid(row=r, column=2,sticky=N+S+E+W)
        c_label = tk.Label(c_frame, bg = bg_color, text=row[2])
        c_label.grid(row=0, column=0, pady = 5, padx = 5)

        d_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        d_frame.grid(row=r, column=3,sticky=N+S+E+W)
        d_label = tk.Label(d_frame, bg = bg_color, text=row[3])
        d_label.grid(row=0, column=0, pady = 5, padx = 5)

        e_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        e_frame.grid(row=r, column=4,sticky=N+S+E+W)
        e_label = tk.Label(e_frame, bg = bg_color, text=row[4])
        e_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)

        f_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        f_frame.grid(row=r, column=5,sticky=N+S+E+W)
        f_label = tk.Label(f_frame, bg = bg_color, text=row[5])
        f_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)




    def apply_filter(self, controller, location,city,state,zipc,flag,sdate,edate): #FIXME: probably need to pass an array with values to filter with
        # titles = ("Location Name", "City", "State", "Zip Code", "Flagged", "Date Flagged")
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames, self.table_frame = self.build_table(location,city,state,zipc,flag,sdate,edate)
        # r = table.index('end').split(',')[0] #get row number <str>
        # idx = r + ',-1'
        # table.set('row', idx, *titles)
        # table.see(idx)
        # filtered_poi = api.get_poi(location,city,state,zipc,flag,sdate,edate)
        # for r in filtered_poi:
        #     self.add_new_data(r, table)

    def add_new_data(self, row, table):
        #table.config(state='normal')
        table.insert_rows('end', 1)
        r = table.index('end').split(',')[0] #get row number <str>
        idx = r + ',-1'
        table.set('row', idx, *row)
        table.see(idx)
        #table.config(state='disabled')


    def reset_filter(self, controller): #FIXME: probably need to pass an array with values to filter with
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames, self.table_frame = self.build_table("any","any","any","",0,"","" )



    def back(self, controller): #FIXME: probably need to pass an array with values to filter with
        controller.show_frame(OffPortalPage)

    def get_loc_options(self):
        return api.get_poi_names()

    def get_state_options(self): 
        return api.get_states()

    def get_city_options(self): #FIXME: pass in state?
        return api.get_cities()

    def get_year_options(self):
        return api.get_years()

    def get_month_options(self):
        return api.get_months()

    def get_day_options(self):
        return api.get_days("1")

    def detail_window(self, poi_name):
        window = tk.Toplevel(self)
        frame = POIDetail(window, self, "", "")
        # window.frames[F] = frame
        frame.grid(row=0, column = 0, sticky=N+E+S+W)
        # self.show_frame(frame)




class AdminPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        pdp_button = tk.Button(self, text="Pending Data Points", command=lambda :self.pdp(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        poffacc_button = tk.Button(self, text="Pending City Official Accounts", command=lambda :self.poffacc(controller)).grid(row=2, column=0, padx = 20, pady = 10)

        logout_button = tk.Button(self, text="Logout", command=lambda :self.logout(controller)).grid(row=3, column=0, padx = 20, pady = 10, sticky="W")


    def pdp(self, controller):
        controller.show_frame(PDPPage)

    def poffacc(self, controller):
        controller.show_frame(POPage)

    def logout(self, controller):
        api.logout()
        controller.show_frame(LoginPage)

class PDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Pending Data Points", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # table goes here
                ##table stuff
        # table_frame = tk.Frame(self)
        # table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        # numrows, numcols = 0, 6

        # titles = ["Select", "Location", "Datatype", "Data Value", "Time&Date of data reading"]
        # cell_frames = []
        # # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        # self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        # pending_data_points = api.get_pending_dp()

        # for i in range(0,len(pending_data_points)):
        #     cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))


        filters = []
        # apply_button = tk.Button(self, text="Show Report", command=lambda :self.apply_filter(controller, table, filters))
        # apply_button.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")
        self.cell_frames, self.table_frame = self.build_table()



        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10)

        reject_button = tk.Button(self, text="Reject", command=lambda :self.reject_selected(self.cell_frames, self.table_frame))
        reject_button.grid(row=9, column=1, padx = 20, pady = 10, sticky = "W")
        accept_button = tk.Button(self, text="Acept", command=lambda :self.accept_selected(self.cell_frames, self.table_frame))
        accept_button.grid(row=9, column=1, padx = 20, pady = 10, sticky = "E")

    def build_table(self):
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6

        titles = ["Select", "Location", "Datatype", "Data Value", "Time&Date of data reading"]
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        pending_data_points = api.get_pending_dp()

        for i in range(0,len(pending_data_points)):
            cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))

        return cell_frames, table_frame




    def accept_selected(self, cell_frames, table_frame):
       
        for f in cell_frames:
            api.datapoint_a(f)
            # if f[0].get() ==1:
            #     api.reject_dp(f[1], f[2])
        print api.get_pending_dp()
        if len(cell_frames)>0: 
            api.datapoint_a(cell_frames[-1])
        print api.get_pending_dp()

        if len(cell_frames)>0: 
            api.datapoint_a(cell_frames[0])
        print api.get_pending_dp()

        for f in cell_frames:
            api.datapoint_a(f)
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames , self.table_frame =  self.build_table()


            
        return

    def reject_selected(self, cell_frames, table_frame):

        for f in cell_frames:
            api.datapoint_r(f)
            # if f[0].get() ==1:
            #     api.reject_dp(f[1], f[2])
        print api.get_pending_dp()
        if len(cell_frames)>0: 
            api.datapoint_r(cell_frames[-1])
        print api.get_pending_dp()

        if len(cell_frames)>0: 
            api.datapoint_r(cell_frames[0])
        print api.get_pending_dp()

        for f in cell_frames:
            api.datapoint_r(f)
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames , self.table_frame =  self.build_table()
    
        return

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0, sticky=N+S+E+W)
        flag_var = IntVar()
        flag_check = Checkbutton(flag_frame, bg = bg_color, variable=flag_var)
        flag_check.grid(row=0, column=0, pady = 5, padx = 5, sticky=N+S+E+W)

        locn_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        locn_frame.grid(row=r, column=1, sticky=N+S+E+W)
        locn_label = tk.Label(locn_frame, bg = bg_color, text=row[0])
        locn_label.pack(side="top", fill="both", expand = True)

        dtype_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dtype_frame.grid(row=r, column=2, sticky=N+S+E+W)
        dtype_label = tk.Label(dtype_frame, bg = bg_color, text=row[1])
        dtype_label.grid(row=0, column=0, pady = 5, padx = 5)

        dval_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dval_frame.grid(row=r, column=3, sticky=N+S+E+W)
        dval_label = tk.Label(dval_frame, bg = bg_color, text=row[2])
        dval_label.grid(row=0, column=0, pady = 5, padx = 5)

        td_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        td_frame.grid(row=r, column=4, sticky=N+S+E+W)
        td_label = tk.Label(td_frame, bg = bg_color, text=row[3])
        td_label.grid(row=0, column=0, pady = 5, padx = 5)

        return (flag_var, row[0],row[3]) #returns flag variable and datetime


        # return row_ref
    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0)
        flag_label = tk.Label(flag_frame, bg = bg_color, text=row[0])
        flag_label.grid(row=0, column=0, pady = 5, padx = 5)

        locn_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        locn_frame.grid(row=r, column=1)
        locn_label = tk.Label(locn_frame, bg = bg_color, text=row[1])
        locn_label.grid(row=0, column=0, pady = 5, padx = 5)

        dtype_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dtype_frame.grid(row=r, column=2)
        dtype_label = tk.Label(dtype_frame, bg = bg_color, text=row[2])
        dtype_label.grid(row=0, column=0, pady = 5, padx = 5)

        dval_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        dval_frame.grid(row=r, column=3)
        dval_label = tk.Label(dval_frame, bg = bg_color, text=row[3])
        dval_label.grid(row=0, column=0, pady = 5, padx = 5)

        td_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        td_frame.grid(row=r, column=4)
        td_label = tk.Label(td_frame, bg = bg_color, text=row[4])
        td_label.grid(row=0, column=0, pady = 5, padx = 5,sticky=N+S+E+W)


    def back(self, controller):
        controller.show_frame(AdminPortalPage)
class POPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Pending City Officials", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        # table goes here
                ##table stuff
        # table_frame = tk.Frame(self)
        # table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        # numrows, numcols = 0, 6

        # titles = ["Select", "Username", "Email", "City", "State", "Title"]
        # cell_frames = []
        # # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        # self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        # pending_data_points = api.get_pending_off()

        # for i in range(0,len(pending_data_points)):
        #     cell_frames.append(self.add_row(table_frame, i+1, pending_data_points[i], "white"))



        # apply_button = tk.Button(self, text="Show Report", command=lambda :self.apply_filter(controller, table, filters))
        # apply_button.grid(row=1, column=0, padx = 20, pady = 10, sticky="E")

        self.cell_frames, self.table_frame = self.build_table()

        back_button = tk.Button(self, text="Back", command=lambda :self.back(controller))
        back_button.grid(row=9, column=0, padx = 20, pady = 10)
        reject_button = tk.Button(self, text="Reject", command=lambda :self.reject_selected(self.cell_frames, self.table_frame))
        reject_button.grid(row=9, column=1, padx = 30, pady = 10, sticky = "W")
        accept_button = tk.Button(self, text="Acept", command=lambda :self.accept_selected(self.cell_frames, self.table_frame))
        accept_button.grid(row=9, column=1, padx = 30, pady = 10, sticky = "E")

    def build_table(self):
        table_frame = tk.Frame(self)
        table_frame.grid(row=2,column=0, columnspan=2, padx=5,pady=5)
        numrows, numcols = 0, 6
        titles = ["Select", "Username", "Email", "City", "State", "Title"]
        cell_frames = []
        # cell_frames.append(self.add_titles(table_frame, 0, titles, "darkgray")) ##a9a9a9
        self.add_titles(table_frame, 0, titles, "darkgray") ##a9a9a9
        pending_officials = api.get_pending_off()

        for i in range(0,len(pending_officials)):
            cell_frames.append(self.add_row(table_frame, i+1, pending_officials[i], "white"))

        return cell_frames, table_frame


    def accept_selected(self, cell_frames, table_frame):
        for f in cell_frames:
            api.official_a(f)
            # if f[0].get() ==1:
            #     api.accept_official(f[1])
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames , self.table_frame =  self.build_table()


            
        return

    def reject_selected(self, cell_frames, table_frame):
        for f in cell_frames:
            api.official_r(f)
            # if f[0].get() ==1:
            #     api.reject_official(f[1])
        self.table_frame.grid_forget()
        self.table_frame.destroy()
        self.cell_frames , self.table_frame =  self.build_table()
            
        return

    def add_row(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        # r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0, sticky=N+S+E+W)
        flag_var = IntVar()
        flag_check = Checkbutton(flag_frame, bg = bg_color, variable=flag_var)
        flag_check.grid(row=0, column=0, pady = 5, padx = 5, sticky=N+S+E+W)

        uname_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        uname_frame.grid(row=r, column=1, sticky=N+S+E+W)
        uname_label = tk.Label(uname_frame, bg = bg_color, text=row[0])
        uname_label.pack(side="top", fill="both", expand = True)

        email_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        email_frame.grid(row=r, column=2, sticky=N+S+E+W)
        email_label = tk.Label(email_frame, bg = bg_color, text=row[1])
        email_label.grid(row=0, column=0, pady = 5, padx = 5)

        city_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        city_frame.grid(row=r, column=3, sticky=N+S+E+W)
        city_label = tk.Label(city_frame, bg = bg_color, text=row[2])
        city_label.grid(row=0, column=0, pady = 5, padx = 5)

        state_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        state_frame.grid(row=r, column=4, sticky=N+S+E+W)
        state_label = tk.Label(state_frame, bg = bg_color, text=row[3])
        state_label.grid(row=0, column=0, pady = 5, padx = 5)

        title_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        title_frame.grid(row=r, column=5, sticky=N+S+E+W)
        title_label = tk.Label(title_frame, bg = bg_color, text=row[4])
        title_label.grid(row=0, column=0, pady = 5, padx = 5)

        return (flag_var, row[0])


        # return row_ref
    def add_titles(self, table, r, row, bg_color):
        # row
        # officials_frame = tk.Frame(self, bd=1, relief=SUNKEN)
        r = 0
        flag_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        flag_frame.grid(row=r, column=0)
        flag_label = tk.Label(flag_frame, bg = bg_color, text=row[0])
        flag_label.grid(row=0, column=0, pady = 5, padx = 5)

        uname_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        uname_frame.grid(row=r, column=1, sticky=N+S+E+W)
        uname_label = tk.Label(uname_frame, bg = bg_color, text=row[1])
        uname_label.pack(side="top", fill="both", expand = True)

        email_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        email_frame.grid(row=r, column=2, sticky=N+S+E+W)
        email_label = tk.Label(email_frame, bg = bg_color, text=row[2])
        email_label.grid(row=0, column=0, pady = 5, padx = 5)

        city_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        city_frame.grid(row=r, column=3, sticky=N+S+E+W)
        city_label = tk.Label(city_frame, bg = bg_color, text=row[3])
        city_label.grid(row=0, column=0, pady = 5, padx = 5)

        state_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        state_frame.grid(row=r, column=4, sticky=N+S+E+W)
        state_label = tk.Label(state_frame, bg = bg_color, text=row[4])
        state_label.grid(row=0, column=0, pady = 5, padx = 5)

        title_frame = tk.Frame(table, bg = bg_color, bd=1, relief=SUNKEN)
        title_frame.grid(row=r, column=5, sticky=N+S+E+W)
        title_label = tk.Label(title_frame, bg = bg_color, text=row[5])
        title_label.grid(row=0, column=0, pady = 5, padx = 5)


    def back(self, controller):
        controller.show_frame(AdminPortalPage)



def main():
    app = TKMain()
    app.mainloop()


if __name__ == '__main__':
    main()