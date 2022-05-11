import logging
from gpnbp.server import GPNBPServer
from gpnbp.webAPI.webAPI import WebAPI

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    server = GPNBPServer()
    WebAPI(server)
