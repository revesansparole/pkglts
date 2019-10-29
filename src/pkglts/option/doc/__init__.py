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
    if not url.startswith("http"):
        url = f"https://{url}"
    if not badge.startswith("http"):
        badge = f"https://{badge}"

    if fmt == 'rst':
        lines = [f".. image:: {badge}",
                 f"    :alt: {txt}",
                 f"    :target: {url}"]
        return "\n" + "\n".join(lines)

    if fmt == 'md':
        return f"[![{txt}]({badge})]({url})"

    raise UserWarning(f"Unknown format '{fmt}'")
