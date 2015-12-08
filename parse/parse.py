#!/usr/bin/python

import re

def getAS_RD(line):

	re1='(Route)'	# Word 1
	re2='(\\s+)'	# White Space 1
	re3='(Distinguisher)'	# Word 2
	re4='(:)'	# Any Single Character 1
	re5='.*?'	# Non-greedy match on filler
	re6='(\\d+)'	# Integer Number 1
	re7='.*?'	# Non-greedy match on filler
	re8='(\\d+)'	# Integer Number 2
	re9='(:)'	# Any Single Character 2
	re10='(\\d+)'	# Integer Number 3

	rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10,re.IGNORECASE|re.DOTALL)
	m = rg.search(line)
	if m:
		word1=m.group(1)
		ws1=m.group(2)
		word2=m.group(3)
		c1=m.group(4)
		ats=m.group(5)
		rd1=m.group(6)
		c2=m.group(7)
		rd2=m.group(8)
		
		ret_array  = {"as" : ats, "rd1": rd1, "rd2":  rd2 }

		return ret_array
	else:
		return False


def get_as_rd_route(line):
	re1='(\\*)'	# Any Single Character 1
	re2='(>)'	# Any Single Character 2
	re3='(\\s+)'	# White Space 1
	re4='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# IPv4 IP Address 1
	re5='(\\/)'	# Any Single Character 3
	re6='(\\d+)'	# Integer Number 1
	re7='.*?'	# Non-greedy match on filler
	re8='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# ip 2

	rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8,re.IGNORECASE|re.DOTALL)
	m = rg.search(line)
	if m:
		c1=m.group(1)
		c2=m.group(2)
		ws1=m.group(3)
		subnet=m.group(4)
		c3=m.group(5)
		mask=m.group(6)
		nexthop=m.group(7)

		ret_array = {"subnet": subnet, "mask" : mask, "nexthop" : nexthop}
		return ret_array
	else:
		return False


def get_tags(line):
	re1='(\\*)'	# Any Single Character 1
	re2='(>)'	# Any Single Character 2
	re3='(\\s+)'	# White Space 1
	re4='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# IPv4 IP Address 1
	re5='(\\/)'	# Any Single Character 3
	re6='(\\d+)'	# Integer Number 1
	re7='.*?'	# Non-greedy match on filler
	re8='((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'	# IPv4 IP Address 2
	re9='.*?'	# Non-greedy match on filler
	re10='((\\d+))'	# Word 1
	re11='(\\/)'	# Any Single Character 4
	re12='((\\d+))'	# Integer Number 2
	
	rg = re.compile(re1+re2+re3+re4+re5+re6+re7+re8+re9+re10+re11+re12,re.IGNORECASE|re.DOTALL)
	#not very pretty but i the regex will take to much time
	line = line.replace("notag","0")
	#print line
	m = rg.search(line)
	if m:
		c1=m.group(1)
		c2=m.group(2)
		ws1=m.group(3)
		prefix=m.group(4)
		c3=m.group(5)
		mask=m.group(6)
		nexthop=m.group(7)
		intag=m.group(9)
		c4=m.group(10)
		outtag=m.group(11)

		#print "("+c1+")"+"("+c2+")"+"("+ws1+")"+"("+prefix+")"+"("+c3+")"+"("+mask+")"+"("+nexthop+")"+"("+intag+")"+"("+c4+")"+"("+outtag+")"+"\n"		

		ret_array = { "intag" : intag, "outtag": outtag, "prefix": prefix, "mask":mask, "nexthop": nexthop }
		return ret_array
	else:
		return False
#end get_tags

def match_enable(line):

	re1='.*?'	# Non-greedy match on filler
	re2='(#)'	# Any Single Character 1

	rg = re.compile(re1+re2,re.IGNORECASE|re.DOTALL)
	m = rg.search(line)
	if m:
		c1=m.group(1)
		return True
	else:
		return False
#end match enable






print ("------------------------------input.txt")
f = open('./input.txt')

line = f.readline()

while((not getAS_RD(line)) or match_enable(line)):
	line = f.readline()
#endwhile
	
while ( (not (line =="")) or match_enable(line)):

	curr_as_rd = getAS_RD(line)
	if (curr_as_rd):
		#print "----- as=" + curr_as_rd["as"] + " rd=" + curr_as_rd["rd1"] +":" + curr_as_rd["rd2"]

		line = f.readline()
		as_rd_route = get_as_rd_route(line)
		if (as_rd_route):
			print "----- as=" + curr_as_rd["as"] +  " rd=" + curr_as_rd["rd1"] +":" + curr_as_rd["rd2"] + " subnet=" + as_rd_route["subnet"] + " mask=" + as_rd_route["mask"] + " nexhop=" + as_rd_route["nexthop"]		
	#end if	
		
	line = f.readline()


f.close()

#--- other command

print "------------------------- input2.txt"

f = open('./input2.txt')


def getTags(f):
	line = f.readline()

	while( (not getAS_RD(line)) or match_enable(line)):
	        line = f.readline()

	#endwhile
	

	while ( (not (line =="")) or match_enable(line)):

        	curr_as_rd = getAS_RD(line)
	        if (curr_as_rd):
		        #print "----- as=" + curr_as_rd["as"] + " rd=" + curr_as_rd["rd1"] +":" + curr_as_rd["rd2"]

		        line = f.readline()
        		tags = get_tags(line)
		        if (tags):
	        	        print "----- as=" + curr_as_rd["as"] + " rd=" + curr_as_rd["rd1"] +":" + curr_as_rd["rd2"] + " intag=" + str(tags["intag"]) + " outtag=" + str(tags["outtag"])
		#end if

	        line = f.readline()

#end get tags

getTags(f)

f.close()

