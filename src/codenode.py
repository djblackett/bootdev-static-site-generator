

from htmlnode import HTMLNode


class CodeNode(HTMLNode):
    def __init__(self, text: str):
        super().__init__(None, text, children=None, props=None)
        self.text = text

    def to_html(self):
        clean = self.text.strip('```').removeprefix('\n')
        if not clean:
            return "<pre><code></code></pre>"
        # Return the code block wrapped in <pre><code> tags
        # This is a simplified version, assuming the text is already formatted correctly
        # In a real implementation, you might want to escape HTML characters
        # and handle other formatting issues.
        # For now, we just return the text as is.
        return f"<pre><code>{clean}</code></pre>"
