admin_roles = ['create_user','edit_user_role','view/access']
user_roles = ['view/access']
admin_username = 'admin'
admin_password = 'admin123'
resource_access_role_dict =  {'manager':{'r1':['read','write'],'r2':['read']},
                            'admin':{'r1':['read','write'],'r2':['read','write']},
                            'user':{'r1':['read'],'r2':['write']}
                            
                            }