# -*- coding: utf-8 -*-
import codecs
import os

class interval:
    def __init__(self,sample_no,xmin,xmax,text):
        self.xmin=xmin
        self.xmax=xmax
        self.text=text
        self.sample_no=sample_no
        

class Textgrid(object):
    def __init__(self, path=None):
        self.path = path
        self.xmin=0
        self.xmax=0
        self.tiers=0
        self.interval_size=0
        self.intrvals=None
    
    def interval_class(self,line):
        if line.find(']:')!=-1:
            return 1
        elif line.find('=')!=-1:
            if line.find('xmin')==0:
                return 2
            if line.find('xmax')==0:
                return 3
            if line.find('text')==0:
                return 4
        else :
            return 5
    
    def parse_file(self):
        #print "enter"
        if not os.path.exists(self.path):
            return False            
        fp=codecs.open(self.path,'r','utf-8')
        i=1
        xmin_main=0
        xmax_main=0
        xmin=0.0
        xmax=0.0
        text=''
        tpe=0
        last_tpe=0
        sample_no=0
        interval_array=[]
        for f in fp:
            f=f.strip()
            if(i==7):
                line=f.strip('\n').split('=',1)
                tiers=int(line[1])
            if(i==12):
                line=f.strip('\n').split('=',1)
                xmin_main=float(line[1])
            if(i==13):
                line=f.strip('\n').split('=',1)
                xmax_main=float(line[1])
            if(i==14):
                line=f.strip('    def \n').split('=',1)
                interval_size=int(line[1])
            if(i>=15):
                l=f.strip('\n')
                tpe=self.interval_class(f.strip('\n'))
                #print i,tpe,l
                if(tpe==1):
                    line=f.strip('intervals [')
                    line=line.split(']',1)[0]
                    sample_no=int(line)
                    if last_tpe==4 or last_tpe==5:
                        a=interval(sample_no-1,xmin,xmax,text.split('"',1)[0])
                        interval_array.append(a)
                        #print sample_no-1,xmin,xmax,text
                if(tpe==2):
                    line=f.strip('xmin = ')
                    xmin=float(line)
                if(tpe==3):
                    line=f.strip('xmax = ')
                    xmax=float(line)
                if(tpe==4):
                    line=f.strip('text =')
                    last_tpe=tpe
                    text=line.strip('"')
                    #print text
                if(tpe==5):
                    if last_tpe==4:
                        #print i,text
                        last_tpe=tpe
                        text=text+' '+f.strip('\n')
                        text=text.strip('"')
                    if last_tpe==5:
                        last_tpe=tpe
                        text=text+' '+f.strip('\n')
                        text=text.strip('"')
                        #print i,text
                if sample_no==interval_size and (tpe==4 or tpe==5):
                    a=interval(sample_no,xmin,xmax,text.split('"',1)[0])
                    interval_array.append(a)
                    #print sample_no,xmin,xmax,text
            i=i+1
        fp.close()
        #print  xmin_main,xmax_main,tiers,interval_size,interval_array
        self.xmin = xmin_main
        self.xmax=xmax_main
        self.tiers=tiers
        self.interval_size=interval_size
        self.intrvals=interval_array
        return True

if __name__ == "__main__":
    tgrid_path='sample.TextGrid'#ok
    
    txtGrd = Textgrid(tgrid_path)
    if not txtGrd.parse_file():
        print 'Error in Parsing txt grid'
        sys.exit(0)
