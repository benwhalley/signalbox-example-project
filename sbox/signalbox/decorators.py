from django.contrib.auth.decorators import user_passes_test


def _is_in_group(u, group_names):
    for g in group_names:
        if bool(u.groups.filter(name__in=g)) | u.is_superuser:
            return True
    return False

def group_required(*group_names):
    """Requires user membership in at least one of the groups passed in.

    Requires a list of strings representing the group names.
    """
    def in_groups(u):
        if u.is_authenticated():
            return _is_in_group(u, group_names)
        return False

    return user_passes_test(in_groups)
