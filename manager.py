from detailsWriter import DetailsWriter
from pagesWriter import PagesWriter
from listWriter import ListWriter


def end():
    print("Now you need to write your bolg content in new_blog")
    print("And add your new picture in the reference position")


class Manager:
    def __init__(self):
        self.file_index = {
            'detail_in': 'D:/GitHub/morethan987.github.io/blogdetail/2024/07/local_overleaf/index.html',
            'detail_out': 'D:/blog_writer/new_blog/index_mod.html',

            'pages_in': 'D:/GitHub/morethan987.github.io/blogpages/index.html',
            'pages_out': 'D:/blog_writer/new_page/index_mod.html',

            'list_in': 'D:/GitHub/morethan987.github.io/list/index.html',
            'list_out': 'D:/blog_writer/new_list/index_mod.html',
        }
        self.cover_information = {}  # 封面中的信息
        self.detail_information = {
            'meta_keyword': '',
            'web_title': '',
            'detail_title': '',
            'category': '',
            'post_date': '',
            'tag_names': []
        }  # 博客详情中的信息

    def run(self):
        # 撰写博客详情页
        details_writer = DetailsWriter(self)
        details_writer.start()

        # 撰写博客封面页
        pages_writer = PagesWriter(self)
        pages_writer.start()

        # 撰写博客列表页
        list_writer = ListWriter(self)
        list_writer.start()

        # 结束
        end()
