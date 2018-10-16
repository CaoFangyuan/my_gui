#
# @file shh_engine.py
#
# @brief Engine to handle remote communication
#        with the Sage device
#
# @author David Chiasson (dchiasso@sjtu.edu.cn)
#

import paramiko
import pexpect

# your raspberry ip, username and password
host='192.168.137.1'
username='sage'
password='wearable17'
# SAGE_HOME is your raspberry pi path
SAGE_HOME='/home/sage/sage_code/rpi_embedded/'
# SAGE is path on your computer
SAGE='/home/liuliu/cfy/sage_gui/'


# Create SSH connect
def create_ssh(host=host, username=username, password=password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    try:
       print("creating connection")
       ssh.connect(host, username=username, password=password, timeout=1)
       print("connected")
       yield ssh
    except:
       print("Not connected.")
       yield None
    finally:
       print("closing connection")
       ssh.close()
       print("closed")

# Execute Python file on raspberry pi       
def exesensordirector():
    for ssh in create_ssh():
        #stdin, stdout, stderr = ssh.exec_command('cd /home/liuliu/Gitdocument/bodynet/embedded/Common/;python Generate_Table.py',get_pty=True)
        stdin, stdout, stderr = ssh.exec_command('cd '+SAGE_HOME+'src/modules/dpm/common/;python Generate_Table.py',get_pty=True)
        #stdin, stdout, stderr = ssh.exec_command('mkdir name;mkdir name1')
        #stdin, stdout, stderr = ssh.exec_command('mkdir name1')
        #stdin, stdout, stderr = ssh.exec_command('sudo python sensordirector.py')
        stdin.write(password+'\n')
        for line in stdout:
            print(line.strip('\n'))
        print("done")


# Delete file or directory of raspberry pi 

def DelDirectory(delFile):
    print(delFile)
    for ssh in create_ssh():
        stdin, stdout, stderr = ssh.exec_command('cd '+SAGE_HOME+'src/modules/dpm/experiment_data/;rm -rfv '+ delFile,get_pty=True)
        print(stderr.read())
        print(stdout.read())
        print("delete")
 
 
# transfer file or directory between from Gui to Ras      
def GuiToRas(source,destination):
      
    child=pexpect.spawn("scp "+source+" "+username+"@"+host+":"+destination) 
    #child=pexpect.spawn("scp /home/liuliu/Documents/GitHub/bodynet/sage_controller/initial_para.py "+model.ssh_engine.username+"@"+model.ssh_engine.host+":/home/liuliu/Documents/Document_TS/")
    #child=pexpect.spawn("scp ./initial_para.py "+model.ssh_engine.username+"@"+model.ssh_engine.host+":/home/liuliu/Gitdocument/bodynet/embedded/TS/")
    i = child.expect([username+"@"+host+"'s password:",".*(yes/no).*"])
    if i == 0:
        child.sendline(password)
    elif i == 1:
        child.sendline('yes')
        child.expect(username+"@"+host+"'s password:")
        child.sendline(password)
    #child.expect("liuliu@192.168.1.109's password:")
    #child.sendline("15113222")
    child.sendline(password)
    child.interact()
    
# transfer file or directory between from Ras to GUi    
def RasToGui(source,destination):
      
    child=pexpect.spawn("scp "+username+"@"+host+":"+source+" "+destination) 
    #child=pexpect.spawn("scp /home/liuliu/Documents/GitHub/bodynet/sage_controller/initial_para.py "+model.ssh_engine.username+"@"+model.ssh_engine.host+":/home/liuliu/Documents/Document_TS/")
    #child=pexpect.spawn("scp ./initial_para.py "+model.ssh_engine.username+"@"+model.ssh_engine.host+":/home/liuliu/Gitdocument/bodynet/embedded/TS/")
    i = child.expect([username+"@"+host+"'s password:", ".*(yes/no).*"])
    if i == 0:
        child.sendline(password)
    elif i == 1:
        child.sendline('yes')
        child.expect(username+"@"+host+"'s password:")
        child.sendline(password)
    #child.expect("liuliu@192.168.1.109's password:")
    #child.sendline("15113222")
    child.sendline(password)
    child.interact()

