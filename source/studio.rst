.. _studio:

oTree Studio
============

`oTree Studio <https://www.otreehub.com/studio>`__
is a point-and-click interface for building oTree apps.

We recommend for new users to start with oTree Studio instead of a text editor (like PyCharm),
because it has makes learning oTree much easier and has a free 30-day trial.

Here are some `YouTube videos <https://www.youtube.com/channel/UCR9BIa4PqQJt1bjXoe7ffPg/videos>`__ about oTree Studio.

How to test your oTree Studio app
---------------------------------

See `this video <https://www.youtube.com/watch?v=b695998sx_A>`__.

1.  :ref:`Install oTree <install>`.
2.  Open your command prompt and run ``otree runzip``.
3.  In oTree Studio, click the button to download your .otreezip file.
    put in the same folder where you ran ``otree runzip`` from.
4.  The oTree server will automatically detect that the .otreezip file was downloaded,
    and run it.
5.  When you make further changes to your app in oTree Studio, repeat step 3.

.. _studio-otreezip:

About .otreezip files
---------------------

.otreezip files are just regular oTree projects.
If you want to see what is inside, run ``otree unzip``.
You will find the usual ``settings.py``, ``models.py``, ``pages.py``, HTML templates, etc.

This means that at any point, you can switch from oTree Studio to editing the
Python/HTML code manually.
