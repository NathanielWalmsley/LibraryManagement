# The Library Manager
The Library Manager is a Python-based project to provide a  
user-friendly interface to an SQL database. The original code for this  
database is provided by:  
https://github.com/AlexanderWong/Library-Management-System.git  

The purpose of this project is to be able to organise the inventory  
of a library or group of libraries, providing a method for readers  
to search for books carried by the branches, and whether they are in  
stock, while also allowing librarians to keep track of their loans  
and users.  

The first iteration of this project includes only the Python module  
and a testing database (accessed through the `tests/schema.sql`  
path). The diagram below shows the structure of the database in this  
iteration:  
![library_manager_new_schema](https://user-images.githubusercontent.com/108919919/186135927-eb1b76f5-1cd6-4026-928c-f214fa14df21.png)


Two important tables in this diagram are `book` and `loan`, which  
together connect to each other table in the database. The former  
keeps track of all the individual titles available at all  
libraries, making no distinction about stock or availability. These  
values are respectively taken care of by the `copies` table and  
a query available in the program that returns the total number  
of copies at a branch, minus the number of copies on loan from  
that branch.  

The second table, `loan` handles the borrowing data for all  
libraries in the cluster - dates borrowed and due, which books,  
by whom, and from which branch. This data is represented by  
foreign keys from tables dealing with each of these specific  
fields in more detail, as shown in the diagram.  

### Updates
- 23/08/22
  The `sql` branch has been merged and a new schema has been  
  created to have a more intuitive design. The `publisher` table  
  has been removed due to lack of use and low potential utility.  
  The `author` and `book` table have been linked by a linking table  
  to reduce redundancy in both.  
- 21/08/22  
  There are currently two branches under construction to provide  
  revisions for this system. Firstly, the `sql` branch looks to  
  refactor the database to create a more intuitive design that  
  reduces duplication and allows for extensibility if new tables  
  or fields are necessary. The second branch, `django`, aims to  
  add a Python-based front-end to the program, which will allow  
  users to search for books through drop-down menus and modular  
  SQL statements.  
