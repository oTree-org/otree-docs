[otree.readthedocs.io](http://otree.readthedocs.io/)

1.   Fork & download this repo
1.   Go to `locales/` and edit the .po files using [poedit](http://poedit.net) or simply using a text editor
1.   `pip install -r requirements.txt`
1.   If translating to Japanese: `sphinx-build -b html -D language=ja source build/html/ja`
1.   If translating to Chinese: `sphinx-build -b html -D language=zh_CN source build/html/zh_CN`
1.   If translating to Spanish: `sphinx-build -b html -D language=es source build/html/es`
1.   Open the HTML files in your browser and check that they look OK
1.   `git commit`
1.   Make a pull request on GitHub.

Then, your changes will be visible at:

[https://otree.readthedocs.io/ja/latest/index.html](https://otree.readthedocs.io/ja/latest/index.html)

To generate new .po files after an update to the English version, run:
		
```
sphinx-build -b gettext source build/gettext
sphinx-intl update -p build/gettext -l zh_CN -l ja 
```