#!/usr/bin/env expect
set timeout 10

set origin_url [lindex $argv 0]
set username [lindex $argv 1]
set password [lindex $argv 2]
spawn git clone $origin_url
expect {
"*Username*" { send "$username\n"; exp_continue }
"*Password*" { send "$password\n"}
}
interact
