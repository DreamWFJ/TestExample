#!/usr/bin/env expect
set timeout 10
spawn git push -u origin --all
expect {
"*Username*" { send "wangfangjie\n"; exp_continue }
"*Password*" { send "pdmi1234\n"}
}
interact
