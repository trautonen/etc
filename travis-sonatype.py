#!/usr/bin/env python
import os
import os.path
import sys
import xml.dom.minidom

homedir = os.path.expanduser("~")
sonatypeSettings = "/.m2/sonatype.xml"
m2 = xml.dom.minidom.parse(homedir + "/.m2/settings.xml")

if os.environ["TRAVIS_SECURE_ENV_VARS"] != "false":
  settings = m2.getElementsByTagName("settings")[0]
  
  serversNodes = settings.getElementsByTagName("servers")
  if not serversNodes:
    serversNode = m2.createElement("servers")
    settings.appendChild(serversNode)
  else:
    serversNode = serversNodes[0]
  
  sonatypeServerNode = m2.createElement("server")
  sonatypeServerId = m2.createElement("id")
  sonatypeServerUser = m2.createElement("username")
  sonatypeServerPass = m2.createElement("password")
  
  idNode = m2.createTextNode("sonatype-nexus-snapshots")
  userNode = m2.createTextNode(os.environ["SONATYPE_USERNAME"])
  passNode = m2.createTextNode(os.environ["SONATYPE_PASSWORD"])
  
  sonatypeServerId.appendChild(idNode)
  sonatypeServerUser.appendChild(userNode)
  sonatypeServerPass.appendChild(passNode)
  
  sonatypeServerNode.appendChild(sonatypeServerId)
  sonatypeServerNode.appendChild(sonatypeServerUser)
  sonatypeServerNode.appendChild(sonatypeServerPass)
  
  serversNode.appendChild(sonatypeServerNode)
  
  print "secure environment variables available, writing custom maven settings for ~" + sonatypeSettings
else:
  print "no secure environment variables available, using default maven settings for ~" + sonatypeSettings

m2Str = m2.toxml()
f = open(homedir + sonatypeSettings, "w")
f.write(m2Str)
f.close()
