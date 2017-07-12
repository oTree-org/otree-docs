.. _mac-adhoc:

Windows Server
==============

If you are just testing your app on your personal computer, you can use
``otree runserver``. You don't need a full server setup as described below,
which is necessary for sharing your app with an audience.

Configure your PC to be a server
--------------------------------

Let's say you have developed your app on your personal computer.
If you only need computers on the same local network to access it
(e.g. your university department network) and don't need to be on the public internet,
you can follow the below steps to use your own computer as a server.

Create a firewall rule
~~~~~~~~~~~~~~~~~~~~~~

You need to allow other computers to connect to oTree through your firewall.

-   Open the Windows Firewall
-   Go to "Inbound Rules"
-   Click "New Rule"
-   Select "Port" to make a port rule
-   Under "Specific local ports", enter 80 and 8000
-   Select "Allow the connection"
-   Click "next" then choose a name for your rule (e.g. "oTree").

(If you use Skype) fix Skype issue
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Skype sometimes uses port 80, which can conflict with oTree.
Either quit Skype, or if you need to keep it running,
go in Skype to Tools > Options > Advanced > Connections
and unselect "Use port 80 and 443 for additional incoming connections".

Find your IP address
~~~~~~~~~~~~~~~~~~~~

Open PowerShell or CMD and enter ``ipconfig``.
Look for the entry ``IPv4 Address``.
Maybe it will look something like ``10.0.1.3``, or could also start with 172 or 192.

Run the server
~~~~~~~~~~~~~~

Start the server with your IP address and port 80, e.g.
``otree runserver 10.0.1.3:80``.

.. note::

    ``runserver`` is just for testing; once you've got everything running,
    you should use ``runprodserver`` as described below. That will require
    installing Redis.

Enter this IP address into the browser of another device on the same network and
you should be able to load the oTree demo page.

If it doesn't work, maybe another app is using port 80 already.

Try starting the server on port 8000 instead of 80.
and then on the client device's browser, connect to the IP address followed by ``:8000``,
e.g. ``10.0.1.3:8000``.

Make sure your IP address doesn't change
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In most university networks, your internal IP address will generally stay the same,
as long as you stay connected to the same network. If it changes unpredictably,
you can ask your IT department to add a rule on their DHCP server to always
assign the same IP to your computer.


Next steps
----------

See :ref:`server_final_steps` for steps you should take before launching your study.

Advanced
--------

(Optional) create a virtualenv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It's a best practice to use a virtualenv (though optional)::

    python3 -m venv venv_otree

You can configure PowerShell to always activate this virtualenv.
Enter::

    notepad $shell

Then put this in the file::

    cd "C:\path\to\oTree"
    . "C:\path\to\oTree\venv_otree\Scripts\activate.ps1"

(Note the dot at the beginning of the line.)


(Optional) use git
~~~~~~~~~~~~~~~~~~

The remaining steps are to deploy your code with Git as described :ref:`here <git-generic>`,
