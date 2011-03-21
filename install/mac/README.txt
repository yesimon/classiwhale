NOTE: This has been tested on Mac OSX 10.6 Snow Leopard.  If you are still running something earlier, figure it out yourself.  If Lion has already come out and you have it, tell me to get off my ass and upgrade this install setup.

To install on Mac:

Install setuptools (easy_install) and python 2.7 or whatever the latest version is.

Install pip.
sudo easy_install pip

Install virtualenv (you may already have it, in which case use --upgrade):
sudo pip install virtualenv

Install virtualenvwrapper (keep track of where it puts virtualenvwrapper.sh)
sudo pip install virtualenvwrapper

You need to either call this every time or, better yet, add it to your ~/.bash_profile:
source /usr/local/bin/virtualenvwrapper.sh
using the path to virtualenvwrapper.sh you kept track of earlier.  Note that you should use the -q flag to make sure it doesn't print out like 6 lines every time you open a console.

If you want, set your environment variable $WORKON_HOME to wherever you want your virtual environments to be (otherwise, it puts it in ~/.virtualenvs)
export WORKON_HOME=~/envs

Create your virtualenv directory
mkdir -p $WORKON_HOME

Create a new virtualenv instance that won't conflict with other stuff on your system.
mkvirtualenv --no-site-packages cw-mac

Now you are in your virtual environment.  Note that the --no-site-packages flag means you don't use the site-packages you have already installed on your system for python, which means you need to re-download them.  Also, you have a python instance that is specific to your environment.  To switch out/between virtual environments, you should probably know the following commands:
workon env2 #switches you to a virtual environment env2
lssitepackages #see all the installed packages in this virtualenv
lsvirtualenv OR workon #see all your virtual environments
deactivate #switch you out of your virtual environment

Note that the Python that virtualenv sets up for your virtual environments (at least for me) is 32-bit.  This is good for our purposes, since psycopg2 is a 32-bit module, but if you want to run 64-bit virtual environment python, you need to hack on it yourself.

Note you need a Fortran compiler for the next part (to install numpy).  gfortran seems to work.  Get it if you don't already have it.

Now, we need to install numpy and scipy:

sudo pip install numpy

Now it's time to install all of our requirements to our virtual environment.

sudo pip install -r requirements.txt

Now, we need to install yaml and nltk
sudo easy_install pyyaml
sudo easy_install nltk

Finally, we need to get the stopwords from the NLTK.  Type the following:

python
import nltk
nltk.download()

And download and install nltk-corpora

