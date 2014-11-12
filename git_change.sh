#! /bin/bash
git remote rm origin 
echo -n "请出入要更新的 git 地址:"
read git_url
git remote add origin $git_url
git branch --set-upstream master origin/master
