#!/usr/bin/python3
# Library
import configparser
import argparse
import datetime
import logging
from os.path import join
from subprocess import call
# Local

def init():
    logging.basicConfig(
        filename=join('logs', str(datetime.date.today()) + '.log'),
        level=logging.DEBUG,
        format='[%(asctime)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info('Initializing')

    parser = argparse.ArgumentParser(description='Runner script for Event aggregation')
    parser.add_argument('--reset_config', action='store_true', help='Reset defaults.cfg to defaults')
    parser.add_argument('--config_file', default='config/defaults.cfg', help='Specify which config file to use')
    args = parser.parse_args()

    # the reset config file flag was given, so we reset the config file and exit
    if args.reset_config:
        logging.info('Creating default config file')
        default_config()
        logging.info('Finished creating default config file, exiting')
        exit()

    config = configparser.RawConfigParser(allow_no_value=True)
    config.optionxform = str
    config.read(args.config_file)

    return args, config

def default_config():
    config = configparser.RawConfigParser(allow_no_value=True)
    config.optionxform = str
    config.add_section('Spiders')
    config.set('Spiders', 'bostoncalendar_spider.py', '-o bostoncalendar_events.json')

    with open('config/defaults.cfg', 'wt') as configfile:
        config.write(configfile)

def write_to_file(content, filename):
    logging.info('Writing data to "' + filename + '"')
    f = open(filename, 'a+')
    f.write(content)
    f.close()

def main():
    args, config = init()
    spiders = config.items('Spiders')
    for spider, args in spiders:
        call(['scrapy', 'crawl', spider] + args.split(), cwd='bostonevents')

main()
