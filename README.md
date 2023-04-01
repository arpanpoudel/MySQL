# MySQL
## Repo containing codes for the mysql implemention with python for DBMS class

requirements:
- python 3.9
- tabulate
- mysql

Function defined and its description:
-	open_database() : opens the database 
- printFormat(): format the results of sql operation
- executeSelect(): performs the operation defined by the query, displays the result in terminal and returns the result.
-	insert(): performs the insert operation on given table, values and query. Query is optional and are used for complex table and values.
-	executeUpdate(): used to delete and update sql operation
-	close_db(): closes the database connection
-	print_menu(): prints the menu available on the terminal
-	find_professor():     Find the professors in user selected department.
-	find_sections(): The user is  asked if they want to see all classes or just open classes. Then ask if they want to search by department or level. If they select search by dept, all classes from that dept (or just the open ones) is shown. If they select search by number, then ask them for level they want (e.g., 4000) and show all classes that start with 1, 2, 3, 4, or 5 (or just the open ones).
Display the dept code, course number, building, room number, days, times, and number of available seats for each section.
-	add_section(): Displays a list of all courses and ask the user which course they are adding a section for.
-	Update_section(): Prompts the user for dept and course number. Shows the section information (including SectionID) for any matches. Prompts the user for the SectionID. Prompts the user for the attribute name they want to update. Prompt the user for the new value. Updates the record.
-	get_Report(): Produces a table that shows the total enrollments by dept.
