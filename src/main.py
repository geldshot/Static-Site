import os.path
import os
import shutil
import sys
from node.textnode import *
from node.markdownutil import generate_page


def main(args):
    txtnode = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(txtnode)

    basepath = "/"
    if len(args) > 1:
        basepath = args[1]

    if os.path.exists("./public"):
        shutil.rmtree("./public")
        os.mkdir("./public")

    copy_directory("./static/", destination="./public" ,basepath=basepath)

    generate_pages("./content/", destination="./public", template="./template.html", basepath=basepath)

def copy_directory(source, path="", destination="./public", basepath="/"):
    target = destination + basepath + path

    if not os.path.exists(target):
        os.mkdir(target)
    
    contents = os.listdir(source + path)
    
    for content in contents:
        if os.path.isfile(source+path+"/"+content):
            shutil.copy(source+path+"/"+content, target)
        else:
            copy_directory(source, path + content +"/", destination, basepath)

def generate_pages(source, path="", destination="./public", template="./template.html", basepath="/"):
    target = destination +basepath+ path

    if not os.path.exists(target):
        os.mkdir(target)
    
    contents = os.listdir(source + path)
    
    for content in contents:

        if os.path.isfile(source+path+content):
            dest_file = content.split(".")[0] + ".html"
            generate_page(source+path+content,template,target + dest_file, basepath)
        else:
            generate_pages(source, path + content +"/", destination, template, basepath)

if __name__ == "__main__":
    main(sys.argv)


