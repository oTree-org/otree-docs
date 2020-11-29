.. _mturk-new-format:

Migrating to the new MTurk format
=================================

oTree now uses a new format for integration with MTurk.
Instead of your study appearing embedded in a frame inside the MTurk website,
workers click a link which opens your study in a separate tab.
On the last page, you give them a completion code, which they then enter into
a small form on the MTurk site.

This is a common practice for MTurk HITs, and MTurk workers are familiar with it.

How do I switch to the new design?
----------------------------------

#.  Install the new version of oTree: ``pip3 install -U otree``
#.  In your ``requirements.txt`` or ``requirements_base.txt``, put ``otree[mturk]>=2.4.0``.
#.  Remove the next_button on the last page of your study.
    oTree will no longer automatically submit the assignment to MTurk;
    instead, you should give them a completion code they can paste into the MTurk site.
#.  In your MTurk HIT settings, change ``'preview_template''`` to
    ``template``, and change its value from ``'global/MTurkPreview.html'`` to ``'global/mturk_template.html'``.
#.  Follow the rest of the instructions :ref:`here <mturk>`.

Once you have done all the above, the process for publishing to MTurk and paying workers is the same
(although the "publish" page looks different because various elements have been removed).

Also, you can test in the MTurk sandbox locally.
With this new version,
you don't need to upload to Heroku until you launch the live (non-Sandbox) HIT.