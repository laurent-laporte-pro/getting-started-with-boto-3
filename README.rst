Description
===========

.. _Sphinx: http://www.sphinx-doc.org
.. _virtualenv: https://virtualenv.pypa.io

Small tutorial to demonstrate the Boto3 usage in order to work with Amazon Glacier


Identification
--------------

- **Title:** Getting started with Boto 3
- **Description:** Small tutorial to demonstrate the Boto3 usage in order to work with Amazon Glacier
- **GitHub:** https://github.com/laurent-laporte-pro/getting-started-with-boto-3
- **Keywords:** Sphinx, Documentation, Tutorial, Amazon, S3, Glacier, AWS, Boto3, Archive


Install the project
-------------------

Install the **getting-started-with-boto-3** project in a virtualenv_ by running::

    # -- Clone the repository
    cd ~/workspace
    git clone https://github.com/laurent-laporte-pro/getting-started-with-boto-3

    # -- Create a new Python executable
    cd ~/virtualenv
    virtualenv py-getting-started-with-boto-3
    source py-getting-started-with-boto-3/bin/activate

    # -- Install the dependencies (Sphinx and plugins)
    cd ~/workspace/getting-started-with-boto-3
    pip install .


Build the documentation
-----------------------

**getting-started-with-boto-3** is a Sphinx_ project.

Build **getting-started-with-boto-3** documentation by running::

    # -- Build the documentation
    cd ~/workspace/getting-started-with-boto-3
    python setup.py build_sphinx

The HTML documentation is then available in the ``dist/docs`` subdirectory.
You can open the index page: ``dist/docs/index.html``.


Release (for maintainers)
-------------------------

Before releasing: activate your virtualenv_ and move to the project's working directory::

    source ~/virtualenv/py-getting-started-with-boto-3/bin/activate
    cd ~/workspace/getting-started-with-boto-3

Prepare the next release: update the change log.

Check the release::

    python setup.py release

Commit and tag your release::

    # -- Bug fix or small improvement (spelling/typo): X.Y.Z => X.Y.Z+1
    bumpversion patch

    # -- Minor release (new articles): X.Y.Z => X.Y+1.0
    bumpversion minor

    # -- Major release (new features): X.Y.Z => X+1.0.0
    bumpversion major

Push the release::

    git push origin master
    git push origin master --tags
