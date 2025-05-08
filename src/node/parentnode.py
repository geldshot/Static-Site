from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        if not tag:
            raise ValueError("tag cannot be None")
        if not children:
            raise ValueError("children cannot be None")
        
        super().__init__(tag=tag, value=None, children=children, props=props)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("value cannot be None")
        if not self.children:
            raise ValueError("children cannot be None")
        
        child_html = "".join(map(lambda x: x.to_html(), self.children))
        props = self.props_to_html()
        return f'<{self.tag}{props}>{child_html}</{self.tag}>'
