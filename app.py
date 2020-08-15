import cherrypy
import pafy
import os

class HelloWorld(object):
    @cherrypy.expose
    def index(self, url="0C80BSgjb8M"):
        video = pafy.new(url)
        bestaudio = video.getbestaudio(preftype="m4")
        bestvideo = video.getbestvideo('mp4')
        
        raise cherrypy.HTTPRedirect(bestaudio.url)

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/assets': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'assets',
    }
}

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(),'/', config=config)