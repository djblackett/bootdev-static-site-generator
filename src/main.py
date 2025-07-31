print("hello world")
from textnode import TextNode, TextType


def main():
    textnode = TextNode("Hello there", TextType.LINK, "www.generalkenobi.fett")
    print(textnode)

main()