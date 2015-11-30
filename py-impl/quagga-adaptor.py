import sys
import re

sys.path.append('../gen-py')

from qbgp import BgpConfigurator
from qbgp.ttypes import *
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from telnetlib import Telnet

import socket


class BgpHandler:
	host = '10.10.10.1'
	port = 2605
	password = 'zebra'
	currentprompt = '>'

	bgp_asNumber = -1

	def __init__(self):
		self.log = {}

	def connectTelnet(self, host, port):
		self.tn = Telnet(host, port)
		print self.tn.read_until('Password:', 1)
		self.tn.write(self.password + '\n')
		print self.tn.read_until('>', 1)
		self.tn.write('enable\n')
		print self.tn.read_until('#', 1)
		self.currentprompt = '#'

	def execTelnetCommand(self, command):
		self.tn.write(command + '\n')
		return self.tn.read_until(self.currentprompt, 1)

	def closeTelnet(self):

		self.tn.close()

	def startBgpServer(self, asNumber, routerId, port, holdTime, keepAliveTime):
		print "StartBGP: " + str(asNumber) + ", " + str(routerId) + ", " + str(port) + ", " + str(
			holdTime) + ", " + str(keepAliveTime)
		self.asNumber = asNumber

		print "Opening telnet to: " + self.host + ":" + str(self.port)

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(asNumber))
		print self.execTelnetCommand('bgp router-id ' + str(routerId))
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def stopBgpServer(self):
		print "StopBGP: "

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('no router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def createPeer(self, ipAddress, asNumber):
		print "CreatePeer: " + str(ipAddress) + ", " + str(asNumber)

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('neighbor ' + str(ipAddress) + ' remote-as ' + str(asNumber))
		print self.execTelnetCommand('neighbor ' + str(ipAddress) + ' activate')
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def deletePeer(self, ipAddress):
		print "delete neigbor:" + str(ipAddress)

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('no neighbor ' + str(ipAddress))
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def addRouteMapToMPBGPPeer(self, ipAddress, routeMapNumber, routeMapDir='out'):
		print "add RouteMap To Peer: " + str(ipAddress) + ", route-map number " + str(
			routeMapNumber) + "direction " + routeMapDir

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('address-family vpn4')
		print self.execTelnetCommand(
			'neighbor ' + str(ipAddress) + ' route-map ' + str(routeMapNumber) + ' ' + routeMapDir)
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def deleteRouteMapToMPBGPPeer(self, ipAddress, routeMapNumber, routeMapDir='out'):
		print "delete RouteMap To Peer: " + str(ipAddress) + ", route-map number " + str(
			routeMapNumber) + "direction " + routeMapDir

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('address-family vpn4')
		print self.execTelnetCommand(
			'no neighbor ' + str(ipAddress) + ' route-map ' + str(routeMapNumber) + ' ' + routeMapDir)
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def addVrf(self, rd, irts, erts):
		print "add vrf: rd:" + str(rd) + " irts:" + str(irts) + " erts:" + str(erts)

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('router bgp ' + str(self.asNumber))
		print self.execTelnetCommand('end')
		self.closeTelnet()

		return 0

	def delVrf(self, rd):
		print "del vrf rd:" + str(rd)
		return 0

	def pushRoute(self, aclNum, routeMapNum, prefix, wildcard, ipAddress):
		seqNum = 1
		# TODO this has to be derived as next available one !
		print "push route prefix:" + str(prefix)
		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('access-list ' + str(aclNum) + ' permit ' + prefix + ' ' + wildcard)
		print self.execTelnetCommand('route-map ' + str(routeMapNum) + ' permit ' + str(seqNum))
		print self.execTelnetCommand('match ip address ' + str(aclNum))
		print self.execTelnetCommand('end')
		print self.execTelnetCommand('clear ip bgp ' + ipAddress + ' vpnv4 unicast out')
		# TODO consider alternative solution: peer group
		# print self.execTelnetCommand('clear ip bgp COCOPEERS vpnv4 unicast out') #TODO addPeer must add to COCOPEERS group

		self.closeTelnet()

		return 0

	def withdrawRoute(self, prefix, routeMapNum, seqNum, ipAddress):
		# TODO find appropriate seqNum using prefix
		print "withdrawRoute prefix " + str(prefix)

		self.connectTelnet(self.host, self.port)
		print self.execTelnetCommand('conf t')
		print self.execTelnetCommand('no route-map ' + str(routeMapNum) + ' permit ' + str(seqNum))
		print self.execTelnetCommand('end')
		print self.execTelnetCommand('clear ip bgp ' + ipAddress + ' vpnv4 unicast out')
		# TODO consider alternative solution: peer group
		# print self.execTelnetCommand('clear ip bgp COCOPEERS vpnv4 unicast out') #TODO addPeer must add to COCOPEERS group
		self.closeTelnet()

		return 0

	def getRoutes(self, optype, winsize):
		print "get routes optype:" + str(optype) + " winsize:" + str(winsize)
		routes = Routes()
		routes.errcode = 0

		routes.updates = []

		self.connectTelnet(self.host, self.port)
		self.tn.write("sh bgp ipv4 vpn tags" + '\n')
		bgproutes = self.readRoutes(self.tn)
		self.closeTelnet()

		for route in bgproutes:
			update = Update()
			update.type = 1
			update.reserved = 1
			update.prefixlen = int(route["mask"])
			update.label = int(route["label"])
			update.rd = route["rd"]
			update.prefix = route["prefix"]
			update.nexthop = route["nexthop"]

			routes.updates.append(update)

		return routes

	def readRoutes(self, f):
		line = f.read_until('\n', 1)

		while ((not self.getAS_RD(line)) or self.match_enable(line)):
			line = f.read_until('\n', 1)

		# endwhile

		routes = []
		while ((not (line == "")) or self.match_enable(line)):

			curr_as_rd = self.getAS_RD(line)
			if (curr_as_rd):
				# print "----- as=" + curr_as_rd["as"] + " rd=" + curr_as_rd["rd1"] +":" + curr_as_rd["rd2"]

				line = f.read_until('\n', 1)
				tags = self.get_tags(line)
				if (tags):
					print "----- as=" + curr_as_rd["as"] + " rd=" + curr_as_rd["rd1"] + ":" + curr_as_rd[
						"rd2"] + " intag=" + str(tags["intag"]) + " outtag=" + str(tags["outtag"])
					route = {"as": curr_as_rd, "rd": curr_as_rd["rd1"] + ":" + curr_as_rd["rd2"],
					         "label": tags["outtag"], "prefix": tags["prefix"], "mask": tags["mask"],
					         "nexthop": tags["nexthop"]}
					routes.append(route)
			# end if
			line = f.read_until('\n', 1)
		return routes

	# end readRoutes


	def getAS_RD(self, line):

		re1 = '(Route)'  # Word 1
		re2 = '(\\s+)'  # White Space 1
		re3 = '(Distinguisher)'  # Word 2
		re4 = '(:)'  # Any Single Character 1
		re5 = '.*?'  # Non-greedy match on filler
		re6 = '(\\d+)'  # Integer Number 1
		re7 = '.*?'  # Non-greedy match on filler
		re8 = '(\\d+)'  # Integer Number 2
		re9 = '(:)'  # Any Single Character 2
		re10 = '(\\d+)'  # Integer Number 3

		rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10, re.IGNORECASE | re.DOTALL)
		m = rg.search(line)
		if m:
			word1 = m.group(1)
			ws1 = m.group(2)
			word2 = m.group(3)
			c1 = m.group(4)
			ats = m.group(5)  # TODO [PZ] what is this really ?
			rd1 = m.group(6)
			c2 = m.group(7)
			rd2 = m.group(8)

			ret_array = {"as": ats, "rd1": rd1, "rd2": rd2}

			return ret_array
		else:
			return False

	# end as rd

	def get_tags(self, line):
		re1 = '(\\*)'  # Any Single Character 1
		re2 = '(>)'  # Any Single Character 2
		re3 = '(\\s+)'  # White Space 1
		re4 = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'  # IPv4 IP Address 1
		re5 = '(\\/)'  # Any Single Character 3
		re6 = '(\\d+)'  # Integer Number 1
		re7 = '.*?'  # Non-greedy match on filler
		re8 = '((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))(?![\\d])'  # IPv4 IP Address 2
		re9 = '.*?'  # Non-greedy match on filler
		re10 = '((\\d+))'  # Word 1
		re11 = '(\\/)'  # Any Single Character 4
		re12 = '((\\d+))'  # Integer Number 2

		rg = re.compile(re1 + re2 + re3 + re4 + re5 + re6 + re7 + re8 + re9 + re10 + re11 + re12,
		                re.IGNORECASE | re.DOTALL)
		# not very pretty but writing the regex will take to much time
		line = line.replace("notag", "0")
		# print line
		m = rg.search(line)
		if m:
			c1 = m.group(1)
			c2 = m.group(2)
			ws1 = m.group(3)
			prefix = m.group(4)
			c3 = m.group(5)
			mask = m.group(6)
			nexthop = m.group(7)
			intag = m.group(9)
			c4 = m.group(10)
			outtag = m.group(11)

			# print "("+c1+")"+"("+c2+")"+"("+ws1+")"+"("+prefix+")"+"("+c3+")"+"("+mask+")"+"("+nexthop+")"+"("+intag+")"+"("+c4+")"+"("+outtag+")"+"\n"

			ret_array = {"intag": intag, "outtag": outtag, "prefix": prefix, "mask": mask, "nexthop": nexthop}
			return ret_array
		else:
			return False

	# end get_tags

	def match_enable(self, line):

		re1 = '.*?'  # Non-greedy match on filler
		re2 = '(#)'  # Any Single Character 1

		rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
		m = rg.search(line)
		if m:
			c1 = m.group(1)
			return True
		else:
			return False
		# end match enable


handler = BgpHandler()
processor = BgpConfigurator.Processor(handler)
transport = TSocket.TServerSocket(port=7644)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)
print "Starting python server..."
server.serve()
print "done!"
