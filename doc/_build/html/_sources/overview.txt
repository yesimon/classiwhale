.. highlight:: rst
.. _ref-overview:

Overview
========
                                                             
The root of the source code is classiwhale.

``classiwhale/doc`` contains the source for the Sphinx documentation used to generate this.

The layout of the ``classiwhale/dxm`` project directory is fairly similar to standard django projects, while ``classiwhale/lsd`` is for handling the computational side of things (as loosely coupled to dxm as humanly possible). 

``classiwhale/lib`` is supposed to maintain libraries that we will be using - for now. We are using a customized python-twitter-0.8 api library although I have general misgivings about the library in general due to it being so heavyweight and creating custom objects. Perhaps json serialization is best for transferring data. Therefore the library is possibly what I consider the weakest part about our setup for now, and choosing another library is open for discussion, including twitter-1.4.2 which is a much lighter wrapper.

classiwhale/

- doc/
- dxm/
- lib/
- lsd/
- requirements.txt

dxm
----

This contains a number of subdirectories for "applications" which are segments of code that are modularized for maintainability reasons. 

The static folder contains all static media, such as pictures, .js, and .css files. Don't worry about packing all css or js into one file because we have an automatic js/css compressor that combines and caches these on the production server. For local development, these are separate for the sake of debugging. Also, you may use a higher level css language such as less or sass. For now, I suggest using less if you choose to do so to for consistency's sake, although the production server can compile a number of these languages. Usage of less is purely on an individual preference basis because you may still use standard css, although proper usage I believe will make your css a bit easier to understand in the future.

Each application folder is laid out according to standard django rules. For a quick overview for those new to django, there are ``templates`` folders in each application directory for templates. These folders are  where the base html templates go corresponding to each application. There may also be folders ``templatetags for custom template tags as well as ``management`` which could incorporate custom management commands. 

``local_settings.py`` is a file that you may create to overwrite settings in the global settings.py. It is not tracked on the git repository and usage of it is for your own discretion. (i.e. used on production server to turn off debug mode)

scripts is a folder for custom scripts - part of django-extensions.

``fcgi`` is a program for gracefully restarting the server on the production server - don't worry about it for local usage.

``media`` symlinks to admin media as where it is located on ubuntu. Not of concern when running local server.

Quick overview of application dirs:

- algorithmio: Interface and driver for recommendation algorithms
- analytics: Middleware handling the insertion of google analytics
- backends: Contains custom authentication backend for twitter.
- base: Contains all of the base templates global to the site.
- contact: Doesn't do anything for now, not even an installed app.
- feedback: Feedback tab cloned from some github repo.
- prediction: View code for viewing prediction - mostly for internal testing
- search: For searchbar - may be augmented by haystack later.
- status: Contains all things relevant to tweets - most code so far.
- twitterauth: Contains views/models relating to the custom twitter oauth user accounts.

lsd
---

This contains all of our algorithm and background processing code.
