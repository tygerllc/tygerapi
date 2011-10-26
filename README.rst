==================
TygerAPI
==================

Tyger is creating an open platform to publish and solve the most important challenges in synthetic biology.

The Challenge application is written in Django and controls the creation, display and update of challenges that are submitted and solved by the Tyger community.

The Canvas application is the IDE for bio-developers.

We will use piston to create open APIs that mimic the core challenge functionality, allowing bio-developers to use the design platform of their choosing.

------------
Installation
------------
Make sure python and django are installed and running on your system. 

1. Clone from github_::

    $ git clone git@github.com:tygerllc/tygerapi.git

2. Run the server

    ./manage.py runserver

3. Direct your browser to the local address http://127.0.0.1/admin. Enter *root* for both username and password fields.


4. You are now a *superuser*. Enjoy!