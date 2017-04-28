#!/usr/bin/env python3

import argparse
import os
import shutil
import subprocess
import yaml

from jinja2 import Template


def start_nginx():
    subprocess.call(['nginx'])


def get_config(config_file=False, output_dir=False):
    if not hasattr(get_config, 'config'):
        with open(config_file) as f:
            get_config.config = yaml.load(f)
        get_config.config['output_dir'] = output_dir
    return get_config.config


def generate_nginx_config(args):
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

def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--start",
                        help="Start nginx after creating the config files",
                        default=False,
                        action="store_true")
    parser.add_argument("--config-file",
                        help="The yaml config file to read from",
                        default='/config.yml',
                        action="store")
    parser.add_argument("--output-dir",
                        help="The directory to save config files to",
                        default='/etc/nginx/conf.d',
                        action="store")

    args = parser.parse_args()

    get_config(args.config_file, args.output_dir)

    generate_nginx_config(args)

    if args.start:
        start_nginx()

if __name__ == "__main__":
    main()
