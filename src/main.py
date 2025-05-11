import os.path
import os
import shutil
from node.textnode import *


def main():
    txtnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(txtnode)
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_directory("./static/")

def copy_directory(source, path="", destination="./public"):
    target = destination + path
    os.mkdir(destination +path)
    contents = os.listdir(source + path)
    for content in contents:
        if os.path.isfile(source+path+"/"+content):
            shutil.copy(source+path+"/"+content, target)
        else:
            copy_directory(source, path + "/" + content, destination)
    

if __name__ == "__main__":
    main()


