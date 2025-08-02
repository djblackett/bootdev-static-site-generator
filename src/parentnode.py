from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("tag is required")
        if not self.children:
            raise ValueError("children are required")

        html_children = ""
        for child in self.children:
            html_children += child.to_html()
        return "".join(
            f"<{self.tag}>{child.to_html()}</{self.tag}>" for child in self.children
        )
        # return f'<{self.tag}>{html_children}</{self.tag}>'
