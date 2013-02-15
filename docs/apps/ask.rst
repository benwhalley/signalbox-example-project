
The 'Ask' Application
=====================================


The ask application deals with creating and displaying questionnaires.

Questionnaires can be spread across multiple pages, and consist of questions. Questions can also be grouped into Instruments, which can be placed in a block into a page.


Structure of questionnaires
------------------------------------



XXX AS DIAGRAM?

Questionnaire – collection of pages that you ask people to complete at a certain time point
    Page – this is literally the page view (e.g. one questionnaire will be one 1 page)
        Questions – individual questions
        Instruments – this can be a set of questions / questionnaire
            Score Sheet – can be used to calculate sum or mean scores of scales
Questions
                    Type – e.g. multiple choice, yes/no, etc.
Choice Set – e.g. totally agree – totally
disagree
                            Choice – e.g. totally agree




Creating questions
------------------

Questions can be created individually (/admin/ask/question/add/), or in bulk (/ask/bulk/question/add/).


Questions are created by using django form field elements, and extending them with additional information required by signalbox.  The types of questions which can be created are documented here: :ref:`question-types`


The fields and widgets are as described in the floppyforms documentation: http://django-floppyforms.readthedocs.org/en/latest/widgets-reference.html



In addition, for IVR telephone calls, there are:

- Uninterruptible instruction (this speaks the text of the questions, but without allowing the user to 'barge-in'and skip the text by pressing a key, as is the case with a normal instruction question.)
- Listen (records audio of the user)
- Hangup (speaks the text of the question and then ends the current call; it is required that the asker ends with a hangup question)




Fields and Widgets
------------------------

The type of field shown to the user is determined by the question_type, and also by attributes held on the Question.

Field and widget Types are as as follows: XXX floppy forms

Additional attributes can be passed to widgets with the `widget_kwargs` attribute of questions. This is a json formatted string, which must deserialise to a python dictionary. The `attrs` key is probably the most useful for passing to widgets.

.. This is an example for the slider-range widget:

.. 	{
.. 	  "attrs": {
.. 	    "max": 400,
.. 	    "step": 100,
.. 	    "value": 100,
.. 	    "min": 0
.. 	  }
.. 	}



Choices and ChoiceSets
----------------------------------------------------------

For structured questions (e.g. pulldown, multiple choice) it is necessary to create a ChoiceSet. This consists of a series of options users must select from. The order attribute of choices determines their position in the html output. The score attribute determines the value saved when the user selects the option.

'Reversed' scoring of questionnaires
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When setting up Questionnaires or Instruments which use 'reversed-scoring', it's possible to do this in two ways. Either:

1. Use the same choiceset for all questions, and reverse scores as necessary in a stats package later (see the option to add stata syntax to instruments xxx)

2. Simply set up two choice sets for the same questionnaire, where for one of them the actual scoring is reversed. Then give them the appropriate name (e.g. HAM-D and HAM-D_reversed). Note, if using ScoreSheets you must set up instruments in this way, or computed sum scores will not make sense.


:warning: It is important to document which option you have chosen, preferably in the notes to the :class:`Instrument` object.




Approximate completion times for questionnaires
------------------------------------------------

These are calculated by a method on the Asker (Questionnaire) model:

.. automethod:: ask.models.Asker.approximate_time_to_complete




Displaying summary scores in ShowScore questions
---------------------------------------------------------

Read about ScoreSheets first XXX

For ShowScore questions, a summary scores will be substituded for the string '{{score}}'. Enter question text as normal, including the {{score}} string, and the score will be substituted as the page is displayed to the user.





Repeating questions within a Questionnaire
----------------------------------------------------

Each question must have unique variable name which will be used to identify data collected. If a question is to be repeated within a questionnaire, it should either be duplicated and given a second, different, name, or placed within an Instrument, and that Instrument given a prefix.





Instruments and question re-use
------------------------------------

Instruments are packages fo questions which can be placed as a unit within a questionnaire, e.g. for
a psychometric scales which will be used in multiple studies.

A useful property of instruments embedded within questionnaires is the ability to make all questions
required or not-required with a single checkbox. This can be turned on once testing is over to
ensure participants complete all questions.








