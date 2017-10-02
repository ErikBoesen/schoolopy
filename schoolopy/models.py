class _base_model_class(dict):
    def __init__(self, json):
        self.json = json
        self.update(json)
        self.update(self.__dict__)
        self.__dict__ = self

    def __repr__(self):
        contents = {k: self[k] for k in self if k != 'json'}  # Exclude :json: from the string
        return '%s(%s)' % (self.__class__.__name__, dict.__repr__(contents))


def _model_class(class_name):
    return type(class_name, (_base_model_class,), {})


class Message(_base_model_class):
    def __init__(self, json):
        super().__init__(json)
        self.recipient_ids = list(map(int, self.recipient_ids.split(',')))

class School(_base_model_class):
    def __init__(self, json):
        super().__init__(json)
        self.id = int(self.id)
        self.postal_code = int(self.postal_code)

#School = _model_class('School')
