import os.path
import os
import shutil
from node.textnode import *
from node.markdownutil import generate_page


def main():
    txtnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(txtnode)
    if os.path.exists("./public"):
        shutil.rmtree("./public")
    copy_directory("./static/")

    generate_pages("./content", destination="./public", template="./template.html")

def copy_directory(source, path="", destination="./public"):
    target = destination + path
    
    if not os.path.exists(destination+path):
        os.mkdir(destination +path)
    
    contents = os.listdir(source + path)
    
    for content in contents:
        if os.path.isfile(source+path+"/"+content):
            shutil.copy(source+path+"/"+content, target)
        else:
            copy_directory(source, path + "/" + content, destination)

def generate_pages(source, path="", destination="./public", template="./template.html"):
    target = destination + path
    
    if not os.path.exists(destination+path):
        os.mkdir(destination +path)
    
    contents = os.listdir(source + path)
    
    for content in contents:
        if os.path.isfile(source+path+"/"+content):
            dest_file = content.split(".")[0] + ".html"
            generate_page(source+path+"/"+content,template,target + "/" + dest_file)
        else:
            generate_pages(source, path + "/" + content, destination, template)

if __name__ == "__main__":
    main()


