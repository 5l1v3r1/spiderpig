#!/usr/bin/python
#
#
#


import os
import sys

def banner():
        print      "     ___      __    "                                               
        print      "    |__      |__| "                             
        print      "    ___|PIDER|  IG"                                 
        print      "  "                                              
        print      " by cons0ul <sachinshinde11[at]gmail.com>  "
        print      " no copyright use it on your own risk.  "
        print      "----------------------------------------------\n\n"    
                
                        

from spig import fuzzer;
import sys
#universal evil params.
string = ["http://"+('A'*9182),"ftp://"+('A'*9182),'A' * 8200, 'A' * 11000, 'A' * 110000, 'A' * 550000, 'A' * 1100000,'A' * 2200000,"\0*99" * 1200, "//AAAA" * 450, "\\AAAA" * 450]

fmt = ["%n%n%n%n%n", "%p%p%p%p%p", "%s%s%s%s%s", "%d%d%d%d%d", "%x%x%x%x%x",
              "%s%p%x%d", "%.1024d", "%.1025d", "%.2048d", "%.2049d", "%.4096d", "%.4097d",
              "%99999999999s", "%08x", "%%20n", "%%20p", "%%20s", "%%20d", "%%20x", 
              "%#0123456x%08x%x%s%p%d%n%o%u%c%h%l%q%j%z%Z%t%i%e%g%f%a%C%S%08x%%"]#, "\0xCD" * 50, "\0xCB" * 50];

numbers = [  "1", "-1", "32767", "-32768", "2147483647", "-2147483647", "2147483648", "-2147483648",
            "4294967294", "4294967295", "4294967296", "357913942", "-357913942", "536870912", "-536870912",
            "1.79769313486231E+308", "3.39519326559384E-313", "99999999999", "-99999999999", "0x100", "0x1000",
            "0x3fffffff", "0x7ffffffe", "0x7fffffff", "0x80000000", "0xffff", "0xfffffffe", "0xfffffff", "0xffffffff",
            "0x10000", "0x100000", "0x99999999", "65535", "65536", "65537", "16777215", "16777216", "16777217",  "-268435455","0x100000000", "0x40000000", "0x20000000", "0x10000000"," 0x01000000"," 0x00100000"," 0x00010000"," 0x00001000"," 0x00000100"," 0x00000010","0","-0"];



"""misc = ["test|touch /tmp/ZfZ-PWNED|test", "test`touch /tmp/ZfZ-PWNED`test", "test'touch /tmp/ZfZ-PWNED'test", "test;touch /tmp/ZfZ-PWNED;test",
             "test&&touch /tmp/ZfZ-PWNED&&test", "test|C:/WINDOWS/system32/calc.exe|test", "test`C:/WINDOWS/system32/calc.exe`test",
             "test'C:/WINDOWS/system32/calc.exe'test", "test;C:/WINDOWS/system32/calc.exe;test", "/bin/sh", "C:/WINDOWS/system32/calc.exe", "%0xa", "%u000"];"""
obj=['this','new Object()','null']


eol="\n"

strDefault="AAAAAAAAAAAAAAAAA"
numDefault="1"
boolDefault="true"
objDefault='null'


def log(struct):
        return 'console.println(\'\\n>>'+struct+' \')'  


def construct(method,params,indexl):
        val=method+"("
        rng=len(indexl)
        i=0;
        for k in indexl:
                 val+=params[k] 
                 if(i+1 < rng):
                        val+=","
                 i+=1
        val+=")"
        return val              

