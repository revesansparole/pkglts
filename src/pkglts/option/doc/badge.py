from dataclasses import dataclass


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

        if self.url.startswith("http"):
            url = self.url
        else:
            url = f"https://{self.url}"

        if self.url_img.startswith("http"):
            url_img = self.url_img
        else:
            url_img = f"https://{self.url_img}"

        if self.text == "":
            txt = self.name
        else:
            txt = self.text

        if doc_fmt == 'rst':
            lines = [f".. image:: {url_img}",
                     f"    :alt: {txt}",
                     f"    :target: {url}"]
            return "\n" + "\n".join(lines)

        if doc_fmt == 'md':
            return f"[![{txt}]({url_img})]({url})"

        raise UserWarning(f"Unknown format '{doc_fmt}'")
