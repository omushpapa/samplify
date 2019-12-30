#! /usr/bin/env python3

import ipaddress
import os
import re
from urllib.parse import urlparse

import click
from pyconfigreader import ConfigReader


email_pattern = re.compile(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$")


def is_valid_url(x):
    """Check if is a valid URl

    :param str x: A string value
    :return: True if is a valid URl, else False
    :rtype: bool
    """
    try:
        result = urlparse(x)
    except:
        return False

    return all([result.scheme, result.netloc, result.path])


def is_valid_ip(v):
    """Check if is a valid IP address

    :param str v: A string value
    :return: IP address version if valid, else 0
    :rtype: int
    """
    try:
        ip = ipaddress.ip_address(v)
    except ValueError:
        version = 0

    else:
        version = ip.version

    return version


def is_email(v):
    """Check if is resembles an email address

    :param str v: A string value
    :return: True if resembles, else False
    :rtype:bool
    """
    match = email_pattern.match(v)
    return bool(match)


def get_literal_type(value):
    """Get the data type

    :param value: The data
    :return: The data type as a string
    :rtype: str
    """
    return type(value).__name__


def get_type(data):
    """Get the data representation

    :param data: The data
    :return: A description of the data
    :rtype: str
    """
    if isinstance(data, str):
        if os.path.isabs(data):
            return 'file path'

        if is_email(data):
            return 'email address'

        if is_valid_url(data):
            return 'URL'

        ip_v = is_valid_ip(data)
        if ip_v:
            return f'IPv{ip_v} address'

    return get_literal_type(data)


class Sample:

    def __init__(self, file_, retain_case):
        self.retain_case = retain_case
        self.config = ConfigReader(file_, case_sensitive=self.retain_case)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def create(self, filename=None):
        """Create a sample file

        :param str filename: The name of the sample.
            Default to the name of the original file suffixed with `.sample`
        """
        if filename is None:
            filename = f'{self.config.filename}.sample'

        try:
            os.remove(filename)
        except FileNotFoundError:
            pass

        with ConfigReader(filename, case_sensitive=self.retain_case) as sample:
            for section in self.config.sections:
                items = self.config.get_items(section)
                for k, v in items.items():
                    value = get_type(v)
                    sample.set(k, value, section=section)

            sample.remove_section('main')
            sample.save()

    def close(self):
        """Close the original file handler"""
        self.config.close()


@click.command()
@click.argument('filename')
@click.option('--output', '-o', default='settings.ini.sample', help='Filename of sample')
@click.option('--no-retain-case', default=False, is_flag=True, help='Convert all keys to lowercase. Defaults to False')
def samplify(filename, output, no_retain_case):
    """Generate a sample configuration file from an existing one"""

    retain_case = not no_retain_case

    click.echo(f'Generating sample file {output} from {filename}')
    with Sample(filename, retain_case) as sample:
        sample.create(output)


if __name__ == "__main__":
    samplify()
