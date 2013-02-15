Randomisation/allocation methods
--------------------------------------------------------

When a :term:`user` signs up for a study (or are added by a :term:`researcher`), then the system may automatically allocate them to a :py:class:`StudyCondition`


At present, allocation is made by one of two methods:


Weighted randomisation
~~~~~~~~~~~~~~~~~~~~~~~

Participants are allocated to :class:`~signalbox.models.StudyCondition`s within a :class:`-signalbox.models.Study` in the proportions specified by the ``weight`` property of each :class:`~signalbox.models.StudyCondition`.

For example, if there are 3 :class:`~signalbox.models.StudyCondition`s attached to a :class:`~signalbox.models.Study` and have weights 2, 2 and 3, then participants will be allocated.

.. autofunction:: signalbox.allocation.weighted_randomisation



Adaptive randomisation
~~~~~~~~~~~~~~~~~~~~~~~

The other method adapts the randomisation to attempt to balance group sizes:

.. autofunction:: signalbox.allocation.balanced_groups_adaptive_randomisation



So, the key thing to remember is to set the ``randomisation_probability`` field on the study (or leave it at it's default) to determine how frequently randomisation should be used, vs. deterministic allocation to the group which least matches the desired size (based on the StudyCondition weights).
