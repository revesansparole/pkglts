from dataclasses import dataclass

from url_normalize import url_normalize


@dataclass
class Badge:
    name: str
    url: str
    url_img: str
    text: str = ""

    def format(self, doc_fmt):
        """Produce valid img hyperlink.

        Args:
            doc_fmt (str): doc format either 'rst' or 'md'

        Returns:
            (str)
        """

        url = url_normalize(self.url)
        url_img = url_normalize(self.url_img)

        if self.text == "":
            txt = self.name
        else:
            txt = self.text

        if doc_fmt == 'rst':
            return ("\n"
                    f".. image:: {url_img}\n"
                    f"    :alt: {txt}\n"
                    f"    :target: {url}\n"
                    )

        if doc_fmt == 'md':
            return f"[![{txt}]({url_img})]({url})"

        raise UserWarning(f"Unknown format '{doc_fmt}'")
