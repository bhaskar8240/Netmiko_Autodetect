from netmiko.ssh_dispatcher import ConnectHandler
from netmiko.ssh_autodetect import SSHDetect
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
from getpass import getpass

#Use this for  password Hiding 
user= input('Enter ssh username:')

password=getpass('Enter ssh password:')

#Use this for open and read your text file 
with open('ip_address FILE ')as f:
    ip_cmd= f.read().splitlines()

with open('D:/python/juniperrtr.cmd.txt')as f:
    juniperrtr_cmd = f.read().splitlines()
    

with open('D:/python/ciscorouter_config.txt')as f:
    ciscortr_cmd = f.read().splitlines() 
           

with open('D:/python/ciscoswitch_config.txt')as f:
    ciscosw_cmd = f.read().splitlines()

#Use your own environment image name.       
Device_img = ['I86BI_LINUX-ADVENTERPRISEK9-M','i86bi_LinuxL2-AdvEnterpriseK9','Junos']

#Loop use for multiple ip .
for ip in ip_cmd:

    remote_devices = {

        'host' : ip ,

        'username' : user,

        'password' : password,

        'device_type': 'autodetect'

    }
 
    #Try and except use for aviod the error of any miscommunicatio with devices 
    try:
        Device =  SSHDetect(**remote_devices)
        best_match = Device.autodetect()
        remote_devices['device_type'] = best_match
        net_connect = ConnectHandler(**remote_devices)
    except(NetMikoTimeoutException):
        print(f'Timeout to device: {ip}')
        continue
    except(NetMikoAuthenticationException):
        print(f'Auth Failure:{ip}')
        continue
    except(SSHException):
        print(f'Chk SSH Config :{ip}')
        continue
    except(EOFError):
        print(f'EOFE for device: {ip}')
        continue
#use for good look .
    print('='* 80 + '\n' + 'CONNECTED_DEVICE: ' + ip +'\n' + '='* 80)
#Use for Find the above mentioned device image .  
    for soft_ver in Device_img:                       

        print('Chking Software version'+soft_ver)     

        output_ver =  net_connect.send_command('show configuration | display set')

        int_version =0
        int_version = output_ver.find(soft_ver)

        if int_version  > 0: 

            print('Device hostname found :'+ soft_ver)

            break

        else:
            print('Device hostname didnot found' +soft_ver)

#Use for push the config file which you open with command .
    if soft_ver == 'junos':
        print('='* 80 + '\n' + 'Config_the_Juniper_devices: ' + soft_ver + '\n' + '='* 80)

        output= net_connect.send_config_set(juniperrtr_cmd)

        output1 = net_connect.commit()
        print(output)
       

    elif soft_ver == 'I86BI_LINUX-ADVENTERPRISEK9-M':

        print('='* 80 + '\n' + 'Config_the_Ciscortr_devices: ' + soft_ver + '\n' + '='* 80)

        output= net_connect.send_config_set(ciscortr_cmd)
        print(output)    

    elif soft_ver == 'i86bi_LinuxL2-AdvEnterpriseK9':

        print('='* 80 + '\n' + 'Config_the_Ciscosw_devices: ' + soft_ver + '\n' + '='* 80)

        output= net_connect.send_config_set(ciscosw_cmd)
        print(output)
    else:
        print('Check the device vendor or type ' + ip)
    
