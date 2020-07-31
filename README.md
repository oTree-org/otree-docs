# The oTree Documentation

This repository contains all the tutorial and documentation of
[oTree](http://otree.org).

![RTD Badge](https://readthedocs.org/projects/otree/badge/?version=latest)

To edit:

-   Clone this repo
-   `pip install -r requirements.txt`
-   Make your changes
-   Run ``./make html``
-   Open the HTML files in your browser and check that they look OK
-   If the HTML output looks OK, then you can push & make a pull request.

To contribute a translation to a different language:

-   Check whether your language is eligible for translation (look in the `locales/` folder).
-   Clone this repo
-   `pip install -r requirements.txt`
-   Go to locales/ and edit the .po files for your language in poedit or simply using a text editor
-   Build the docs, using your language code (e.g. zh_CN for Chinese): `sphinx-build -b html -D language=zh_CN source build/html/zh_CN`    
-   Open the HTML files in your browser and check that they look OK
-   If the HTML output looks OK, then commit your changes to the .po files & make a pull request.

Note: The content on [otree.readthedocs.org](http://otree.readthedocs.io/en/latest/index.html)
is built only when a push is made to the oTree-org/otree-docs repo.
It will not build immediately after a pull request is accepted.