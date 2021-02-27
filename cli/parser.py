import argparse

def get_parser():
    ap=argparse.ArgumentParser()
    subparsers = ap.add_subparsers(dest="action", help="Run or help[default]")
    ap_run = subparsers.add_parser("run", help="run manager[-h for more help]")
    runner_parser(ap_run)
    return ap

def runner_parser(ap_run=None):
    if not ap_run:
        ap_run=argparse.ArgumentParser()
    ap_run.add_argument('-n','--name',help="define app running name manually(Optional)",nargs="?",
                    action='store', type=str,default=None)
    ap_run.add_argument('-d','--debug',help="Use debug mode to start(Optional)",action='store_true')
    ap_run.add_argument('-c','--config',help="set custom store place where read config file(Optional)",nargs="?",
                    action='store', type=str,default=None) 
    ap_run.add_argument('-p','--port',help="set server port manually(Optional)",nargs="?",
                    action='store', type=int,default=3003)    
    return ap_run