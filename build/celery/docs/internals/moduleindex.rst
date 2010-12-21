.. _internals-module-overview:

==============
 Module Index
==============

.. contents::
    :local:

Worker
======

celery.worker
-------------

* :class:`~celery.worker.WorkController`

This is the worker's main process. It starts and stops all the components
required by the worker: Pool, Mediator, Scheduler, ClockService, and Listener.

* :func:`~celery.worker.process_initializer`

This is the function used to initialize pool processes. It sets up loggers and
imports required task modules, etc.

celery.worker.job
-----------------

* :class:`~celery.worker.job.TaskRequest`

A request to execute a task. Contains the task name, id, args and kwargs.
Handles acknowledgement, execution, writing results to backends and error handling
(including error e-mails)

celery.worker.pool
------------------

celery.worker.listener
----------------------

celery.worker.controllers
-------------------------

celery.worker.scheduler
-----------------------

celery.worker.buckets
---------------------

celery.worker.heartbeat
-----------------------

celery.worker.revoke
--------------------

celery.worker.control
---------------------

* celery.worker.registry

* celery.worker.builtins


Tasks
=====

celery.decorators
-----------------

celery.registry
---------------

celery.task
-----------

celery.task.base
----------------

celery.task.http
----------------

celery.task.control
-------------------

celery.task.builtins
--------------------

Execution
=========

celery.execute
--------------

celery.execute.trace
--------------------

celery.result
-------------

celery.states
-------------

celery.signals

Messaging
=========

celery.messaging
----------------

Result backends
===============

celery.backends
---------------

celery.backends.base
--------------------

celery.backends.amqp
--------------------

celery.backends.database
------------------------

Loaders
=======

celery.loaders
--------------

Loader autodetection, and working with the currently
selected loader.

celery.loaders.base - Loader base classes
-----------------------------------------

celery.loaders.default - The default loader
-------------------------------------------

CeleryBeat
==========

celery.beat
-----------

Events
======

celery.events
-------------

Logging
=======

celery.log
----------

celery.utils.patch
------------------

Configuration
=============

celery.conf
-----------

Miscellaneous
=============

celery.datastructures
---------------------

celery.exceptions
-----------------

celery.platform
---------------

celery.utils
------------

celery.utils.info
-----------------

celery.utils.compat
-------------------
