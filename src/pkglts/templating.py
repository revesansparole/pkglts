from os.path import exists
import re

opening_marker = "{" + "#"
closing_marker = "#" + "}"

block_re = re.compile(r"\{#[ ]pkglts,[ ](?P<key>.*?)\n(?P<cnt>.*?)#\}",
                      re.DOTALL | re.MULTILINE)


def parse_source(txt):
    """Parse text to find preserved blocks

    Args:
        txt (str): full text to parse

    Returns:
        (list of (str, str, str, str)): ordered list of blocks:
                    - block_id (or None if content is not preserved
                    - line start before start for preserved content
                    - content
                    - line start before end for preserved content
    """
    blocks = []
    last_end = 0

    for res in block_re.finditer(txt):
        i = res.start()
        while i > last_end and txt[i] != "\n":
            i -= 1

        if i >= last_end:
            blocks.append((None, "", txt[last_end: (i + 1)], ""))

        bef = txt[(i + 1): res.start()]

        bid = res.group('key')

        cnt = res.group('cnt')

        i = len(cnt) - 1
        while i > 0 and cnt[i] != "\n":
            i -= 1
        aft = cnt[(i + 1): len(cnt)]
        cnt = cnt[:i]
        last_end = res.end() + 1

        blocks.append((bid, bef, cnt, aft))

    if last_end < len(txt):
        blocks.append((None, "", txt[last_end: len(txt)], ""))

    return blocks


def render(env, src_pth, tgt_pth):
    """Render src_pth templated file into tgt_pth

    Notes: keeps 'preserved' block structure

    Args:
        env (jinja2.Environment): current pkg environment
        src_pth (str): path to reference file
        tgt_pth (str): path to potentially non existent yet target file

    Returns:
        (list of (str, str)): key, cnt for preserved blocks
    """
    # parse src file to find 'preserved' blocks
    with open(src_pth, 'r') as f:
        src_blocks = parse_source(f.read())

    blocks = []
    if exists(tgt_pth):  # retrieves preserved blocks from source
        # parse tgt file to find 'preserved' blocks
        with open(tgt_pth, 'r') as f:
            tgt_blocks = parse_source(f.read())

        src_blocks = dict((bid, cnt) for (bid, bef, cnt, aft) in src_blocks
                          if bid is not None)
        for bid, bef, cnt, aft in tgt_blocks:
            # check stored content hash

            if bid is not None:
                cnt = src_blocks[bid]

            blocks.append((bid, bef, cnt, aft))
    else:  # format non preserved blocks for the first and only time
        for bid, bef, cnt, aft in src_blocks:
            if bid is None:
                template = env.from_string(cnt)
                cnt = template.render()

            blocks.append((bid, bef, cnt, aft))

    # regenerate preserved block content
    # print "blocks", [bid for bid, bef, cnt, aft in blocks]
    preserved = []
    tgt = ""
    for bid, bef, cnt, aft in blocks:
        if bid is None:
            tgt += cnt
        else:
            # format cnt
            template = env.from_string(cnt)
            cnt = template.render()
            preserved.append((bid, cnt))
            # rewrite preserved tag if necessary
            tgt += bef + "{" + "# pkglts, %s\n" % bid
            tgt += cnt
            tgt += "\n" + aft + "#" + "}\n"

    with open(tgt_pth, 'w') as f:
        f.write(tgt)

    return preserved
