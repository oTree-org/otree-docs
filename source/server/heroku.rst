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

.. _perf:

Server performance
------------------

Heroku offers different performance tiers for resources such as your dyno and database.
What tier you need depends on how much traffic your app will get, and how it is coded.

Performance is a complicated subject since there are many factors that affect performance.
oTree Hub's Pro plan has a "monitor" section that will analyze your logs to identify
performance issues.

General tips:

-   Upgrade oTree to the latest version
-   Use browser bots to stress-test your app.
-   With the higher dyno tiers, Heroku provides a "Metrics" tab. Look at "Dyno load".
    If users are experiencing slow page load times and your your dyno load stays above 1,
    then you should get a faster dyno. (But don't run more than 1 web dyno.)
-   If your dyno load stays under 1 but page load times are still slow,
    the bottleneck might be something else like your Postgres database.


The most demanding sessions are the ones with a combination of (1) many rounds, (2) players
spending just a few seconds on each page, and (3) many players playing concurrently,
because these sessions have a high number of page requests per second, which can overload the server.
Consider adapting these games to use :ref:`live`, which will result in much faster performance.
