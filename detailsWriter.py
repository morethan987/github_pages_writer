from bs4 import BeautifulSoup
from datetime import datetime


class DetailsWriter:
    # 博客详情编写，管理流程中的第一个
    def __init__(self, manager):
        self.manager = manager
        self.templet_path = self.manager.file_index['detail_in']
        self.obj_path = self.manager.file_index['detail_out']
        self.soup = None

    def start(self):
        self.init()
        self.change_meta()
        self.change_title()
        self.change_detail_title()
        self.change_post_date()
        self.change_tags()
        self.write()

    def init(self):
        print("开始编辑blogdetails，读取details模板中......")

        # 读取原始文件内容
        with open(self.templet_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        self.soup = BeautifulSoup(original_content, 'lxml')
        if self.soup:
            print("已成功获取blogdetails模板！开始编辑blogdetails")
        else:
            print("获取模板失败，请重新指定路径！")

    def change_meta(self):
        # 定位meta标签
        mata_tag = self.soup.find('meta', attrs={'name': 'keyword'})
        # 检查是否找到了标签并修改内容
        if mata_tag:
            print("original tag: " + str(mata_tag))
            new_content = input("input your new content: ")
            mata_tag['content'] = new_content
            self.manager.detail_information['meta_keyword'] = mata_tag['content']
        else:
            print("No such tag!")

    def change_title(self):
        # 定位网页title标签
        title_tag = self.soup.find('title')
        # 检查是否找到了标签并修改内容
        if title_tag:
            print("original web title: " + str(title_tag))
            new_content = input("input your new web title: ")
            title_tag.string = new_content
            self.manager.detail_information['web_title'] = new_content
        else:
            print("No such tag!")

    def change_detail_title(self):
        # 定位文章标题
        h2_tag = self.soup.find("h2", attrs={
            'class': 'text-2xl font-semibold leading-normal text-black dark:text-white mt-7 lg:mt-10 article-title '
                     'lg:text-3xl lg:leading-normal'})
        # 检查是否找到了标签并修改内容
        if h2_tag:
            print("original detail title: " + str(h2_tag.string))
            new_content = input("input your new detail title: ")
            h2_tag.string = new_content
            self.manager.detail_information['detail_title'] = new_content
        else:
            print("No such tag!")

    def change_category(self):
        if self.soup.find('h6', string='CATEGORY:'):
            p_tag = self.soup.find('h6', string='CATEGORY:').find_next_sibling('p')
            # 检查是否找到了标签并修改内容
            if p_tag:
                print("original category: " + str(p_tag.string))
                new_content = input("input your new content: ")
                p_tag.string = new_content
                self.manager.detail_information['category'] = new_content
            else:
                print("No such tag!")

    def change_post_date(self):
        # 定位发布时间
        if self.soup.find('h6', string='POSTED ON:'):
            p_tag = self.soup.find('h6', string='POSTED ON:').find_next_sibling('p')
            # 检查是否找到了标签并修改内容
            if p_tag:
                print("original post date: " + str(p_tag.string))
                p_tag.string = f"{datetime.now().year}/{datetime.now().month:02d}/{datetime.now().day:02d}"
                self.manager.detail_information['post_date'] = p_tag.string
            else:
                print("No such tag!")
        else:
            print("No such tag!")

    def change_tags(self):
        tag_names = []  # 存储新输入的标签
        # 定位tags
        target_div = self.soup.find('div', attrs={'class': 'flex flex-wrap items-center gap-2.5'})
        if target_div:
            # 先删除所有原有内容
            for child in target_div.find_all(True):
                child.extract()
            # 再写入新的内容
            print("请输入你的新标签，输入ok完成编辑")
            while True:
                new_tag_name = input("Your new tag:")
                if new_tag_name != "ok":
                    new_tag = self.soup.new_tag('a', attrs={
                                                'href': "https://morethan987.github.io/tags/#" + new_tag_name.lower(),
                                                'class': "inline-block border border-dashed border-greyBlack "
                                                        "rounded-md text-sm py-1.5 px-2 transition-all "
                                                        "hover:text-theme dark:hover:text-white"})
                    new_tag.string = new_tag_name
                    target_div.append(new_tag)
                    tag_names.append(new_tag_name)
                    self.manager.detail_information['tag_names'] = tag_names
                else:
                    break
        else:
            print("No such tag!")

    def write(self):
        # 将修改后的HTML内容写入到新文件中
        with open(self.obj_path, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))
        print(f"File has been modified and saved to {self.obj_path}")
