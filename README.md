# schoolopy
Python wrapper for Schoology's API.

## Setup & Authorization
Before using the library, you'll need to initialize it as follows, using your OAuth keys:

```py
sc = schoolopy.Schoology(key, secret)
```

Obtain your consumer API key and secret from `[your school's subdomain].schoology.com/api`.

Some schools use direct logins through Schoology's website. As a general rule of thumb, go to your Schoology homepage and replace the path in the URL with `/api`.

## Methods
* `sc.messages()` - returns a list of `Message` objects representing recent direct messages to your user account.

## Author
This library was created by [Erik Boesen](https://github.com/ErikBoesen).

## Licensing
This software is available under the [MIT License](LICENSE).
