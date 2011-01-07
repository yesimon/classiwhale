.. _ref-algorithm:

==============================
Algorithm Interface and Driver
==============================

Interface
---------

The design of the algorithm interface was to allow the algorithm designer maximum flexibility in implementing an algorithm. You can choose to use Django models and therefore the rest of the Classiwhale database as storage, or you can use NoSQL or no storage at all. Therefore, to make the interface as general as possible, each algorithm must provide one subclass that implements the ``Classifier`` abc::

    class Classifier(object):
        """
        Abstract interface that an algorithm absolutely must implement.
        """

        # Be careful of race condition when asynch tasking on this. Essentially, 
        # don't save prof model in a task without refetching
        def __init__(self, prof):
            self.prof = prof

        @abc.abstractmethod
        def force_train(self):
            """Force a train on a user immediately"""
            return NotImplementedError

        @abc.abstractmethod
        def predict(self, statuses):
            """Predict ratings using algorithm, returns list of float from [-1 1]"""
            return NotImplementedError

The default constructor passes in a ``UserProfile`` object. This is reasonable for most classifiers. But for classifiers that are global in nature, and thus return the same results for each user, you may choose to override the default constructor and throw away the profile. The driver will still pass in prof as an argument, but you may get rid of it if your algorithm does not make use of it.


Driver
------

The driver selects the current classifier and classifier version from the UserProfile model and exec's the correct code path at that stage. For the code itself::

    def get_predictions(prof, statuses, session=None):
        """Statuses could be list of ids, list of api status objects, or list of
        django status models, inspect to decide next steps"""
        if statuses is None: return None
        if statuses[0] in (int, long):
            statuses = Status.objects.filter(id__in=statuses)
            # TODO: Do some integrity checks to make sure they are good?
        # TODO: Logic to obtain predictions from cache if at all possible
        algo = prof.active_classifier
        exec "predictions = {0}(prof).predict(statuses)\n".format(algo)
        return predictions

    def force_train(prof):
        algo, version = prof.active_classifier, prof.classifier_version
   	exec "{0}(prof).force_train()\n".format(algo)
        return

One active classifier is stored per user, while the version field is a totally "up to the algorithm designer" field. Some more likely uses of version would be for updating algorithm source code, MVCC, and asynchronous training for users.
