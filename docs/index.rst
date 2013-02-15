SignalBox
=====================================


Overview
---------------------

SignalBox is a web application application designed to make it easy to run clinical and other studies, including large numbers of participants who must provide self-report data via email, telephone, or SMS message. Signalbox was designed to replace the numerous, ad-hoc systems which have been developed by research groups, providing a flexible, secure, and well-tested system; it may also replace expensive proprietary software for some projects.

Signalbox provides allows researchers to host studies to which participants can be recruited online; participants can then be prompted by email, SMS or automated telephone call to provide data. An administrative interface allows data to be managed and exported for analysis. A demo of the system is available at: http://signalbox.herokuapp.com

The system is open source and free to use. It is licensed under the `AGPL <http://www.gnu.org/licenses/agpl.html>_. requiring that modifications to the software in turn be released. Alternative licensing may be available by arrangement.



Functional anatomy
---------------------

Below is a description of the data model used by the system. In essence, all capitalised words are tables in the database; the text below helps describe their structural and functional interrelations.


Core components
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A :class:`~signalbox.models.Study` is lined to a number of :class:`~signalbox.models.StudyCondition`\s which can each use a number of :class:`~signalbox.models.Script`\s.  A :class:`~signalbox.models.Script` links to an :class:`~ask.models.Asker` (a questionnaire) which includes a number of :class:`~ask.models.Page`\s that contain :class:`~ask.models.Question`\s. :class:`~ask.models.Question`\s can use a :class:`~ask.models.ChoiceSet` which represents a set of :class:`~ask.models.Choice`\s which define the range of allowed :class:`~signalbox.models.Answer`\s (e.g. as part of a Likert type scale).

When a :class:`~django.contrib.auth.models.User` joins a :class:`~signalbox.models.Study` then a :class:`~signalbox.models.Membership` is created, which stores the randomisation times etc. When a :class:`~signalbox.models.Membership` is randomised to a :class:`~signalbox.models.StudyCondition` then the :class:`~signalbox.models.Script` is used to create :class:`~signalbox.models.Observation`\s (scripts use a special syntax to describe the offset at which each :class:`~signalbox.models.Observation` will be created, by default counting from when the user is randomised).

When :class:`~signalbox.models.Observation`\s are due then they are executed by a background task, causing an email, SMS to be sent, or a phone call to be made. In responding, users create a :class:`~signalbox.models.Reply` to the :class:`~signalbox.models.Observation`: A :class:`~signalbox.models.Reply` consists of multiple :class:`~signalbox.models.Answer`\s, which represent responses to individual questions.  Because a :class:`~signalbox.models.Reply` might be interrupted or left incomplete, multiple replies can be made to each :class:`~signalbox.models.Observation` (which the administrator needs to remember when the data are exported; they can chose a particular :class:`~signalbox.models.Reply` to use by marking it as canonical).



Additional components which may not always be used
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As noted above, :class:`~ask.models.Asker`\s contain :class:`~ask.models.Page`\s which in turn contain :class:`~ask.models.Question`\s. However, :class:`~ask.models.Page`\s can also contain :class:`~ask.models.Instrument`\s, which represent a bundle of :class:`~ask.models.Question`\s which are commonly shown together (e.g. a psychometric scale).

:class:`~signalbox.models.Script``s` generate :class:`~signalbox.models.Observation`\s, but can also generate :class:`~signalbox.models.Reminder`\s for those :class:`~signalbox.models.Observation`\s, and these send an additional messages to users at intervals after the :class:`~signalbox.models.Observation` falls due.

:class:`~signalbox.models.Script`\s can also have :class:`~signalbox.models.ScoreSheet`\s attached to them, which are sets of rules which describe how a set of :class:`~ask.models.Answer`\s in response to the Script's Asker can be reduced to a single number (e.g. the mean or total for a set of Questions). ScoreSheets create scores which can be viewed for a particular User (e.g. to check whether a user meets a criteria for study entry from a screening questionnaire). ShowIfs are rules which evaluate to a boolean (yes/no) based on Replies Users have previously made (or Replies that are in progress). ShowIfs can be used to determine whether a particular Question should be shown based on previous responses. They can also be used to create new Observations based on a Reply, using an ObservationCreator. For example, if a User completes a depression questionnaire (Asker) and a ScoreSheet computes they have scored above a certain threshold, then an additional Observation could be created and a followup email sent.

Users are linked to a UserProfile which can contain additional fields like a telephone number, address etc. A Study can specify the subset of these fields which are required when a user signs up. ContactRecords are made when the administration interface is used to send a User a message. In some studies, its necessary to collect data from some Users (e.g. therapists) about other Users (e.g. clients); where this is the case a Membership can store an additional field indicating which User the data is about, as well as who it has been collected from

StudySites represent different locations in a multi-site trial, can can be used to filter Memberships when viewing date. StudyPeriods represent ranges of days which the Membership has been randomised, and can again be used to filter Replies.




Signalbox Documentation
--------------------------

.. toctree::
    :maxdepth: 1

    overview
    roles

    apps/signalbox
    apps/ask
    apps/twiliobox
    apps/rct

    managing_data

    apps/reference
    site-specific-settings
    system-requirements

    install-and-management

    glossary



Reframed trial documentation
-----------------------------

.. toctree::
    :maxdepth: 1

    cms
    usage-policies
    study-setup
    frequent-tasks
    markdown



Developer Notes
-------------------------------------

.. toctree::
    :maxdepth: 1

    developer


Indices and tables
----------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

