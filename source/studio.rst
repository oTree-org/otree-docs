.. _studio:

oTree Studio
============

`oTree Studio <https://www.otreehub.com/studio/>`__
is a new point-and-click interface for creating oTree projects.

We have some `YouTube videos <https://www.youtube.com/channel/UCR9BIa4PqQJt1bjXoe7ffPg/videos>`__
on how to use oTree Studio.

oTree Studio will generate Python & HTML code as if you had written it by hand.

How does oTree Studio work?
---------------------------

#.  Make an account on `oTree Hub <https://www.otreehub.com/studio>`__.
    oTree Studio is part of oTree Hub
    (the other part of oTree Hub is for Heroku server deployment)
#.  Build your app in oTree Studio's point-and-click interface.
#.  When you want to test your app, download your .otreezip file and run it
    on your computer.

How to build your app in oTree Studio
-------------------------------------

:ref:`Here <tutorial-studio>` is a tutorial showing how to make a simple app in oTree Studio.
Also, this oTree documentation site is written so it applies both to oTree Studio and the code-based
version.

How to test your app
--------------------

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
You are not "locked in" to oTree Studio.


Are all oTree features supported?
---------------------------------

oTree Studio does not support all oTree features.
If at any point you need to use one of these features, you are not stuck;
you can just download the code of your project and switch to editing it in PyCharm.
(But you cannot upload those changes back into oTree Studio.)


Is oTree Studio stable?
-----------------------

oTree Studio is in beta. However, it is quite stable.
