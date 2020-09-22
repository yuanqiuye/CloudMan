from configparser import ConfigParser
import os

def parseCfg(name):
    cfg = ConfigParser()
    cfg.read('cm.ini')
    return cfg['general'][name]
