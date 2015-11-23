def fmt_keywords(txt, env):
    del txt
    keywords = env['doc']['keywords']
    return ", ".join(keywords)


mapping = {'doc.setup_keywords': fmt_keywords}
