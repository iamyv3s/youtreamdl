import cherrypy
import pafy
import os
import subprocess


class HelloWorld(object):
    @cherrypy.expose
    def index(self, url="0C80BSgjb8M"):
        video = pafy.new(url)
        title = video.title.replace(" ", "_")
        bestaudio = video.getbestaudio(preftype="m4a")
        BESTFILE = os.getcwd() + "/" + str(title) + "." + str(bestaudio.extension)
        MP3FILE = os.getcwd() + "/" + str(title) + ".mp3"
        print (BESTFILE, MP3FILE)
        bestaudio.download(BESTFILE)
        print ("You have successfully downloaded the ."+str(bestaudio.extension)+" file")
        command = "ffmpeg -i "+str(BESTFILE)+" -vn -ab 128k -ar 44100 -y "+str(MP3FILE)
        subprocess.call(command, shell=True)
        os.remove(BESTFILE)
        return """
            <html>
            <head>
                <title> Download </title>
            </head>
            <body>
            <a href="%(link)s" download="%(file)s">download</a>
            </body>
            </html>
            """ %{ 'link': MP3FILE, 'file': str(title)}

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