"""
Set of functions to extend jinja2.
"""

import re

from .small_tools import ensure_path

OPENING_MARKER = "{" + "#"
CLOSING_MARKER = "#" + "}"

BLOCK_RE = re.compile(
    r"\{#[ ]pkglts,[ ](?P<key>[a-zA-Z0-9._]*)(?P<aft_head>.*?)\n(?P<cnt>.*?)#\}(?P<aft_foot>.*?(?=\n))",
    re.DOTALL | re.MULTILINE,
)

NON_BIN_EXT = (
    "",
    ".bat",
    ".cfg",
    ".json",
    ".in",
    ".ini",
    ".md",
    ".no",
    ".ps1",
    ".py",
    ".rst",
    ".sh",
    ".svg",
    ".toml",
    ".tpl",
    ".txt",
    ".yml",
    ".yaml",
)


class TplBlock:
    """Simple container for template blocks."""

    def __init__(self):
        self.before_header = ""
        self.bid = None
        self.loc = None
        self.after_header = ""
        self.content = ""
        self.before_footer = ""
        self.after_footer = ""

    def __str__(self):
        return (
            f"Block(\n"
            f"|{self.before_header}|{self.bid}|{self.after_header}|\n"
            f"|{repr(self.content)}|\n|{self.before_footer}|{self.after_footer}|\n)"
        )

    def pkglts_defined(self, bid, cnt):
        """Create a block regenerated by pkglts.

        Args:
            bid (str): id for this block (unique per file only)
            cnt (str): content

        Returns:
            None
        """
        self.bid = bid
        self.content = cnt

    def user_defined(self, cnt):
        """Make this block a user defined one.

        Args:
            cnt (str): content

        Returns:
            None
        """
        self.bid = None
        self.content = cnt


def parse_source(txt):
    """Parse text to find preserved blocks

    Args:
        txt (str): full text to parse

    Returns:
        (list of [str, str, str, str]): ordered list of blocks:
                    - block_id (or None if content is not preserved
                    - line start before start for preserved content
                    - content
                    - line start before end for preserved content
    """
    blocks = []
    last_end = -1

    for res in BLOCK_RE.finditer(txt):
        i = res.start()
        while i > last_end and txt[i] != "\n":
            i -= 1

        if i > last_end:
            block = TplBlock()
            block.user_defined(txt[(last_end + 1) : (i + 1)])
            blocks.append(block)

        bef = txt[(i + 1) : res.start()]

        bid = res.group("key")
        aft_head = res.group("aft_head")
        cnt = res.group("cnt")
        aft_foot = res.group("aft_foot")

        i = len(cnt) - 1
        while i > 0 and cnt[i] != "\n":
            i -= 1
        aft = cnt[(i + 1) : len(cnt)]
        cnt = cnt[: (i + 1)]
        last_end = res.end()

        block = TplBlock()
        block.pkglts_defined(bid, cnt)
        block.before_header = bef
        block.after_header = aft_head
        block.before_footer = aft
        block.after_footer = aft_foot

        if aft_head.startswith(", after"):
            block.loc = ("after", aft_head[7:].split(" ")[1])
        elif aft_head.startswith(", before"):
            block.loc = ("before", aft_head[8:].split(" ")[1])
        elif aft_head.startswith(", replace"):
            block.loc = ("replace", aft_head[8:].split(" ")[1])

        blocks.append(block)

    if last_end < (len(txt) - 1):
        block = TplBlock()
        block.user_defined(txt[(last_end + 1) : len(txt)])
        blocks.append(block)

    return blocks


class Template(object):
    """Simple container that holds a list of blocks

    The may objective is to represent a full templated file
    """

    def __init__(self):
        self.blocks = []
        self.bin_cnt = None  # binary content for binary files

    def add(self, block):
        """Insert a new block in the overall template

        Notes: will use block loc to position it.

        Args:
            block (TplBlock): block with all fields filled

        Returns:
            None
        """
        if block.loc is None:
            self.blocks.append(block)
        else:
            ind = [b.bid for b in self.blocks].index(block.loc[1])
            if block.loc[0] == "after":
                self.blocks.insert(ind + 1, block)
            elif block.loc[0] == "before":
                self.blocks.insert(ind, block)
            elif block.loc[0] == "replace":
                self.blocks[ind] = block
            else:
                raise NotImplementedError

    def parse(self, pth):
        """Parse file and append all blocks into this template

        Args:
            pth (Path): path to file to read

        Returns:
            None
        """
        if pth.suffix in NON_BIN_EXT:
            for block in parse_source(pth.read_text()):
                self.add(block)
        else:
            self.bin_cnt = pth.read_bytes()

    def render(self, cfg, tgt_pth):
        """Render template into tgt_pth

        Notes: keeps 'preserved' block structure

        Args:
            cfg (Config):  current package configuration
            tgt_pth (Path): path to potentially non existent yet target file

        Returns:
            (list of [str, str]): key, cnt for preserved blocks
        """
        if self.bin_cnt is not None:
            ensure_path(tgt_pth)
            tgt_pth.write_bytes(self.bin_cnt)
        else:
            return self._render_non_bin(cfg, tgt_pth)

    def _render_non_bin(self, cfg, tgt_pth):
        blocks = []
        if tgt_pth.exists():  # retrieves preserved blocks from source
            # parse tgt file to find 'preserved' blocks
            tgt_blocks = parse_source(tgt_pth.read_text())

            tpl_bids = set(b.bid for b in self.blocks if b.bid is not None)
            tgt_bids = set(b.bid for b in tgt_blocks if b.bid is not None)
            if tpl_bids != tgt_bids:
                raise UserWarning(f"File '{tgt_pth}' not compatible with current template")

            src_blocks = dict((b.bid, b) for b in self.blocks if b.bid is not None)
            for tgt_block in tgt_blocks:
                # reset content of preserved blocks only
                if tgt_block.bid is not None:
                    tgt_block.content = src_blocks[tgt_block.bid].content

                blocks.append(tgt_block)
        else:  # format non preserved blocks for the first and only time
            for block in self.blocks:
                if block.bid is None:
                    block.content = cfg.render(block.content)

                blocks.append(block)

        # regenerate preserved block content
        preserved = []
        tgt = ""
        for block in blocks:
            if block.bid is None:
                tgt += block.content
            else:
                # format cnt
                cnt = cfg.render(block.content)
                if len(cnt) == 0 or cnt[-1] != "\n":  # case where templating has eaten the remaining spaces and '\n'
                    cnt += "\n"
                preserved.append((block.bid, cnt))
                # rewrite preserved tag
                tgt += block.before_header + "{" + f"# pkglts, {block.bid}{block.after_header}\n"
                tgt += cnt
                tgt += block.before_footer + "#" + "}" + f"{block.after_footer}\n"

        ensure_path(tgt_pth)
        tgt_pth.write_text(tgt)

        return preserved
