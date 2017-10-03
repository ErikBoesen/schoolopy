from .models import *
import requests
import time
import random
import json


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

    def get_district_events(self, id):
        return [Event(raw) for raw in self._get('districts/%s/events' % id)]

    def get_school_events(self, id):
        return [Event(raw) for raw in self._get('schools/%s/events' % id)]

    def get_user_events(self, id):
        return [Event(raw) for raw in self._get('users/%s/events' % id)]

    def get_section_events(self, id):
        return [Event(raw) for raw in self._get('sections/%s/events' % id)]

    def get_group_events(self, id):
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


    def get_district_blog_posts(self, id):
        return [BlogPost(raw) for raw in self._get('districts/%s/posts' % id)]

    def get_school_blog_posts(self, id):
        return [BlogPost(raw) for raw in self._get('schools/%s/posts' % id)]

    def get_user_blog_posts(self, id):
        return [BlogPost(raw) for raw in self._get('users/%s/posts' % id)]

    def get_section_blog_posts(self, id):
        return [BlogPost(raw) for raw in self._get('sections/%s/posts' % id)]

    def get_group_blog_posts(self, id):
        return [BlogPost(raw) for raw in self._get('groups/%s/posts' % id)]


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

    # TODO: Support all User-Specific Objects, User Information, etc. requests
