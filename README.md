[![Circle CI](https://circleci.com/gh/cxsmarkchan/ieee-crawler/tree/master.svg?style=svg&circle-token=a501498e163a1da45481db45f679d236ea878ba5)](https://circleci.com/gh/cxsmarkchan/ieee-crawler/tree/master)

This is a crawling tool to obtain article information of a certain journal from www.ieeexplore.org

# Installation
1. Install [mongodb](https://www.mongodb.com/download-center).

    To verify if mongodb is installed successfully, type the following codes in the shell:

    ```shell
    mongod --version
    ```

2. Install python 3.x, and pip. (You can use virtualenv if you like it)

3. For linux, install libxml2 and libxslt. For windows, download lxml model from [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml), then type the following codes:
    ```shell
    cd /path/to/ieee-crawler
    # open virtualenv if you like
    pip install wheel
    pip install /path/to/lxml-x.x.x.whl
    ```

3. Type the following codes in the shell

    ```shell
    cd /path/to/ieee-crawler
    # open virtualenv if you like
    pip install -r requirements.txt
    ```

# How to Use
1. Type the following codes in the shell

    ```shell
    cd /path/to/ieee-crawler
    mongod --dbpath db
    ```

2. Open another shell, and type the following codes:

    ```shell
    cd /path/to/ieee-crawler
    python run.py <number-of-journal> <mode>
    ```

    where:

    - **number-of-journal**: the number of the journal you are interested in. For instance, the number of "IEEE Transactions on Smart Grid" is 5165411
    - **mode**: there are three modes, i.e. "current"(current issue), "early"(early access), "new"(new articles)

    All article information will be saved into the database. If you choose Mode "new", articles already in the database will not be crawled again.
    Mode "new" can be used when you want to get the most recent articles that you've never watched before.

3. The results are saved in directory "out". There are 3 kinds of files:

    - [number-of-journal]_current_issue.txt: for current issue
    - [number-of-journal]_early_access.txt: for early access
    - [number-of-journal]_new_articles.txt: for new articles

    the name and abstract will be shown in these files.
