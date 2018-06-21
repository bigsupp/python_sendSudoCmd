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
- Support logging stdout to files
- **Did not test with large numbers of remote host
