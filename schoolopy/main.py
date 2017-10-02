from .models import *
import requests
import time
import random
import json
from xml.etree.ElementTree import fromstring


class Schoology:
    key = ''
    secret = ''

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def _oauth_header(self):
        auth = 'OAuth realm="Schoology API",'
        auth += 'oauth_consumer_key="%s",' % self.key
        auth += 'oauth_token="",'
        auth += 'oauth_nonce="%s",' % ''.join([str(random.randint(0, 9)) for i in range(8)])
        auth += 'oauth_timestamp="%d",' % time.time()
        auth += 'oauth_signature_method="PLAINTEXT",'
        auth += 'oauth_version="1.0",'
        auth += 'oauth_signature="%s%%26"' % self.secret
        return auth

    def _get(self, path):
        return json.loads(requests.get('https://api.schoology.com/v1/%s' % path, headers={'Authorization': self._oauth_header()}).content.decode())

    def get_messages(self):
        return [Message(raw) for raw in self._get('messages/inbox')['message']]

    def get_schools(self):
        return [School(raw) for raw in self._get('schools')['school']]

    def get_school(self, id):
        return School(self._get('schools/%s' % id))

    def get_buildings(self, id):
        return [Building(raw) for raw in self._get('schools/%s/buildings' % id)]

    def get_users(self):
        return [User(raw) for raw in self._get('users')['user']]

    def get_user(self, id):
        return User(self._get('users/%s' % id))

    def get_groups(self):
        return [Group(raw) for raw in self._get('groups')['group']]

    def get_group(self, id):
        return Group(self._get('groups/%s' % id))

    def get_courses(self):
        return [Course(raw) for raw in self._get('courses')['course']]

    def get_course(self, id):
        return Course(self._get('courses/%s' % id))

    def get_sections(self):
        return [Section(raw) for raw in self._get('sections')['section']]

    def get_section(self, id):
        return Section(self._get('sections/%s' % id))

    def get_section_enrollments(self, id):
        return [User(raw) for raw in self._get('sections/%s/enrollments' % id)]

    def get_group_enrollments(self, id):
        return [User(raw) for raw in self._get('groups/%s/enrollments' % id)]

    # Support getting accesscode

    # TODO: Support ID at the end of enrollments path

    def get_district_events(self):
        return [Event(raw) for raw in self._get('districts/%s/events' % id)]

    def get_school_events(self):
        return [Event(raw) for raw in self._get('schools/%s/events' % id)]

    def get_user_events(self):
        return [Event(raw) for raw in self._get('users/%s/events' % id)]

    def get_section_events(self):
        return [Event(raw) for raw in self._get('sections/%s/events' % id)]

    def get_group_events(self):
        return [Event(raw) for raw in self._get('groups/%s/events' % id)]

    def get_district_event(self, district_id, event_id):
        return Event(self._get('districts/%s/events/%s' % (district_id, event_id)))

    def get_school_event(self, school_id, event_id):
        return Event(self._get('schools/%s/events/%s' % (school_id, event_id)))

    def get_user_event(self, user_id, event_id):
        return Event(self._get('users/%s/events/%s' % (user_id, event_id)))

    def get_section_event(self, section_id, event_id):
        return Event(self._get('sections/%s/events/%s' % (section_id, event_id)))

    def get_group_event(self, group_id, event_id):
        return Event(self._get('groups/%s/events/%s' % (group_id, event_id)))
