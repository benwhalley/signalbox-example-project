
Assessors and blinded studies
=====================================

Some larger RCTs may require blinded assessments to be made, and employ assessors to interview partipants. Although assessors need access to the system to enter (and perhaps double enter) data, it's important that they don't encounter information which might compromise the blind. Such a situation would obviously occur if assessors could see the condition to which a participant was added. However less obvious situations might occur, when assessments differ between study conditions. For example, if assessors could:

- See scripts (or information from scripts) which are only relevant to a particular condition
- See observations or replies which include reference to questionnaires or instruments only shown to a particular condition.

To prevent this, assessors have only limited access to the site, and have a specific view designed to let them safely access observations and update client data. This is available at:

    ``/admin/signalbox/observations/outstanding``

From here, assessors can filter clients by username (which is likely to be a unique alphanumeric code rather than a name) and list Observations which are due to be made. This view automatically filters out observations which:

1. Have a script which is marked `breaks_blind`
2. Have been added on an ad-hoc basis (determined by checking whether the Observation has an attached script).

From this view, assessors can select an observation and enter data for it.


.. warning:: Assessor access to observations-due

    Care is needed when creating scripts and questionnaires which blind assessors will access. In particular the following must not include content which could reveal which group a participant is in as the assessor enters data:

    - `label` attribute of :class:`Script`s (this is used when listing observations for assessors)
    - The content of questionnaires themselves (clearly no questions should be visible which identify study condition – for example, therapy-relevant information).



