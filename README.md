**Note: This library is currently under active development, and does not yet support all possible API requests that Schoology does. Function names may change, and no guarantee of backward compatibility is provided at this stage in development.**

# schoolopy
Python wrapper for Schoology's API.

## Setup & Authorization
Before using the library, you'll need to initialize it as follows, using your OAuth keys:

```py
sc = schoolopy.Schoology('key', 'secret')
```

Obtain your consumer API key and secret from `[Schoology URL]/api`.

Some schools host Schoology on schoology.com, some from a subdomain like fccps.schoology.com, and some in other ways. As a rule of thumb, simply open your Schoology homepage and switch the path at the end of the URL to `/api`.

## Example
`example.py` contains sample code which may be used to run simple requests. You will need to write your key and secret into `example_config.yml.example` and rename that file to `example_config.yml`.

## Methods
This library contains a large number of functions for interaction with the API, and listing them all would be impractical.

For a comprehensive list of what endpoints are available, consult the [REST API v1 documentation](https://developers.schoology.com/api-documentation/rest-api-v1).

Most objects' functions follow a similar pattern to the following example.

`[realm]` represents the name of any realm type; in this case you can use `district`, `school`, `user`, `section`, or `group`. Valid realms may vary for different objects.

`event` represents an `Event` object.

* `sc.get_events([realm]_id=)`
* `sc.get_[realm]_events([realm]_id)`
* `sc.create_event(event, [realm]_id=)`
* `sc.create_[realm]_event(event, [realm]_id)`
* `sc.get_event(event_id, [realm]_id=)`
* `sc.get_[realm]_events([realm]_id)`
* `sc.update_event(event, event_id, [realm]_id=)`
* `sc.update_[realm]_event(event, event_id, [realm]_id)`
* `sc.delete_event(event_id, [realm]_id=)`
* `sc.delete_[realm]_event(event_id, [realm_id])`

## Author
This library was created by [Erik Boesen](https://github.com/ErikBoesen).

## Licensing
This software is available under the [MIT License](LICENSE).
