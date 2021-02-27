import os
import sys
import logging

from cli.parser import get_parser
from utils import ConfigData as CD
from utils.logger import init_logging
from utils.config import AppSettings


if __name__=='__main__':
    ap=get_parser()
    args=ap.parse_args()
    if args.action=='run':
        CD.APP_ROOT_PATH=os.path.abspath(os.path.dirname(__name__))
        #override basic config
        if args.config:
            try:
                CD.APP_CONFIG=AppSettings(_env_file=(args.config).lstrip())
                if args.name:
                    CD.APP_CONFIG.APP_NAME=args.name
                CD.APP_CONFIG.LOG_ROOT=CD.APP_CONFIG.APP_NAME
            except Exception as e:
                print(str(e))
                exit(1)
        else:
            CD.APP_CONFIG=AppSettings()
        #override port
        if args.port:
            CD.APP_CONFIG.PORT=args.port
            #override debug mark
        if args.debug:
            CD.APP_CONFIG.DEBUGMODE=True
        #end ready start server
        from app import start_server
        start_server()
    else:
        ap.print_help()
