# change the limit of open files in os
exec {'change limit soft':
  command  => "sudo sed -i 's/holberton soft nofile 4/holberton soft nofile 88888/g'  /etc/security/limits.conf",
  provider => shell
}

# change the limit of open files in  os
exec {'change limit hard':
  command  => "sudo sed -i 's/holberton hard nofile 5/holberton hard nofile 88888/g'  /etc/security/limits.conf",
  provider => shell
}
