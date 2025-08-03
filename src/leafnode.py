from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        void_tags = {"img", "br", "hr", "input", "meta", "link", "area",
                     "base", "col", "embed", "param", "source", "track", "wbr"}
        if self.value is None and (self.tag not in void_tags):
            print(self.tag)
            raise ValueError("value required")
        elif not self.tag:
            return self.value
        elif self.tag in void_tags:
            return f'<{self.tag}{self.props_to_html()} />'
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
