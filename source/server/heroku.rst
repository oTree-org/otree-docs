.. _heroku:

Basic Server Setup (Heroku)
===========================

`Heroku <https://www.heroku.com/>`__ is a commercial cloud hosting provider.
If you are not experienced with web server administration, Heroku may be
the simplest option for you.

The Heroku free plan is sufficient for small-scale testing of your app,
but once you are ready to launch a study, you should upgrade to a paid server,
which can handle more traffic. However, Heroku is quite inexpensive,
because you only pay for the time you actually use it.
If you run a study for only 1 day, you can turn off your dynos and addons,
and then you only pay 1/30 of the monthly cost.
Often this means you can run a study for just a few dollars.

Heroku setup
------------

New as of January 2019: the recommended way to deploy to Heroku is to use
`oTree Hub <https://www.otreehub.com/>`__,
which automates your Heroku setup and allows you to deploy
through a point-and-click interface.
It's free for public projects.

The previous instructions for deploying to oTree through the command line and git
are `here <https://pastebin.com/MiakiJaj>`__.