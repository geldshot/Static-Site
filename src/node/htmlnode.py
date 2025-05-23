

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props:
            return " "+" ".join(map(lambda x: f'{x[0]}="{x[1]}"', self.props.items()))
        return ""

    def __repr__(self):
        props = self.props_to_html()
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {props})"