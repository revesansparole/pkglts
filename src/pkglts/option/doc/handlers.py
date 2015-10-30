from pkglts.templating import same

try:
    from .readme import badges, get_body
except ImportError:
    badges = same
    get_body = same

try:
    from .authors import leading_list, contributing_list
except ImportError:
    leading_list = same
    contributing_list = same

try:
    from .history import history
except ImportError:
    history = same


mapping = {'doc.badges': badges,
           'doc.lead_authors': leading_list,
           'doc.contribute_authors': contributing_list,
           'doc.history': history,
           'doc.readme_body': get_body}
