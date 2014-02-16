#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys

cwd = os.getcwd()
home = os.getenv('HOME')

devnull = open(os.devnull, 'w')

def find_svn_root(path):
    try:
        svn_cmd = ['/usr/bin/svn', 'info']
        svn_info = subprocess.check_output(svn_cmd, stderr=devnull).decode()
        info = dict()
        for line in svn_info.splitlines():
            if ':' in line:
                key, value = line.split(':', maxsplit=1)
                info[key]=value.strip()
        return info.get('Working Copy Root Path')
    except:
        return False  
        
def find_git_root(path):
    try:
        git_cmd = ['/usr/bin/git', 'rev-parse', '--show-toplevel']
        git_root = subprocess.check_output(git_cmd, stderr=devnull)
        git_root = git_root[:-1] # remove new_line
        return git_root.decode()
    except:
        return False

git_root = find_git_root(cwd)
svn_root = find_svn_root(cwd)
if git_root:
    repo_name = os.path.split(git_root)[-1]
    git_tag = "\033[1;31m{0}\033[1;37m".format(repo_name)
    cwd = cwd.replace(git_root, repo_name)
elif svn_root:
    repo_name = svn_root.split('/')[-1]
    svn_tag =  "\033[1;34m{0}\033[1;37m".format(repo_name)
    cwd = cwd.replace(svn_root, svn_tag)
elif cwd.startswith(home):
    cwd = cwd.replace(home,'~')

components = cwd.split('/')

if len(components) > 3:
    first = components[0]
    last = components[-1]
    cwd = "{}/…/{}".format(first, last)
print("\033[1;37m{cwd}\033[0m".format(cwd=cwd))
