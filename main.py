import tkinter as tk
import pandas as pd
from tkinter.filedialog import asksaveasfile
from tkinter import ttk, VERTICAL, RIGHT, Y, HORIZONTAL, BOTTOM, X, filedialog, messagebox, LEFT, W, EW, END
from pandas.errors import OptionError


class EmployeeData:
    """class to contain the employee data and methods to manipulate the data"""
    def __init__(self):
        col_names = ['EmployeeID', 'FirstName', 'LastName', 'Position', 'Salary', 'Email', 'HomeAddress',
                     'HomePostcode', 'HomePhone', 'MobilePhone', 'StartDate', 'ReportsTo', 'EmergencyContactName',
                     'EmergencyContactPhone', 'BirthDate']
        self.df = pd.DataFrame(columns=col_names)

    def load_file(self, filename):
        """load data from a csv or xlsx file and store in df"""
        if filename[-3:] == 'csv':
            # try:
            self.df = pd.read_csv(filename)
            # except UnicodeDecodeError:
            #   what if error

        elif filename[-4:] == "xlsx":
            # try:
            self.df = pd.read_excel(filename)
            # except OptionError:
            #     messagebox.showerror(title="Employee Management",
            #                          message="File format not recognised")

        else:
            pass
            # messagebox.showerror(title="Employee Management",
            #                      message="File type not supported")

    def save_file(self, filename):
        """save data to a csv or xlsx file"""
        if filename[-3:] == 'csv':
            self.df.to_csv(filename, index=False, encoding='utf-8')
        elif filename[-4:] == 'xlsx':
            writer = pd.ExcelWriter(filename)
            self.df.to_excel(writer, index=False)
            writer.save()
        else:
            #  do something if file type not supported
            pass

    def get_employee(self, employee_id):
        return self.df.loc[self.df['EmployeeID'] == employee_id]

    def get_new_employee_id(self):
        """return the next available employee id number or 1000001 if no employees"""
        if self.df.empty:
            # if df is empty return the first employee number
            return 1000001
        else:
            # otherwise return one plus the largest employee number
            return self.df['EmployeeID'].max() + 1

    def add_employee(self, new_record):
        """add employee using the next available employee number"""
        # get a new employee number
        new_record['EmployeeID'] = self.get_new_employee_id()
        # add the new employee to the dataframe
        self.df = self.df.append(new_record, ignore_index=True)

    def edit_employee(self, updated_record):
        """update employee details for the given employee id"""
        # find dataframe row number for the given employee id
        row_num = self.df[self.df['EmployeeID'] == updated_record['EmployeeID']].index[0]

        # update the dataframe row with the updated record
        for field in updated_record:
            if updated_record[field] != 'EmployeeID':
                self.df.at[row_num, field] = updated_record[field]

    def delete_employee(self, employee_id):
        """delete employee with given employee id"""
        # get df row index using the employee id
        row_num = self.df[self.df['EmployeeID'] == employee_id].index[0]

        # delete the row
        self.df = self.df.drop(row_num)


