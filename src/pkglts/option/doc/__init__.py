def fmt_badge(badge, url, txt):
    lines = [".. image:: https://%s" % badge,
             "    :alt: %s" % txt,
             "    :target: https://%s" % url]
    return "\n" + "\n".join(lines)

