from pkglts.templating import get_comment_marker, replace


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


def test_replace_keep_template_fmt_in_pkglts_div():
    txt = """
print("toto")
# {{pkglts,
print("titi")
# }}
print("tutu")
"""
    new_txt = replace(txt, {}, {})
    assert new_txt == txt


def test_replace_keep_template_fmt_in_pkglts_div_inline():
    txt = """
print{{pkglts, ("titi")}}
"""
    new_txt = replace(txt, {}, {})
    assert new_txt == txt


def test_template_pkglts_divs_can_be_reformatted():
    txt = """
print("toto")
# {{pkglts,
print("titi")
# }}
print("tutu")
"""
    new_txt = replace(txt, {}, {})
    new_txt2 = replace(new_txt, {}, {})
    assert new_txt2 == new_txt


def test_template_pkglts_divs_can_be_reformatted2():
    txt = """
print("toto")
# {{pkglts modif,
print("titi")
# }}
print("tutu")
"""

    def modif(txt, env):
        return txt.upper()

    new_txt = replace(txt, dict(modif=modif), {})

    def modif(txt, env):
        return txt.lower()

    new_txt2 = replace(new_txt, dict(modif=modif), {})
    assert new_txt2 != new_txt


def test_template_handle_different_types_of_comments_inline():
    txt = "print#{{div, ('titi')}}"
    new_txt = replace(txt, {}, {}, comment_marker="#")
    assert new_txt == "print('titi')"

    txt = "print%{{div, ('titi')}}"
    new_txt = replace(txt, {}, {}, comment_marker="%")
    assert new_txt == "print('titi')"

    txt = "before\n.. {{div, inline}}\n\nafter"
    new_txt = replace(txt, {}, {}, comment_marker=".. ")
    assert new_txt == "before\ninline\n\nafter"


def test_template_handle_different_types_of_comments_div():
    txt = "before = 1\n# {{div,\ninside = 1\n# }}\nafter = 1"
    new_txt = replace(txt, {}, {}, comment_marker="#")
    assert new_txt == "before = 1\ninside = 1\nafter = 1"

    txt = "before = 1\n% {{div,\ninside = 1\n% }}\nafter = 1"
    new_txt = replace(txt, {}, {}, comment_marker="%")
    assert new_txt == "before = 1\ninside = 1\nafter = 1"

    txt = "before = 1\n.. {{div,\n\ninside = 1\n.. }}\n\nafter = 1"
    new_txt = replace(txt, {}, {}, comment_marker=".. ")
    assert new_txt == "before = 1\n\ninside = 1\n\nafter = 1"


def test_get_comment_marker():
    assert get_comment_marker("toto.py") == "#"
    assert get_comment_marker("toto.ini") == "#"
    assert get_comment_marker("toto.cfg") == "#"
    assert get_comment_marker("toto.yml") == "#"
    assert get_comment_marker("toto.rst") == ".. "
    assert get_comment_marker("toto.bat") == "REM "
