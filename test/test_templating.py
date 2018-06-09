from pkglts.templating import parse_source


def test_parse_finds_all_blocks():
    txt = ("print 'toto'\n"
           "print 'titi'\n"
           "# {# pkglts, bid\n"
           "this is content\n"
           "# #}\n"
           "after block")
    blocks = parse_source(txt)
    assert len(blocks) == 3
    b1, b2, b3 = blocks
    assert b1.before_header == ""
    assert b1.bid is None
    assert b1.after_header == ""
    assert b1.content == ("print 'toto'\n"
                          "print 'titi'\n")
    assert b1.before_footer == ""
    assert b1.after_footer == ""

    assert b2.before_header == "# "
    assert b2.bid == "bid"
    assert b2.after_header == ""
    assert b2.content == "this is content\n"
    assert b2.before_footer == "# "
    assert b2.after_footer == ""

    assert b3.before_header == ""
    assert b3.bid is None
    assert b3.after_header == ""
    assert b3.content == "after block"
    assert b3.before_footer == ""
    assert b3.after_footer == ""


def test_parse_finds_bef_after_header():
    txt = ("print 'toto'\n"
           "print 'titi'\n"
           "# bef header{# pkglts, bid after header\n"
           "this is content\n"
           "# #}\n"
           "after block")
    blocks = parse_source(txt)
    assert len(blocks) == 3
    _, block, _ = blocks
    assert block.before_header == "# bef header"
    assert block.bid == "bid"
    assert block.after_header == " after header"
    assert block.content == "this is content\n"
    assert block.before_footer == "# "
    assert block.after_footer == ""


def test_parse_finds_bef_after_footer():
    txt = ("print 'toto'\n"
           "print 'titi'\n"
           "# {# pkglts, bid\n"
           "this is content\n"
           "# bef footer#} after footer\n"
           "after block")
    blocks = parse_source(txt)
    assert len(blocks) == 3
    _, block, _ = blocks
    assert block.before_header == "# "
    assert block.bid == "bid"
    assert block.after_header == ""
    assert block.content == "this is content\n"
    assert block.before_footer == "# bef footer"
    assert block.after_footer == " after footer"


def test_parse_finds_single_pkglts_block():
    txt = ("# {# pkglts, bid\n"
           "this is content\n"
           "# bef footer#} after footer\n")
    blocks = parse_source(txt)
    for block in blocks:
        print("bl", block)
    assert len(blocks) == 1
    block, = blocks
    assert block.before_header == "# "
    assert block.bid == "bid"
    assert block.after_header == ""
    assert block.content == "this is content\n"
    assert block.before_footer == "# bef footer"
    assert block.after_footer == " after footer"

