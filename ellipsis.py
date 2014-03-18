#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import subprocess
import sys


devnull = open(os.devnull, 'w')


def find_svn(path):
    try:
        svn_cmd = ['/usr/bin/svn', 'info']
        svn_info = subprocess.check_output(svn_cmd, stderr=devnull).decode()
        info = dict()
        for line in svn_info.splitlines():
            if ':' in line:
                key, value = line.split(':', maxsplit=1)
                info[key]=value.strip()
        root = info.get('Working Copy Root Path')
        abbr = 'SVN:{name}'.format(name=os.path.split(root)[-1])
        return (root, abbr)
    except:
        return False  


def find_git(path):
    try:
        git_cmd = ['/usr/bin/git', 'rev-parse', '--show-toplevel']
        git_root = subprocess.check_output(git_cmd, stderr=devnull)
        git_root = git_root[:-1] # remove new_line
        git_root = git_root.decode()
        branch_cmd = ['/usr/bin/git', 'rev-parse', '--abbrev-ref', 'HEAD']
        git_branch = subprocess.check_output(branch_cmd, stderr=devnull)
        git_branch = git_branch[:-1] # remove new_line
        git_branch = git_branch.decode()
        abbr = 'GIT:{name}({branch})'.format(name=os.path.split(git_root)[-1], branch=git_branch)
        return (git_root, abbr) 
    except:
        return False


def find_home(path):
    home = os.getenv('HOME')
    if path.startswith(home):
        return (home, '~')
    else:
        return False


cwd = os.getcwd()
git_sub = find_git(cwd)
svn_sub = find_svn(cwd)
home_sub = find_home(cwd)
substitution = git_sub or svn_sub or home_sub
if substitution:
    original, replacement = substitution
    cwd = cwd.replace(original, replacement)

components = cwd.split('/')

if len(components) > 4:
    first = components[0]
    tail = '/'.join(components[-2:])
    cwd = '{}/…/{}'.format(first, tail)
print(cwd)
