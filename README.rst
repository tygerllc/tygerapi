TygerAPI
==================

Tyger is creating an open platform to publish and solve the most important challenges in synthetic biology.

The Challenge application is written in Django and controls the creation, display and update of challenges that are submitted and solved by the Tyger community.

The Canvas application (Bench) is the IDE for bio-developers.

We will use piston to create open APIs that mimic the core challenge functionality, allowing bio-developers to use the design platform of their choosing.

Installation
------------
Make sure python and django are installed and running on your system. 

Also, make sure the following dependencies are installed on your working environment:

* `Piston <https://bitbucket.org/jespern/django-piston/wiki/Home>`_
* `South <http://south.aeracode.org/>`_
* `tagging <http://code.google.com/p/django-tagging/>`_
* `profiles <https://bitbucket.org/ubernostrum/django-profiles>`_


To run the project:

1. Clone from github:

    $ git clone git@github.com:tygerllc/tygerapi.git

2. Run the server::

    ./manage.py runserver

3. Direct your browser to the local address http://127.0.0.1:8000/. Enter *root* for both username and password fields.


4. Enjoy!