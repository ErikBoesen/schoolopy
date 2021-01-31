class _base_model(dict):
    def __init__(self, json={}):
        self.update(json)
        self.update(self.__dict__)
        self.__dict__ = self

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.json())

    def json(self):
        return dict.__repr__(self)


def _model(class_name):
    return type(class_name, (_base_model,), {})

School = _model('School')
Building = _model('Building')
User = _model('User')
Enrollment = _model('Enrollment')
Group = _model('Group')
Course = _model('Course')
Section = _model('Section')
Event = _model('Event')
BlogPost = _model('BlogPost')
BlogPostComment = _model('BlogPostComment')
Discussion = _model('Discussion')
DiscussionReply = _model('DiscussionReply')
Update = _model('Update')
UpdateComment = _model('UpdateComment')
Reminder = _model('Reminder')
MediaAlbum = _model('MediaAlbum')
Media = _model('Media')
Document = _model('Document')
GradingScale = _model('GradingScale')
GradingCategory = _model('GradingCategory')
GradingGroup = _model('GradingGroup')
Rubric = _model('Rubric')
Assignment = _model('Assignment')
FriendRequest = _model('FriendRequest')
Invite = _model('Invite')
Grade = _model('Grade')
Language = _model('Language')
Association = _model('Association')
Session = _model('Session')
MessageThread = _model('MessageThread')
Message = _model('Message')
Action = _model('Action')
Role = _model('Role')
