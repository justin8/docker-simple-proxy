#!/usr/bin/env python3

import click
import os
import shutil
import subprocess
import yaml
import logging
import sys
from pathlib import Path

from jinja2 import Template

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
log = logging.getLogger()


def start_nginx():
    try:
        subprocess.check_output(['nginx'])
    except subprocess.CalledProcessError as e:
        log.error("Failed to start nginx!")
        sys.exit(e.returncode)


def get_config(config_file=False, output_dir=False):
    if not hasattr(get_config, 'config'):
        config = {'services': []}
        if config_file.exists():
            with config_file.open() as f:
                config = yaml.load(f)
        config['output_dir'] = output_dir
        config = parse_config_from_env(config)
        log.debug("Parsed config: " + str(config))
        get_config.config = config
    return get_config.config


def parse_config_from_env(config):
    if 'DNS_TLD' in os.environ:
        config['tld'] = os.environ['DNS_TLD']
    if 'PROXY_PORT' in os.environ:
        config['port'] = os.environ['PROXY_PORT']
    if 'PROXY_ENDPOINTS' in os.environ:
        for vhost in os.environ['PROXY_ENDPOINTS'].split(';'):
            name, host = vhost.split(',')
            config['services'].append({'name': name, 'host': host})
    return config


def generate_nginx_config():
    config = get_config()
    try:
        shutil.rmtree(config['output_dir'])
    except:
        pass
    os.makedirs(config['output_dir'], exist_ok=True)

    for service in config['services']:
        generate_service_config(service)


def generate_service_config(service):
    config = get_config()
    path = os.path.dirname(os.path.realpath(__file__))
    template = os.path.join(path, 'service.template')
    output_config = os.path.join(config['output_dir'], service['name'] + ".conf")
    print("Generating config for service: Name: %s, TLD: %s, Host: %s, File: %s" % (service['name'], config['tld'], service['host'], output_config))
    # Wait for python 3.6 on alpine linux
    #print("Generating config for service: Name: {service['name']}, TLD: {config['tld']}, Host: {service['host']}, File: {output_config}")

    with open(template) as f:
        service_template = Template(f.read())

    with open(output_config, 'w') as f:
        f.write(service_template.render(tld=config['tld'],
                                        name=service['name'],
                                        host=service['host'],
                                        port=config['port'],))


@click.command()
@click.option("-v", "--verbose", count=True, help="Enable more logging. More -v's for more logging")
@click.option("--start", flag_value=True, help="Start nginx after creating the config files")
@click.option("--config-file", default="/config.yml", show_default=True, help="The yaml config file to read from")
@click.option("--output-dir", default="/etc/nginx/conf.d", show_default=True, help="The directory to save config files to")
def main(verbose, start, config_file, output_dir):
    log_level = logging.WARNING
    if verbose == 1:
        log_level = logging.INFO
    if verbose >= 2:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level)

    get_config(Path(config_file), output_dir)

    generate_nginx_config()

    if start:
        start_nginx()

if __name__ == "__main__":
    main()
