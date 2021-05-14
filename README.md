# Assignment

## Role Based Access Control:

### How to run the program

1. open cmd in the folders directory
2. python user_rbac.py
3. you will be logged in as admin by default.
4. to create a user: type 2 and the username and password eg to create user deepika:
2 deepika abc123
5. to assign role to a user eg. to assign read role to deepika to r1 resource:
3 deepika r1 read
6. to delete a role eg. to delete read access from r1 resource of deepika:
3 deepika r1 -read
7. to login as another user type option and username password eg:
1 deepika abc123
8. once you are logged in as deepika, or any other user that you created previously you can view or access resources assigned to you eg to view accesses on resource r1:
4 view r1
9. to read resource r1:
4 access r1 read
if you have read permission you will be shown appropriate msg else you will be shown that you don't ahve permission
10. you can log back as admin using admin crdentials mention in config.py file eg:
1 admin admin123
11. if you are logged in any user other than admin, you won't be able to  create_user , edit or delete role .
12. if you log in as invalid user for eg. if you type wrong credentials you will bee prompted to enter correct ones.

## files

1. config.py contains admin crdentials and list of roles to which admin or normal user can have access.
2. test_tdd.py contains unittestcase
3. user_rbac.py contains the main script
