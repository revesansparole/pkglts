# from pkglts.option.version.handlers import fetch_github_version
#
#
# def test_handlers():
#     pkg_cfg = dict()
#     txt = fetch_github_version("", pkg_cfg)
#     assert txt == ""


# def test_handlers_not_available(mocker):
#     def import_call(*args):
#         print args
#
#     with mocker.patch("pkglts.option.version.handlers.__builtins__",
#                     new_callable=import_call):
#         # from pkglts.option.version.handlers import fetch_github_version
#         assert fetch_github_version == "0"