class EmployeeManagementGUI(tk.Tk):
    # constructor
    def __init__(self):
        super().__init__()
        self.employee_data = EmployeeData()

        # Define Form Variables
        self.employee_id = tk.StringVar()
        self.first_name = tk.StringVar()
        self.last_name = tk.StringVar()
        self.position = tk.StringVar()
        self.salary = tk.StringVar()
        self.start_date = tk.StringVar()
        self.reports_to = tk.StringVar()
        self.email = tk.StringVar()
        self.home_address = tk.StringVar()
        self.home_postcode = tk.StringVar()
        self.home_phone = tk.StringVar()
        self.mobile_phone = tk.StringVar()
        self.birth_date = tk.StringVar()
        self.emergency_contact_name = tk.StringVar()
        self.emergency_contact_phone = tk.StringVar()

        # Define Dataframe
        # no used any more self.df = pd.DataFrame()

        # Other variables
        font_ems = ('Helvetica', 12)
        font_ems_bold = font_ems + ('bold',)
        # this is a class variable so it doesn't need to be passed as argument to save and load functions
        self.file_types = (('Excel File', '*.xlsx'), ('Comma Separated Values', '*.csv'), ('All Files', '*.*'))

        # Window Setup
        self.title('Employee Management System')  # TODO can i add employee id here?
        self.geometry('850x620+600+100')

        # Widgets
        # Main Frame - data entry form
        main_frame = tk.Frame(self)
        main_frame.grid(row=0, column=0, columnspan=4)

        # ROW 1
        # First Name
        lbl_first_name = tk.Label(main_frame, text='First Name', font=font_ems)
        lbl_first_name.grid(row=0, column=0, padx=10, pady=10, sticky=W)
        self.text_first_name = tk.Entry(main_frame, textvariable=self.first_name, font=font_ems)
        self.text_first_name.grid(row=0, column=1, padx=10, pady=10, sticky=W)
        # Last Name
        lbl_last_name = tk.Label(main_frame, text='Last Name', font=font_ems)
        lbl_last_name.grid(row=0, column=2, padx=10, pady=10, sticky=W)
        self.text_last_name = tk.Entry(main_frame, textvariable=self.last_name, font=font_ems)
        self.text_last_name.grid(row=0, column=3, padx=10, pady=10, sticky=W)

        # ROW 2
        # Position
        lbl_position = tk.Label(main_frame, text='Position', font=font_ems)
        lbl_position.grid(row=1, column=0, padx=10, pady=10, sticky=W)
        self.text_position = tk.Entry(main_frame, textvariable=self.position, font=font_ems)
        self.text_position.grid(row=1, column=1, padx=10, pady=10, sticky=W)
        # Salary
        lbl_salary = tk.Label(main_frame, text='Salary', font=font_ems)
        lbl_salary.grid(row=1, column=2, padx=10, pady=10, sticky=W)
        self.text_salary = tk.Entry(main_frame, textvariable=self.salary, font=font_ems)
        self.text_salary.grid(row=1, column=3, padx=10, pady=10, sticky=W)

        # ROW 3
        # StartDate
        lbl_start_date = tk.Label(main_frame, text='Start Date', font=font_ems)
        lbl_start_date.grid(row=2, column=0, padx=10, pady=10, sticky=W)
        self.text_start_date = tk.Entry(main_frame, textvariable=self.start_date, font=font_ems)
        self.text_start_date.grid(row=2, column=1, padx=10, pady=10, sticky=W)
        # ReportsTo
        lbl_reports_to = tk.Label(main_frame, text='Reports To', font=font_ems)
        lbl_reports_to.grid(row=2, column=2, padx=10, pady=10, sticky=W)
        self.text_reports_to = tk.Entry(main_frame, textvariable=self.reports_to, font=font_ems)
        self.text_reports_to.grid(row=2, column=3, padx=10, pady=10, sticky=W)

        # ROW 4
        # Email (Long)
        lbl_email = tk.Label(main_frame, text='Email', font=font_ems)
        lbl_email.grid(row=4, column=0, pady=10, padx=10, sticky=W)
        self.text_email = tk.Entry(main_frame, textvariable=self.email, width=67, font=font_ems)
        self.text_email.grid(row=4, column=1, columnspan=3, padx=10, pady=10, sticky=W)

        # ROW 5
        # Separator
        ttk.Separator(main_frame, orient=HORIZONTAL).grid(row=5, column=0, columnspan=4, sticky=EW, padx=10)

        # ROW 6
        # HomeAddress (long)
        lbl_home_address = tk.Label(main_frame, text='Home Address', font=font_ems)
        lbl_home_address.grid(row=6, column=0, pady=10, padx=10, sticky=W)
        self.text_home_address = tk.Entry(main_frame, textvariable=self.home_address, width=67, font=font_ems)
        self.text_home_address.grid(row=6, column=1, columnspan=3, padx=10, pady=10, sticky=W)

        # ROW 7
        # HomePostcode
        lbl_home_postcode = tk.Label(main_frame, text='Home Postcode', font=font_ems)
        lbl_home_postcode.grid(row=7, column=0, padx=10, pady=10, sticky=W)
        self.text_home_postcode = tk.Entry(main_frame, textvariable=self.home_postcode, font=font_ems)
        self.text_home_postcode.grid(row=7, column=1, padx=10, pady=10, sticky=W)
        # HomePhone
        lbl_home_phone = tk.Label(main_frame, text='Home Phone', font=font_ems)
        lbl_home_phone.grid(row=7, column=2, padx=10, pady=10, sticky=W)
        self.text_home_phone = tk.Entry(main_frame, textvariable=self.home_phone, font=font_ems)
        self.text_home_phone.grid(row=7, column=3, padx=10, pady=10, sticky=W)

        # ROW 8
        # Mobile Phone
        lbl_mobile_phone = tk.Label(main_frame, text='Mobile Phone', font=font_ems)
        lbl_mobile_phone.grid(row=8, column=0, padx=10, pady=10, sticky=W)
        self.text_mobile_phone = tk.Entry(main_frame, textvariable=self.mobile_phone, font=font_ems)
        self.text_mobile_phone.grid(row=8, column=1, padx=10, pady=10, sticky=W)
        # Birth Date
        lbl_birth_date = tk.Label(main_frame, text='Birth Date', font=font_ems)
        lbl_birth_date.grid(row=8, column=2, padx=10, pady=10, sticky=W)
        self.text_birth_date = tk.Entry(main_frame, textvariable=self.birth_date, font=font_ems)
        self.text_birth_date.grid(row=8, column=3, padx=10, pady=10, sticky=W)

        # ROW 9
        # Emergency Contact Name
        lbl_emergency_contact_name = tk.Label(main_frame, text='Emergency Contact Name', font=font_ems)
        lbl_emergency_contact_name.grid(row=9, column=0, padx=10, pady=10, sticky=W)
        self.text_emergency_contact_name = tk.Entry(main_frame, textvariable=self.emergency_contact_name,
                                                    font=font_ems)
        self.text_emergency_contact_name.grid(row=9, column=1, padx=10, pady=10, sticky=W)
        # Emergency Contact Phone
        lbl_emergency_contact_phone = tk.Label(main_frame, text='Emergency Contact Phone', font=font_ems)
        lbl_emergency_contact_phone.grid(row=9, column=2, padx=10, pady=10, sticky=W)
        self.text_emergency_contact_phone = tk.Entry(main_frame, textvariable=self.emergency_contact_phone,
                                                     font=font_ems)
        self.text_emergency_contact_phone.grid(row=9, column=3, padx=10, pady=10, sticky=W)

        # ROW 10
        # Button Frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.grid(row=10, column=0, columnspan=4, padx=10, pady=10, sticky=W)

        # Load Data Button
        tk.Button(btn_frame, command=self.load_file, text='Load Data', font=font_ems_bold,
                  width=15).grid(row=0, column=0)

        # Data Button
        tk.Button(btn_frame, command=self.save_file, text='Save Data', font=font_ems_bold,
                  width=15).grid(row=0, column=1, padx=5)

        # Add Employee Button
        tk.Button(btn_frame, command=self.add_record, text='Add Employee',  font=font_ems_bold,
                  width=15).grid(row=0, column=2, padx=5)

        # Delete Employee Button
        tk.Button(btn_frame, command=self.delete_record, text='Delete Employee',  font=font_ems_bold,
                  width=15).grid(row=0, column=3, padx=5)

        # Save Changes Button
        tk.Button(btn_frame, command=self.save_changes, text='Save Changes', font=font_ems_bold,
                  width=15).grid(row=0, column=4)

        # Staff List Frame
        staff_list_frame = ttk.Frame(self)
        staff_list_frame.place(x=10, y=420, width=830, height=190)

        # Staff List Style
        style = ttk.Style(self)
        style.theme_use('winnative')
        style.configure('Treeview', font=font_ems, columnwidth=10, rowheight=20,
                        background='white', fieldbackground='white')
        style.configure('Treeview.Heading', font=font_ems_bold)
        style.map('Treeview', background=[('selected', 'blue')])
        style.configure('TFrame', background='white')

        # Staff List Treeview
        self.staff_list_tv = ttk.Treeview(staff_list_frame, show='headings',
                                          columns=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15))

        # Staff List Scroll Bars
        # Vertical
        sbv = ttk.Scrollbar(staff_list_frame, orient=VERTICAL)
        sbv.pack(side=RIGHT, fill=Y)
        self.staff_list_tv.config(yscrollcommand=sbv.set)
        sbv.config(command=self.staff_list_tv.yview)
        # Horizontal
        sbh = ttk.Scrollbar(staff_list_frame, orient=HORIZONTAL)
        sbh.pack(side=BOTTOM, fill=X)
        self.staff_list_tv.config(xscrollcommand=sbh.set)
        sbh.config(command=self.staff_list_tv.xview)
        # Bind double click to select row for edit
        self.staff_list_tv.bind('<Double-1>', self.edit_record)

    def load_file(self):
        """Load staff data from a csv file selected by the user"""
        filename = filedialog.askopenfilename(title="Select A File", filetype=self.file_types)
        if filename[-3:] == 'csv' or filename[-4:] == "xlsx":
            self.employee_data.load_file(filename)
            self.display_all()
        else:
            messagebox.showerror(title="Employee Management",
                                 message="File type not supported")

    def save_file(self):
        """Function to save staff list data to a file selected by the user"""
        filename = asksaveasfile(filetypes=self.file_types, defaultextension=self.file_types)
        if filename.name[-3:] == 'csv' or filename.name[-4:] == 'xlsx':
            self.employee_data.save_file(filename.name)
        else:
            messagebox.showerror(title='Employee Management System',
                                 message='Cannot save file')

    def display_all(self):
        """Display the data frame in the staff list treeview"""
        # clear the previous list
        self.staff_list_tv.delete(*self.staff_list_tv.get_children())
        # set up the headings
        self.staff_list_tv['column'] = list(self.employee_data.df.columns)
        self.staff_list_tv['show'] = 'headings'
        for column in self.staff_list_tv['columns']:
            self.staff_list_tv.heading(column, text=column)
        # convert data frame to list of lists as treeview does not work with dataframes
        df_rows = self.employee_data.df.to_numpy().tolist()
        # insert data in the treeview row by row
        for row in df_rows:
            self.staff_list_tv.insert('', 'end', values=row)
        # display treeview in the frame
        self.staff_list_tv.pack(side=LEFT)

    def add_record(self):
        """Function to add a new employee"""
        # check if any inputs are blank
        if self.text_first_name.get() == '' or self.text_last_name.get() == '' \
                or self.text_position.get() == '' or self.text_salary.get() == '' \
                or self.text_start_date.get() == '' or self.text_reports_to.get() == '' \
                or self.text_email.get() == '' or self.text_home_address.get() == '' \
                or self.text_home_postcode.get() == '' or self.text_home_phone.get() == '' \
                or self.text_mobile_phone.get() == '' or self.text_birth_date.get() == '' \
                or self.text_emergency_contact_name.get() == '' or self.text_emergency_contact_phone.get() == '':
            messagebox.showerror(title='Employee Management System',
                                 message='Please complete all fields')
        else:
            new_record = {'FirstName': self.text_first_name.get(),
                          'LastName': self.text_last_name.get(),
                          'Position': self.text_position.get(),
                          'Salary': self.text_salary.get(),
                          'Email': self.text_email.get(),
                          'HomeAddress': self.text_home_address.get(),
                          'HomePostcode': self.text_home_postcode.get(),
                          'HomePhone': self.text_home_phone.get(),
                          'MobilePhone': self.text_mobile_phone.get(),
                          'StartDate': self.text_start_date.get(),
                          'ReportsTo': self.text_reports_to.get(),
                          'EmergencyContactName': self.text_emergency_contact_name.get(),
                          'EmergencyContactPhone': self.text_emergency_contact_phone.get(),
                          'BirthDate': self.text_birth_date.get()}

            self.employee_data.add_employee(new_record)
            self.display_all()
            self.clear_boxes()
            messagebox.showinfo(message='record added')

    def delete_record(self):
        """Function to delete an employee record"""
        # get details of employee to delete
        current_item = self.staff_list_tv.focus()
        current_row = self.staff_list_tv.item(current_item)
        current_record = current_row['values']
        emp_id = current_record[0]
        first_name = current_record[1]
        last_name = current_record[2]

        # are you sure message
        delete_message = f"Are you sure you want to delete \nemployee {emp_id}: {first_name} {last_name}?"

        # check its ok to delete
        if messagebox.askyesno(title="EMS", message=delete_message):
            # delete if yes
            self.employee_data.delete_employee(emp_id)
            self.display_all()
            # status message
            messagebox.showinfo(title="EMS", message="Employee deleted")

    def edit_record(self, btn_press_state):
        """function to load a record from the treeview and display it in the form for editing"""
        # get row data from tree view
        current_item = self.staff_list_tv.focus()
        current_row = self.staff_list_tv.item(current_item)
        current_record = current_row['values']

        # display data in entry boxes
        self.employee_id.set(current_record[0])
        self.first_name.set(current_record[1])
        self.last_name.set(current_record[2])
        self.position.set(current_record[3])
        self.salary.set(current_record[4])
        self.email.set(current_record[5])
        self.home_address.set(current_record[6])
        self.home_postcode.set(current_record[7])
        self.home_phone.set(current_record[8])
        self.mobile_phone.set(current_record[9])
        self.start_date.set(current_record[10])
        self.reports_to.set(current_record[11])
        self.emergency_contact_name.set(current_record[12])
        self.emergency_contact_phone.set(current_record[13])
        self.birth_date.set(current_record[14])

        # update window title with employee number?
        messagebox.showinfo(title='EMS', message=f'Employee {current_record[0]} selected')

    def save_changes(self):
        """Function to save changes to the current record"""
        # check if any inputs are blank
        if self.text_first_name.get() == '' or self.text_last_name.get() == '' \
                or self.text_position.get() == '' or self.text_salary.get() == '' \
                or self.text_start_date.get() == '' or self.text_reports_to.get() == '' \
                or self.text_email.get() == '' or self.text_home_address.get() == '' \
                or self.text_home_postcode.get() == '' or self.text_home_phone.get() == '' \
                or self.text_mobile_phone.get() == '' or self.text_birth_date.get() == '' \
                or self.text_emergency_contact_name.get() == '' or self.text_emergency_contact_phone.get() == '':
            messagebox.showerror(title='Employee Management System',
                                 message='Please complete all fields')
        else:
            # save the changes
            updated_record = {'EmployeeID': int(self.employee_id.get()),
                              'FirstName': self.text_first_name.get(),
                              'LastName': self.text_last_name.get(),
                              'Position': self.text_position.get(),
                              'Salary': self.text_salary.get(),
                              'Email': self.text_email.get(),
                              'HomeAddress': self.text_home_address.get(),
                              'HomePostcode': self.text_home_postcode.get(),
                              'HomePhone': self.text_home_phone.get(),
                              'MobilePhone': self.text_mobile_phone.get(),
                              'StartDate': self.text_start_date.get(),
                              'ReportsTo': self.text_reports_to.get(),
                              'EmergencyContactName': self.text_emergency_contact_name.get(),
                              'EmergencyContactPhone': self.text_emergency_contact_phone.get(),
                              'BirthDate': self.text_birth_date.get()}

            self.employee_data.edit_employee(updated_record)
            self.display_all()
            self.clear_boxes()
            messagebox.showinfo(message=f'Employee {updated_record["EmployeeID"]} updated')

    def clear_boxes(self):
        """function to clear all the boxes in the form"""
        self.text_first_name.delete(0, END)
        self.text_last_name.delete(0, END)
        self.text_position.delete(0, END)
        self.text_salary.delete(0, END)
        self.text_start_date.delete(0, END)
        self.text_reports_to.delete(0, END)
        self.text_email.delete(0, END)
        self.text_home_address.delete(0, END)
        self.text_home_postcode.delete(0, END)
        self.text_home_phone.delete(0, END)
        self.text_mobile_phone.delete(0, END)
        self.text_birth_date.delete(0, END)
        self.text_emergency_contact_name.delete(0, END)
        self.text_emergency_contact_phone.delete(0, END)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = EmployeeManagementGUI()
    app.mainloop()
