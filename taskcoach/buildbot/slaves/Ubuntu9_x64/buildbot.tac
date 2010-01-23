
from twisted.application import service
from buildbot.slave.bot import BuildSlave

basedir = r'/home/fraca7/Buildslave'
host = '192.168.1.2'
port = 9989
slavename = 'Ubuntu9_x64'
passwd = file('.passwd', 'rb').readlines()[0].strip()
keepalive = 600
usepty = 1
umask = None

application = service.Application('buildslave')
s = BuildSlave(host, port, slavename, passwd, basedir, keepalive, usepty,
               umask=umask)
s.setServiceParent(application)
