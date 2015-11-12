from os.path import exists
import sys


def list_python_envs(versions):
    """ Check the system for all available python distributions

    args:
     - versions (list of str): list of python versions
                           (e.g. '27', '34') to check
    """
    if 'win' in sys.platform:
        installed = []
        # check known locations
        for pyver in versions:
            if exists("C:/Python%s/python.exe" % pyver):
                # TODO check alternative location
                installed.append("py%s" % pyver)

        return installed
    else:  # use which command
        print("need some linux to try")
        return []


def pyversions(txt, env):
    del txt  # unused
    py_exe_list = list_python_envs(env['pydist']['intended_versions'])
    return ", ".join(py_exe_list)


mapping = {'tox.pyversions': pyversions}
