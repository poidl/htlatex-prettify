#!/bin/python
# pylint: disable=C0103

"""HTML modifications"""

from bs4 import BeautifulSoup


def mytitle(path, newtitle):
    """Set an alternative HTML document title. Empty string is ignored
    (leaves old title in place)."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    title = soup.find_all('title')
    # print(title)
    if newtitle:
        title[0].string.replace_with(newtitle)
    # soup['title'] = newtitle
    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)


def viewport(path):
    """Set the viewport."""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')
    new_tag = soup.new_tag("meta")
    new_tag['name'] = "viewport"
    new_tag['content'] = "width=device-width, initial-scale=1"
    soup.head.append(new_tag)

    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)


def toc(path):
    """Generate a table of content from tex files processed with htlatex"""
    f = open(path + "/main.html")
    s = f.read()

    soup = BeautifulSoup(s, 'html.parser')

    sectitlelist = soup.find_all('h3')
    ls = len(sectitlelist)
    ids = [[] for i in range(ls)]
    titles = ids.copy()
    #     l = list(sectitlelist[i].children)
    #     if l[0].get('class') == ['titlemark']:
    # for l in sectitlelist:
    for i in range(ls):
        l = sectitlelist[i]
        if l['class'] == ['sectionHead']:
            ids[i] = l.a['id']
            titles[i] = l.contents[4].strip()
            continue
        # the remaining one is for the bibliography, which is not numbered
        ids[i] = l.get('id')
        titles[i] = l.text.strip()

        # The html structure for an ordered list is:

        # <ol>
        #       <li><a href="HREF">NAME</a></li>
        # </ol>

        # HREF are fragment identifiers here (#)

    s1 = "<li><a href=\"#"
    s2 = "\">"
    s3 = "</a></li>"

    s1 = [s1] * ls
    s2 = [s2] * ls
    s3 = [s3] * ls

    z = list(zip(s1, ids, s2, titles, s3))
    labels = [''.join(str(x) for x in z[jj]) for jj in range(ls)]
    labels = ''.join(labels)

    ol = ''.join(["<ol>", labels, "</ol>"])

    soup_ol = BeautifulSoup(ol, 'html.parser')
    # print(soup_ol.prettify())

    elem = soup.body.find_all("h3", {"class": "sectionHead"})[0]
    idx = soup.body.contents.index(elem)
    soup.body.contents.insert(idx, soup_ol.ol)
    html = soup.prettify()
    f = open(path + "/main.html", "w")
    f.write(html)