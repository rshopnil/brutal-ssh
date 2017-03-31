# brutal-ssh
It's a basic ssh botnet which can brute force system passwords with provided list. Only for educational purposes :)

goto the dir containing the script & invoke it like:
  $ python sshBotnet.py -H <host_addr> -u <user> -F <passwd_file>
  
 given the paswd_file is in the current dir, this script would guess the pass for all the words inside the file.
 So, an attempt would be as good as the passFile provided
