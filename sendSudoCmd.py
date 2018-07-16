import paramiko,socket
import getpass
import datetime,time
import sys,os
import re

####

class LogWriter:
  logFilename = None
  def __init__(self, logFilename):
    self.logFilename = logFilename
  def write(self, line):
    # print 'write to %s' % self.logFilename
    file = open(self.logFilename, 'a')
    file.write(line)
    file.close()

####

def send_string_and_wait(command, wait_time, should_print=False, should_logfile=False):

  global shell
  global logWriter

  shell.send(command + "\n")
  # if should_logfile:
  #   logWriter.write(command)
  time.sleep(wait_time)
  receive_buffer = shell.recv(1024)
  if should_print:
    print receive_buffer
  if should_logfile:
    # logWriter.write("SEND >>>> \n" + receive_buffer)
    logWriter.write(receive_buffer)
    

def ssh_connect(host_address, username, password_ssh, password_sudo):

  global shell
  global logWriter

  print ""
  print '==> Host Address: %s' % host_address
  print ""
  print '(i) connecting'

  try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host_address, username=username, password=password_ssh)
  except socket.error:
    print("(x) !! Socket error, please verify host and port of %s" % host_address)
    list_host_failed_socket.append( host_address )
    return
  except paramiko.AuthenticationException:
    print("(x) !! Authentication failed, please verify your credentials")
    list_host_failed_auth.append( host_address )
    return
  except paramiko.SSHException as sshException:
    print("(x) !! Unable to establish SSH connection: %s" % sshException)
    list_host_failed_ssh.append( host_address )
    return
  except paramiko.BadHostKeyException as badHostKeyException:
    print("(x) !! Unable to verify server's host key: %s" % badHostKeyException)
    list_host_failed_hostkey.append( host_address )
    return

  print '(i) connected'

  print '(i) invoke shell'
  shell = client.invoke_shell()

  logWriter.write("\n")
  logWriter.write( "## Started for %s at %s\n\n" % (host_address, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')) )

  print '(i) logon sudoer'
  send_string_and_wait("sudo -s", 1, should_print=False, should_logfile=False)
  send_string_and_wait(password_sudo, 1, should_print=False, should_logfile=False)

  ################################################################
  ##  List of command(s)
  ################################################################
  commands = [
    'sudo touch /opt/paramiko.log',
    'sudo echo $(date) >> /opt/paramiko.log',
    # 'sudo ls -l /etc/freeradius/sites-enabled',
    # 'sudo systemctl -q status freeradius.service --no-pager',
    # 'sudo echo done >> /opt/paramiko.log'
  ]
  ################################################################

  print '(i) sending commands'
  
  print ""
  for command in commands:
    # print '\nSEND >>>> %s\n' % command
    send_string_and_wait(command, 1, should_print=True, should_logfile=True)

  print ""
  client.close()
  print '(i) client closed'

  list_host_done.append( host_address )

####

def main():

  global logWriterMaster
  global logWriter

  hosts = []
  if len(sys.argv) >= 2:
    hosts = sys.argv[1].split(",")

  today = datetime.datetime.today().strftime('%Y%m%d_%H%M%S')

  logWriterMaster = LogWriter( os.path.join(os.getcwd(), "log", today + "_operation"  + ".log") )
  logWriterMaster.write("\n" + "----------------" + "\n")
  logWriterMaster.write("## Executed at " + today + "\n")
  logWriterMaster.write( "## Entered %d host(s):\n" % len(hosts) )

  print ""
  print '--------------------------------'
  print "==> Entered %d host(s):" % len(hosts)
  for host in hosts:
    logWriterMaster.write( host + "\n" )
    print host

  print ""
  print "==> START"

  ################################################################
  ##  Get username/password and sudo enable password
  ################################################################
  # usrSSH = getpass.getpass("Input SSH username: ")
  # pwdSSH = getpass.getpass("Input SSH password: ")
  # pwdSUDO = getpass.getpass("Input SUDO password: ")
  usrSSH = "dcsadmin"
  pwdSSH = "Nig@team!"
  pwdSUDO = "Nig@team!"
  ################################################################

  for host in hosts:
    logWriter = LogWriter( os.path.join(os.getcwd(), "log", today + "_host_" + host + ".log") )
    logWriter.write("\n" + "----------------" + "\n")
    logWriter.write("## Executed at " + today + "\n")

    ssh_connect(host_address=host, username=usrSSH, password_ssh=pwdSSH, password_sudo=pwdSUDO)

  counter_total_done = len(list_host_done)
  counter_total_failed = (len(list_host_failed_auth) + len(list_host_failed_socket) + len(list_host_failed_ssh) + len(list_host_failed_hostkey))

  print ""
  print "==> END"
  print ""
  # print '--------------------------------'
  print "==> Result"
  print "Total Done: %d" % counter_total_done
  print "Total Failed: %d" % counter_total_failed

####

shell = None
logWriterMaster = None
logWriter = None

list_host_done = []
list_host_failed_auth = []
list_host_failed_socket = []
list_host_failed_ssh = []
list_host_failed_hostkey = []

if __name__ == "__main__":
  main()
