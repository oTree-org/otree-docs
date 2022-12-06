:orphan:

.. _install-nostudio:

oTree Setup (text editor)
=========================

.. warning::

    Using oTree with a text editor is not recommended for most users.
    **If someone advised you to use a text editor,
    please direct any oTree questions to them.**

Setup commands::

    pip3 install -U otree
    otree startproject myproject
    cd myproject
    otree devserver

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

To create a new app, run ``otree startapp your_app_name``.

Session configs are defined in ``settings.py``.