#
#
# def upper(txt, env):
#     del env
#     return txt.upper()
#
#
# def use_env(txt, env):
#     del txt
#     return env['toto']
#
#
# def test_replace_handle_no_div():
#     txt = "print 'toto'"
#     new_txt = replace(txt, {}, None)
#     assert txt == new_txt
#
#
# def test_replace_handle_bracket_end():
#     txt = "d = {'toto': 1}"
#     new_txt = replace(txt, {}, None)
#     assert txt == new_txt
#
#     txt = "d = {'toto': 1{"
#     new_txt = replace(txt, {}, None)
#     assert txt == new_txt
#
#
# def test_replace_handle_unknown_div_class():
#     txt = """
# print 'before'
# # {{,
# print 'titi'
# # }}
# print 'after'
# """
#     new_txt = replace(txt, {}, None)
#     assert new_txt == "\nprint 'before'\nprint 'titi'\nprint 'after'\n"
#
#
# def test_replace_handle_non_commented_lines():
#     txt = """
# print 'before'
# {{,
# print 'titi'
# }}
# print 'after'
# """
#     new_txt = replace(txt, {}, None)
#     assert new_txt == "\nprint 'before'\n\nprint 'titi'\n\nprint 'after'\n"
#
#
# def test_replace_handle_inline_div():
#     txt = "print #{{, 'titi'}}"
#     new_txt = replace(txt, {}, None)
#     assert new_txt == "print 'titi'"
#
#
# def test_replace_handle_nested_div():
#     txt = "print '{{upper, titi {{, toto}} retiti}}'"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print 'TITI TOTO RETITI'"
#
#
# def test_replace_handle_multi_class():
#     txt = "print '{{toto upper, toto}}'"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print 'TOTO'"
#
#
# def test_replace_handle_remove_class():
#     txt = "print 'toto{{toto remove, titi}}'"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print 'toto'"
#
#
# def test_replace_handle_delete_class():
#     txt = "print 'toto{{toto del, titi}}'"
#     handlers = {}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print 'toto_'"
#
#
# def test_replace_handle_existing_inferior_sign_in_file():
#     txt = "print '<toto>'{{remove, titi}}"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print '<toto>'"
#
#
# def test_replace_pass_env_to_handlers():
#     txt = "print '{{use_env, }}'"
#     handlers = {'use_env': use_env}
#     new_txt = replace(txt, handlers, {'toto': 'new toto'})
#     assert new_txt == "print 'new toto'"
#
#
# def test_replace_preserve_indentation():
#     txt = "print 'toto'\n\t# {{upper, toto}}"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "print 'toto'\n\tTOTO"
#
#
# def test_replace_preserve_upstream_fmt1():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_upstream_fmt2():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
#
# # {{upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
#
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_upstream_fmt3():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper,
# inside = 1
# # }}
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_upstream_fmt4():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
#
# # {{upper,
# inside = 1
# # }}
# after = 1
# """
#     res = """
# before = 1
#
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_upstream_fmt5():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
#
# # {{upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
#
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_upstream_fmt6():
#     handlers = {'upper': upper}
#
#     txt = """
#  {{upper, inside = 1}}
# after = 1
# """
#     res = """
#  INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None, ".. ")
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt1():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt2():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper, inside = 1}}
#
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
#
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt3():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper,
# inside = 1
# # }}
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt4():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper,
# inside = 1
# # }}
#
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
#
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt5():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper,
# inside = 1
#
# # }}
# after = 1
# """
#     res = """
# before = 1
# INSIDE = 1
#
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_downstream_fmt6():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{upper,
#
# inside = 1
#
# # }}
# after = 1
# """
#     res = """
# before = 1
#
# INSIDE = 1
#
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_replace_preserve_spacing():
#     txt = "title\n=====\n\n{{upper, toto}}\n\n"
#     handlers = {'upper': upper}
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == "title\n=====\n\nTOTO\n\n"
#
#
# def test_replace_builtin_func_key():
#     txt = "print '{{key, toto}}'"
#     handlers = {}
#     env = {'toto': 'aaaa'}
#     new_txt = replace(txt, handlers, env)
#     assert new_txt == "print 'aaaa'"
#
#
# def test_replace_builtin_func_key_nested():
#     txt = "print '{{key, toto.titi}}'"
#     handlers = {}
#     env = {'toto.titi': 'aaaa', 'toto': {'titi': 'bbbb'}}
#     new_txt = replace(txt, handlers, env)
#     assert new_txt == "print 'bbbb'"
#
#
# def test_replace_builtin_func_unknown_key():
#     txt = "print '{{key, toto}}'"
#     new_txt = replace(txt, {}, {})
#     assert new_txt == "print 'toto'"
#
#     txt = "print '{{key, toto.titi}}'"
#     new_txt = replace(txt, {}, {})
#     assert new_txt == "print 'toto.titi'"
#
#
# def test_replace_keep_template_fmt_in_pkglts_div():
#     txt = """
# print("toto")
# # {{pkglts,
# print("titi")
# # }}
# print("tutu")
# """
#     new_txt = replace(txt, {}, {})
#     assert new_txt == txt
#
#
# def test_replace_keep_template_fmt_in_pkglts_div_inline():
#     txt = """
# print{{pkglts, ("titi")}}
# """
#     new_txt = replace(txt, {}, {})
#     assert new_txt == txt
#
#
# def test_template_pkglts_divs_can_be_reformatted():
#     txt = """
# print("toto")
# # {{pkglts,
# print("titi")
# # }}
# print("tutu")
# """
#     new_txt = replace(txt, {}, {})
#     new_txt2 = replace(new_txt, {}, {})
#     assert new_txt2 == new_txt
#
#
# def test_template_pkglts_divs_can_be_reformatted2():
#     txt = """
# print("toto")
# # {{pkglts modif,
# print("titi")
# # }}
# print("tutu")
# """
#
#     def modif(txt, env):
#         return txt.upper()
#
#     new_txt = replace(txt, dict(modif=modif), {})
#
#     def modif(txt, env):
#         return txt.lower()
#
#     new_txt2 = replace(new_txt, dict(modif=modif), {})
#     assert new_txt2 != new_txt
#
#
# def test_template_handle_different_types_of_comments_inline():
#     txt = "print#{{div, ('titi')}}"
#     new_txt = replace(txt, {}, {}, comment_marker="#")
#     assert new_txt == "print('titi')"
#
#     txt = "print%{{div, ('titi')}}"
#     new_txt = replace(txt, {}, {}, comment_marker="%")
#     assert new_txt == "print('titi')"
#
#     txt = "before\n.. {{div, inline}}\n\nafter"
#     new_txt = replace(txt, {}, {}, comment_marker=".. ")
#     assert new_txt == "before\ninline\n\nafter"
#
#
# def test_template_handle_different_types_of_comments_div():
#     txt = "before = 1\n# {{div,\ninside = 1\n# }}\nafter = 1"
#     new_txt = replace(txt, {}, {}, comment_marker="#")
#     assert new_txt == "before = 1\ninside = 1\nafter = 1"
#
#     txt = "before = 1\n% {{div,\ninside = 1\n% }}\nafter = 1"
#     new_txt = replace(txt, {}, {}, comment_marker="%")
#     assert new_txt == "before = 1\ninside = 1\nafter = 1"
#
#     txt = "before = 1\n.. {{div,\n\ninside = 1\n.. }}\n\nafter = 1"
#     new_txt = replace(txt, {}, {}, comment_marker=".. ")
#     assert new_txt == "before = 1\n\ninside = 1\n\nafter = 1"
#
#
# def test_template_pkglts_upstream_fmt1():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{pkglts upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper, INSIDE = 1}}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_upstream_fmt2():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
#
# # {{pkglts upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
#
# # {{pkglts upper, INSIDE = 1}}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_upstream_fmt3():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{pkglts upper,
# inside = 1
# # }}
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper,
# INSIDE = 1
# # }}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_upstream_fmt4():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
#
# # {{pkglts upper,
# inside = 1
# # }}
# after = 1
# """
#     res = """
# before = 1
#
# # {{pkglts upper,
# INSIDE = 1
# # }}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_downstream_fmt1():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{pkglts upper, inside = 1}}
#
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper, INSIDE = 1}}
#
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_downstream_fmt2():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{pkglts upper, inside = 1 }}
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper, INSIDE = 1 }}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_downstream_fmt3():
#     handlers = {'upper': upper}
#
#     txt = """
# before = 1
# # {{pkglts upper,
# inside = 1
#
# # }}
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper,
# INSIDE = 1
#
# # }}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_template_pkglts_inline_to_div1():
#     def upper_div(txt, env):
#         return "\n" + txt.upper() + "\n"
#
#     handlers = {'upper': upper_div}
#
#     txt = """
# before = 1
# # {{pkglts upper, inside = 1}}
# after = 1
# """
#     res = """
# before = 1
# # {{pkglts upper,
# INSIDE = 1
# # }}
# after = 1
# """
#     new_txt = replace(txt, handlers, None)
#     assert new_txt == res
#
#
# def test_get_comment_marker():
#     assert get_comment_marker("toto.py") == "#"
#     assert get_comment_marker("toto.ini") == "#"
#     assert get_comment_marker("toto.cfg") == "#"
#     assert get_comment_marker("toto.yml") == "#"
#     assert get_comment_marker("toto.rst") == ".. "
#     assert get_comment_marker("toto.bat") == "REM "
#
#
# def test_reconstruct_txt():
#     txt = """
# before = 1  # {{upper, inline = 1}}
# # {{lower,
# div = 1
# # }}
# after = 1
# """
#     root = parse(txt, "#")
#     new_txt = reconstruct_txt_div(root)
#     assert new_txt == txt
#
#
# def test_swap_divs():
#     src_txt = """
# before = 1  # {{pkglts upper, inline = 1}}{{pkglts up2, inline = 3}}
# # {{pkglts lower,
# div = 1
# # }}
# after = 1
# # {{pkglts, inline = 2}}
# after2 = 1
# """
#     tgt_txt = """
# before = 1  # {{pkglts upper, None}}{{pkglts up2, None}}
# # {{pkglts lower,
# None
# # }}
# after = 1
# # {{pkglts, None}}
# after2 = 1
# """
#     new_txt = swap_divs(src_txt, tgt_txt, "#")
#     assert new_txt == src_txt
#
#
# def test_swap_divs_returns_none_if_some_pkglts_divs_missing():
#     src_txt = """
# before = 1  # {{pkglts upper, inline = 1}}{{pkglts up2, inline = 3}}
# # {{pkglts lower,
# div = 1
# # }}
# after = 1
# # {{pkglts, inline = 2}}
# after2 = 1
# """
#     tgt_txt = """
# before = 1  # {{pkglts upper, None}}
# # {{pkglts lower,
# None
# # }}
# after = 1
# # {{pkglts, None}}
# after2 = 1
# """
#     txt = swap_divs(src_txt, tgt_txt, "#")
#     assert txt is None
#
#
# def test_template_core_handler_get_key_return_str():
#     src_txt = "{{key, base.param}}"
#     cfg = dict(base={'param': 0})
#     tgt_txt = replace(src_txt, {}, cfg)
#
#     assert tgt_txt == "0"
