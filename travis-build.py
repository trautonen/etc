#!/usr/bin/env python
import os
import subprocess
import sys
import yaml

jdks = {
    "oraclejdk8": "java-8-oracle",
    "oraclejdk7": "java-7-oracle",
    "openjdk7":   "java-7-openjdk",
    "openjdk6":   "java-6-openjdk"
}

options = sys.argv[1::]
goals = ["clean"]
mainjdk = False

with open(os.getcwd() + "/.travis.yml", "r") as conf:
    travis = yaml.load(conf)

if jdks[travis["jdk"][0]] in os.environ["JAVA_HOME"]:
    mainjdk = True

pullrequest = os.environ["TRAVIS_PULL_REQUEST"]
version = subprocess.check_output("mvn help:evaluate -Dexpression=project.version | grep -Ev '(^\[|Download\w+:)'", shell=True).strip()

if pullrequest == "false" and version.endswith("-SNAPSHOT") and mainjdk:
    options.append("-Pprepare-deploy")
    goals.append("deploy")
else:
    goals.append("verify")

command = "mvn " + " ".join(options + goals)

print "$" + command
sys.exit(subprocess.call(command, shell=True))