class fuzz():
        def __init__(self,pdfpath,protofile):
                self.path=pdfpath
                self.fileproto=protofile
                self.stream=""
                self.counter=0

                        
        def readproto(self):
                commaindex=0
                commaindex2=0
                f=file(self.fileproto,"rb")          
                dic={}
                methods=f.read();
                if(methods == None or methods == ""):
                        sys.exit(0)
                for proto in methods.splitlines():        
                        commaindex=proto.find('(');
                        #print(proto)
                        if(commaindex == -1):
                                print('[-]\'(\' not found.');
                                continue
                                
                        commaindex2=proto.find(')');
                        if(commaindex2 == -1):
                                print('[-] \')\' not found.');
                                continue
                        func=proto[:commaindex]
                        #print func        
                        s=proto[commaindex+1:commaindex2]       
                        params=s.split(',')
                        dic[func]=params
                return dic
                                                        
        def createsource(self,dic):
                templ=[]
                tempstr=""
                #print dic        
                self.stream="console.show();"+eol
                for k in dic.keys():
                        print '>> writing fuzzer for %s'%k 
                        self.stream="console.show()"+eol
                        for i in range(len(dic[k])):
                                tmp_dic={}
                        
                                for param in dic[k]:
                                        if(param[0]=='c'):
                                                tmp_dic[param]="\""+strDefault+"\""       
                                        elif(param[0]=='n' or param[0]=='b'):
                                                tmp_dic[param]=numDefault
                                        elif(param[0]=='o'):
                                                tmp_dic[param]=objDefault
                                                
                                if(dic[k][i][0]=='c'):
                                        for evilstr in string:
                                                if(tmp_dic.has_key(dic[k][i]) == True):
                                                        tmp_dic[dic[k][i]]="\""+evilstr+"\""
                                                        tmpstr=construct(k,tmp_dic,dic[k]) 
                                                        tmp_dic[dic[k][i]]="A("+str(len(evilstr))+")"     
                                                        tmpc=construct(k,tmp_dic,dic[k])
                                                        self.stream+=log(tmpc)+eol
                                                        self.stream+=tmpstr+eol
                                        for evilfmt in fmt:
                                                if(tmp_dic.has_key(dic[k][i])== True):
                                                        tmp_dic[dic[k][i]]="\""+evilfmt+"\""
                                                        tmpstr=construct(k,tmp_dic,dic[k]) 
                                                        self.stream+=log(tmpstr)+eol
                                                        self.stream+=tmpstr+eol
                                                        
                        
                                elif(dic[k][i][0]=='n' or dic[k][i][0]=='b'):
                                        for evilnum in numbers:
                                                if(tmp_dic.has_key(dic[k][i])==True):     
                                                        tmp_dic[dic[k][i]]=evilnum
                                                        tmpstr=construct(k,tmp_dic,dic[k])        
                                                        self.stream+=log(tmpstr)+eol
                                                        self.stream+=tmpstr+eol
                                        for evilfmt in fmt:
                                                if(tmp_dic.has_key(dic[k][i])== True):
                                                        tmp_dic[dic[k][i]]="\""+evilfmt+"\""
                                                        tmpstr=construct(k,tmp_dic,dic[k]) 
                                                        self.stream+=log(tmpstr)+eol
                                                        self.stream+=tmpstr+eol              
                                elif(dic[k][i][0]=='o'):
                                        for evilobj in obj:
                                                if(tmp_dic.has_key(dic[k][i]) == True):
                                                        tmp_dic[dic[k][i]]=evilobj
                                                        tmpstr=construct(k,tmp_dic,dic[k])        
                                                        self.stream+=log(tmpstr)+eol
                                                        self.stream+=tmpstr+eol                         
                        print '>> creating file %s'%(self.path+k+".pdf")
                        #f=file(self.path+k+".js","w");
                        #f.write(self.stream)
                        #f.close()                               
                        self.counter+=fuzzer(self.path+k+".pdf",self.stream)
                print '>> %d file(s) created.Good Luck!!' % self.counter
                                                
def main(args):
        banner();
        if(len(args) < 2):
                print 'usage:sp.py <dir-path> <prototype-file>'
                sys.exit(0)
        if(args[0][-1] != '\\' and args[0][-1] != '/'):
                if(os.name == 'nt'):
                        args[0]+='\\'
                else:
                        args[0]+='/'
        f= fuzz(args[0],args[1])
        meths=f.readproto()
        f.createsource(meths)
        

if __name__ == '__main__':
        main(sys.argv[1:])
        
