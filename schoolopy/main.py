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

    def get_schools(self):
        return [School(raw) for raw in self._get('schools')['school']]

    def get_school(self, school_id):
        return School(self._get('schools/%s' % school_id))

    def get_buildings(self, building_id):
        return [Building(raw) for raw in self._get('schools/%s/buildings' % building_id)]

    def get_users(self):
        return [User(raw) for raw in self._get('users')['user']]

    def get_user(self, user_id):
        return User(self._get('users/%s' % user_id))

    def get_groups(self):
        return [Group(raw) for raw in self._get('groups')['group']]

    def get_group(self, group_id):
        return Group(self._get('groups/%s' % group_id))

    def get_courses(self):
        return [Course(raw) for raw in self._get('courses')['course']]

    def get_course(self, course_id):
        return Course(self._get('courses/%s' % course_id))

    def get_sections(self):
        return [Section(raw) for raw in self._get('sections')['section']]

    def get_section(self, section_id):
        return Section(self._get('sections/%s' % section_id))

    def get_section_enrollments(self, section_id):
        return [User(raw) for raw in self._get('sections/%s/enrollments' % section_id)['enrollment']]

    def get_group_enrollments(self, group_id):
        return [User(raw) for raw in self._get('groups/%s/enrollments' % group_id)['enrollments']]

    # Support getting accesscode

    # TODO: Support ID at the end of enrollments path

    def get_district_events(self, district_id):
        return [Event(raw) for raw in self._get('districts/%s/events' % district_id)]

    def get_school_events(self, school_id):
        return [Event(raw) for raw in self._get('schools/%s/events' % school_id)]

    def get_user_events(self, user_id):
        return [Event(raw) for raw in self._get('users/%s/events' % user_id)]

    def get_section_events(self, section_id):
        return [Event(raw) for raw in self._get('sections/%s/events' % section_)]

    def get_group_events(self, group_id):
        return [Event(raw) for raw in self._get('groups/%s/events' % group_id)]


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
        return [BlogPost(raw) for raw in self._get('districts/%s/posts' % district_id)]

    def get_school_blog_posts(self, school_id):
        return [BlogPost(raw) for raw in self._get('schools/%s/posts' % school_id)]

    def get_user_blog_posts(self, user_id):
        return [BlogPost(raw) for raw in self._get('users/%s/posts' % user_id)]

    def get_section_blog_posts(self, section_id):
        return [BlogPost(raw) for raw in self._get('sections/%s/posts' % section_id)]

    def get_group_blog_posts(self, group_id):
        return [BlogPost(raw) for raw in self._get('groups/%s/posts' % group_id)]


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
        return BlogPostComment(self._get('districts/%s/posts/%s' % (district_id, post_id)))

    def get_school_blog_post_comments(self, school_id, post_id):
        return BlogPostComment(self._get('schools/%s/posts/%s' % (school_id, post_id)))

    def get_user_blog_post_comments(self, user_id, post_id):
        return BlogPostComment(self._get('users/%s/posts/%s' % (user_id, post_id)))

    def get_section_blog_post_comments(self, section_id, post_id):
        return BlogPostComment(self._get('sections/%s/posts/%s' % (section_id, post_id)))

    def get_group_blog_post_comments(self, group_id, post_id):
        return BlogPostComment(self._get('groups/%s/posts/%s' % (group_id, post_id)))


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
        return [Discussion(raw) for raw in self._get('districts/%s/discussions' % district_id)]

    def get_school_discussions(self, school_id):
        return [Discussion(raw) for raw in self._get('schools/%s/discussions' % school_id)]

    def get_section_discussions(self, section_id):
        return [Discussion(raw) for raw in self._get('sections/%s/discussions' % section_id)]

    def get_group_discussions(self, group_id):
        return [Discussion(raw) for raw in self._get('groups/%s/discussions' % group_id)]


    def get_district_discussion(self, district_id, discussion_id):
        return Discussion(self._get('districts/%s/discussions/%s' % (district_id, discussion_id)))

    def get_school_discussion(self, school_id, discussion_id):
        return Discussion(self._get('schools/%s/discussions/%s' % (school_id, discussion_id)))

    def get_section_discussion(self, section_id, discussion_id):
        return Discussion(self._get('sections/%s/discussions/%s' % (section_id, discussion_id)))

    def get_group_discussion(self, group_id, discussion_id):
        return Discussion(self._get('groups/%s/discussions/%s' % (group_id, discussion_id)))


    def get_district_discussion_replies(self, district_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('districts/%s/discussions/%s/comments' % (district_id, discussion_id))]

    def get_school_discussion_replies(self, school_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('schools/%s/discussions/%s/comments' % (school_id, discussion_id))]

    def get_section_discussion_replies(self, section_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('sections/%s/discussions/%s/comments' % (section_id, discussion_id))]

    def get_group_discussion_replies(self, group_id, discussion_id):
        return [DiscussionReply(raw) for raw in self._get('groups/%s/discussions/%s/comments' % (group_id, discussion_id))]


    def get_district_discussion_reply(self, district_id, discussion_id, reply_id):
        return DiscussionReply(self._get('districts/%s/discussions/%s/comments/%s' % (district_id, discussion_id, reply_id)))

    def get_school_discussion_reply(self, school_id, discussion_id, reply_id):
        return DiscussionReply(self._get('schools/%s/discussions/%s/comments/%s' % (school_id, discussion_id, reply_id)))

    def get_section_discussion_reply(self, section_id, discussion_id, reply_id):
        return DiscussionReply(self._get('sections/%s/discussions/%s/comments/%s' % (section_id, discussion_id, reply_id)))

    def get_group_discussion_reply(self, group_id, discussion_id, reply_id):
        return DiscussionReply(self._get('groups/%s/discussions/%s/comments/%s' % (group_id, discussion_id, reply_id)))


    def get_user_updates(self, user_id):
        return [Update(raw) for raw in self._get('users/%s/updates' % user_id)]

    def get_section_updates(self, section_id):
        return [Update(raw) for raw in self._get('sections/%s/updates' % section_id)]

    def get_group_updates(self, group_id):
        return [Update(raw) for raw in self._get('groups/%s/updates' % group_id)]


    # TODO: This may get something different
    def get_recent_updates(self):
        return Update(self._get('recent'))


    def get_user_update(self, user_id, update_id):
        return Update(self._get('users/%s/updates/%s' % (user_id, discussion_id)))

    def get_section_update(self, section_id, update_id):
        return Update(self._get('sections/%s/updates/%s' % (section_id, discussion_id)))

    def get_group_update(self, group_id, update_id):
        return Update(self._get('groups/%s/updates/%s' % (group_id, discussion_id)))


    # TODO: Investigate whether we can get individual comments
    def get_user_update_comments(self, user_id, update_id):
        return [UpdateComment(raw) for raw in self._get('users/%s/updates/%s/comments' % (user_id, update_id))]

    def get_section_update_comments(self, section_id, update_id):
        return [UpdateComment(raw) for raw in self._get('sections/%s/updates/%s/comments' % (section_id, update_id))]

    def get_group_update_comments(self, group_id, update_id):
        return [UpdateComment(raw) for raw in self._get('groups/%s/updates/%s/comments' % (group_id, update_id))]


    # TODO: These function names might be confusing; figure out what /reminders/type endpoint really returns
    def get_reminders(self):
        return [Reminder(raw) for raw in self._get('reminders/type')]

    def get_section_reminders(self, section_id):
        return [Reminder(raw) for raw in self._get('sections/%s/reminders/type' % section_id)]


    # TODO: Support Media Albums
    # TODO: Support Documents
    # TODO: Support Grading Scales, Rubrics, Categories, and Groups


    def get_assignments(self, section_id):
        return Assignment(self._get('section/%s/assignments' % section_id))

    def get_assignment(self, section_id, assignment_id):
        return Assignment(self._get('section/%s/assignments/%s' % (section_id, assignment_id)))


    def get_assignment_comments(self, section_id, assignment_id):
        return Assignment(self._get('section/%s/assignments/%s/comments' % (section_id, assignment_id)))

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
        return [FriendRequest(raw) for raw in self._get('users/%s/requests/friends' % user_id)]

    def get_friend_request(self, user_id, request_id):
        return FriendRequest(self._get('users/%s/requests/friends/%s' % (user_id, request_id)))


    def get_user_section_invites(self, user_id):
        return [Invite(raw) for raw in self._get('users/%s/invites/sections' % user_id)]

    def get_user_section_invite(self, user_id, invite_id):
        return Invite(self._get('users/%s/invites/sections/%s' % (user_id, invite_id)))

    def get_user_group_invites(self, user_id):
        return [Invite(raw) for raw in self._get('users/%s/invites/groups' % user_id)]

    def get_user_group_invite(self, user_id, invite_id):
        return Invite(self._get('users/%s/invites/groups/%s' % (user_id, invite_id)))

    def get_user_network(self, user_id):
        return [User(raw) for raw in self._get('users/%s/network' % user_id)['users']]


    def get_user_grades(self, user_id):
        return [Grade(raw) for raw in self._get('users/%s/grades' % user_id)['section']]


    def get_user_sections(self, user_id):
        return [Section(raw) for raw in self._get('users/%s/sections' % user_id)]

    def get_user_groups(self, user_id):
        return [Group(raw) for raw in self._get('users/%s/groups' % user_id)]

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
        return [Message(raw) for raw in self._get('messages/inbox/%s' % message_id)]

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
        # TODO: The API automatically returns the number of likers. Figure out a way to work that in for ease of use.
        return [User(raw) for raw in self._get('like/%s' % id)['users']]


    # TODO: Support all User-Specific Objects, User Information, etc. requests
