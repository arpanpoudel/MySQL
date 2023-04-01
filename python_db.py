#   DO:  more $HOME/.my.cnf to see your MySQL username and  password
#  CHANGE:  MYUSERNAME and MYMYSQLPASSWORD in the test section of
#  this program to your username and mysql password
#  RUN: ./runpython.sh

import mysql.connector
from tabulate import tabulate
import logging
import os

def open_database(hostname, user_name, mysql_pw, database_name):

    global conn,cursor
    try:
        
        conn= mysql.connector.connect(
            host=hostname,
            user=user_name,
            password=mysql_pw,
            database=database_name,
            port=3306
        )
        #print("Connection successful")
        logger.info("Database open successful")
        cursor = conn.cursor()
    except mysql.connector.Error as error:
        print("Failed to connect to database: {}".format(error))


def printFormat(result):
    header = []
    for cd in cursor.description:  # get headers
        header.append(cd[0])
    print('')
    print('Query Result:')
    print('')
    print(tabulate(result, headers=header))  # print results in table format

# select and display query


def executeSelect(query,disp=True):
    cursor.execute(query)
    try:
        result = cursor.fetchall()
        if disp==True:
            printFormat(result)
        return result
    except mysql.connector.Error as err:
        print("An error occurred:", err)
        return False
        


def insert(table, values, query=None):
    if query==None:
        query = "INSERT into " + table + " values (" + values + ")" + ';'
    cursor.execute(query,values)
    conn.commit()


def executeUpdate(query):  # use this function for delete and update
    cursor.execute(query)
    conn.commit()


def close_db():  # use this function to close db
    
    if 'connection' in locals() and conn.is_connected():
    
        cursor.close()
        conn.close()
        print("Connection closed")
        logging.info("Connection closed")


# Define a function to print the menu options
def print_menu():
    # Get the width of the console
    width = os.get_terminal_size().columns
    
    # Define the menu options as a list of tuples
    menu_options = [
        ("1) Find Professors", "Find professors in the database"),
        ("2) Find Sections", "Find sections in the database"),
        ("3) Add Section", "Add a new section to the database"),
        ("4) Update Section", "Update an existing section in the database"),
        ("5) Report Enrollments", "Generate a report of student enrollments"),
        ("6) Quit", "Exit the program")
    ]
    
    # Print the menu options with each line centered in the console
    print("MENU".center(width))
    for option in menu_options:
        print(option[0].center(width))


    # Get user input for the menu selection
    selection = input("Enter a number to select a menu option: ")
    
    return selection

# function to find the profesors
def find_profesors():
    """
    Find the profesors in user selected department.
    """
    #sql command to retrieve the list of departments
    sql_command = "SELECT * FROM DEPT;"
    print("\n ___Departments____")
    dept_list=executeSelect(sql_command)
    dept=[data[0] for data in dept_list]
    department_code= input("\n Enter the department code you want to find the profesors above: ")
    if department_code in dept: 
        sql_command = f"SELECT * FROM PROFESSOR WHERE DEPT_CODE='{department_code}';"
        _=executeSelect(sql_command)
    else:
        print("\n Department code not found")
    
    
# function to find the sections
def find_sections():
    choice=input("1. See all classes \n 2. See open classes: ")
    if choice=='1':
        choice1=input("1. Search by department \n 2. Search by level: ")
        if choice1=='1':
            #sql command to retrieve the list of departments
            sql_command = "SELECT * FROM DEPT;"
            dept_list=executeSelect(sql_command)
            dept=[data[0] for data in dept_list]
            department_code= input("\n Enter the department code you want to section above: ")
            if department_code in dept: 
                sql_command = f"SELECT DEPT_CODE, PROF_ID, COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION WHERE DEPT_CODE='{department_code}';"
                _=executeSelect(sql_command)
            else:
                print("\n Department code not found")

        #choice1 is level
        
        elif choice1=='2':
            level=input("Enter the level or initial of level you want to search: ")
            #check if the level is initial or full length
            if len(level)==1:
                #  start with 1, 2, 3, 4, or 5
                sql_command = f"SELECT DEPT_CODE, PROF_ID, COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION WHERE COURSE_NUM LIKE '{level}%';"
                _=executeSelect(sql_command)
            else:
                sql_command = f"SELECT DEPT_CODE, PROF_ID, COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION  WHERE COURSE_NUM ={level};"
                _=executeSelect(sql_command)
            
            
               
    elif choice=='2':
        choice1=input("1. Search by department \n 2. Search by level: ")
        if choice1=='1':
            #sql command to retrieve the list of departments
            sql_command = "SELECT * FROM DEPT;"
            dept_list=executeSelect(sql_command)
            dept=[data[0] for data in dept_list]
            department_code= input("\n Enter the department code you want to section above: ")
            if department_code in dept: 
                sql_command = f"SELECT DEPT_CODE, PROF_ID, COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION WHERE DEPT_CODE='{department_code}' AND CURRENT_ENROLLMENT<MAX_ENROLLMENT;"
                _=executeSelect(sql_command)
            else:
                print("\n Department code not found")
        #choice1 is level
        elif choice1=='2':
            level=input("Enter the level or initial of level you want to search: ")
            #check if the level is initial or full length
            if len(level)==1:
                #  start with 1, 2, 3, 4, or 5
                sql_command = f"SELECT DEPT_CODE, PROF_ID, COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION WHERE COURSE_NUM LIKE '{level}%' AND CURRENT_ENROLLMENT<MAX_ENROLLMENT;"
                _=executeSelect(sql_command)
            else:
                sql_command = f"SELECT DEPT_CODE, PROF_ID COURSE_NUM, BUILDING, ROOM_NUM, DAYS, START_TIME, END_TIME,(MAX_ENROLLMENT-CURRENT_ENROLLMENT) AS AVAILABLE FROM SECTION WHERE COURSE_NUM ={level} AND CURRENT_ENROLLMENT<MAX_ENROLLMENT;"
                _=executeSelect(sql_command)
        
  
    else:
        print("Invalid choice")
          
