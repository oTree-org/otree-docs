:orphan:

.. _install-nostudio:

oTree Setup (text editor)
=========================

Suggestion: We have released an **AI model** that can write oTree code
directly in your text editor.
You can use it in the `Cursor IDE <https://www.cursor.com/>`__.
Instructions `here <https://www.otreehub.com/code_assistant/>`__.

Setup commands::

    pip3 install -U otree
    otree startproject myproject
    cd myproject
    otree devserver

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

To create a new app, run ``otree startapp your_app_name``.

Session configs are defined in ``settings.py``.
