from detailsWriter import DetailsWriter
from pagesWriter import PagesWriter
from listWriter import ListWriter
from tagsWriter import TagsWriter
import os


def end():
    print("Now you need to write your bolg content in the objective file path")


def create_folder():
    # 新建img文件路径
    img_path = 'D:/blog_writer/image'
    # 检查文件夹是否存在
    if not os.path.exists(img_path):
        # 如果不存在，则创建文件夹
        os.makedirs(img_path)
        print(f"文件夹 {img_path} 已创建。")
    else:
        print(f"文件夹 {img_path} 已存在。")


class Manager:
    def __init__(self):
        self.file_index = {
            'detail_in': 'D:/GitHub/morethan987.github.io/blogdetail/2024/08/native_llm/index.html',
            'detail_out': '',

            'pages_in': 'D:/GitHub/morethan987.github.io/blogpages/index.html',
            'pages_out': 'D:/GitHub/morethan987.github.io/blogpages/index_mod.html',

            'list_in': 'D:/GitHub/morethan987.github.io/list/index.html',
            'list_out': 'D:/GitHub/morethan987.github.io/list/index_mod.html',

            'tags_in': 'D:/GitHub/morethan987.github.io/tags/index.html',
            'tags_out': 'D:/GitHub/morethan987.github.io/tags/index_mod.html',
        }
        self.detail_information = {
            'meta_keyword': '',
            'web_title': '',
            'detail_title': '',
            'category': '',
            'post_date': '',
            'tag_names': [],
            'new_file_name': ''
        }  # 博客详情中的信息
        self.cover_information = {
            'post_month': '',
            'cover_image_name': ''
        }  # 封面中的信息
        self.list_information = {}  # 列表中的信息
        self.tags_information = {}  # 标签中的信息

    def run(self):
        # 初始化检验文件夹创建
        create_folder()
        print("Program has create relative folders in 'D:/blog_writer'")

        # 撰写博客详情页
        details_writer = DetailsWriter(self)
        details_writer.start()

        # 撰写博客封面页
        pages_writer = PagesWriter(self)
        pages_writer.start()

        # 撰写博客列表页
        list_writer = ListWriter(self)
        list_writer.start()

        # 撰写博客标签页
        tags_writer = TagsWriter(self)
        tags_writer.start()

        # 结束
        end()
