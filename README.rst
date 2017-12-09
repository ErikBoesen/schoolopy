schoolopy
=========

    Python wrapper for Schoology’s API.

.. image:: https://badge.fury.io/py/schoolopy.svg
    :target: https://badge.fury.io/py/schoolopy

Installation
------------
You may easily install ``schoolopy`` from PyPI with ``pip3 install schoolopy``.

Setup & Authorization
---------------------

Before any use of ``schoolopy``, you'll need to import it.

.. code:: py
    import schoolopy

You'll then need to instantiate the ``Auth`` class and, using that object, instantiate the API wrapper. There are two ways of authenticating with Schoology: two-legged and three-legged. The former is far simpler and useful for apps used by only one user who is capable of managing their own API keys, but if you're building a web app to interact with Schoology you'll need to use three-legged.

Obtain your consumer API key and secret from ``[Schoology URL]/api``.

.. code:: py
    # Two-legged
    sc = schoolopy.Schoology(schoolopy.Auth(key, secret))
    sc.get_feed()  # etc.

.. code:: py
    # Three-legged
    auth = schoolopy.Auth(key, secret, three_legged=True, domain='https://schoology.com')  # Replace URL with that of your school's Schoology
    url = auth.request_authorization()
    # Redirect user to that URL as appropriate for your application. Once user has performed action, continue.
    if not auth.authorize():
        raise SystemExit('User not authorized!')
    sc = schoolopy.Schoology(auth)

Example
-------

More in-depth examples of both two- and three-legged authentication in action can be found in ``example-twolegged.py`` and ``example-threelegged.py``. You will need to write your key and secret into ``example_config.yml.example`` and rename that file to ``example_config.yml``.

Methods
-------

This library contains a large number of functions for interaction with the API, and listing them all would be impractical.

For a comprehensive list of what endpoints are available, consult the `REST API v1 documentation <https://developers.schoology.com/api-documentation/rest-api-v1>`_.

Most objects’ functions follow a similar pattern to the following example.

``[realm]`` represents the name of any realm type; in this case you can use ``district``, ``school``, ``user``, ``section``, or ``group``. Valid realms may vary for different objects.

``event`` represents an ``Event`` object.

-  ``sc.get_events([realm]_id=)``
-  ``sc.get_[realm]_events([realm]_id)``
-  ``sc.create_event(event, [realm]_id=)``
-  ``sc.create_[realm]_event(event, [realm]_id)``
-  ``sc.get_event(event_id, [realm]_id=)``
-  ``sc.get_[realm]_events([realm]_id)``
-  ``sc.update_event(event, event_id, [realm]_id=)``
-  ``sc.update_[realm]_event(event, event_id, [realm]_id)``
-  ``sc.delete_event(event_id, [realm]_id=)``
-  ``sc.delete_[realm]_event(event_id, [realm]_id)``

Author
------

This library was created by `Erik Boesen <https://github.com/ErikBoesen>`_.

Licensing
---------

This software is available under the `MIT License <LICENSE>`_.
