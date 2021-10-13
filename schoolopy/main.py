from .errors import NoDataError, NoDifferenceError
from .models import *
from .authentication import AuthorizationError
import time
import json

try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError


class Schoology:
    key = ''
    secret = ''
    limit = 20
    start = 0

    def __init__(self, schoology_auth, api_host='https://api.schoology.com/v1/'):
        if not schoology_auth.authorized:
            raise AuthorizationError('Auth instance not authorized. Run authorize() after requesting authorization.')
        self.key = schoology_auth.consumer_key
        self.secret = schoology_auth.consumer_secret
        self.schoology_auth = schoology_auth
        self.api_host = api_host

    def _get(self, path):
        """
        GET data from a given endpoint.

        :param path: Path (following API root) to endpoint.
        :return: JSON response.
        """
        response = self.schoology_auth.oauth.get(url='%s%s?limit=%s' % (self.api_host, path, self.limit), headers=self.schoology_auth._request_header(), auth=self.schoology_auth.oauth.auth)
        response.raise_for_status()
        try:
            return response.json()
        except JSONDecodeError:
            raise NoDataError(f'Get request to {response.url} failed: {response.text}')

    def _post(self, path, data):
        """
        POST valid JSON to a given endpoint.

        :param path: Path (following API root) to endpoint.
        :param data: JSON data to POST.
        :return: JSON response.
        """
        response = self.schoology_auth.oauth.post(url='%s%s?limit=%s' % (self.api_host, path, self.limit), json=data, headers=self.schoology_auth._request_header(), auth=self.schoology_auth.oauth.auth)
        response.raise_for_status()
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise NoDataError(f'Post request to {response.url} failed: {response.text}')

    def _put(self, path, data):
        """
        PUT valid JSON to a given endpoint.

        :param path: Path (following API root) to endpoint.
        :param data: JSON data to PUT.
        :return: JSON response.
        """
        response = self.schoology_auth.oauth.put(url='%s%s?limit=%s' % (self.api_host, path, self.limit), json=data, headers=self.schoology_auth._request_header(), auth=self.schoology_auth.oauth.auth)
        response.raise_for_status()
        try:
            return response.json()
        except json.decoder.JSONDecodeError:
            raise NoDataError(f'Put request to {response.url} failed: {response.text}')

    def _delete(self, path):
        """
        Send a DELETE request to a given endpoint.

        :param path: Path (following API root) to endpoint.
        """
        response = self.schoology_auth.oauth.delete(url='%s%s' % (self.api_host, path), headers=self.schoology_auth._request_header(), auth=self.schoology_auth.oauth.auth)
        response.raise_for_status()
        return response

    def get_schools(self):
        """
        Get data on all schools.

        :return: List of school objects of which a user is aware.
        """
        return [School(raw) for raw in self._get('schools')['school']]

    def get_school(self, school_id):
        """
        Get data on a school.

        :return: School object with data on the requested school.
        """
        return School(self._get('schools/%s' % school_id))

    def create_school(self, school):
        """
        Create a new school.

        :param school: School object containing necessary fields.
        :return: School object obtained from API.
        """
        return School(self._post('schools', school.json()))

    def edit_school(self, school_id, school):
        """
        Edit a school.

        :param school_id: ID of school to edit.
        :param school: School object containing necessary fields.
        :return: School object obtained from API.
        """
        # TODO: Does this endpoint return anything?
        self._put('schools/%s' % school_id, school.json())

    def get_buildings(self, school_id):
        """
        Get data on buildings in a given school.

        :param school_id: ID of school whose buildings to get.
        :return: List of building objects in that school.
        """
        return [Building(raw) for raw in self._get('schools/%s/buildings' % school_id)]

    # There is currently no endpoint for getting data on individual buildings.
    # This is due in part to the oft-blurred line Schoology draws between schools and buildings.

    def create_building(self, school_id, building):
        """
        Create a new building.

        :param building: Building object containing necessary fields.
        :return: Building object obtained from API.
        """
        return Building(self._post('schools/%s/buildings' % school_id, building.json()))

    def get_self_user_info(self):
        """
        Gets user info for yourself, if you have a current Schoology sessions

        :return: Session object obtained from API.
        """
        return Session(self._get('app-user-info'))

    def get_me(self):
        """
        Get data of the client using this method (Yourself).

        :return: User object obtained from API. (Of yourself)
        """
        return User(self._get('users/me'))

    def get_users(self, inactive=False):
        """
        Get data on all users.

        :param inactive: Gets inactive users instead of normal ones.
        :return: List of User objects.
        """
        return [User(raw) for raw in self._get('users' + ('/inactive' if inactive else ''))['user']]

    def get_user(self, user_id, inactive=False):
        """
        Get data on a user.

        :param user_id: ID of user to get data from.
        :param inactive: Gets inactive users instead of normal ones.
        :return: User object.
        """
        return User(self._get(('users/' + ('inactive/' if inactive else '') + '%s') % user_id))

    def create_user(self, user):
        """
        Create a new user.

        :param user: User object containing necessary fields.
        :return: User object obtained from API.
        """
        return User(self._post('users', user))

    def create_users(self, users):
        """
        Bulk create users.

        :param users: A list of User objects.
        :return: User objects obtained from API.
        """
        return [User(raw) for raw in self._post('users', {'users': {'user': [user.json() for user in users]}})]

    def update_user(self, user, user_id):
        """
        Update an existing user.

        :param user: User object containing necessary fields.
        :param user_id: ID of user you wish to update.
        :return: User object obtained from API.
        """
        self._put('users/%s' % user_id, user)

    def update_users(self, users):
        """
        Bulk update users.

        :param users: A list of users.
        :return: User objects obtained from API.
        """
        return [User(raw) for raw in self._put('users', {'users': {'user': [user.json() for user in users]}})]

    def delete_user(self, user_id):
        """
        Delete a user.

        :param user_id: ID of user you wish to delete.
        """
        self._delete('users/%s' % user_id)

    def get_languages(self):
        """
        Get data on all supported languages.

        :return: A list of Language objects.
        """
        return [Language(raw) for raw in self._get('users/languages')['language']]

    def get_groups(self):
        """
        Get data on all groups.

        :return: List of Group objects.
        """
        return [Group(raw) for raw in self._get('groups')['group']]

    def get_group(self, group_id):
        """
        Get data on a group.

        :param group_id: ID of group on which to get data.
        :return: Group object.
        """
        return Group(self._get('groups/%s' % group_id))

    def get_courses(self):
        """
        Get data on all courses.

        :return: List of Course objects.
        """
        return [Course(raw) for raw in self._get('courses')['course']]

    def get_course(self, course_id):
        """
        Get data on a course.

        :param course_id: ID of course on which to get data.
        :return: Course object.
        """
        return Course(self._get('courses/%s' % course_id))

    def get_sections(self, course_id):
        """
        Get data on all sections.

        :return: List of Section objects.
        """
        return [Section(raw) for raw in self._get('courses/%s/sections' % course_id)['section']]

    def get_section(self, section_id):
        """
        Get data on a section.

        :param section_id: ID of section on which to get data.
        :return: Section object.
        """
        return Section(self._get('sections/%s' % section_id))


    def create_enrollment(self, enrollment, section_id=None, group_id=None):
        """
        Helper function for creating an enrollment in any realm.

        :param enrollment: Enrollment object to post to API.
        :param *_id: ID of realm.
        :return: Enrollment object recieved from API.
        """
        if section_id:
            return self.create_section_enrollment(enrollment, section_id)
        elif group_id:
            return self.create_group_enrollment(enrollment, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_section_enrollment(self, enrollment, section_id):
        return Enrollment(self._post('sections/%s/enrollments' % section_id, enrollment.json()))

    def create_group_enrollment(self, enrollment, group_id):
        return Enrollment(self._post('groups/%s/enrollments' % group_id, enrollment.json()))


    def get_enrollments(self, section_id=None, group_id=None):
        """
        Helper function to get enrollments in any realm. Realm will be decided based on named parameters passed.

        :param *_id: ID of realm.
        :return: List of User objects.
        """
        if section_id:
            return self.get_section_enrollments(section_id)
        elif group_id:
            return self.get_group_enrollments(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_section_enrollments(self, section_id):
        return [Enrollment(raw) for raw in self._get('sections/%s/enrollments' % section_id)['enrollment']]

    def get_group_enrollments(self, group_id):
        return [Enrollment(raw) for raw in self._get('groups/%s/enrollments' % group_id)['enrollment']]


    # TODO: Do we need to provide the ID of the realm?
    def join_section(self, access_code):
        return Enrollment(self._post('sections/accesscode' % access_code, {'access_code': access_code}))

    def join_group(self, access_code):
        return Enrollment(self._post('sections/accesscode' % access_code, {'access_code': access_code}))


    def create_enrollments(self, enrollments, section_id=None, group_id=None):
        """
        Create multiple enrollments.

        :param enrollments: List of Enrollment objects to post to API.
        :param *_id: ID of realm.
        :return: List of User objects.
        """
        if section_id:
            return self.create_section_enrollments(enrollments, section_id)
        elif group_id:
            return self.create_group_enrollments(enrollments, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_section_enrollments(self, enrollments, section_id):
        return [Enrollment(raw) for raw in self._post('sections/%s/enrollments' % section_id, {'enrollments': {'enrollment': [enrollment.json() for enrollment in enrollments]}})]

    def create_group_enrollments(self, enrollments, group_id):
        return [Enrollment(raw) for raw in self._post('groups/%s/enrollments' % group_id, {'enrollments': {'enrollment': [enrollment.json() for enrollment in enrollments]}})]

    def update_enrollment(self, enrollment, group_id=None, section_id=None):
        """
        Helper function for updating an enrollment.

        Either group_id or section_id must be specified by name in calls to this method.

        :param enrollment: Enrollment object containing new data.
        :param *_id: ID of realm.
        :return: List of Enrollment objects recieved from API.
        """
        if section_id:
            return self.update_section_enrollment(section_id, enrollment)
        elif group_id:
            return self.update_group_enrollment(group_id, enrollment)
        else:
            raise TypeError('Realm id property required.')

    def update_section_enrollment(self, enrollment, section_id):
        return self.update_section_enrollments(section_id, [enrollment])

    def update_group_enrollment(self, enrollment, group_id):
        return self.update_group_enrollments(group_id, [enrollment])

    def update_section_enrollments(self, enrollments, section_id):
        return [Enrollment(raw) for raw in self._put('sections/%s/enrollments' % section_id, {'enrollments': {'enrollment': [enrollment.json() for enrollment in enrollments]}})]

    def update_group_enrollments(self, enrollments, group_id):
        return [Enrollment(raw) for raw in self._put('groups/%s/enrollments' % group_id, {'enrollments': {'enrollment': [enrollment.json() for enrollment in enrollments]}})]

    def delete_enrollment(self, enrollment_id, section_id=None, group_id=None):
        """
        Delete an enrollment in any realm.

        Either group_id or section_id must be specified by name in calls to this method.

        :param enrollment_id: ID of enrollment to delete.
        :param *_id: ID of realm.
        """
        if section_id:
            return self.delete_section_enrollment(section_id, enrollment_id)
        elif group_id:
            return self.delete_group_enrollment(group_id, enrollment_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_section_enrollment(self, enrollment_id, section_id):
        self._delete('sections/%s/enrollments/%s' % (section_id, enrollment_id))

    def delete_group_enrollment(self, enrollment_id, group_id):
        self._delete('groups/%s/enrollments/%s' % (group_id, enrollment_id))


    def delete_enrollments(self, enrollment_ids):
        self._delete('enrollments?enrollment_ids=' + ','.join(enrollment_ids))

    # Course enrollments imports not implemented, similar effect can be obtained through extant methods

    def get_events(self, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get data on events in any realm.

        :param *_id: ID of realm.
        :return: List of Event objects.
        """
        if district_id:
            return self.get_district_events(district_id)
        elif school_id:
            return self.get_school_events(school_id)
        elif user_id:
            return self.get_user_events(user_id)
        elif section_id:
            return self.get_section_events(section_id)
        elif group_id:
            return self.get_group_events(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_events(self, district_id):
        return [Event(raw) for raw in self._get('districts/%s/events' % district_id)['event']]

    def get_school_events(self, school_id):
        return [Event(raw) for raw in self._get('schools/%s/events' % school_id)['event']]

    def get_user_events(self, user_id):
        return [Event(raw) for raw in self._get('users/%s/events' % user_id)['event']]

    def get_section_events(self, section_id):
        return [Event(raw) for raw in self._get('sections/%s/events' % section_id)['event']]

    def get_group_events(self, group_id):
        return [Event(raw) for raw in self._get('groups/%s/events' % group_id)['event']]


    def create_event(self, event, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating a new event in any realm.

        :param event: Event object.
        :param *_id: ID of realm.
        :return: Event object from API.
        """
        if district_id:
            return self.create_district_event(event, district_id)
        elif school_id:
            return self.create_school_event(event, school_id)
        elif user_id:
            return self.create_user_event(event, user_id)
        elif section_id:
            return self.create_section_event(event, section_id)
        elif group_id:
            return self.create_group_event(event, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_district_event(self, event, district_id):
        return Event(self._post('districts/%s/events' % district_id, event.json()))

    def create_school_event(self, event, school_id):
        return Event(self._post('schools/%s/events' % school_id, event.json()))

    def create_user_event(self, event, user_id):
        return Event(self._post('users/%s/events' % user_id, event.json()))

    def create_section_event(self, event, section_id):
        return Event(self._post('sections/%s/events' % section_id, event.json()))

    def create_group_event(self, event, group_id):
        return Event(self._post('groups/%s/events' % group_id, event.json()))


    def get_event(self, event_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get data on an event in any realm.

        :param event_id: ID of event on which to get data.
        :param *_id: ID of realm.
        :return: Event object.
        """
        if district_id:
            return self.get_district_event(event_id, district_id)
        elif school_id:
            return self.get_school_event(event_id, school_id)
        elif user_id:
            return self.get_user_event(event_id, user_id)
        elif section_id:
            return self.get_section_event(event_id, section_id)
        elif group_id:
            return self.get_group_event(event_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_event(self, event_id, district_id):
        return Event(self._get('districts/%s/events/%s' % (district_id, event_id)))

    def get_school_event(self, event_id, school_id):
        return Event(self._get('schools/%s/events/%s' % (school_id, event_id)))

    def get_user_event(self, event_id, user_id):
        return Event(self._get('users/%s/events/%s' % (user_id, event_id)))

    def get_section_event(self, event_id, section_id):
        return Event(self._get('sections/%s/events/%s' % (section_id, event_id)))

    def get_group_event(self, event_id, group_id):
        return Event(self._get('groups/%s/events/%s' % (group_id, event_id)))

    def update_event(self, event, event_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for updating individual events in any realm.

        :param event_id: ID of event on which to get data.
        :param *_id: ID of realm.
        """
        if district_id:
            self.update_district_event(event, event_id, district_id)
        elif school_id:
            self.update_school_event(event, event_id, school_id)
        elif user_id:
            self.update_user_event(event, event_id, user_id)
        elif section_id:
            self.update_section_event(event, event_id, section_id)
        elif group_id:
            self.update_group_event(event, event_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def update_district_event(self, event, event_id, district_id):
        self._put('districts/%s/events/%s' % (district_id, event.id), event.json())

    def update_school_event(self, event, event_id, school_id):
        self._put('schools/%s/events/%s' % (school_id, event.id), event.json())

    def update_user_event(self, event, event_id, user_id):
        self._put('users/%s/events/%s' % (user_id, event.id), event.json())

    def update_section_event(self, event, event_id, section_id):
        self._put('sections/%s/events/%s' % (section_id, event.id), event.json())

    def update_group_event(self, event, event_id, group_id):
        self._put('groups/%s/events/%s' % (group_id, event.id), event.json())


    def delete_event(self, event_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Delete an event in any realm.

        :param event_id: ID of event to delete.
        :param *_id: ID of realm.
        """
        if district_id:
            self.delete_district_event(event_id, district_id)
        elif school_id:
            self.delete_school_event(event_id, school_id)
        elif user_id:
            self.delete_user_event(event_id, user_id)
        elif section_id:
            self.delete_section_event(event_id, section_id)
        elif group_id:
            self.delete_group_event(event_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_district_event(self, event_id, district_id):
        self._delete('districts/%s/events/%s' % (district_id, event_id))

    def delete_school_event(self, event_id, school_id):
        self._delete('schools/%s/events/%s' % (school_id, event_id))

    def delete_user_event(self, event_id, user_id):
        self._delete('users/%s/events/%s' % (user_id, event_id))

    def delete_section_event(self, event_id, section_id):
        self._delete('sections/%s/events/%s' % (section_id, event_id))

    def delete_group_event(self, event_id, group_id):
        self._delete('groups/%s/events/%s' % (group_id, event_id))


    def create_blog_post(self, post, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating a blog post in any realm.

        :param post: BlogPost object to post in the given realm.
        :param *_id: ID of realm.
        :return: BlogPost object recieved from API.
        """
        if district_id:
            return self.create_district_blog_post(post, district_id)
        elif school_id:
            return self.create_school_blog_post(post, school_id)
        elif user_id:
            return self.create_user_blog_post(post, user_id)
        elif section_id:
            return self.create_section_blog_post(post, section_id)
        elif group_id:
            return self.create_group_blog_post(post, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_district_blog_post(self, post, district_id):
        return BlogPost(self._post('districts/%s/posts' % district_id, post.json()))

    def create_school_blog_post(self, post, school_id):
        return BlogPost(self._post('schools/%s/posts' % school_id, post.json()))

    def create_user_blog_post(self, post, user_id):
        return BlogPost(self._post('users/%s/posts' % user_id, post.json()))

    def create_section_blog_post(self, post, section_id):
        return BlogPost(self._post('sections/%s/posts' % section_id, post.json()))

    def create_group_blog_post(self, post, group_id):
        return BlogPost(self._post('groups/%s/posts' % group_id, post.json()))


    def get_blog_posts(self, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating blog posts in any realm.

        :param *_id: ID of realm.
        :return: List of BlogPost objects recieved from API.
        """
        if district_id:
            return self.get_district_blog_posts(district_id)
        elif school_id:
            return self.get_school_blog_posts(school_id)
        elif user_id:
            return self.get_user_blog_posts(user_id)
        elif section_id:
            return self.get_section_blog_posts(section_id)
        elif group_id:
            return self.get_group_blog_posts(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_blog_posts(self, district_id):
        return [BlogPost(raw) for raw in self._get('districts/%s/posts' % district_id)['post']]

    def get_school_blog_posts(self, school_id):
        return [BlogPost(raw) for raw in self._get('schools/%s/posts' % school_id)['post']]

    def get_user_blog_posts(self, user_id):
        return [BlogPost(raw) for raw in self._get('users/%s/posts' % user_id)['post']]

    def get_section_blog_posts(self, section_id):
        return [BlogPost(raw) for raw in self._get('sections/%s/posts' % section_id)['post']]

    def get_group_blog_posts(self, group_id):
        return [BlogPost(raw) for raw in self._get('groups/%s/posts' % group_id)['post']]


    def get_blog_post(self, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get data on a blog post in any realm.

        :param *_id: ID of realm.
        :return: List of BlogPost objects recieved from API.
        """
        if district_id:
            return self.get_district_blog_post(post_id, district_id)
        elif school_id:
            return self.get_school_blog_post(post_id, school_id)
        elif user_id:
            return self.get_user_blog_post(post_id, user_id)
        elif section_id:
            return self.get_section_blog_post(post_id, section_id)
        elif group_id:
            return self.get_group_blog_post(post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_blog_post(self, post_id, district_id):
        return BlogPost(self._get('districts/%s/posts/%s' % (district_id, post_id)))

    def get_school_blog_post(self, post_id, school_id):
        return BlogPost(self._get('schools/%s/posts/%s' % (school_id, post_id)))

    def get_user_blog_post(self, post_id, user_id):
        return BlogPost(self._get('users/%s/posts/%s' % (user_id, post_id)))

    def get_section_blog_post(self, post_id, section_id):
        return BlogPost(self._get('sections/%s/posts/%s' % (section_id, post_id)))

    def get_group_blog_post(self, post_id, group_id):
        return BlogPost(self._get('groups/%s/posts/%s' % (group_id, post_id)))


    def update_blog_post(self, post, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating blog posts in any realm.

        :param *_id: ID of realm.
        :return: List of BlogPost objects recieved from API.
        """
        if district_id:
            self.update_district_blog_post(post, district_id)
        elif school_id:
            self.update_school_blog_post(post, school_id)
        elif user_id:
            self.update_user_blog_post(post, user_id)
        elif section_id:
            self.update_section_blog_post(post, section_id)
        elif group_id:
            self.update_group_blog_post(post, group_id)
        else:
            raise TypeError('Realm id property required.')

    def update_district_blog_post(self, post, district_id):
        self._put('districts/%s/posts/%s' % (district_id, post.id), post.json())

    def update_school_blog_post(self, post, school_id):
        self._put('schools/%s/posts/%s' % (school_id, post.id), post.json())

    def update_user_blog_post(self, post, user_id):
        self._put('users/%s/posts/%s' % (user_id, post.id), post.json())

    def update_section_blog_post(self, post, section_id):
        self._put('sections/%s/posts/%s' % (section_id, post.id), post.json())

    def update_group_blog_post(self, post, group_id):
        self._put('groups/%s/posts/%s' % (group_id, post.id), post.json())


    def delete_blog_post(self, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Delete blog posts in any realm.

        :param *_id: ID of realm.
        """
        if district_id:
            self.delete_district_blog_post(post_id, district_id)
        elif school_id:
            self.delete_school_blog_post(post_id, school_id)
        elif user_id:
            self.delete_user_blog_post(post_id, user_id)
        elif section_id:
            self.delete_section_blog_post(post_id, section_id)
        elif group_id:
            self.delete_group_blog_post(post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_district_blog_post(self, post_id, district_id):
        self._delete('districts/%s/posts/%s' % (district_id, post_id))

    def delete_school_blog_post(self, post_id, school_id):
        self._delete('schools/%s/posts/%s' % (school_id, post_id))

    def delete_user_blog_post(self, post_id, user_id):
        self._delete('users/%s/posts/%s' % (user_id, post_id))

    def delete_section_blog_post(self, post_id, section_id):
        self._delete('sections/%s/posts/%s' % (section_id, post_id))

    def delete_group_blog_post(self, post_id, group_id):
        self._delete('groups/%s/posts/%s' % (group_id, post_id))


    def create_blog_post_comment(self, comment, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating blog posts in any realm.

        :param post: BlogPost object to post in the given realm.
        :param *_id: ID of realm.
        :return: BlogPostComment object recieved from API.
        """
        if district_id:
            return self.create_district_blog_post_comment(comment, post_id, district_id)
        elif school_id:
            return self.create_district_blog_post_comment(comment, post_id, school_id)
        elif user_id:
            return self.create_district_blog_post_comment(comment, post_id, user_id)
        elif section_id:
            return self.create_district_blog_post_comment(comment, post_id, section_id)
        elif group_id:
            return self.create_district_blog_post_comment(comment, post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_district_blog_post_comment(self, comment, post_id, district_id):
        return BlogPostComment(self._post('districts/%s/posts/%s/comments' % (district_id, post_id), comment.json()))

    def create_school_blog_post_comment(self, comment, post_id, school_id):
        return BlogPostComment(self._post('schools/%s/posts/%s/comments' % (school_id, post_id), comment.json()))

    def create_user_blog_post_comment(self, comment, post_id, user_id):
        return BlogPostComment(self._post('users/%s/posts/%s/comments' % (user_id, post_id), comment.json()))

    def create_section_blog_post_comment(self, comment, post_id, section_id):
        return BlogPostComment(self._post('sections/%s/posts/%s/comments' % (section_id, post_id), comment.json()))

    def create_group_blog_post_comment(self, comment, post_id, group_id):
        return BlogPostComment(self._post('groups/%s/posts/%s/comments' % (group_id, post_id), comment.json()))


    def get_blog_post_comments(self, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get data on blog post comments in any realm.

        :param *_id: ID of realm.
        :return: List of BlogPostComment objects recieved from API.
        """
        if district_id:
            return self.get_district_blog_post_comments(post_id, district_id)
        elif school_id:
            return self.get_school_blog_post_comments(post_id, school_id)
        elif user_id:
            return self.get_user_blog_post_comments(post_id, user_id)
        elif section_id:
            return self.get_section_blog_post_comments(post_id, section_id)
        elif group_id:
            return self.get_group_blog_post_comments(post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_blog_post_comments(self, post_id, district_id):
        return [BlogPostComment(raw) for raw in self._get('districts/%s/posts/%s/comments' % (district_id, post_id))['comment']]

    def get_school_blog_post_comments(self, post_id, school_id):
        return [BlogPostComment(raw) for raw in self._get('schools/%s/posts/%s/comments' % (school_id, post_id))['comment']]

    def get_user_blog_post_comments(self, post_id, user_id):
        return [BlogPostComment(raw) for raw in self._get('users/%s/posts/%s/comments' % (user_id, post_id))['comment']]

    def get_section_blog_post_comments(self, post_id, section_id):
        return [BlogPostComment(raw) for raw in self._get('sections/%s/posts/%s/comments' % (section_id, post_id))['comment']]

    def get_group_blog_post_comments(self, post_id, group_id):
        return [BlogPostComment(raw) for raw in self._get('groups/%s/posts/%s/comments' % (group_id, post_id))['comment']]


    def get_blog_post_comment(self, comment_id, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get data on individual blog post comments in any realm.

        :param comment_id: ID of the comment to fetch.
        :param post_id: ID of the post on which the comment is written.
        :param *_id: ID of realm.
        :return: List of BlogPostComment objects recieved from API.
        """
        if district_id:
            return self.get_district_blog_post_comment(comment_id, post_id, district_id)
        elif school_id:
            return self.get_school_blog_post_comment(comment_id, post_id, school_id)
        elif user_id:
            return self.get_user_blog_post_comment(comment_id, post_id, user_id)
        elif section_id:
            return self.get_section_blog_post_comment(comment_id, post_id, section_id)
        elif group_id:
            return self.get_group_blog_post_comment(comment_id, post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_blog_post_comment(self, comment_id, post_id, district_id):
        return BlogPostComment(self._get('districts/%s/posts/%s/comments/%s' % (district_id, post_id, comment_id)))

    def get_school_blog_post_comment(self, comment_id, post_id, school_id):
        return BlogPostComment(self._get('schools/%s/posts/%s/comments/%s' % (school_id, post_id, comment_id)))

    def get_user_blog_post_comment(self, comment_id, post_id, user_id):
        return BlogPostComment(self._get('users/%s/posts/%s/comments/%s' % (user_id, post_id, comment_id)))

    def get_section_blog_post_comment(self, comment_id, post_id, section_id):
        return BlogPostComment(self._get('sections/%s/posts/%s/comments/%s' % (section_id, post_id, comment_id)))

    def get_group_blog_post_comment(self, comment_id, post_id, group_id):
        return BlogPostComment(self._get('groups/%s/posts/%s/comments/%s' % (group_id, post_id, comment_id)))


    def delete_blog_post_comment(self, comment_id, post_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Delete blog post comments in any realm.

        :param comment_id: ID of comment to delete.
        :param post_id: ID of the post on which the comment is written.
        :param *_id: ID of realm.
        """
        if district_id:
            self.delete_district_blog_post_comment(comment_id, post_id, district_id)
        elif school_id:
            self.delete_school_blog_post_comment(comment_id, post_id, school_id)
        elif user_id:
            self.delete_user_blog_post_comment(comment_id, post_id, user_id)
        elif section_id:
            self.delete_section_blog_post_comment(comment_id, post_id, section_id)
        elif group_id:
            self.delete_group_blog_post_comment(comment_id, post_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_district_blog_post_comment(self, comment_id, post_id, district_id):
        self._delete('districts/%s/posts/%s/comments/%s' % (district_id, post_id, comment_id))

    def delete_school_blog_post_comment(self, comment_id, post_id, school_id):
        self._delete('schools/%s/posts/%s/comments/%s' % (school_id, post_id, comment_id))

    def delete_user_blog_post_comment(self, comment_id, post_id, user_id):
        self._delete('users/%s/posts/%s/comments/%s' % (user_id, post_id, comment_id))

    def delete_section_blog_post_comment(self, comment_id, post_id, section_id):
        self._delete('sections/%s/posts/%s/comments/%s' % (section_id, post_id, comment_id))

    def delete_group_blog_post_comment(self, comment_id, post_id, group_id):
        self._delete('groups/%s/posts/%s/comments/%s' % (group_id, post_id, comment_id))


    def get_discussions(self, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Get data on all discussions in any realm.

        :param *_id: ID of realm.
        :return: List of BlogPostComment objects recieved from API.
        """
        if district_id:
            return self.get_district_discussions(district_id)
        elif school_id:
            return self.get_school_discussions(school_id)
        elif section_id:
            return self.get_section_discussions(section_id)
        elif group_id:
            return self.get_group_discussions(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_discussions(self, district_id):
        return [Discussion(raw) for raw in self._get('districts/%s/discussions' % district_id)['discussion']]

    def get_school_discussions(self, school_id):
        return [Discussion(raw) for raw in self._get('schools/%s/discussions' % school_id)['discussion']]

    def get_section_discussions(self, section_id):
        return [Discussion(raw) for raw in self._get('sections/%s/discussions' % section_id)['discussion']]

    def get_group_discussions(self, group_id):
        return [Discussion(raw) for raw in self._get('groups/%s/discussions' % group_id)['discussion']]


    def create_discussion(self, discussion, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Helper function for creating a discussion in any realm.

        :param discussion: Discussion object to post.
        :param *_id: ID of realm.
        :return: Discussion object recieved from API.
        """
        if district_id:
            return self.create_district_discussion(discussion, district_id)
        elif school_id:
            return self.create_school_discussion(discussion, school_id)
        elif section_id:
            return self.create_section_discussion(discussion, section_id)
        elif group_id:
            return self.create_group_discussion(discussion, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_district_discussion(self, discussion, district_id):
        return Discussion(self._post('districts/%s/discussions/%s' % (district_id, discussion.id), discussion.json()))

    def create_school_discussion(self, discussion, school_id):
        return Discussion(self._post('schools/%s/discussions/%s' % (school_id, discussion.id), discussion.json()))

    def create_section_discussion(self, discussion, section_id):
        return Discussion(self._post('sections/%s/discussions/%s' % (section_id, discussion.id), discussion.json()))

    def create_group_discussion(self, discussion, group_id):
        return Discussion(self._post('groups/%s/discussions/%s' % (group_id, discussion.id), discussion.json()))


    def get_discussion(self, discussion_id, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Get data on individual discussion in any realm.

        :param discussion_id: ID of the discussion on which to get data.
        :param *_id: ID of realm.
        :return: Discussion object recieved from API.
        """
        if district_id:
            return self.get_district_discussion(discussion_id, district_id)
        elif school_id:
            return self.get_school_discussion(discussion_id, school_id)
        elif section_id:
            return self.get_section_discussion(discussion_id, section_id)
        elif group_id:
            return self.get_group_discussion(discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_discussion(self, discussion_id, district_id):
        return Discussion(self._get('districts/%s/discussions/%s' % (district_id, discussion_id)))

    def get_school_discussion(self, discussion_id, school_id):
        return Discussion(self._get('schools/%s/discussions/%s' % (school_id, discussion_id)))

    def get_section_discussion(self, discussion_id, section_id):
        return Discussion(self._get('sections/%s/discussions/%s' % (section_id, discussion_id)))

    def get_group_discussion(self, discussion_id, group_id):
        return Discussion(self._get('groups/%s/discussions/%s' % (group_id, discussion_id)))


    def delete_discussion(self, discussion_id, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Delete discussions in any realm.

        :param comment_id: ID of the comment to delete.
        :param post_id: ID of the post on which the comment is written.
        :param *_id: ID of realm.
        """
        if district_id:
            self.delete_district_discussion(discussion_id, district_id)
        elif school_id:
            self.delete_school_discussion(discussion_id, school_id)
        elif section_id:
            self.delete_section_discussion(discussion_id, section_id)
        elif group_id:
            self.delete_group_discussion(discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_district_discussion(self, discussion_id, district_id):
        self._delete('districts/%s/discussions/%s' % (district_id, discussion_id))

    def delete_school_discussion(self, discussion_id, school_id):
        self._delete('schools/%s/discussions/%s' % (school_id, discussion_id))

    def delete_section_discussion(self, discussion_id, section_id):
        self._delete('sections/%s/discussions/%s' % (section_id, discussion_id))

    def delete_group_discussion(self, discussion_id, group_id):
        self._delete('groups/%s/discussions/%s' % (group_id, discussion_id))


    def create_discussion_reply(self, reply, discussion_id, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Helper function for creating discussion replies in any realm.

        :param reply: DiscussionReply object to post on the discussion with the given ID.
        :param *_id: ID of realm.
        :return: BlogPost object recieved from API.
        """
        if district_id:
            return self.create_district_discussion_reply(reply, discussion_id, district_id)
        elif school_id:
            return self.create_school_discussion_reply(reply, discussion_id, school_id)
        elif section_id:
            return self.create_section_discussion_reply(reply, discussion_id, section_id)
        elif group_id:
            return self.create_group_discussion_reply(reply, discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_district_discussion_reply(self, reply, discussion_id, district_id):
        return DiscussionReply(self._post('districts/%s/discussions/%s/comments' % (district_id, discussion_id), reply))

    def create_school_discussion_reply(self, reply, discussion_id, school_id):
        return DiscussionReply(self._post('schools/%s/discussions/%s/comments' % (school_id, discussion_id), reply))

    def create_section_discussion_reply(self, reply, discussion_id, section_id):
        return DiscussionReply(self._post('sections/%s/discussions/%s/comments' % (section_id, discussion_id), reply))

    def create_group_discussion_reply(self, reply, discussion_id, group_id):
        return DiscussionReply(self._post('groups/%s/discussions/%s/comments' % (group_id, discussion_id), reply))


    def get_discussion_replies(self, discussion_id, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Get data on discussion replies in any realm.

        :param reply: DiscussionReply object to post on the discussion with the given ID.
        :param *_id: ID of realm.
        :return: List of DiscussionReply objects recieved from API.
        """
        if district_id:
            return self.get_district_discussion_replies(discussion_id, district_id)
        elif school_id:
            return self.get_school_discussion_replies(discussion_id, school_id)
        elif section_id:
            return self.get_section_discussion_replies(discussion_id, section_id)
        elif group_id:
            return self.get_group_discussion_replies(discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_discussion_replies(self, discussion_id, district_id):
        return [DiscussionReply(raw) for raw in self._get('districts/%s/discussions/%s/comments' % (district_id, discussion_id))['comment']]

    def get_school_discussion_replies(self, discussion_id, school_id):
        return [DiscussionReply(raw) for raw in self._get('schools/%s/discussions/%s/comments' % (school_id, discussion_id))['comment']]

    def get_section_discussion_replies(self, discussion_id, section_id):
        return [DiscussionReply(raw) for raw in self._get('sections/%s/discussions/%s/comments' % (section_id, discussion_id))['comment']]

    def get_group_discussion_replies(self, discussion_id, group_id):
        return [DiscussionReply(raw) for raw in self._get('groups/%s/discussions/%s/comments' % (group_id, discussion_id))['comment']]


    def get_discussion_reply(self, reply_id, discussion_id, district_id=None, school_id=None, user_id=None, section_id=None, group_id=None):
        """
        Get individual discussion replies in any realm.

        :param comment_id: ID of the reply to get.
        :param discussion_id: ID of the discussion on which the reply is written.
        :param *_id: ID of realm.
        """
        if district_id:
            return self.get_district_discussion_reply(reply_id, discussion_id, district_id)
        elif school_id:
            return self.get_school_discussion_reply(reply_id, discussion_id, school_id)
        elif user_id:
            return self.get_user_discussion_reply(reply_id, discussion_id, user_id)
        elif section_id:
            return self.get_section_discussion_reply(reply_id, discussion_id, section_id)
        elif group_id:
            return self.get_group_discussion_reply(reply_id, discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_district_discussion_reply(self, reply_id, discussion_id, district_id):
        return DiscussionReply(self._get('districts/%s/discussions/%s/comments/%s' % (district_id, discussion_id, reply_id)))

    def get_school_discussion_reply(self, reply_id, discussion_id, school_id):
        return DiscussionReply(self._get('schools/%s/discussions/%s/comments/%s' % (school_id, discussion_id, reply_id)))

    def get_user_discussion_reply(self, reply_id, discussion_id, user_id):
        return DiscussionReply(self._get('schools/%s/discussions/%s/comments/%s' % (user_id, discussion_id, reply_id)))

    def get_section_discussion_reply(self, reply_id, discussion_id, section_id):
        return DiscussionReply(self._get('sections/%s/discussions/%s/comments/%s' % (section_id, discussion_id, reply_id)))

    def get_group_discussion_reply(self, reply_id, discussion_id, group_id):
        return DiscussionReply(self._get('groups/%s/discussions/%s/comments/%s' % (group_id, discussion_id, reply_id)))


    def delete_discussion_reply(self, reply_id, discussion_id, district_id=None, school_id=None, section_id=None, group_id=None):
        """
        Delete blog post comments in any realm.

        :param comment_id: ID of the comment to delete.
        :param post_id: ID of the post on which the comment is written.
        :param *_id: ID of realm.
        """
        if district_id:
            self.delete_district_discussion_reply(reply_id, discussion_id, district_id)
        elif school_id:
            self.delete_school_discussion_reply(reply_id, discussion_id, school_id)
        elif section_id:
            self.delete_section_discussion_reply(reply_id, discussion_id, section_id)
        elif group_id:
            self.delete_group_discussion_reply(reply_id, discussion_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_district_discussion_reply(self, reply_id, discussion_id, district_id):
        self._delete('districts/%s/discussions/%s/comments/%s' % (district_id, discussion_id, reply_id))

    def delete_school_discussion_reply(self, reply_id, discussion_id, school_id):
        self._delete('schools/%s/discussions/%s/comments/%s' % (school_id, discussion_id, reply_id))

    def delete_section_discussion_reply(self, reply_id, discussion_id, section_id):
        self._delete('sections/%s/discussions/%s/comments/%s' % (section_id, discussion_id, reply_id))

    def delete_group_discussion_reply(self, reply_id, discussion_id, group_id):
        self._delete('groups/%s/discussions/%s/comments/%s' % (group_id, discussion_id, reply_id))


    def create_update(self, update, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating an update in any realm.

        :param update: Update object to post.
        :param *_id: ID of realm.
        """
        if user_id:
            self.create_user_update(update, user_id)
        elif section_id:
            self.create_section_update(update, section_id)
        elif group_id:
            self.create_group_update(update, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_user_update(self, update, user_id):
        return Update(self._post('users/%s/updates' % user_id, update.json()))

    def create_section_update(self, update, section_id):
        return Update(self._post('sections/%s/updates' % section_id, update.json()))

    def create_group_update(self, update, group_id):
        return Update(self._post('groups/%s/updates' % group_id, update.json()))


    def get_updates(self, user_id=None, section_id=None, group_id=None):
        """
        Get updates in any realm.

        :param *_id: ID of realm.
        """
        if user_id:
            self.get_user_updates(user_id)
        elif section_id:
            self.get_section_updates(section_id)
        elif group_id:
            self.get_group_updates(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_user_updates(self, user_id):
        return [Update(raw) for raw in self._get('users/%s/updates' % user_id)['update']]

    def get_section_updates(self, section_id):
        return [Update(raw) for raw in self._get('sections/%s/updates' % section_id)['update']]

    def get_group_updates(self, group_id):
        return [Update(raw) for raw in self._get('groups/%s/updates' % group_id)['update']]


    def get_feed(self):
        """
        Get update feed for the current user.

        Use this function to see what's on the user's home feed.
        Theoretically, users/[user ID]/updates could be used as an alternative to this.

        :return: List of recent updates.
        """
        return [Update(raw) for raw in self._get('recent')['update']]


    def get_update(self, update_id, user_id=None, section_id=None, group_id=None):
        """
        Get updates in any realm.

        :param *_id: ID of realm.
        """
        if user_id:
            self.get_user_update(update_id, user_id)
        elif section_id:
            self.get_section_update(update_id, section_id)
        elif group_id:
            self.get_group_update(update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_user_update(self, update_id, user_id):
        return Update(self._get('users/%s/updates/%s' % (user_id, update_id)))

    def get_section_update(self, update_id, section_id):
        return Update(self._get('sections/%s/updates/%s' % (section_id, update_id)))

    def get_group_update(self, update_id, group_id):
        return Update(self._get('groups/%s/updates/%s' % (group_id, update_id)))


    def delete_update(self, update_id, user_id=None, section_id=None, group_id=None):
        """
        Delete an update in any realm.

        :param update_id: ID of update to delete.
        :param *_id: ID of realm.
        """
        if user_id:
            self.delete_user_update(update_id, user_id)
        elif section_id:
            self.delete_section_update(update_id, section_id)
        elif group_id:
            self.delete_group_update(update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_user_update(self, update_id, user_id):
        return Update(self._delete('users/%s/updates/%s' % (user_id, update_id)))

    def delete_section_update(self, update_id, section_id):
        return Update(self._delete('sections/%s/updates/%s' % (section_id, update_id)))

    def delete_group_update(self, update_id, group_id):
        return Update(self._delete('groups/%s/updates/%s' % (group_id, update_id)))


    def update_update(self, update, user_id=None, section_id=None, group_id=None):
        """
        Helper function for updating an update in any realm.

        :param update: Update object to post.
        :param *_id: ID of realm.
        """
        if user_id:
            return self.update_user_update(update, user_id)
        elif section_id:
            return self.update_section_update(update, section_id)
        elif group_id:
            return self.update_group_update(update, group_id)
        else:
            raise TypeError('Realm id property required.')

    def update_user_update(self, update, user_id):
        return Update(self._put('users/%s/updates' % user_id, update.json()))

    def update_section_update(self, update, section_id):
        return Update(self._put('sections/%s/updates' % section_id, update.json()))

    def update_group_update(self, update, group_id):
        return Update(self._put('groups/%s/updates' % group_id, update.json()))


    def create_update_comment(self, comment, update_id, user_id=None, section_id=None, group_id=None):
        """
        Helper function for creating a comment on an update in any realm.

        :param comment: UpdateComment object to post.
        :param update_id: ID of update on which to create comment.
        :param *_id: ID of realm.
        """
        if user_id:
            return self.create_user_update_comment(comment, update_id, user_id)
        elif section_id:
            return self.create_section_update_comment(comment, update_id, section_id)
        elif group_id:
            return self.create_group_update_comment(comment, update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_user_update_comment(self, comment, update_id, user_id):
        return Update(self._post('users/%s/updates/%s/comments' % (user_id, update_id), comment.json()))

    def create_section_update_comment(self, comment, update_id, section_id):
        return Update(self._post('sections/%s/updates/%s/comments' % (section_id, update_id), comment.json()))

    def create_group_update_comment(self, comment, update_id, group_id):
        return Update(self._post('groups/%s/updates/%s/comments' % (group_id, update_id), comment.json()))


    def get_update_comments(self, update_id, user_id=None, section_id=None, group_id=None):
        """
        Get data on update comments in any realm.

        :param update_id: ID of update from which to get comments.
        :param *_id: ID of realm.
        """
        if user_id:
            return self.get_user_update_comments(update_id, user_id)
        elif section_id:
            return self.get_section_update_comments(update_id, section_id)
        elif group_id:
            return self.get_group_update_comments(update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_user_update_comments(self, update_id, user_id):
        return [UpdateComment(raw) for raw in self._get('users/%s/updates/%s/comments' % (user_id, update_id))['comment']]

    def get_section_update_comments(self, update_id, section_id):
        return [UpdateComment(raw) for raw in self._get('sections/%s/updates/%s/comments' % (section_id, update_id))['comment']]

    def get_group_update_comments(self, update_id, group_id):
        return [UpdateComment(raw) for raw in self._get('groups/%s/updates/%s/comments' % (group_id, update_id))['comment']]


    def get_update_comment(self, comment_id, update_id, user_id=None, section_id=None, group_id=None):
        """
        Get data on an update comment in any realm.

        :param comment_id: ID of comment on which to get data.
        :param update_id: ID of update on which to create comment.
        :param *_id: ID of realm.
        """
        if user_id:
            return self.get_user_update_comment(comment_id, update_id, user_id)
        elif section_id:
            return self.get_section_update_comment(comment_id, update_id, section_id)
        elif group_id:
            return self.get_group_update_comment(comment_id, update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_user_update_comment(self, comment_id, update_id, user_id):
        return UpdateComment(self._get('users/%s/updates/%s/comments/%s' % (user_id, update_id, comment_id)))

    def get_section_update_comment(self, comment_id, update_id, section_id):
        return UpdateComment(self._get('sections/%s/updates/%s/comments/%s' % (section_id, update_id, comment_id)))

    def get_group_update_comment(self, comment_id, update_id, group_id):
        return UpdateComment(self._get('groups/%s/updates/%s/comments/%s' % (group_id, update_id, comment_id)))


    def delete_update_comment(self, comment_id, update_id, user_id=None, section_id=None, group_id=None):
        """
        Delete an update comment in any realm.

        :param comment_id: ID of comment to delete.
        :param update_id: ID of update on which to delete comment.
        :param *_id: ID of realm.
        """
        if user_id:
            self.delete_user_update_comment(comment_id, update_id, user_id)
        elif section_id:
            self.delete_section_update_comment(comment_id, update_id, section_id)
        elif group_id:
            self.delete_group_update_comment(comment_id, update_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_user_update_comment(self, comment_id, update_id, user_id):
        self._delete('users/%s/updates/%s/comments/%s' % (user_id, update_id, comment_id))

    def delete_section_update_comment(self, comment_id, update_id, section_id):
        self._delete('sections/%s/updates/%s/comments/%s' % (section_id, update_id, comment_id))

    def delete_group_update_comment(self, comment_id, update_id, group_id):
        self._delete('groups/%s/updates/%s/comments/%s' % (group_id, update_id, comment_id))

    # TODO: Implement Reminder requests
    # It's unclear what endpoints we should use

    def create_media_album(self, album, section_id=None, group_id=None):
        """
        Get data on an update comment in any realm.

        :param album: Album object to post to API.
        :param *_id: ID of realm.
        """
        if section_id:
            return self.create_section_media_album(album, section_id)
        elif group_id:
            return self.create_group_media_album(album, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_section_media_album(self, album, section_id):
        return MediaAlbum(self._post('sections/%s/albums' % section_id, album.json()))

    def create_group_media_album(self, album, group_id):
        return MediaAlbum(self._post('groups/%s/albums' % group_id, album.json()))


    def get_media_albums(self, section_id=None, group_id=None):
        """
        Get data on media albums in any realm.

        :param *_id: ID of realm.
        :return: List of MediaAlbum objects.
        """
        if section_id:
            return self.get_section_media_albums(section_id)
        elif group_id:
            return self.get_group_media_albums(group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_section_media_albums(self, section_id):
        return [MediaAlbum(raw) for raw in self._get('sections/%s/albums' % section_id)['album']]

    def get_group_media_albums(self, group_id):
        return [MediaAlbum(raw) for raw in self._get('groups/%s/albums' % group_id)['album']]


    def get_media_album(self, album_id, section_id=None, group_id=None):
        """
        Get data on a media album in any realm.

        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            return self.get_section_media_album(album_id, section_id)
        elif group_id:
            return self.get_group_media_album(album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_section_media_album(self, album_id, section_id):
        return MediaAlbum(self._get('sections/%s/albums/%s' % (section_id, album_id)))

    def get_group_media_album(self, album_id, group_id):
        return MediaAlbum(self._get('groups/%s/albums/%s' % (group_id, album_id)))


    def update_media_album(self, album_id, section_id=None, group_id=None):
        """
        Helper function for updating a media album in any realm.

        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            return self.update_section_media_album(album_id, section_id)
        elif group_id:
            return self.update_group_media_album(album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def update_section_media_album(self, album_id, section_id):
        return MediaAlbum(self._get('sections/%s/albums/%s' % (section_id, album_id)))

    def update_group_media_album(self, album_id, group_id):
        return MediaAlbum(self._get('groups/%s/albums/%s' % (group_id, album_id)))


    def delete_media_album(self, album_id, section_id=None, group_id=None):
        """
        Delete a media album in any realm.

        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            self.delete_section_media_album(album_id, section_id)
        elif group_id:
            self.delete_group_media_album(album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_section_media_album(self, album_id, section_id):
        self._delete('sections/%s/albums/%s' % (section_id, album_id))

    def delete_group_media_album(self, album_id, group_id):
        self._delete('groups/%s/albums/%s' % (group_id, album_id))


    def get_media_album_content(self, content_id, album_id, section_id=None, group_id=None):
        """
        Get data on a media item from an album in any realm.

        Note: We could use the realm-ambiguous /album/[id] for this, but as of 2/15/15
        that endpoint is no longer maintained. For forward-compatibility, it's better to deal
        with this request as we do others.

        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            self.get_section_media_album_content(content_id, album_id, section_id)
        elif group_id:
            self.get_group_media_album_content(content_id, album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def get_section_media_album_content(self, content_id, album_id, section_id):
        return Media(self._get('sections/%s/albums/%s/content/%s' % (section_id, album_id, content_id)))

    def get_group_media_album_content(self, content_id, album_id, group_id):
        return Media(self._get('groups/%s/albums/%s/content/%s' % (group_id, album_id, content_id)))


    def update_media_album_content(self, content, content_id, album_id, section_id=None, group_id=None):
        """
        Helper function for updating a media item from an album in any realm.

        Note: We could use the realm-ambiguous /album/[id] for this, but as of 2/15/15
        that endpoint is no longer maintained. For forward-compatibility, it's better to deal
        with this request as we do others.

        :param content: Content object containing data to update.
        :param content_id: ID of content to update.
        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            self.update_section_media_album_content(content, content_id, album_id, section_id)
        elif group_id:
            self.update_group_media_album_content(content, content_id, album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def update_section_media_album_content(self, content, content_id, album_id, section_id):
        self._put('sections/%s/albums/%s/content/%s' % (section_id, album_id, content_id), content.json())

    def update_group_media_album_content(self, content, content_id, album_id, group_id):
        self._put('groups/%s/albums/%s/content/%s' % (group_id, album_id, content_id), content.json())


    def create_media_album_content(self, content, content_id, album_id, section_id=None, group_id=None):
        """
        Helper function for creating a media item in an album in any realm.

        Note: We could use the realm-ambiguous /album/[id] for this, but as of 2/15/15
        that endpoint is no longer maintained. For forward-compatibility, it's better to deal
        with this request as we do others.

        :param content: Content object containing data to update.
        :param content_id: ID of content to update.
        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            self.create_section_media_album_content(content, content_id, album_id, section_id)
        elif group_id:
            self.create_group_media_album_content(content, content_id, album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def create_section_media_album_content(self, content, content_id, album_id, section_id):
        return Media(self._post('sections/%s/albums/%s/content' % (section_id, album_id), content.json()))

    def create_group_media_album_content(self, content, content_id, album_id, group_id):
        return Media(self._post('groups/%s/albums/%s/content' % (group_id, album_id), content.json()))


    def delete_media_album_content(self, content_id, album_id, section_id=None, group_id=None):
        """
        Helper function for updating a media item from an album in any realm.

        Note: We could use the realm-ambiguous /album/[id] for this, but as of 2/15/15
        that endpoint is no longer maintained. For forward-compatibility, it's better to deal
        with this request as we do others.

        :param content: Content object containing data to update.
        :param content_id: ID of content to update.
        :param *_id: ID of realm.
        :return: MediaAlbum object.
        """
        if section_id:
            self.delete_section_media_album_content(content_id, album_id, section_id)
        elif group_id:
            self.delete_group_media_album_content(content_id, album_id, group_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_section_media_album_content(self, content_id, album_id, section_id):
        self._delete('sections/%s/albums/%s/content/%s' % (section_id, album_id, content_id))

    def delete_group_media_album_content(self, content_id, album_id, group_id):
        self._delete('groups/%s/albums/%s/content/%s' % (group_id, album_id, content_id))


    def create_document(self, document, section_id=None, group_id=None):
        """
        Helper function for creating a document in any realm.

        :param document: Document object to post to API.
        :param *_id: ID of realm.
        """
        if group_id:
            return self.create_section_media_album(document, group_id)
        if section_id:
            return self.create_section_media_album(document, section_id)
        else:
            raise TypeError('Realm id property required.')

    def create_school_media_album(self, document, school_id):
        return Document(self._post('schools/%s/documents' % school_id, document.json()))



    def get_documents(self, section_id=None, group_id=None):
        """
        Helper function for creating a document in any realm.

        :param document: Document object to post to API.
        :param *_id: ID of realm.
        """
        if group_id:
            return self.get_school_documents(group_id)
        if section_id:
            return self.get_section_documents(section_id)
        else:
            raise TypeError('Realm id property required.')

    def get_school_documents(self, school_id):
        return [Document(raw) for raw in self._get('schools/%s/documents' % school_id)['document']]

    def get_section_documents(self, section_id):
        return [Document(raw) for raw in self._get('sections/%s/documents' % section_id)['document']]


    def get_document(self, document_id, section_id=None, group_id=None):
        """
        Get data on a document in any realm.

        :param document: Document object to post to API.
        :param *_id: ID of realm.
        """
        if group_id:
            return self.get_school_document(document_id, group_id)
        if section_id:
            return self.get_section_document(document_id, section_id)
        else:
            raise TypeError('Realm id property required.')

    def get_school_document(self, document_id, school_id):
        return Document(self._get('schools/%s/documents/%s' % (school_id, document_id)))

    def get_section_document(self, document_id, section_id):
        return Document(self._get('sections/%s/documents/%s' % (section_id, document_id)))


    def update_document(self, document, document_id, section_id=None, group_id=None):
        """
        Helper function for updating adocument in any realm.

        :param document: Document object to post to API.
        :param *_id: ID of realm.
        """
        if group_id:
            self.update_school_document(document, document_id, group_id)
        if section_id:
            self.update_section_document(document, document_id, section_id)
        else:
            raise TypeError('Realm id property required.')

    def update_school_document(self, document, document_id, school_id):
        self._put('schools/%s/documents/%s' % (school_id, document_id), document.json())

    def update_section_document(self, document, document_id, section_id):
        self._put('sections/%s/documents/%s' % (section_id, document_id), document.json())


    def delete_document(self, document_id, section_id=None, group_id=None):
        """
        Delete adocument in any realm.

        :param document_id: ID of document to delete.
        :param *_id: ID of realm.
        """
        if group_id:
            self.delete_school_document(document_id, group_id)
        if section_id:
            self.delete_section_document(document_id, section_id)
        else:
            raise TypeError('Realm id property required.')

    def delete_school_document(self, document_id, school_id):
        self._delete('schools/%s/documents/%s' % (school_id, document_id))

    def delete_section_document(self, document_id, section_id):
        self._delete('sections/%s/documents/%s' % (section_id, document_id))


    def get_grading_scale(self, section_id):
        """
        Get data on the grading scale used in a course section.

        The documentation on this endpoint is incorrect, a single object is returned rather than a list.

        :param section_id: ID of section whose grading scale to get data on.
        :return: GradingScale object.
        """
        return GradingScale(self._get('sections/%s/grading_scales' % section_id))


    def get_rubrics(self, section_id):
        """
        Get list of rubrics used in a given course section.

        :param section_id: ID of section from which to get rubrics.
        :return: List of Rubric objects.
        """
        return [Rubric(raw) for raw in self._get('sections/%s/grading_rubrics' % section_id)['grading_rubric']]

    def get_rubric(self, rubric_id, section_id):
        """
        Get data on a rubric.

        :param rubric_id: ID of rubric on which to get data.
        :param section_id: ID of section in which rubric is used.
        """
        return Rubric(self._get('sections/%s/grading_rubrics/%s' % (section_id, rubric_id)))


    def create_grading_categories(self, categories, section_id):
        """
        Create multiple grading categories.

        :param categories: List of GradingCategory objects to create.
        :param section_id: ID of section in which to create categories.
        """
        return [GradingCategory(raw) for raw in self._put('sections/%s/grading_categories' % section_id, {'grading_categories': {'grading_category': [category.json() for category in categories]}})['grading_category']]

    def get_grading_categories(self, section_id):
        """
        Get a list of grading categories in a course section.

        :param section_id: ID of section whose categories to get.
        """
        return [GradingCategory(raw) for raw in self._get('sections/%s/grading_categories' % section_id)['grading_category']]

    def get_grading_category(self, category_id, section_id):
        """
        Get agrading category in a course section.

        :param category_id: ID of category.
        :param section_id: ID of category's section.
        """
        return GradingCategory(self._get('sections/%s/grading_categories/%s' % (section_id, category_id)))

    def update_grading_category(self, category, section_id):
        """
        Get data on a grading category in a course section.

        :param category: Category object to update.
        :param section_id: ID of category's section.
        :return: GradingCategory object recieved from API.
        """
        return self.create_grading_categories([category], section_id)[0]

    def delete_grading_category(self, category_id, section_id):
        """
        Delete agrading category in a course section.

        :param category_id: ID of category.
        :param section_id: ID of category's section.
        """
        self._delete('sections/%s/grading_categories/%s' % (section_id, category_id))

    def create_grading_groups(self, groups, section_id):
        """
        Create multiple grading groups.

        :param groups: List of GradingGroup objects to create.
        :param section_id: ID of section in which to create groups.
        """
        return [GradingGroup(raw) for raw in self._put('sections/%s/grading_groups' % section_id, {'grading_groups': {'grading_group': [group.json() for group in groups]}})['grading_group']]

    def get_grading_groups(self, section_id):
        """
        Get a list of grading groups in a course section.

        :param section_id: ID of section whose groups to get.
        """
        return [GradingGroup(raw) for raw in self._get('sections/%s/grading_groups' % section_id)['grading_group']]

    def get_grading_group(self, group_id, section_id):
        """
        Get a grading group in a course section.

        :param group_id: ID of group.
        :param section_id: ID of group's section.
        """
        return GradingGroup(self._get('sections/%s/grading_groups/%s' % (section_id, group_id)))

    def update_grading_group(self, group, section_id):
        """
        Get data on a grading group in a course section.

        :param group: Group object to update.
        :param section_id: ID of group's section.
        :return: GradingGroup object recieved from API.
        """
        return self.create_grading_groups([group], section_id)[0]

    def delete_grading_group(self, group_id, section_id):
        """
        Delete agrading group in a course section.

        :param group_id: ID of group.
        :param section_id: ID of group's section.
        """
        self._delete('sections/%s/grading_groups/%s' % (section_id, group_id))


    def get_assignments(self, section_id):
        return [Assignment(raw) for raw in self._get('sections/%s/assignments' % section_id)['assignment']]

    def get_assignment(self, section_id, assignment_id):
        return Assignment(self._get('sections/%s/assignments/%s' % (section_id, assignment_id)))


    def get_assignment_comments(self, section_id, assignment_id):
        return [Assignment(raw) for raw in self._get('sections/%s/assignments/%s/comments' % (section_id, assignment_id))['comment']]

    def get_assignment_comment(self, section_id, assignment_id, comment_id):
        return Assignment(self._get('sections/%s/assignments/%s' % (section_id, assignment_id)))


    # TODO: Support Grades
    # TODO: Support Attendance
    # TODO: Support Submissions
    # TODO: Support Course Content Folders
    # TODO: Support Pages
    # TODO: Support SCORM Packages
    # TODO: Support Web Content Package
    # TODO: Support Completion

    def get_friend_requests(self, user_id):
        return [FriendRequest(raw) for raw in self._get('users/%s/requests/friends' % user_id)['request']]

    def get_friend_request(self, user_id, request_id):
        return FriendRequest(self._get('users/%s/requests/friends/%s' % (user_id, request_id)))


    def get_user_section_invites(self, user_id):
        return [Invite(raw) for raw in self._get('users/%s/invites/sections' % user_id)['invite']]

    def get_user_group_invites(self, user_id):
        return [Invite(raw) for raw in self._get('users/%s/invites/groups' % user_id)['invite']]

    def get_user_section_invite(self, user_id, invite_id):
        return Invite(self._get('users/%s/invites/sections/%s' % (user_id, invite_id)))

    def get_user_group_invite(self, user_id, invite_id):
        return Invite(self._get('users/%s/invites/groups/%s' % (user_id, invite_id)))


    def get_user_network(self, user_id):
        return [User(raw) for raw in self._get('users/%s/network' % user_id)['users']]


    def get_user_grades(self, user_id):
        return [Grade(raw) for raw in self._get('users/%s/grades' % user_id)['section']]
    
    def get_user_grades_by_section(self, user_id, section_id):
        return [Grade(raw) for raw in self._get('users/%s/grades?section_id=%s' % (user_id, section_id))['section']]
    
    def get_user_sections(self, user_id):
        return [Section(raw) for raw in self._get('users/%s/sections' % user_id)['section']]

    def get_user_groups(self, user_id):
        return [Group(raw) for raw in self._get('users/%s/groups' % user_id)['group']]

    # TODO: Implement get_user_requests
    # TODO: Implement get_user_invites
    # TODO: Implement get_user_external_id

    # TODO: Implement get_grading_periods and get_grading_period

    def get_roles(self):
        return [Role(raw) for raw in self._get('roles')['role']]

    def get_role(self, role_id):
        return Role(self._get('roles/%s' % role_id))

    def get_messages(self, message_folder):
        """
        List messages in one of the valid message folders.

        :param message_folder: Either 'sent' or 'inbox'
        """
        if message_folder == 'sent':
            return self.get_sent_messages()
        else:
            return self.get_inbox_messages()

    def get_sent_messages(self):
        return [MessageThread(raw) for raw in self._get('messages/sent')['message']]

    def get_inbox_messages(self):
        return [MessageThread(raw) for raw in self._get('messages/inbox')['message']]

    def get_message(self, message_id):
        """
        Fetch data on a specific message thread.

        Note: The endpoints messages/inbox/[message id] and messages/sent/[message id] can be used for this with the same result. Odd that the API would be set up this way.

        :param message_id: ID of the message thread desired.
        :return: list of messages in that thread.
        """
        return [Message(raw) for raw in self._get('messages/inbox/%s' % message_id)['message']]


    def create_message(self, message):
        """
        Create a new message.

        :param message: Message object to create.
        """
        if isinstance(message.recipient_ids, list):
            message.recipient_ids = ','.join(message.recipient_ids)
        return Message(self._post('messages', message.json()))

    def send_message(self, subject, content, user_ids):
        """
        Helper function for sending messages.

        :param subject: A string holding the subject of a message.
        :param content: A string holding the body of a message.
        :param user_ids: A list of IDs of users to which to send the message.
        """
        return self.create_message(Message({'subject': subject, 'message': content, 'recipient_ids': user_ids}))

    def delete_message(self, message_id):
        """
        Delete a message.

        Note: both the sent/ and inbox/ endpoints can be used for this operation with the same result.
        :param message_id: ID of the message thread for deletion.
        """
        self._delete('messages/inbox/%s' % message_id)

    # TODO: Support replying to messages

    # TODO: Implement resource collections, resource templates

    def _like(self, path):
        """
        Post a like request.

        :param path: The path with values to POST to.
        :return: Number of likes on the object.
        """
        try:
            return self._post(path, {'like_action': True})['likes']
        except TypeError:
            raise NoDifferenceError('You have already liked this post.')

    def _unlike(self, path):
        """
        Post an unlike request.

        :param path: The path with values to POST to.
        :return: Number of likes on the object.
        """
        try:
            return self._post(path, {'like_action': False})['likes']
        except TypeError:
            raise NoDifferenceError('You have already unliked this post.')

    def like(self, id):
        """
        Like an object.

        :param id: ID of object to like.
        :return: Number of likes on the object.
        """
        return self._like('like/%s' % id)

    def unlike(self, id):
        """
        UNlike an object.

        :param id: ID of object to unlike.
        :return: Number of likes on the object.
        """
        return self._unlike('like/%s' % id)

    def get_likes(self, id):
        """
        Get all users who have liked an object.

        :param id: ID of object to check likes of.
        :return: List of users who have liked an object.
        """
        return [User(raw) for raw in self._get('like/%s' % id)['users']]

    def like_comment(self, id, comment_id):
        """
        Like a comment on an object.

        :param id: ID of object on which the comment was written.
        :param comment_id: ID of comment to like.
        """
        return self._like('like/%s/comment/%s' % (id, comment_id))

    def unlike_comment(self, id, comment_id):
        """
        UNlike a comment on an object.

        :param id: ID of object on which the comment was written.
        :param comment_id: ID of comment to unlike.
        """
        return self._unlike('like/%s/comment/%s' % (id, comment_id))

    def get_comment_likes(self, id, comment_id):
        """
        Get all users who have liked a comment on an object.

        :param id: ID of object on which the comment was written.
        :param comment_id: ID of comment to check likes of.
        :return List of users who have liked the comment.
        """
        return [User(raw) for raw in self._get('like/%s/comment/%s' % (id, comment_id))['users']]
    
    def vote(self, poll_id, choice_id):
        """
        Cast a vote on a poll.

        Poll data is packaged in update objects. Choice and poll IDs can be found there.

        :param poll_id: ID of poll to vote on.
        :param choice_id: ID of choice you'd like to make.
        """
        return self._post('poll/%s/vote' % poll_id, {'id': choice_id, 'select': True})

    def get_user_actions(self, user_id, start_time=None, end_time=int(time.time())):
        """
        Get analysis of a user's actions over a given period of time.

        This endpoint is typically only available to site admins.

        :param user_id: ID of user to get actions of.
        :param start_time: Timestamp at which to start action list. Defaults to 7 days before end.
        :param end_time: Timestamp at which to end action list.
        :return: List of Actions the user has completed.
        """
        start_time = end_time - 604800 if start_time is None else start_time
        if start_time < end_time - 604800:
            raise AttributeError('Start timestamp must be no earlier than 7 days before end timestamp.')
        return [Action(raw) for raw in self._get('analytics/users/%s?start_time=%s&end_time=%s&start=%s&limit=%s' % (user_id, start_time, end_time, self.start, self.limit))['actions']]

    # TODO: Implement other analytics endpoints
    # TODO: Implement multi-get(!) and multi-options requests. Don't seem to work right now.

    # TODO: Support all User-Specific Objects, User Information, etc. requests

    def _search(self, keywords, search_type):
        """
        Get the items for a search of keywords and type.

        :param keywords: The keywords you wish to search with.
        :param type: The type of search (user, group, course).
        :return: A list of dictionaries representing search outputs.
        """
        return self._get('search?keywords=%s&type=%s' % ('+'.join(keywords), search_type))[search_type+'s']['search_result']

    def search_users(self, keywords):
        """
        Get the items for a search of keywords in users.

        :param keywords: The keywords you wish to search with.
        :return: A list of dictionaries representing search outputs.
        """
        return self._search(keywords, 'user')

    def search_groups(self, keywords):
        """
        Get the items for a search of keywords in groups.

        :param keywords: The keywords you wish to search with.
        :return: A list of dictionaries representing search outputs.
        """
        return self._search(keywords, 'group')

    def search_courses(self, keywords):
        """
        Get the items for a search of keywords in courses.

        :param keywords: The keywords you wish to search with.
        :return: A list of dictionaries representing search outputs.
        """
        return self._search(keywords, 'course')
