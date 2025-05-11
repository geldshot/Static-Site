import re

def extract_title(markdown):
    regex = "(?:^|\\n)# (.*)"
    title = re.findall(regex, markdown)

    if not title or not title[0]:
        raise Exception("no title header")
    
    return title[0]
    
