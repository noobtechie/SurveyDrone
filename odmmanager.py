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
        self.pathToImage = pathToImage
        self.token = token
        self.host = host
        self.port = port
        self.timeout = timeout

    def processImages(self):
        n = Node(self.host, self.port, self.token, self.timeout)
        task = n.create_task(glob.glob(self.path),{'dsm':True})
        task.wait_for_completion()
        task.download_assets("results")

