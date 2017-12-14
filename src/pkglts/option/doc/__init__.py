"""
helper function for formatting documentation.
"""


def fmt_badge(badge, url, txt, fmt):
    """Produce valid img hyperlink.

    Args:
        badge (str): url of img
        url (str): url target of link
        txt (str): associated text
        fmt (str): doc format either 'rst' or 'md'

    Returns:
        (str)
    """
    if fmt == 'rst':
        lines = [".. image:: https://%s" % badge,
                 "    :alt: %s" % txt,
                 "    :target: https://%s" % url]
        return "\n" + "\n".join(lines)

    if fmt == 'md':
        return "[![%s](%s)](%s)" % (txt, badge, url)

    raise UserWarning("Unknown format '{}'".format(fmt))
