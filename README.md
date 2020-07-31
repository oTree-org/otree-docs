# oTree Documentation

[otree.readthedocs.io](http://otree.readthedocs.io/)

To contribute a translation in Chinese or Japanese:

1.   Clone this repo
1.   `pip install -r requirements.txt`
1.   Go to locales/ and edit the .po files using [poedit](http://poedit.net) or simply using a text editor
1.   To preview your changes:
    - Chinese: `sphinx-build -b html -D language=zh_CN source build/html/zh_CN`
    - Japanese: `sphinx-build -b html -D language=ja source build/html/ja`
1.   Open the HTML files in your browser and check that they look OK
1.   Commit your changes to the .po files & make a pull request.

Then, your changes will be visible at:

[https://otree.readthedocs.io/zh_CN/latest/index.html](https://otree.readthedocs.io/zh_CN/latest/index.html)
[https://otree.readthedocs.io/ja/latest/index.html](https://otree.readthedocs.io/ja/latest/index.html)

To rebuild .pot files, run `sphinx-build -b gettext source build/gettext`.