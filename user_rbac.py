import  sys
import config

class checkPermission:
    def __init__(self,username,password):
        self.username = username
        self.password = password

    def check_credentials(self):
        if self.username==config.admin_username and self.password==config.admin_password:
            return True
        return userDb.user_db_dict[self.username]['password']==self.password

class checkAccess:
    def check_access(self,username,action):
        if username == config.admin_username :
            if action in config.admin_roles:
                return True
        elif username=='invalid user':
            print('you don have access')
            return False
            
        elif action in config.user_roles :
            return True
            

class loginUser:
    logged_user = ''
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def get_logged_user(self):
        if checkPermission(self.username,self.password).check_credentials():
            loginUser.logged_user = self.username
            return self.username
        else:
            loginUser.logged_user = 'invalid user'
            return 'invalid user'

class userDb:
    user_db_dict = {}
    def __init__(self,**kwargs):
        self.user_dict = {}
        self.user_dict = {'username':kwargs['username'],'password':kwargs['password']}
        print(f'creating user..{self.user_dict}')
        userDb.user_db_dict[kwargs['username']] = self.user_dict
        print(f"user added to db..{userDb.user_db_dict[kwargs['username']]}")
        
    def get_created_user(self):
        return userDb.user_db_dict
        

class addUser:

    def __init__(self,username,password):
        self.username = username
        self.password = password

    def create_user(self):
        user_dict = {'username':self.username , 'password':self.password}
        user_obj = userDb(**user_dict).get_created_user()
        return user_obj

class createRole:
    def __init__(self,username):
        self.username = username
    def create_role(self,resource,action):
        if resource in userDb.user_db_dict[self.username] and action not in userDb.user_db_dict[self.username][resource] :
            userDb.user_db_dict[self.username][resource].append(action)
        elif resource not in userDb.user_db_dict[self.username]:
            userDb.user_db_dict[self.username][resource] = []
            userDb.user_db_dict[self.username][resource].append(action)
        return userDb.user_db_dict[self.username][resource]

class deleteRole:
    def __init__(self,username):
        self.username = username
    def delete_role(self,resource,action):
            userDb.user_db_dict[self.username][resource].remove(action[1:])
            return userDb.user_db_dict[self.username][resource]

class createUserDriver:
    def call_create_user_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'create_user'):
            print('you cant create user')
        username = txt[1]
        password = txt[2]
        user_obj = addUser(username,password).create_user()
        print(f'user with user name {userDb.user_db_dict[username]} has been successfully created!' )
        print(user_obj)
        return user_obj
        print('***************************************************************************************\n')

class editRoleDriver:
    def call_edit_role_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'edit_user_role'):
            print('you cant create user')
        username = txt[1]
        resource = txt[2]
        action = txt[3]
        if '-' in action:
            user_resource_obj = deleteRole(username).delete_role(resource,action)
        else:
            user_resource_obj = createRole(username).create_role(resource,action)
        print(f'role has been modified...updated role is {user_resource_obj}\n' )
        print('***************************************************************************************\n')

class logInAsUserDriver:
    def call_login_func(self,txt):
        username = txt[1]
        password = txt[2]
        user_obj = loginUser(username,password).get_logged_user()
        print(f'you ave been logged as {user_obj} ')
        
        print('***************************************************************************************\n')
        return user_obj

class accessView:
    def access_view_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'view/access'):
            print('you cant create user')
        print(txt)
        action = txt[1]
        resource = txt[2]
        # access = txt[3]
        if action=='view':
            print(userDb.user_db_dict[loginUser.logged_user])
        elif action=='access' and resource in userDb.user_db_dict[loginUser.logged_user] and txt[3] in userDb.user_db_dict[loginUser.logged_user][resource] :
            print('**you have access to below resources')
            print(userDb.user_db_dict[loginUser.logged_user][resource])
        else:
            print('you do not have access to this resource....')
        print('***************************************************************************************\n')


class displayMsg:
    def __init__(self,username):
        self.username = loginUser.logged_user
    def get_display_msg(self):
        if self.username=='admin':
            print('------------------------------------------------')
            print('press 1 for login as another user   (eg: 1 username password)')
            print('press 2 for create user  (eg: 2 username password)')
            print('press 3 for edit role (3 username resource_name access_type)')
            print('------------------------------------------------')
        elif self.username=='invalid user':
            print('------------------------------------------------')
            print('enter correct credentials')
            print('------------------------------------------------')
        else:
            print('------------------------------------------------')
            print('press 1 for login as another user (1 username password)')
            print('press 4 to view/access (4 view resource_name)  (4 access resource_name access_name)')
            print('------------------------------------------------')
            

if __name__ == '__main__':
    loginUser.logged_user = 'admin'
    while True:
        
        displayMsg(loginUser.logged_user).get_display_msg()
        txt = input("your input ---------> ")
        print('processing...............................\n')
        if 'quit' in txt:
            break
        txt = txt.split(' ')
        option = txt[0]
        
        if '2' in txt[0]:
            createUserDriver().call_create_user_func(txt)
           
        if '3' in txt[0]:
            editRoleDriver().call_edit_role_func(txt)
            
        if '1' in txt[0]:
            loginUser.logged_user = logInAsUserDriver().call_login_func(txt)

        if '4' in txt[0]:
            accessView().access_view_func(txt)
            