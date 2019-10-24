.. _mturk-new-format:

Migrating to the new MTurk format
=================================

oTree now uses a new format for integration with MTurk.
Instead of your study appearing embedded in a frame inside the MTurk website,
workers click a link which opens your study in a separate tab.
On the last page, you give them a completion code, which they then enter into
a small form on the MTurk site.

This is a common practice for MTurk HITs, and MTurk workers are familiar with it.

Why did we make this change?
----------------------------

-   There were technical challenges to having oTree embedded inside a frame.
    Users reported "CSRF" errors that only occur inside the frame.
    When oTree is tightly integrated with MTurk, issues like this were bound to happen
    and some of them were outside oTree's control.
-   Previously it was not possible for a worker to submit an assignment if they don't get
    to the last page. For example, if they get stuck waiting for someone else on a wait page.
    With the new design, you can give them a completion code to enter if they end up waiting
    too long.
-   Previously it was not possible to do MTurk sandbox testing locally because it required an HTTPS
    server. The new design does not require HTTPS, making local sandbox testing easy.
-   Being embedded inside MTurk limits the screen space available for your study and
    may be awkward in terms of distractions, difficulty scrolling, etc.
-   You will not need special testing to see how your app works inside the MTurk frame.


How do I switch to the new design?
----------------------------------

#.  Install the new version of oTree: ``pip3 install -U otree``
#.  In your ``requirements_base.txt``, put ``otree[mturk]>=2.4.0``.
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

How can I continue using the old format?
----------------------------------------

The old format is being removed in the new versions of oTree,
so the only way to continue using it is to delay upgrading past oTree 2.2.
Use ``otree[mturk]<2.3`` in ``requirements_base.txt`` and your ``pip3 install`` commands.

Here is the
`old documentation <https://github.com/oTree-org/otree-docs/blob/cebcfbb743fced18621df9077da5ab4de8f5d25c/source/mturk.rst>`__
