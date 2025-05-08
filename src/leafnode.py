from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None,  props=None):
        if not value:
            raise ValueError("value cannot be None")
        
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.tag:
            props = self.props_to_html()
            return f'<{self.tag}{props}>{self.value}</{self.tag}>'
        return f'{self.value}'
    


