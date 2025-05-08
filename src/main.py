from textnode import *


def main():
    txtnode = TextNode("This is some anchor text", TextType.LINK_TEXT, "https://www.boot.dev")
    print(txtnode)

if __name__ == "__main__":
    main()