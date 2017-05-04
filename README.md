# The oTree Documentation

This repository contains all the tutorial and documentation of
[oTree](http://otree.org).

![RTD Badge](https://readthedocs.org/projects/otree/badge/?version=latest)

To edit:

-   Clone this repo
-   `pip install -r requirements.txt`
-   Make your edits (using [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html) syntax)
-   Build by running ``./make html`` from the root directory.
    Errors will be printed to the console, and HTML output will be in
    `build/html`. Open it in your browser and look.
-   If the HTML output looks OK, then you can push & make a pull request.
-   The content on [otree.readthedocs.org](http://otree.readthedocs.io/en/latest/index.html)
    is built only when a push is made to the oTree-org/otree-docs repo.
    For example, if you make a commit directly in the web interface,
    it will not build until the next push is made.