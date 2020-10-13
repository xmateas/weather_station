import pysftp
myHostname = '192.168.1.16'
myUsername = "pi"
myPassword = "Hehe250994"
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None
with pysftp.Connection(host=myHostname, username=myUsername, password=myPassword, cnopts=cnopts) as sftp:
    print("Connection succesfully stablished ... ")

    remote_path = '/home/pi/Desktop/station/data'
    local_path ='data'

    sftp.get_d(remote_path,local_path)