#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import sys
import ConfigParser
import getopt

conf = 'sshlink.ini'
grunfile = os.getcwd()+'/grun'


def sshlink(line,gbkflag):
    global grunfile
    tmp = line.split(":")

    strssh = 'ssh -p {0} {1}'
    if gbkflag :
        strssh =  grunfile+' ssh -p {0} {1}'
        
    strcmd = ''

    if len(tmp)==2:
        strcmd = strssh.format(tmp[1],tmp[0])
    elif len(tmp)==1:
        strcmd = strssh.format('22',tmp[0])
    
    print strcmd + "\n"
    os.system(strcmd)
   
def checkgbk(section):
    section = section.strip().lower()
    strend = section[-3:]
    gbkflag = False
    strfinal = section
    if strend == 'gbk':
        gbkflag = True
        strfinal = section[:-3]
        releasegrun()

    return gbkflag,strfinal


def getHost(section):
    global conf
    if not os.path.isfile(conf):
        print u"配置文件不存在\t"+conf
        sys.exit()
    cf = ConfigParser.ConfigParser()
    cf.readfp(open(conf))

    secs = cf.sections()
    if section == "":
        print "\t\t".join(secs)
        sys.exit()
    else :
        if section in secs:
            ss = cf.options(section)
            print "\t\t".join(ss)
            sys.exit()
        else:
            for s in secs:
                ss = cf.options(s)
                if section in ss:
                    opts = cf.get(s,section)
                    if opts :
                        return section,opts

            #未找到，可能是ip地址
            for s in secs :
                items = cf.items(s)

                for k,v in items:
                    if section in v:
                        return k,v


    print u"未找到对应的主机"
    sys.exit()

def releasegrun():
    global grunfile
    if not os.path.isfile(grunfile):
        strcmd = '#!/bin/bash\necho -e "\033]50;SetProfile=GBK\a"\nexport LANG=zh_CN.GBK\nexport LC_ALL=zh_CN.GBK\necho -ne "\033]0;"$@"\007"\n$@\necho -ne "\033]0;"${PWD/#$HOME/~}"\007"\necho -e "\033]50;SetProfile=Default\a"\nexport LANG=zh_CN.UTF-8\nexport LC_ALL=zh_CN.UTF-8'
        try:
            f = open(grunfile,'w')
            try:
                f.write(strcmd)
            finally:
                f.close()
        except IOError:
            print "Error: grun 写入失败"

    os.chmod(grunfile,0o755)
    
def usage():
    print u"\nssh快速连接\nusage: sshlink alias|ip"
    print u"\t-h:帮助"
    print u"\t-l [alias|ip]: 查找机器"

def getopts(key,opts):
    if key not in opts:
        print u"输入参数有误\n"
        sys.exit()
    return opts[key]

if __name__ == '__main__':
    opts,args = getopt.getopt(sys.argv[1:],"hl")
    l = len(args)
    if len(opts) == 0 and l==0 :
        usage()
        sys.exit()

    opt_dict = {}
    for op,value in opts:
        opt_dict[op] = value

    secstr = ''
    if l==1:
        secstr = args[0]

    gbkflag,section = checkgbk(secstr)

    for op,value in opts:
        if op == '-l':
            k,v = getHost(section)
            print k,"=>",v
            sys.exit()

    if section :
        k,v = getHost(section)
        print u"正在连接\t" + k + "\n"
        sshlink(v,gbkflag)
        sys.exit()

    usage()
    sys.exit()
