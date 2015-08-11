Deprecation Policy
------------------

Deprecation is an attribute applied to a computer software feature,
characteristic, or practice to indicate that it should be avoided
(often because it is being superseded).

While a deprecated software feature remains in the software, its use may
raise warning_ messages recommending alternative practices; deprecated
status may also indicate the feature will be removed in the future.
Features are deprecated rather than immediately removed, to provide
`backward compatibility`_ and give programmers time to bring affected code
into compliance with the new standard. [WDPR]_


Deprecation Policy in oTree
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Occasionally, when you execute your oTree code you may get a message like this:

.. code-block:: python

    [WARNING|2015-07-05 22:28:26,358] py.warnings > file.py:1:
        OTreeDeprecationWarning: Call to deprecated function 'otree.foo'.
        Instead please use 'otree.modern_foo'

Here is a breakdown of the information contained:

- ``[WARNING|2015-07-05 22:28:26,358] py.warning``: information about when the
  deprecated code is called.
- ``file.py:1`` File and line number containing the deprecated code.
- ``OTreeDeprecationWarning``: This is the class that oTree use for manage
  his deprecated code.
- The next part is the deprecation message that informs the function ``otree.foo``
  is deprecated and suggest to you to use ``otree.modern_foo`` instead.

When you get a message like this take in account that the function
``otree.foo`` will be removed from future versions of oTree.


``OTreeDeprecationWarning`` Settings
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can change how ``OTreeDeprecationWarning`` informs about a deprecated
function.

In the file ``settings.py`` you can add a configuration with the name
``OTREE_DEPRECATION_WARNING``. This key can accept all the values from
`Python warning filter`_


+---------------+-------------------------------------------------------+
| Value         | Disposition                                           |
+===============+=======================================================+
| ``"error"``   | turn otree deprecation warnings into exceptions       |
+---------------+-------------------------------------------------------+
| ``"ignore"``  | never print otree deprecation warnings                |
+---------------+-------------------------------------------------------+
| ``"always"``  | always print otree deprecation warnings               |
+---------------+-------------------------------------------------------+
| ``"default"`` | print the first occurrence of otree deprecation       |
|               | warnings for each location where the warning          |
|               | is issued                                             |
+---------------+-------------------------------------------------------+
| ``"module"``  | print the first occurrence of otree deprecation       |
|               | warnings for each module where the warning            |
|               | is issued                                             |
+---------------+-------------------------------------------------------+
| ``"once"``    | print only the first occurrence of otree deprecation  |
|               | warnings, regardless of location                      |
+---------------+-------------------------------------------------------+


Using oTree Deprecation facility from your app
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. warning::

    This is an advanced feature mostly used internally in oTree.

If you develop an experiment in several steps over the months, and in some
intermediate step you want to remove some functionality, is a good idea to
first deprecate your old code before the real deletion.

oTree brings a module for integrating your deprecation cycle inside oTree policy.

**First Case: Deprecate a function or method.**

For example if you have a ``app.models.SubSession`` model with a custom funcion
like *my_custom_function* used in ``before_session_starts``

.. code-block:: python

    class Subsession(otree.models.BaseSubsession):

        def my_custom_function(self):
            some logic here

        def before_session_starts(self):
            self.my_custom_function()


and you want to rename it *my_custom_method* and you are not sure
if this method is called from another file. oTree helps you with this decorator

.. code-block:: python

    from otree import deprecate

    class Subsession(otree.models.BaseSubsession):

        @deprecate.deprecated("my_custom_method")
        def my_custom_function(self):
            self.my_custom_method()

        def my_custom_method(self):
            some logic here

        def before_session_starts(self):
            self.my_custom_method()


As you can see all the logic is now in *my_custom_method* and the old code only
calls it.

**Second Case: Deprecate a an entire module or some part of an arbitrary code.**

For this case you can show a warning with a function ``deprecate.dwarning``.
*dwarning* accept as parameter a single message to be show.

For example:

.. code-block:: python

    from otree import deprecate

    deprecate.dwarning(
        "This entire module is deprecated. Please search for an alternative")


.. _warning: https://docs.python.org/2/library/warnings.html
.. _backward compatibility:
    https://en.wikipedia.org/wiki/Backward_compatibility
.. _python warning filter:
    https://docs.python.org/2/library/warnings.html#default-warning-filters

.. [WDPR] https://en.wikipedia.org/wiki/Deprecation

