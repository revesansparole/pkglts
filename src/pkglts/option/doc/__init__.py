def fmt_badge(badge, url, txt, fmt):
    if fmt == 'rst':
        lines = [".. image:: https://%s" % badge,
                 "    :alt: %s" % txt,
                 "    :target: https://%s" % url]
        return "\n" + "\n".join(lines)

    if fmt == 'md':
        return "[![%s](%s)](%s)" % (txt, badge, url)

    raise UserWarning("Unknown format '{}'".format(fmt))
