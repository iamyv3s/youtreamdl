import cherrypy
import pafy
import os
import subprocess


class HelloWorld(object):
    @cherrypy.expose
    def index(self, url="0C80BSgjb8M"):
        video = pafy.new(url)
        title1 = video.title.replace("(", "")
        title2 = title1.replace(")", "")
        title = title2.replace(" ", "_")
        bestaudio = video.getbestaudio(preftype="m4a")
        BESTFILE = os.getcwd() + "/media/" + str(title) + "." + str(bestaudio.extension)
        MP3FILE = os.getcwd() + "/media/" + str(title) + ".mp3"
        COVER = os.getcwd() + "/media/cover.png"
        MP3FINAL = os.getcwd() + "/media/[youtream.com]-" + str(title) + ".mp3"
        print (BESTFILE, MP3FILE)
        bestaudio.download(BESTFILE)
        print ("You have successfully downloaded the ."+str(bestaudio.extension)+" file")
        command1 = "ffmpeg -i "+str(BESTFILE)+" -vn -ab 128k -ar 44100 -metadata album=\"Youtream\" -y "+str(MP3FILE)
        command2 = "ffmpeg -i "+str(MP3FILE)+" -i "+str(COVER)+" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title='Album cover' -metadata:s:v comment='Cover (front)' -y "+str(MP3FINAL)
        subprocess.call(command1, shell=True)
        subprocess.call(command2, shell=True)
        os.remove(BESTFILE)
        os.remove(MP3FILE)
        return """
            <html>
            <head>
                <title> Download </title>
            </head>
            <body>
            <a href="%(link)s" download>download</a>
            </body>
            </html>
            """ %{ 'link': '/media/[youtream.com]-'+ str(title) + ".mp3", 'file': str(title)}

config = {
    'global': {
        'server.socket_host': '0.0.0.0',
        'server.socket_port': int(os.environ.get('PORT', 5000)),
    },
    '/media': {
        'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__)),
        'tools.staticdir.on': True,
        'tools.staticdir.dir': 'media',
    }
}

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld(),'/', config=config)