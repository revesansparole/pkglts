from pkglts.templating import replace


print(__file__)


def upper(txt, env):
    return txt.upper()


def use_env(txt, env):
    return env['toto']


def test_replace_handle_no_div():
    txt = "print 'toto'"
    new_txt = replace(txt, {}, None)
    assert txt == new_txt


def test_replace_handle_unknown_div_class():
    txt = """
print 'before'
# {{,
print 'titi'
# }}
print 'after'
"""
    new_txt = replace(txt, {}, None)
    assert new_txt == "\nprint 'before'\nprint 'titi'\nprint 'after'\n"


def test_replace_handle_non_commented_lines():
    txt = """
print 'before'
{{,
print 'titi'
}}
print 'after'
"""
    new_txt = replace(txt, {}, None)
    assert new_txt == "\nprint 'before'\n\nprint 'titi'\n\nprint 'after'\n"


def test_replace_handle_inline_div():
    txt = "print #{{, 'titi'}}"
    new_txt = replace(txt, {}, None)
    assert new_txt == "print 'titi'"


def test_replace_handle_nested_div():
    txt = "print '{{upper, titi {{, toto}} retiti}}'"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'TITI TOTO RETITI'"


def test_replace_handle_multi_class():
    txt = "print '{{toto upper, toto}}'"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'TOTO'"


def test_replace_handle_remove_class():
    txt = "print 'toto{{toto remove, titi}}'"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'toto'"


def test_replace_handle_delete_class():
    txt = "print 'toto{{toto del, titi}}'"
    handlers = {}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'toto_'"


def test_replace_handle_existing_inferior_sign_in_file():
    txt = "print '<toto>'{{remove, titi}}"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print '<toto>'"


def test_replace_pass_env_to_handlers():
    txt = "print '{{use_env, }}'"
    handlers = {'use_env': use_env}
    new_txt = replace(txt, handlers, {'toto': 'new toto'})
    assert new_txt == "print 'new toto'"


def test_replace_preserve_indentation():
    txt = "print 'toto'\n\t# {{upper, toto}}"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "print 'toto'\n\tTOTO"


def test_replace_preserve_spacing():
    txt = "title\n=====\n\n{{upper, toto}}\n\n"
    handlers = {'upper': upper}
    new_txt = replace(txt, handlers, None)
    assert new_txt == "title\n=====\n\nTOTO\n\n"


def test_replace_builtin_func_key():
    txt = "print '{{key, toto}}'"
    handlers = {}
    env = {'toto': 'aaaa'}
    new_txt = replace(txt, handlers, env)
    assert new_txt == "print 'aaaa'"


def test_replace_builtin_func_key_nested():
    txt = "print '{{key, toto.titi}}'"
    handlers = {}
    env = {'toto.titi': 'aaaa', 'toto': {'titi': 'bbbb'}}
    new_txt = replace(txt, handlers, env)
    assert new_txt == "print 'bbbb'"


def test_replace_builtin_func_unknown_key():
    txt = "print '{{key, toto}}'"
    new_txt = replace(txt, {}, {})
    assert new_txt == "print 'toto'"

    txt = "print '{{key, toto.titi}}'"
    new_txt = replace(txt, {}, {})
    assert new_txt == "print 'toto.titi'"
