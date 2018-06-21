import paramiko
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

  client = paramiko.SSHClient()
  client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  client.connect(host_address, username=username, password=password_ssh)

  shell = client.invoke_shell()

  logWriter.write("\n")
  logWriter.write( "## Started for %s at %s\n\n" % (host_address, datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')) )

  send_string_and_wait("sudo -s", 1, should_print=False, should_logfile=False)
  send_string_and_wait(password_sudo, 1, should_print=False, should_logfile=False)

  ################################################################
  ##  List of command(s)
  ################################################################
  commands = [
    'sudo touch /opt/paramiko.log',
    'sudo echo $(date) >> /opt/paramiko.log',
    'sudo ls -l /etc/freeradius/sites-enabled',
    'sudo systemctl -q status freeradius.service --no-pager',
    'sudo echo done >> /opt/paramiko.log'
  ]
  ################################################################

  for command in commands:
    # print '\nSEND >>>> %s\n' % command
    send_string_and_wait(command, 1, should_print=True, should_logfile=True)

  client.close()

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
  print "Entered %d host(s):" % len(hosts)
  for host in hosts:
    logWriterMaster.write( host + "\n" )
    print host

  ################################################################
  ##  Get username/password and sudo enable password
  ################################################################
  usrSSH = getpass.getpass("Input SSH username: ")
  # usrSSH = 'myadmin'
  pwdSSH = getpass.getpass("Input SSH password: ")
  pwdSUDO = getpass.getpass("Input SUDO password: ")
  ################################################################

  for host in hosts:
    logWriter = LogWriter( os.path.join(os.getcwd(), "log", today + "_host_" + host + ".log") )
    logWriter.write("\n" + "----------------" + "\n")
    logWriter.write("## Executed at " + today + "\n")
    ssh_connect(host_address=host, username=usrSSH, password_ssh=pwdSSH, password_sudo=pwdSUDO)

####

shell = None
logWriterMaster = None
logWriter = None

if __name__ == "__main__":
  main()

