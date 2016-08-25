from src.controller import WebScrapingController
from src.model import WebScraper
from src.view import PythonView
from src.cmd_interpreter import CmdInterpreter

if __name__ == "__main__":
    cs = WebScrapingController(PythonView(), WebScraper())
    cs.go()

    #cmd = CmdInterpreter()
    #cmd.cmdloop()