from lxml import html
import requests

import xpath_strings as xp

BASE_PATH = 'http://kurser.dtu.dk/course/'


class MultipleTargetsException(Exception):
    """Query targets multiple nodes
    """
    pass


def fetch_course_page(code):
    cookies = requests.get(BASE_PATH + url).cookies
    page = requests.get(url, cookies=cookies)
    tree = html.fromstring(page)

    return tree


def node_text(tree, xpath_string):
    nodes = tree.xpath(xpath_string)
    if len(nodes) != 1:
        raise MultipleTargetsException()
    content = nodes[0].text

    return content


class Course:
    @classmethod
    def create(cls, code):
        tree = fetch_course_page(code)
        course_name = node_text(tree, xp.COURSE_NAME)
        course_points = node_text(tree, xp.ECTS_POINTS)

        return cls(name=course_name, points=course_points, code=code)

    def __init__(self, name, points, code):
        self.name = name
        self.points = points
        self.code = code

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        self._code = code
        self.url = BASE_PATH + self._code

    def __repr__(self):
        return f"Course w/name {self.name}, code {self.code}, points {self.points}"


url = 'http://kurser.dtu.dk/course/02110'

# Perform request twice to attach cookie and actually get the freaking
# page. Jesus, DTU.
cookies = requests.get(url).cookies
page = requests.get(url, cookies=cookies)

tree = html.fromstring(page.content)

course_02110 = Course("Algorithms and data structures 2",
                      tree.xpath(xp.ECTS_POINTS)[0].text, '02110')

print(course_02110)
