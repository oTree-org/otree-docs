.. _heroku:

Basic Server Setup (Heroku)
===========================

`Heroku <https://www.heroku.com/>`__ is a commercial cloud hosting provider.
It is the simplest way to deploy oTree.

The Heroku free plan is sufficient for testing your app,
but once you are ready to launch a study, you should upgrade to a paid server,
which can handle more traffic. However, Heroku is quite inexpensive,
because you only pay for the time you actually use it.
If you run a study for only 1 day, you can turn off your dynos and addons,
and then you only pay 1/30 of the monthly cost.
Often this means you can run a study for just a few dollars.

Heroku setup
------------

The recommended way to deploy to Heroku is to use
`oTree Hub <https://www.otreehub.com/>`__,
which automates your Heroku setup.
It's free for public projects.

oTree Hub also offers error/performance monitoring and a Sentry service.

The previous instructions for deploying to oTree through the command line and git
are
`here <https://github.com/oTree-org/otree-docs/blob/143a6ab7b61d54ec2be1a8bc09515d78e0b07c71/source/server/heroku.rst#heroku-setup-option-2>`__
However, you are more likely to run into issues this way and I am not able to provide much support.
