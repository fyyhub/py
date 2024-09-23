#!/bin/bash

# 检查是否传递了密码参数
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <password>"
    exit 1
fi

# 获取输入的密码
ssh_password="$1"

# 机器列表
machines=(
    "fyy5210@s6.serv00.com"
    "566521a@s8.serv00.com"
    "178621833abc@s10.serv00.com"
    "jeffisme@s11.serv00.com"
    "thisismy001@s12.serv00.com"
    "thisismy002@s12.serv00.com"
)

# 获取当前用户名
current_user=$(whoami)

# 要执行的 SSH 命令
command_to_run="sh pm2.sh"

# 遍历机器列表
for machine in "${machines[@]}"; do
    username="${machine%@*}"  # 获取用户名
    hostname="${machine#*@}"   # 获取主机名

    # 检查是否是当前机器
    if [ "$current_user" != "$username" ]; then
        echo "Executing on $machine..."
        sshpass -p "$ssh_password" ssh "$machine" "$command_to_run"
    else
        echo "Skipping $machine (current user)"
    fi
done