oTree programming For Django Devs
=================================

Intro to oTree for Django developers
------------------------------------

# TODO!


Differences between oTree and Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# TODO!

Models
^^^^^^

-  Field labels should go in the template formfield, rather than the
   model field's ``verbose_name``.
-  ``null=True`` and ``default=None`` are not necessary in your model
   field declarations; in oTree fields are null by default.
-  On ``CharField``\ s, ``max_length`` is not required.
