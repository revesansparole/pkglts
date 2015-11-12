def twice(txt, env):
    del env  # unused
    return txt * 2


mapping = {'test.twice': twice}
