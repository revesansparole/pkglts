# from nose.tools import with_setup
# from os import mkdir
# from os.path import exists
# from shutil import rmtree
#
# from pkglts.manage_tools import check_tempering, regenerate_dir
# from pkglts.templating import same
#
#
# print(__file__)
#
#
# tmp_dir = "tchikiboum"
#
#
# def setup():
#     if not exists(tmp_dir):
#         mkdir(tmp_dir)
#
#
# def teardown():
#     if exists(tmp_dir):
#         rmtree(tmp_dir)
#
#
# @with_setup(setup, teardown)
# def test_no_tempering_on_creation():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     fnames = []
#     check_tempering("pkglts_data/test", tmp_dir,
#                     handlers, pkg_cfg, fnames)
#
#     assert len(fnames) == 0
#
#
# @with_setup(setup, teardown)
# def test_tempering_walk_deep_files_in_ltpkgbuilder_data():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test/test2", tmp_dir, handlers, pkg_cfg)
#
#     with open(tmp_dir + "/subtest/tutu.txt", 'w') as f:
#         f.write("modification")
#
#     fnames = []
#     check_tempering("pkglts_data/test/test2", tmp_dir,
#                     handlers, pkg_cfg, fnames)
#
#     assert fnames == [tmp_dir + "/subtest/tutu.txt"]
#
#
# @with_setup(setup, teardown)
# def test_tempering_do_not_complain_if_removed_dirs():
#     pkg_cfg = {'hash': {}}
#     handlers = {}
#
#     regenerate_dir("pkglts_data/test/test2", tmp_dir, handlers, pkg_cfg)
#
#     rmtree(tmp_dir + "/subtest")
#
#     fnames = []
#     check_tempering("pkglts_data/test/test2", tmp_dir,
#                     handlers, pkg_cfg, fnames)
#
#     assert len(fnames) == 0
#
#
# @with_setup(setup, teardown)
# def test_tempering_handle_src_directory():
#     pkg_cfg = {'hash': {}, 'base': {'namespace': 'myns', 'pkgname': 'mypkg'}}
#     handlers = {'base': same}
#
#     regenerate_dir("pkglts_data/test", tmp_dir, handlers, pkg_cfg)
#
#     with open(tmp_dir + "/src/myns/__init__.py", 'w') as f:
#         f.write("modification")
#
#     with open(tmp_dir + "/src/myns/mypkg/info.rst", 'w') as f:
#         f.write("modification")
#
#     fnames = []
#     check_tempering("pkglts_data/test", tmp_dir,
#                     handlers, pkg_cfg, fnames)
#
#     assert set(fnames) == {tmp_dir + "/src/myns/__init__.py",
#                            tmp_dir + "/src/myns/mypkg/info.rst"}
