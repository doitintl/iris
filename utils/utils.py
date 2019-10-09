"""Misc utils."""
import json
import logging
import os
import uuid

from google.appengine.api import app_identity


def detect_gae():
    """Determine whether or not we're running on GAE.

    This is based on:
      https://developers.google.com/appengine/docs/python/#The_Environment

    Returns:
      True iff we're running on GAE.
    """
    server_software = os.environ.get('SERVER_SOFTWARE', '')
    return not server_software.startswith('Development/')


def _get_project_id():
    logging.info("-------------------Running Localy--------------------")
    with open('dev_config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['project']


def get_project_id():
    """
    Return the real or local project id.

    :return: project_id
    """
    if detect_gae():
        project = app_identity.get_application_id()
    else:
        project = _get_project_id()
    return project


def get_host_name():
    """
    Return the real or local hostname.

    :return: hostname
    """
    if detect_gae():
        hostname = '{}.appspot.com'.format(app_identity.get_application_id())
    else:
        hostname = '{}.appspot.com'.format(_get_project_id())
    return hostname


def fatal_code(e):
    """
    In case of a 500+ errcode do backoff.

    :param e: execption
    :return:
    """
    return e.resp.status < 500


def is_service_enbaled(service_list, service):
    if 'services' in service_list:
        for srv in service_list['services']:
            if srv['config']['name'].lower() == service.lower():
                logging.debug("Service %s was found as %s in the list",
                              service.lower(), srv['config']['name'].lower())
                return True
    return False

def get_uuid():
    uuid.uuid4()


def get_tags():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['tags']


def get_ondemand():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config['on_demand']


def project_inheriting():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    if 'project_inheriting' in config:
        return config['project_inheriting']
    else:
        return False


def get_prfeix():
    return 'iris'
