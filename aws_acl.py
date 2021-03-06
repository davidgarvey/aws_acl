import cherrypy
cherrypy.config.update({'server.socket_port': 9999})
cherrypy.server.socket_host = 'your_ip'
#cherrypy.engine.restart()
from os import path
import os
from jinja2 import Environment, FileSystemLoader
current_dir = path.dirname(path.abspath(__file__))
env = Environment(loader=FileSystemLoader(path.join(current_dir,'templates3')))

config = {
 '/': {},
}


class Root(object):
 
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template("root.html")
        return tmpl.render()
 
    @cherrypy.expose
    def deleteIP(self):
        cmd = "/home/ansible/www/del_ipadd_ec2_sg.py"
        os.system(cmd)
        return self.refresh()

    @cherrypy.expose
    def form(self):
        tmpl = env.get_template("form.html")
        return tmpl.render()

    @cherrypy.expose
    def addIP(self, ipaddress=None):
        cmd = "/home/ansible/www/add_ipadd_ec2_sg.py --ip %s" %ipaddress
        os.system(cmd)
        return self.refresh()

    @cherrypy.expose
    def refresh(self):
        return self.index()
 
app = cherrypy.tree.mount(Root(), "/", config)
cherrypy.engine.start()
cherrypy.engine.block()
