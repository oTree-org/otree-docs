:orphan:

.. _install-nostudio:

oTree Setup (text editor)
=========================

oTree installation
------------------

Setup commands::

    pip3 install -U otree
    otree startproject myproject
    cd myproject
    otree devserver

Open your browser to `http://localhost:8000/ <http://localhost:8000/>`__.
You should see the oTree demo site.

To create a new app, run ``otree startapp your_app_name``.

How to write oTree code with AI
-------------------------------

We have released an **AI agent** that can write oTree code
directly in your text editor.

.. note::

    This is a new beta feature as of July 2025.

Setup steps
~~~~~~~~~~~

Install Cursor
++++++++++++++

Install `Cursor <https://www.cursor.com/>`__ (you can use the free version).

Install the oTree plugin
++++++++++++++++++++++++

On the left sidebar, click the "Plugins" icon.
Search for "oTree" and install the plugin.

.. image:: _static/LLM/cursor-otree-plugin.png
   :alt: Cursor plugins

This gives you support for oTree syntax highlighting and error checking.
(Useful even if you don't use our AI features.)

Get your access keys
++++++++++++++++++++

Go to oTree Hub (register if necessary) and get your access key `here <https://www.otreehub.com/code_assistant/>`__.

Configure Cursor to use oTree's AI model
++++++++++++++++++++++++++++++++++++++++

(1) Open Cursor and click the "settings" icon at the top right.
(2) Go to the "Models" section.
(3) At the bottom, click "API Keys" to expand that section.
(4) In the "OpenAI API Key" section, enable the "Override OpenAI Base URL" option, 
    and paste in ``https://code-assistant.otreehub.com/v1``. Then verify it.
(5) Paste in your OpenAI API key and click verify.
(6) Make sure the toggle is set to "on".

Screenshots:

.. image:: _static/LLM/cursor-config.png
   :alt: Cursor settings

Check that it works
+++++++++++++++++++

Open the chat sidebar on the right and try asking it a question.
It will start with something like "I'm the oTree code assistant".

.. image:: _static/LLM/cursor-chat.png
   :alt: Cursor assistant

It will start every conversation by identifying itself as the oTree code assistant.
If it doesn't do this and says e.g. "I am a coding assistant", 
that means it's just using the regular Cursor AI model
(even if it mentions you have an oTree project).

It's important to check from time to time that you are still using oTree's AI model,
because in some situations Cursor may switch back to its built-in AI model.

oTree AI FAQ
~~~~~~~~~~~~

*"Why use this and not ChatGPT or GitHub Copilot etc?"*

When it comes to oTree programming,
ChatGPT and other tools are unreliable and often "hallucinate", 
i.e. write code that looks similar to oTree code,
but doesn't actually make sense.
Unless you are very experienced with oTree,
it's hard to tell which parts of the code are correct and which are not.

Our model is specifically designed and tested for oTree.

*"Does this require using Cursor or can I use it with Visual Studio Code / PyCharm etc?"*

These other editors may have AI features, but they don't support custom AI models.
