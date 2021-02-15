from pyodm import Node
import glob
import asyncio

class OdmManager:
    def __init(self):
        self.pathToImages = ""
        self.token = ''
        self.host = 'localhost'
        self.port = 3000
        self.timeout = 30
        self.task = None

    def config(self, pathToImage, token, host, port, timeout=30):
        """
        Configures the odm manager with login details and path to images

        Parameters
        ----------
        pathToImage: string
                path to the folder containing the image for example "images/*"
        token: string
                token for the WebODM Lightning
        host: string
                Hostname of the WenODM server
        port: int
                Port number of WebODM

        """
        self.pathToImage = pathToImage
        self.token = token
        self.host = host
        self.port = port
        self.timeout = timeout

    def processImages(self):
        """
        Uploads images to WebODM Lightning and downloads result after processing

        Parameters
        ----------


        """
        n = Node(self.host, self.port, self.token, self.timeout)
        task = n.create_task(glob.glob(self.pathToImage),{'dsm':True})
        task.wait_for_completion()
        task.download_assets("results")