#function to add section
def add_section():
    """
    add section for course.
    """
    #sql command to retrieve the list of departments
    sql_command = "SELECT * FROM COURSE;"
    print("___COURSE____")
    course_list=executeSelect(sql_command)
    course=[data[1] for data in course_list]
    course_code= input("Enter the Course Num: ")
    if course_code in course: 
        sql_command = f"SELECT DEPT_CODE FROM COURSE WHERE COURSE_NUM={course_code} ;"
        cursor.execute(sql_command)
        dept_code= cursor.fetchall()
        dept_code=dept_code[0][0]
        prof_id=input("Enter the professor ID: ")


        while not prof_id:
            print("Professor ID cannot be empty.")
            prof_id = input("Enter the professor ID: ")
        
        prof_id=int(prof_id)

        room_number=input("Enter the room number: ")
        while not room_number:
            print("Room number cannot be empty.")
            room_number = input("Enter room number : ")
        room_number=int(room_number)
        building=input("Enter the building:  ")
        while not building:
            print("Building cannot be empty.")
            building = input("Enter the building : ")
        days=input("Enter the Days:  ")
        start=input("Enter the class start time: ")
        end=input("Enter the class end time: ")
        start_day=input("Enter the class start day: ")
        while not start_day:
            print("start day cannot be empty.")
            start_day = input("Enter start day : ")
        end_day=input("Enter the class end day: ")
        while not end_day:
            print("end day cannot be empty.")
            start_day = input("Enter end day : ")
        max_enroll=int(input("Enter the maximum enrollment: "))
        current_enroll=int(input("Enter the current enrollment: "))
        values=(dept_code,course_code,prof_id,room_number,building,days,start,end,start_day,end_day,max_enroll,current_enroll)
        table='SECTION'
        query = "INSERT INTO {} (DEPT_CODE, COURSE_NUM, PROF_ID, ROOM_NUM, BUILDING, DAYS, START_TIME, END_TIME, START_DAY, END_DAY, MAX_ENROLLMENT, CURRENT_ENROLLMENT) VALUES ({})".format(table, ','.join(['%s'] * len(values)))
        insert(table,values,query)
    else:
        print("Course not found")

#function to update section
def update_section():
     #function to get user prompt
    def get_user_input(prompt):
        return input(prompt)
    
    #function to get the sectioon info with dept code and course num
    def get_section_info(dept_code, course_num):
        query = f"SELECT * FROM SECTION WHERE DEPT_CODE = '{dept_code}' AND COURSE_NUM = '{course_num}';"
        result=executeSelect(query)
        return result

    #update attribute
    def update_section_attribute(section_id, attribute, new_value):
        query = f"UPDATE SECTION SET {attribute} = %s WHERE SID = %s;"
        cursor.execute(query, (new_value, section_id))
    
    dept_code = get_user_input("Enter the department code: ")
    course_num = get_user_input("Enter the course number: ")
    
    section_info = get_section_info(dept_code, course_num)
    
    if not section_info:
        print("No matching sections found.")
    else:
        section_id = int(get_user_input("Enter the SectionID: "))
        update=True
        while update:
            attribute = get_user_input("Enter the attribute name you want to update: ")
            #avoid updating PK
            if attribute.upper() == "SID":
                print("You cannot update the primary key (SID).")
            
            else:
                new_value = get_user_input(f"Enter the new value for {attribute}: ")
                if attribute.upper()=="PROF_NAME":
                    attribute = 'PROF_ID'
                    query=f"select prof_id from professor where prof_name='{new_value}'"
                    new_value = executeSelect(query,disp=False)[0][0]
                update_section_attribute( section_id, attribute, new_value)
                more=input("Record updated successfully. Want to update more for same SID (Y/N)? : ")
                if more.upper()=='N':
                    update=False
                    
#function to get report
def get_Report():
    query ="SELECT DEPT_CODE, SUM(CURRENT_ENROLLMENT) AS TOTAL_ENROLLMENT FROM SECTION GROUP BY DEPT_CODE;"
    _=executeSelect(query) 
    
def main():
    ##### Test #######
    mysql_username = 'root'  # please change to your username
    mysql_password = 'inc0rrect'  # please change to your MySQL password
    
    #logger
    global logger
    # Create a logger object
    logger = logging.getLogger(__name__)
    # Set the log level to INFO
    logger.setLevel(logging.INFO)
    # Create a file handler that logs to a file called 'example.log'
    file_handler = logging.FileHandler('Database.log')
    # Set the log level for the file handler to DEBUG
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    # Add the file handler to the logger object
    logger.addHandler(file_handler)
    #open the database connection
    open_database(hostname='localhost', user_name=mysql_username,mysql_pw=mysql_password,database_name='arpan')  # open database
    
    #alter the table to add auto-increment
    cursor.execute('ALTER TABLE SECTION MODIFY COLUMN SID INT NOT NULL auto_increment;')
    #get the input from the user
    selection=None
    while selection!='6':

        selection=print_menu()

        # find the professors from the department
        if selection=='1':
            find_profesors()
        elif selection=='2':
            find_sections()
            
        elif selection=='3':
            add_section()
        elif selection=='4': 
            update_section()
        elif selection=='5': 
            get_Report()
        elif selection=='6':
            print('Exit program')
        else:
            print('Invalid selection, try again')
    
if __name__ == "__main__":
    # Call the main function
    main()


