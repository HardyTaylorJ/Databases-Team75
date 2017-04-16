import tkinter as tk
from tkinter import *
from tkinter import ttk

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
        for F in (LoginPage, RegisterPage, SciPortalPage):

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
        controller.show_frame(LoginPage)


class AddDPPage(PageTemplate):
    def __init__(self, parent, controller):
        PageTemplate.__init__(self,parent)
        main_label = tk.Label(self, text="Register", font=LARGE_FONT).grid(row=0, column=0, columnspan=2, pady = 10)

        locn_label = tk.Label(self, text="POI Location Name").grid(row=1, column=0, pady = 5)
        timedate_label = tk.Label(self, text="Time and Date of Data Reading").grid(row=2, column=0, pady = 5)
        datatype_label = tk.Label(self, text="Data Type").grid(row=3, column=0, pady = 5)
        dataval_label = tk.Label(self, text="Data Value").grid(row=4, column=0, pady = 5)

        uname_entry = tk.Entry(self).grid(row=1, column=1, pady = 5, padx= 20)
        email_entry = tk.Entry(self).grid(row=2, column=1, pady = 5, padx= 20)
        pwd_entry = tk.Entry(self).grid(row=3, column=1, pady = 5, padx= 20)
        cpwd_entry = tk.Entry(self).grid(row=4, column=1, pady = 5, padx= 20)

        #variable in the dropdown
        locname_var = StringVar(self)
        locname_var.set("City Officials")

        # #FIXME: get these from database
        # loc_options = [
        #     "atl",
        #     "nyc",
        #     "san fran"
        # ]
        loc_options = self.get_loc_options()

        #dropdown box

        ## for the datatype option
        datatype_var = StringVar(self)
        datatype_var.set("Mold")
        datatype_option = OptionMenu(self, var, "Mold", "Air Quality reading").grid(row=5, column=1, padx = 20, pady = 10, sticky="W")

        sub_button = tk.Button(self, text="Submit", command=lambda :self.submit(controller))
        sub_button.grid(row=7, column=0, padx = 20, pady = 10)

    def submit(self, controller): #FIXME: probably need to pass an array with values to register with
        controller.show_frame(LoginPage)

    def get_loc_options(): #FIXME: get these from database
        return [ "atl","nyc","san fran"]

# class LoginPage(tk.frame):
#     def __init__(self, master):
#         # self.master = master
#         # self.frame = tk.Frame(self.master)
#         self.button1 = tk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
#         self.button1.pack()
#         self.frame.pack()

#     def login(self):
#         # self.newWindow = tk.Toplevel(self.master)
#         self.app = Demo2(self.master)

# class Demo2(tk.frame):
#     def __init__(self, master):
#         # self.master = master
#         # self.frame = tk.Frame(self.master)
#         self.quitButton = tk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
#         self.quitButton.pack()
#         self.frame.pack()

#     def close_windows(self):
#         self.master.destroy()

print("started anything")
def main():
    app = TKMain()
    app.mainloop()


if __name__ == '__main__':
    main()