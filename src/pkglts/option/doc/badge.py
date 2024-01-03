from dataclasses import dataclass

from url_normalize import url_normalize


@dataclass
class Badge:
    name: str
    url: str
    url_img: str
    text: str = ""

    def __post_init__(self):
        self.url = url_normalize(self.url)
        self.url_img = url_normalize(self.url_img)

    def format(self, doc_fmt):
        """Produce valid img hyperlink.

        Args:
            doc_fmt (str): doc format either 'rst' or 'md'

        Returns:
            (str)
        """
        if self.text == "":
            txt = self.name
        else:
            txt = self.text

        if doc_fmt == 'rst':
            return ("\n"
                    f".. image:: {self.url_img}\n"
                    f"    :alt: {txt}\n"
                    f"    :target: {self.url}\n"
                    )

        if doc_fmt == 'md':
            return f"[![{txt}]({self.url_img})]({self.url})"

        raise UserWarning(f"Unknown format '{doc_fmt}'")
