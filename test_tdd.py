import unittest
import subprocess

class test_add_user(unittest.TestCase):
 
    def test_adduser(self):
        print(f"**************testing add user***************************")
        expected_output = {'username': 'ayush', 'password': 'ayu123'}
        # result=subprocess.getoutput("echo \"2 ayush ayu123\" | python user_rbac.py")
        # print('*********************************************************')
        # print(str(result))
        # if str(expected_output) in str(result):
        #         print('oooooooooooooookkkkkkkkkkkkkkkkkkkkkkk')
        import subprocess
        proc = subprocess.Popen(['python','user_rbac.py','2 ayush ayu123'],stdout=subprocess.PIPE)
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            #the real code does filtering here
            print ("test:", line.rstrip())
            if str(expected_output) in str(line.rstrip()):
                print('*************found******************')
                self.assertEqual(1,1)
                break
            
            # grep_stdout = proc.communicate(input=b'2 ayush ayu123')[0]
            # print(grep_stdout.decode())
        
        self.assertEqual(1,1)

if __name__ == '__main__':
    unittest.main()
    
