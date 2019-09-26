.. _mturk-new-format:

Migrating to the new MTurk format
=================================

oTree is currently testing a new format for integration with MTurk.
Instead of your study appearing embedded in a frame inside the MTurk website,
workers will click a link which opens your study in a separate tab.
On the last page, you give them a completion code, which they then enter into
a small form on the MTurk site.

This is a common design and MTurk workers are familiar with it.

Why are we making this change?
------------------------------

-   There are technical challenges to having oTree embedded inside a frame.
    Many users recently reported "CSRF" errors that only occur with MTurk studies.
-   Being embedded inside a frame is a "tight integration" with MTurk,
    meaning that whenever oTree is updated, we need to do special testing
    to ensure that oTree still works well inside the MTurk frame.
    It is hard to do this in an automated and reliable way.
-   Currently it's not possible for a worker to submit an assignment if they don't get
    to the last page. For example, if they get stuck waiting for someone else on a wait page.
    With the new design, you could give them a completion code to enter if they end up waiting
    too long.
-   Currently it is hard to do MTurk sandbox testing locally because it requires an HTTPS
    server. The new design does not require HTTPS.
-   Being embedded inside MTurk limits the screen space available for your study and
    may be awkward in terms of distractions, difficulty scrolling, etc.

How do I switch to the new design?
----------------------------------

#.  Install the new beta of oTree: ``pip3 install -U --pre otree``
#.  In your ``requirements_base.txt``, put ``otree[mturk]>=2.4.0b1``.
#.  Remove the "next button" on the last page of your study.
    (oTree will no longer automatically submit the assignment to MTurk.)
#.  On the last page of your study, give the user a completion code.
    For example, you can simply display:
    "You have completed the study. Your completion code is TRUST2020."
    If you like, you can generate unique completion codes.
    You don't need to worry too much about completion codes,
    because oTree tracks each worker by their MTurk ID and displays that in
    the admin interface and shows whether they arrived on the last page or not.
    The completion code is just an extra layer of verification, and it gives
    workers a specific objective which they are used to having.
#.  In your MTurk HIT settings, replace ``preview_template`` with
    ``template``, and make it point to an HTML file with the following contents:

.. code-block:: html+django

    <script src="https://assets.crowd.aws/crowd-html-elements.js"></script>

    <crowd-form>
      <div style="padding: 20px">
        <p>
          This HIT is an academic experiment on decision making from XYZ University....
          After completing this HIT, you will receive your reward plus a bonus payment....
        </p>

        <p>After
          you have accepted this HIT, the URL to the study will appear here: <b><a class="otree-link">link</a></b>.
        </p>
        <p>
          On the last page, you will be given a completion code.
          Please copy/paste that code below.
        </p>

        <crowd-input name="completion_code" label="Enter your completion code here" required></crowd-input>
        <br>
      </div>
    </crowd-form>

Modify the content inside the ``<crowd-form>`` as you wish, but make sure it has the following:

#.  The link to the study, which should look like ``<a class="otree-link">Link text</a>``.
    Once the user has accepted the assignment, oTree will automatically add the ``href`` to those links to make them point to your study.
#.  If you want the completion code to be displayed in the oTree Admin interface (Payments tab),
    you need a ``<crowd-input>`` named ``completion_code``.

You can easily test the appearance of this template by double-clicking the HTML file to open it in your browser.

Once you have done all the above, the process for publishing to MTurk is the same
(although the "publish" page looks different because various elements have been removed).

Also, you can test in the MTurk sandbox locally. 
(Before 2.4 you needed to first push to an HTTPS server like Heroku first.)