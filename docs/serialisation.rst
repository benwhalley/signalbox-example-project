Serialising data
~~~~~~~~~~~~~~~~


Read this first: `https://docs.djangoproject.com/en/dev/topics/serialization/ <https://docs.djangoproject.com/en/dev/topics/serialization/>`_.



Then see: `http://stackoverflow.com/questions/1499898/django-create-fixtures-without-specifying-a-primary-key <http://stackoverflow.com/questions/1499898/django-create-fixtures-without-specifying-a-primary-key>`_.

So, to export use:

    app/manage.py dumpdata --indent 2 --natural > data.json

Then use a regex like this to replace all pk's with null to be sure they don't clash with others in the db:

    "pk": (?<path>\d+),
