# python_sendSudoCmd
Python script for sending command(s) to remote Ubuntu server via SSH (support with sudo)

Usage:
```
python sendSudoCmd.py <remote hosts separated by comma>
```
Example:
```
python sendSudoCmd.py 192.168.1.101,192.168.1.102,192.168.1.103,192.168.1.104,192.168.1.105
```

Information:
- Requires paramiko python module as SSH client
  - Windows:
  ```
  D:\<Python installed directory>\Scripts\pip install paramiko
  ```
  - Linux:
  ```
  # pip install paramiko
  ```
- Test run on Python 2.x
- Support logging stdout to log files: operation log and remote host log
  - operation log: contains execution time and target hosts
  - remote host log: contains execution time on target hosts and stdout
- **Did not test with large numbers of remote host

---

Example of running the script:

```
$ python sendSudoCmd.py 192.168.150.19,10.9.11.210,192.168.150.55

--------------------------------
==> Entered 3 host(s):
192.168.150.19
10.9.11.210
192.168.150.55

==> START

==> Host Address: 192.168.150.19

(i) connecting
(i) connected
(i) invoke shell
(i) logon sudoer
(i) sending commands

sudo touch /opt/paramiko.log
root@appservice01:~#
sudo echo $(date) >> /opt/paramiko.log
root@appservice01:~#

(i) client closed

==> Host Address: 10.9.11.210

(i) connecting
(x) !! Socket error, please verify host and port of 10.9.11.210

==> Host Address: 192.168.150.55

(i) connecting
(i) connected
(i) invoke shell
(i) logon sudoer
(i) sending commands

sudo touch /opt/paramiko.log
root@radpolicy:~#
sudo echo $(date) >> /opt/paramiko.log
root@radpolicy:~#

(i) client closed

==> END

==> Result
Total Done: 2
Total Failed: 1

```
