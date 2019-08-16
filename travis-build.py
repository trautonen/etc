#!/usr/bin/env python
import os
import subprocess
import sys
import yaml

jdks = {
    "openjdk8":  "java-1.8.0-openjdk",
    "openjdk10": "openjdk10",
    "openjdk11": "openjdk11"
}

options = sys.argv[1::]
goals = ["clean"]
mainjdk = False

print("JAVA_HOME: " + os.environ["JAVA_HOME"])

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

print("$" + command)
sys.exit(subprocess.call(command, shell=True))
