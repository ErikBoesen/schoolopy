**Note: This library is currently under active development, and does not yet support all possible API requests that Schoology does. Function names may change, and no guarantee of backward compatibility is provided at this stage in development.**

# schoolopy
Python wrapper for Schoology's API.

## Setup & Authorization
Before using the library, you'll need to initialize it as follows, using your OAuth keys:

```py
sc = schoolopy.Schoology(key, secret)
```

Obtain your consumer API key and secret from `[your school's subdomain].schoology.com/api`.

Some schools use direct logins through Schoology's website. As a general rule of thumb, go to your Schoology homepage and replace the path in the URL with `/api`.

## Example
`example.py` contains sample code which may be used to run simple requests. You will need to write your key and secret into `example_config.yml.example` and rename that file to `example_config.yml`.

## Methods
* `sc.get_messages()` - returns a list of `Message` objects representing recent direct messages to your user account.

## Author
This library was created by [Erik Boesen](https://github.com/ErikBoesen).

## Licensing
This software is available under the [MIT License](LICENSE).
