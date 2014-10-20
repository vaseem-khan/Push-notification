Push Web Notification System
===============
The application is a web based Push notification system implemented using node.js and socket.io.


User will post listings of the items. Other users who are interested in that particular listing can shortlist and place offer on that product. Upon shortlisting, system will send notifications to users who have shortlisted that product earlier.

We’re going to build a Django application, using the following packages, python and node.js modules:

* python
* python-virtualenv
* redis-server
* nginx (from the official Nginx ppa)
* nodejs (from Chris Leas’s ppa)
* npm, socket.io and cookie
* django
* django-user-sessions
* celery

npm packages to be installed with the project:

* cookie
* redis
* socket.io
* socket.io-redis
