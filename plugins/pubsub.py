import logging

from google.auth import app_engine
from googleapiclient import discovery, errors

from pluginbase import Plugin

SCOPES = ['https://www.googleapis.com/auth/pubsub']

CREDENTIALS = app_engine.Credentials(scopes=SCOPES)


class CloudPubSub(Plugin):

    def __init__(self):
        Plugin.__init__(self)
        self.pubsub = discovery.build(
            'pubsub', 'v1', credentials=CREDENTIALS)
        self.batch = self.pubsub.new_batch_http_request(
            callback=self.batch_callback)

    def register_signals(self):
        logging.debug("Cloud PubSub class created and registering signals")

    def _get_topic(self, project_id, name):
        try:
            result = self.pubsub.projects().topics().get(
                name="projects/" + project_id + "/topics/" + name).execute()
        except errors.HttpError as e:
            logging.error(e)
            return None
        return result

    def get_gcp_object(self, data):
        try:
            instance = self._get_topic(
                data['resource']['labels']['project_id'],
                data['protoPayload']['request']['instanceId'])
            return instance
        except Exception as e:
            logging.error(e)
            return None

    def _get_name(self, gcp_object):
        try:
            name = gcp_object['name']
            name = name.replace(".", "_").lower()[:62]
        except KeyError as e:
            logging.error(e)
            return None
        return name

    def _get_region(self, gcp_object):
        try:
            region = gcp_object['region']
            region = region.lower()
        except KeyError as e:
            logging.error(e)
            return None
        return region