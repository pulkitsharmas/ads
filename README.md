# kmps
Budget approval System

The budget approval system is a solution to track budget requests or any kind of reimbursements. The employee sends a request to its manager and the manager can forward it to the finance department. This can save a lot of paperwork and travel.


## Steps to install
### Setting up the environment
1. Install python 2.7
2. Use pip to install Flask, Flask-SQLAlchemy, Flask-Uploads, Flask-Login, wtforms, Flask-Wtf
3. Clone the repository.
### Running the flask application
1. run app.py
2. explore using localhost at port 5000

## How to use Kmps to track your application
There are 2 types of departments:
1. Department : A simple department.
2. Finance Department: A department that would be handling all the money. To create a finance department, simply check the "finance department" checkbox while creating a department.


There are 4 type of users in the scene:
1. Admin : The Creator of organization, all departments, all the employee accounts.
2. Regular Employee : A simple user of some department.
3. Manager : Manager of some department.
4. Finance Manager: Manager of some finance department.

#### Act I: Setting things up.
1. Register a new organisation. This would create the admin user. Login the admin user.
2. Create the two types of departments. A simple department say X and a finance department say Y.
3. Create a regular employee account and a Manager employee Account with department as X.
4. Create a manager employee with department as Y. This would be the finance manager.
5. All users are ready.

#### Act II: Playground
1. Login the regular employee.
2. Click on the FAB Add button to create a request. Fill the particulars.
3. The Created Request can be seen at home.
4. Login using the Manager Employee(X department).
5. View the request. Forward it( you can reject it but let's save it for next time.).
6. Login using the Manager Account( Y department, the finance manager).
7. Follow similar steps to approve the request.
8. The request is now approved.

This is the basic use.
