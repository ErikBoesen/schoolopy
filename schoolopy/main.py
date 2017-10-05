from .models import *
import requests
import time
import random
import json


class Schoology:
    _ROOT = 'https://api.schoology.com/v1/'
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
        """
        GET data from a given endpoint.

        :param path: Path (following API root) to endpoint.
        :return: JSON response.
        """
        return requests.get(self._ROOT + path, headers={'Authorization': self._oauth_header()}).json()

    def _post(self, path, data):
        """
        POST valid JSON to a given endpoint.

        :param path: Path (following API root) to endpoint.
        :param data: JSON data to POST.
        :return: JSON response.
        """
        return requests.post(self._ROOT + path, data=data, headers={'Authorization': self._oauth_header()}).json()

    def _post(self, path, data):
        """
        PUT valid JSON to a given endpoint.

        :param path: Path (following API root) to endpoint.
        :param data: JSON data to PUT.
        :return: JSON response.
        """
        return requests.put(self._ROOT + path, data=data, headers={'Authorization': self._oauth_header()}).json()

    def _delete(self, path):
        """
        Send a DELETE request to a given endpoint.

        :param path: Path (following API root) to endpoint.
        """
        requests.delete(self._ROOT + path, headers={'Authorization': self._oauth_header()})


    def get_schools(self):
        """
        Get data on all schools.

        :return: List of school objects of which a user is aware.
        """
        return [School(raw) for raw in self._get('schools')['school']]

    def get_school(self, school_id):
        """
        Get data on an individual school.

        :return: School object with data on the requested school.
        """
        return School(self._get('schools/%s' % school_id))

    def create_school(self, school):
        """
        Create a new school.

        :param school: School object containing necessary fields.
        :return: School object obtained from API.
        """
        return School(self._post('schools', school.json))

    def edit_school(self, school_id, school):
        """
        Edit a school.

        :param school_id: ID of school to edit.
        :param school: School object containing necessary fields.
        :return: School object obtained from API.
        """
        # TODO: Does this endpoint return anything?
        self._put('schools/%s' % school_id, school.json)

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
        return Building(self._post('schools/%s/buildings' % school_id, building.json))

    def get_users(self):
        """
        Get data on all users.

        :return: List of User objects.
        """
        return [User(raw) for raw in self._get('users')['user']]

    def get_user(self, user_id):
        """
        Get data on an individual user.

        :param user_id: ID of user on whom to get data.
        :return: User object.
        """
        return User(self._get('users/%s' % user_id))

    def get_groups(self):
        """
        Get data on all groups.

        :return: List of Group objects.
        """
        return [Group(raw) for raw in self._get('groups')['group']]

    def get_group(self, group_id):
        """
        Get data on an individual group.

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
        Get data on an individual course.

        :param course_id: ID of course on which to get data.
        :return: Course object.
        """
        return Course(self._get('courses/%s' % course_id))

    def get_sections(self):
        """
        Get data on all sections.

        :return: List of Section objects.
        """
        return [Section(raw) for raw in self._get('sections')['section']]

    def get_section(self, section_id):
        """
        Get data on an individual section.

        :param section_id: ID of section on which to get data.
        :return: Section object.
        """
        return Section(self._get('sections/%s' % section_id))

    def get_enrollments(self, section_id=None, group_id=None):
        """
        Helper function to get enrollments in any realm. Realm will be decided based on named parameters passed.

        You must provide either a section_id or group_id, and name your parameters.

        :param section_id: ID of section whose enrollments to get.
        :param group_id: ID of group whose enrollments to get.
        :return: List of User objects.
        """
        if section_id:
            return get_section_enrollments(section_id)
        elif group_id:
            return get_group_enrollments(group_id)
        else:
            raise TypeError('Realm identifier required.')

    def get_section_enrollments(self, section_id):
        return [Enrollment(raw) for raw in self._get('sections/%s/enrollments' % section_id)['enrollment']]

    def get_group_enrollments(self, group_id):
        return [Enrollment(raw) for raw in self._get('groups/%s/enrollments' % group_id)['enrollments']]

    # TODO: Create generic create_enrollment method

    def create_section_enrollment(self, section_id, user_id, admin=False, status=1):
        return Enrollment(self._post('sections/%s/enrollments' % section_id, {'uid': user_id, 'admin': int(admin), 'status': status}))

    def create_group_enrollment(self, group_id, user_id, admin=False, status=1):
        return Enrollment(self._post('groups/%s/enrollments' % group_id, {'uid': user_id, 'admin': int(admin), 'status': status}))

    # TODO: Do we need to provide the ID of the realm?
    def join_section(self, access_code):
        return Enrollment(self._post('sections/accesscode' % access_code, {'access_code': access_code}))

    def join_group(self, access_code):
        return Enrollment(self._post('sections/accesscode' % access_code, {'access_code': access_code}))


    def create_section_enrollments(self, section_id, enrollments):
        """
        Create section enrollments in bulk.

        :param section_id: ID of section in which to create enrollments.
        :param enrollments: List of Enrollment objects to be created. Up to 50 enrollments can be created at a time.
        :return: List of Enrollment objects recieved from Schoology API.
        """
        return [Enrollment(raw) for raw in self._post('sections/%s/enrollments' % section_id, {'enrollments': {'enrollment': [enrollment.json for enrollment in enrollments]}})]

    def create_group_enrollments(self, group_id, enrollments):
        """
        Create group enrollments in bulk.

        :param group_id: ID of group in which to create enrollments.
        :param enrollments: List of Enrollment objects to be created. Up to 50 enrollments can be created at a time.
        :return: List of Enrollment objects recieved from Schoology API.
        """
        return [Enrollment(raw) for raw in self._post('groups/%s/enrollments' % group_id, {'enrollments': {'enrollment': [enrollment.json for enrollment in enrollments]}})]

    # TODO: Implement course enrollments import

    def get_district_events(self, district_id):
        return [Event(raw) for raw in self._get('districts/%s/events' % district_id)['event']]

    def get_school_events(self, school_id):
        return [Event(raw) for raw in self._get('schools/%s/events' % school_id)['event']]

    def get_user_events(self, user_id):
        return [Event(raw) for raw in self._get('users/%s/events' % user_id)['event']]

    def get_section_events(self, section_id):
        return [Event(raw) for raw in self._get('sections/%s/events' % section_)['event']]

    def get_group_events(self, group_id):
        return [Event(raw) for raw in self._get('groups/%s/events' % group_id)['event']]


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


    def get_district_blog_post(self, district_id, post_id):
        return BlogPost(self._get('districts/%s/posts/%s' % (district_id, post_id)))

    def get_school_blog_post(self, school_id, post_id):
        return BlogPost(self._get('schools/%s/posts/%s' % (school_id, post_id)))

    def get_user_blog_post(self, user_id, post_id):
        return BlogPost(self._get('users/%s/posts/%s' % (user_id, post_id)))

    def get_section_blog_post(self, section_id, post_id):
        return BlogPost(self._get('sections/%s/posts/%s' % (section_id, post_id)))

    def get_group_blog_post(self, group_id, post_id):
        return BlogPost(self._get('groups/%s/posts/%s' % (group_id, post_id)))


    def get_district_blog_post_comments(self, district_id, post_id):
        return [BlogPostComment(raw) for raw in self._get('districts/%s/posts/%s/comments' % (district_id, post_id))['comment']]

    def get_school_blog_post_comments(self, school_id, post_id):
        return [BlogPostComment(raw) for raw in self._get('schools/%s/posts/%s/comments' % (school_id, post_id))['comment']]

    def get_user_blog_post_comments(self, user_id, post_id):
        return [BlogPostComment(raw) for raw in self._get('users/%s/posts/%s/comments' % (user_id, post_id))['comment']]

    def get_section_blog_post_comments(self, section_id, post_id):
        return [BlogPostComment(raw) for raw in self._get('sections/%s/posts/%s/comments' % (section_id, post_id))['comment']]

    def get_group_blog_post_comments(self, group_id, post_id):
        return [BlogPostComment(raw) for raw in self._get('groups/%s/posts/%s/comments' % (group_id, post_id))['comment']]


    def get_district_blog_post_comment(self, district_id, post_id, comment_id):
        return BlogPostComment(self._get('districts/%s/posts/%s/comments/%s' % (district_id, post_id, comment_id)))

    def get_school_blog_post_comment(self, school_id, post_id, comment_id):
        return BlogPostComment(self._get('schools/%s/posts/%s/comments/%s' % (school_id, post_id, comment_id)))

    def get_user_blog_post_comment(self, user_id, post_id, comment_id):
        return BlogPostComment(self._get('users/%s/posts/%s/comments/%s' % (user_id, post_id, comment_id)))

    def get_section_blog_post_comment(self, section_id, post_id, comment_id):
        return BlogPostComment(self._get('sections/%s/posts/%s/comments/%s' % (section_id, post_id, comment_id)))

    def get_group_blog_post_comment(self, group_id, post_id, comment_id):
        return BlogPostComment(self._get('groups/%s/posts/%s/comments/%s' % (group_id, post_id, comment_id)))


    def get_district_discussions(self, district_id):
        return [Discussion(raw) for raw in self._get('districts/%s/discussions' % district_id)['discussion']]

    def get_school_discussions(self, school_id):
        return [Discussion(raw) for raw in self._get('schools/%s/discussions' % school_id)['discussion']]

    def get_section_discussions(self, section_id):
        return [Discussion(raw) for raw in self._get('sections/%s/discussions' % section_id)['discussion']]

    def get_group_discussions(self, group_id):
        return [Discussion(raw) for raw in self._get('groups/%s/discussions' % group_id)['discussion']]


    def get_district_discussion(self, district_id, discussion_id):
        return Discussion(self._get('districts/%s/discussions/%s' % (district_id, discussion_id)))

    def get_school_discussion(self, school_id, discussion_id):
        return Discussion(self._get('schools/%s/discussions/%s' % (school_id, discussion_id)))

    def get_section_discussion(self, section_id, discussion_id):
        return Discussion(self._get('sections/%s/discussions/%s' % (section_id, discussion_id)))

    def get_group_discussion(self, group_id, discussion_id):
        return Discussion(self._get('groups/%s/discussions/%s' % (group_id, discussion_id)))


    def get_district_discussion_replies(self, district_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('districts/%s/discussions/%s/comments' % (district_id, discussion_id))['comment']]

    def get_school_discussion_replies(self, school_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('schools/%s/discussions/%s/comments' % (school_id, discussion_id))['comment']]

    def get_section_discussion_replies(self, section_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('sections/%s/discussions/%s/comments' % (section_id, discussion_id))['comment']]

    def get_group_discussion_replies(self, group_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('groups/%s/discussions/%s/comments' % (group_id, discussion_id))['comment']]


    def get_district_discussion_reply(self, district_id, discussion_id, reply_id):
        return DiscussionReply(self._get('districts/%s/discussions/%s/comments/%s' % (district_id, discussion_id, reply_id)))

    def get_school_discussion_reply(self, school_id, discussion_id, reply_id):
        return DiscussionReply(self._get('schools/%s/discussions/%s/comments/%s' % (school_id, discussion_id, reply_id)))

    def get_section_discussion_reply(self, section_id, discussion_id, reply_id):
        return DiscussionReply(self._get('sections/%s/discussions/%s/comments/%s' % (section_id, discussion_id, reply_id)))

    def get_group_discussion_reply(self, group_id, discussion_id, reply_id):
        return DiscussionReply(self._get('groups/%s/discussions/%s/comments/%s' % (group_id, discussion_id, reply_id)))


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


    def get_user_update(self, user_id, update_id):
        return Update(self._get('users/%s/updates/%s' % (user_id, update_id)))

    def get_section_update(self, section_id, update_id):
        return Update(self._get('sections/%s/updates/%s' % (section_id, update_id)))

    def get_group_update(self, group_id, update_id):
        return Update(self._get('groups/%s/updates/%s' % (group_id, update_id)))


    # TODO: Investigate whether we can get individual comments
    def get_user_update_comments(self, user_id, update_id):
        return [UpdateComment(raw) for raw in self._get('users/%s/updates/%s/comments' % (user_id, update_id))['comment']]

    def get_section_update_comments(self, section_id, update_id):
        return [UpdateComment(raw) for raw in self._get('sections/%s/updates/%s/comments' % (section_id, update_id))['comment']]

    def get_group_update_comments(self, group_id, update_id):
        return [UpdateComment(raw) for raw in self._get('groups/%s/updates/%s/comments' % (group_id, update_id))['comment']]


    # TODO: Implement Reminder requests
    # It's unclear what endpoints we should use

    # TODO: Support Media Albums
    # TODO: Support Documents
    # TODO: Support Grading Scales, Rubrics, Categories, and Groups


    def get_assignments(self, section_id):
        return [Assignment(raw) for raw in self._get('section/%s/assignments' % section_id)['assignment']]

    def get_assignment(self, section_id, assignment_id):
        return Assignment(self._get('section/%s/assignments/%s' % (section_id, assignment_id)))


    def get_assignment_comments(self, section_id, assignment_id):
        return [Assignment(raw) for raw in self._get('section/%s/assignments/%s/comments' % (section_id, assignment_id))['comment']]

    def get_assignment_comment(self, section_id, assignment_id, comment_id):
        return Assignment(self._get('section/%s/assignments/%s' % (section_id, assignment_id)))


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

    def get_messages(self):
        return [MessageThread(raw) for raw in self._get('messages')['message']]

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

    # Implement search, resource collections, resource templates

    def like(self, id):
        """
        Like an object.

        :param id: ID of object to like.
        :return: Number of likes on the object.
        """
        return self._post('like/%s' % id, {'like_action': True})['likes']

    def unlike(self, id):
        """
        UNlike an object.

        :param id: ID of object to unlike.
        :return: Number of likes on the object.
        """
        return self._post('like/%s' % id, {'like_action': False})['likes']

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
        return self._post('like/%s/comment/%s' % (id, comment_id), {'like_action': True})['likes']

    def unlike_comment(self, id, comment_id):
        """
        UNlike a comment on an object.

        :param id: ID of object on which the comment was written.
        :param comment_id: ID of comment to unlike.
        """
        return self._post('like/%s/comment/%s' % (id, comment_id), {'like_action': False})['likes']

    def vote(self, poll_id, choice_id):
        """
        Cast a vote on a poll.

        Poll data is packaged in update objects. Choice and poll IDs can be found there.

        :param poll_id: ID of poll to vote on.
        :param choice_id: ID of choice you'd like to make.
        """
        return self._post('poll/%s/vote' % poll_id, {'id': choice_id, 'select': True})


    def get_user_actions(self, user_id, start=0, end=time.time()):
        """
        Get analysis of a user's actions over a given period of time.

        This endpoint is typically only available to site admins.

        :param user_id: ID of user to get actions of.
        :param start: Timestamp at which to start action list.
        :param end: Timestamp at which to end action list.
        """
        return [Action(raw) for raw in self._get('analytics/users/%s?start_time=%d&end_time=%d' % (user_id, start, end))['actions']]

    # TODO: Implement other analytics endpoints
    # TODO: Implement multi-get(!) and multi-options requests. Don't seem to work right now.

    # TODO: Support all User-Specific Objects, User Information, etc. requests
