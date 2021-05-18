import  sys
import config

class checkPermission:
    def __init__(self,username,password,role):
        self.username = username
        self.password = password
        self.role = role

    def check_credentials(self):
        if self.username==config.admin_username and self.password==config.admin_password:
            return True
        return userDb.user_db_dict[self.username+'.'+self.role]['password']==self.password

class checkAccess:
    def check_access(self,username,action):
        if username == config.admin_username or '.admin' in username:
            if action in config.admin_roles:
                return True
        elif username=='invalid user':
            print('you don have access')
            return False
            
        elif action in config.user_roles :
            return True
            

class loginUser:
    logged_user = ''
    def __init__(self,username,password,role=''):
        self.username = username
        self.password = password
        self.role = role
    def get_logged_user(self):
        if checkPermission(self.username,self.password,self.role).check_credentials():
            loginUser.logged_user = self.username+'.'+self.role
            return loginUser.logged_user
        else:
            loginUser.logged_user = 'invalid user'
            return 'invalid user'

class userDb:
    user_db_dict = {}
    def __init__(self,**kwargs):
        self.user_dict = {}
        self.user_dict = {'username':kwargs['username'],'password':kwargs['password']}
        print(f'creating user..{self.user_dict}')
        userDb.user_db_dict[kwargs['username']+'.'+kwargs['role']] = self.user_dict
        print(userDb.user_db_dict)
        print(f"user added to db..{userDb.user_db_dict[kwargs['username']+'.'+kwargs['role']]}")
        
    def get_created_user(self):
        return userDb.user_db_dict
        

class addUser:

    def __init__(self,username,password,role):
        self.username = username
        self.password = password
        self.role = role

    def create_user(self):
        user_dict = {'username':self.username , 'password':self.password,'role':self.role}
        user_obj = userDb(**user_dict).get_created_user()
        return user_obj

class check_if_valid_access_for_role:
    def check_access_role_combo(role,resource,action):
        if action in config.resource_access_role_dict[role][resource]:
            return True
        else:
            return False

class createRole:
    def __init__(self,username,role):
        self.username = username
        self.role = role
        
    def create_role(self,resource,action):
        if not check_if_valid_access_for_role.check_access_role_combo(self.role,resource,action):
            raise Exception(f'you do not access to apply {action} on {resource} for role {self.role}')
        if resource in userDb.user_db_dict[self.username+'.'+self.role] and action not in userDb.user_db_dict[self.username+'.'+self.role][resource] :
            userDb.user_db_dict[self.username+'.'+self.role][resource].append(action)
        elif resource not in userDb.user_db_dict[self.username+'.'+self.role]:
            userDb.user_db_dict[self.username+'.'+self.role][resource] = []
            userDb.user_db_dict[self.username+'.'+self.role][resource].append(action)
        return userDb.user_db_dict[self.username+'.'+self.role][resource]

class deleteRole:
    def __init__(self,username,role):
        self.username = username
        self.role = role
        
    def delete_role(self,resource,action):
            userDb.user_db_dict[self.username+'.'+self.role][resource].remove(action[1:])
            return userDb.user_db_dict[self.username+'.'+self.role][resource]

class createUserDriver:
    def call_create_user_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'create_user'):
            print('you cant create user')
        username = txt[1]
        password = txt[2]
        role = txt[3]
        user_obj = addUser(username,password,role).create_user()
        print(f'user with user name {userDb.user_db_dict[username+"."+role]} has been successfully created!' )
        print(user_obj)
        return user_obj
        print('***************************************************************************************\n')

class editRoleDriver:
    def call_edit_role_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'edit_user_role'):
            print('you cant create user')
        print(txt)
        username = txt[1]
        role = txt[2]
        resource = txt[3]
        action = txt[4]
        
        if '-' in action:
            user_resource_obj = deleteRole(username,role).delete_role(resource,action)
        else:
            user_resource_obj = createRole(username,role).create_role(resource,action)
        print(f'role {role} has been modified...updated role has accesses-> {user_resource_obj}\n' )
        print('***************************************************************************************\n')

class logInAsUserDriver:
    def call_login_func(self,txt):
        username = txt[1]
        password = txt[2]
        if username.lower() !='admin':
            role = txt[3]
        else:
            role = ''
        user_obj = loginUser(username,password,role).get_logged_user()
        print(f'you ave been logged as {user_obj} ')
        
        print('***************************************************************************************\n')
        return user_obj

class accessView:
    def access_view_func(self,txt):
        if not checkAccess().check_access(loginUser.logged_user,'view/access'):
            print('you cant create user')
        print(txt)
        action = txt[1]
        if action !='view':
            resource = txt[2]
        # access = txt[3]
        if action=='view':
            print(userDb.user_db_dict[loginUser.logged_user])
        elif action=='access' and resource in userDb.user_db_dict[loginUser.logged_user] and txt[3] in userDb.user_db_dict[loginUser.logged_user][resource] :
            print(f'**you have below accesses on {resource}')
            print(userDb.user_db_dict[loginUser.logged_user][resource])
        else:
            print(f'you do not have {txt[3]} on {resource}....')
        print('***************************************************************************************\n')


class displayMsg:
    def __init__(self,username):
        self.username = loginUser.logged_user
    def get_display_msg(self):
        if self.username=='admin' or '.admin' in self.username:
            print('------------------------------------------------')
            print('press 1 for login as another user   (eg: 1 username password role) eg. deepika abc123 admin')
            print('press 2 for create user  (eg: 2 username password role) eg. 2 deepika abc123 manager')
            print('press 3 for edit role (3 username role resource_name access_type) eg. 3 deepika manager r1 read')
            print('------------------------------------------------')
        elif self.username=='invalid user':
            print('------------------------------------------------')
            print('enter correct credentials')
            print('------------------------------------------------')
        else:
            print('------------------------------------------------')
            print('press 1 for login as another user (1 username password role) eg. 1 deepika abc123 manager')
            print('press 4 to view all you resources and accesses (4 view) eg. 4 view')
            print('press 4 to access a resource (4 access resource_name access_name) eg. 4 access r1 read')
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
        try:
            if '2' in txt[0]:
                createUserDriver().call_create_user_func(txt)
            
            if '3' in txt[0]:
                editRoleDriver().call_edit_role_func(txt)
                
            if '1' in txt[0]:
                loginUser.logged_user = logInAsUserDriver().call_login_func(txt)

            if '4' in txt[0]:
                accessView().access_view_func(txt)
        except Exception as e:
            print(e)
            