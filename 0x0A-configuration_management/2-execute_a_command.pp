# kills a process named killmenow
exec { 'killmenow':
  command => 'pkill -n killmenow',
  path    => '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin',
  onlyif  => 'test `pgrep killmenow|wc -l` -ge 1',
}
