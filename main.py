import Tkinter as tk
from Tkinter import *
# from Tkinter import ttk

LARGE_FONT=("Verdana", 12)

class TKMain (tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)


        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # All frames (pages) must be included in this list
        for F in (LoginPage, RegisterPage, SciPortalPage, AddDPPage, AddPOIPage):

            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column = 0, sticky="nsew")
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
        main_label = tk.Label(self, text="Login", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        uname_label = tk.Label(self, text="Username").grid(row=1, column=0, pady = 20)
        pwd_label = tk.Label(self, text="Password").grid(row=2, column=0, pady = 20)

        uname_entry = tk.Entry(self).grid(row=1, column=1, pady = 20, padx= 20)
        pwd_entry = tk.Entry(self).grid(row=2, column=1, pady = 20, padx= 20)


        reg_button = tk.Button(self, text="Register", command=lambda :self.register(controller))
        reg_button.grid(row=4, column=0, padx = 20, pady = 10)

        login_button = tk.Button(self, text="Login", command=lambda :self.login(controller))
        login_button.grid(row=4, column=1, padx = 20, sticky="E")



    def login(self, controller):
        #check login creds
        #
        #if not valid:
        #   give login error and return
        #
        #if admin:
        #   go to admin portal
        #
        #if city official:
        #   go to city official portal
        #
        #if city scientist:
        #   go to city scientist portal
        controller.show_frame(SciPortalPage)

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

        uname_entry = tk.Entry(self).grid(row=1, column=1, pady = 5, padx= 20)
        email_entry = tk.Entry(self).grid(row=2, column=1, pady = 5, padx= 20)
        pwd_entry = tk.Entry(self).grid(row=3, column=1, pady = 5, padx= 20)
        cpwd_entry = tk.Entry(self).grid(row=4, column=1, pady = 5, padx= 20)

        #variable in the dropdown
        var = StringVar(self)
        var.set("City Officials")
        #set trace on var
        # observer_name = trace_variable("w", callback)

        #dropdown box
        type_option = OptionMenu(self, var, "City Officials", "City Scientists").grid(row=5, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(LoginPage)

class SciPortalPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Choose Functionality", font=LARGE_FONT).grid(row=0, column=0,columnspan=2, pady = 10)

        add_dp_button = tk.Button(self, text="Add Data Point", command=lambda :self.add_dp(controller)).grid(row=1, column=0, padx = 20, pady = 10)
        add_poi_button = tk.Button(self, text="Add POI", command=lambda :self.add_poi(controller)).grid(row=2, column=0, padx = 20, pady = 10)

    def add_dp(self, controller):
        controller.show_frame(AddDPPage)

    def add_poi(self, controller):
        controller.show_frame(AddPOIPage)


class AddDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add Data Point", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        timedate_label = tk.Label(self, text="Time and Date of Data Reading").grid(row=2, column=0, pady = 5)
        datatype_label = tk.Label(self, text="Data Type").grid(row=3, column=0, pady = 5)
        dataval_label = tk.Label(self, text="Data Value").grid(row=4, column=0, pady = 5)

        timedate_entry = tk.Entry(self).grid(row=2, column=1, pady = 5, padx= 20)
        dataval_entry = tk.Entry(self).grid(row=4, column=1, pady = 5, padx= 20)


        ## location option menu
        #variable in the dropdown
        loc_options = self.get_loc_options()
        locname_var = StringVar(self)
        locname_var.set(loc_options[0])

        loc_dropdown = apply(OptionMenu, (self, locname_var) + tuple(loc_options)).grid(row=1, column=1, padx = 20, pady = 10, sticky="W")

        ## datatype option menu
        datatype_options = self.get_datatype_options()
        datatype_var = StringVar(self)
        datatype_var.set(datatype_options[0])
        datatype_dropdown = apply(OptionMenu, (self, datatype_var) + tuple(datatype_options)).grid(row=3, column=1, padx = 20, pady = 10, sticky="W")


        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(SciPortalPage)

    def get_loc_options(self): #FIXME: get these from database
        return [ "Atl, GA","NYC, NY","San Fran, CA"]

    def get_datatype_options(self): #FIXME: get these from database
        return [ "Mold","Air Quality reading"]

class AddPOIPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Add a New Location", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        city_label = tk.Label(self, text="City").grid(row=2, column=0, pady = 5)
        state_label = tk.Label(self, text="State").grid(row=3, column=0, pady = 5)
        zip_label = tk.Label(self, text="Zip Code").grid(row=4, column=0, pady = 5)

        locn_entry = tk.Entry(self).grid(row=1, column=1, pady = 5, padx= 20)
        dataval_entry = tk.Entry(self).grid(row=4, column=1, pady = 5, padx= 20)


        ## city option menu
        city_options = self.get_city_options()
        city_var = StringVar(self)
        city_var.set(city_options[0])

        city_dropdown = apply(OptionMenu, (self, city_var) + tuple(city_options)).grid(row=3, column=1, padx = 20, pady = 10, sticky="W")

        ## state option menu
        state_options = self.get_state_options()
        state_var = StringVar(self)
        state_var.set(state_options[0])
        state_dropdown = apply(OptionMenu, (self, state_var) + tuple(state_options)).grid(row=2, column=1, padx = 20, pady = 10, sticky="W")


        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(SciPortalPage)

    def get_state_options(self): #FIXME: get these from database
        return [ "atl","nyc","san fran"]

    def get_city_options(self): #FIXME: get these from database, also pass in state?
        return [ "GA","TN", "CA", "NY"]

def main():
    app = TKMain()
    app.mainloop()


if __name__ == '__main__':
    main()