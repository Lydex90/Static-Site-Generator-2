

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("This method is not implemented yet")


    def props_to_html(self):
        string = ""
        if not self.props:
            return string
        prop_keys = list(self.props.keys())
        
        for i in prop_keys:
            string += f' {i}="{self.props[i]}"'
        
        return string
        

    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})")

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    
    def __repr__(self):
        return (f"HTMLNode({self.tag}, {self.value}, {self.props})")


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Missing tag")
        if not self.children:
            raise ValueError("missing children")
        string = ''
        for child in self.children:
            string += child.to_html()

        return f'<{self.tag}{self.props_to_html()}>{string}</{self.tag}>'