from bs4 import BeautifulSoup
from datetime import datetime
import shutil
import os


class PagesWriter:
    # 博客封面编写，管理流程中的第二个
    def __init__(self, manager):
        self.manager = manager
        self.templet_path = self.manager.file_index['pages_in']
        self.obj_path = self.manager.file_index['pages_out']
        self.soup = None

    def start(self):
        self.init()
        self.update_tags()
        self.update_insights()
        self.change_cover_image()
        self.write()

    def init(self):
        print("开始编辑blogpages,读取pages模板中......")

        # 读取原始文件内容
        with open(self.templet_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        self.soup = BeautifulSoup(original_content, 'lxml')
        if self.soup:
            print("已成功获取blogpages模板！开始编辑blogpages")
        else:
            print("获取模板失败，请重新指定路径！")

    def update_tags(self):
        original_tag_names = []
        # 定位tags Section
        target_div = self.soup.find('div', attrs={'class': 'inline-flex flex-wrap items-center gap-2 mb-5 text-sm '
                                                           'md:gap-4'})
        if target_div:
            # 获取原标签
            for child in target_div.find_all(True):
                original_tag_names.append(child.string)

            # 标签查重
            for tag_name in self.manager.detail_information['tag_names']:
                if tag_name not in original_tag_names:
                    new_tag = self.soup.new_tag('a', attrs={
                        'href': "https://morethan987.github.io/tags/#" + tag_name.lower(),
                        'class': "inline-block px-3.5 py-2 transition duration-300 border "
                                 "border-dashed text-black dark:text-white/70 "
                                 "border-platinum dark:border-greyBlack rounded-3xl md:px-5 "
                                 "md: md:py-2 hover:text-theme dark:hover:text-white"})
                    new_tag.string = tag_name
                    target_div.append(new_tag)
                    print("add a new tag!")

        else:
            print("No such tag!")

    def update_insights(self):
        # 轮换最新blog
        target_div = self.soup.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
        if target_div:
            # 获取最后一个子标签
            last_child_copy = target_div.find_all('div', attrs={
                'class': 'grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack '
                         'items-center rounded-2xl p-3.5'})[-1]

            # 更改链接地址信息
            new_file_name = self.manager.detail_information['new_file_name']
            parent_div = last_child_copy.find('div', attrs={
                'class': 'flex col-span-12 overflow-hidden thumbnail sm:col-span-6 md:col-span-5'})
            # 新建文件路径
            folder_path = 'D:/GitHub/morethan987.github.io/blogdetail/' + f"{datetime.now().year}/{datetime.now().month:02d}/" + new_file_name

            # 检查文件夹是否存在
            if not os.path.exists(folder_path):
                # 如果不存在，则创建文件夹
                os.makedirs(folder_path)
                print(f"文件夹 {folder_path} 已创建。")
            else:
                print(f"文件夹 {folder_path} 已存在。")
            # 更新代码中的文件指向
            new_address = '../blogdetail/' + f"{datetime.now().year}/{datetime.now().month:02d}/" + new_file_name
            parent_div.find('a')['href'] = new_address
            last_child_copy.find('div', attrs={'class': 'read-details'}).find('a')['href'] = new_address
            self.manager.cover_information['post_month'] = f"{datetime.now().year}/{datetime.now().month:02d}"

            # 更改标签内容
            cover_tag = last_child_copy.find('div', attrs={'class': 'text-sm font-medium tags'})
            a_tag = cover_tag.find('a')
            a_tag['href'] = ('https://morethan987.github.io/tags/#' +
                             self.manager.detail_information['tag_names'][0].lower())
            a_tag.string = self.manager.detail_information['tag_names'][0]
            cover_tag.find('span').string = self.manager.detail_information['post_date']

            # 更改封面标题
            new_cover_title = input("your new cover title: ")
            cover_title = last_child_copy.find('div', attrs={'class': 'post-title mt-3 md:mt-4.5 mb-6 md:mb-8'}).find(
                'a')
            cover_title.string = new_cover_title
            cover_title['href'] = new_address

            # 将复制的内容插入到标签的开头
            target_div.insert(0, last_child_copy)

        else:
            print("No such tag!")

    def change_cover_image(self):
        # 定位上级标签
        parent_div = self.soup.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
        first_child_div = parent_div.find('div', attrs={
                'class': 'grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack '
                         'items-center rounded-2xl p-3.5'})
        img_tag = first_child_div.find('img', attrs={'alt': 'Post Title'})
        print("Please put your image into 'D:/blog_writer/image' and rename it as 'example.png'")
        print("Recommend size: 700*700")
        img_name = input("input your cover image name: ")
        self.manager.cover_information['cover_image_name'] = img_name
        if img_tag:
            # 实际复制图片到指定目录
            # 指定源图片文件的路径
            source_image_path = 'D:/blog_writer/image/' + img_name

            # 指定目标文件夹的路径
            destination_folder_path = 'D:/GitHub/morethan987.github.io/blogpages/assets/img/blog'

            # 确保目标文件夹存在
            if not os.path.exists(destination_folder_path):
                os.makedirs(destination_folder_path)

            # 构建目标图片文件的完整路径
            destination_image_path = os.path.join(destination_folder_path, os.path.basename(source_image_path))

            # 复制图片文件
            try:
                shutil.copy(source_image_path, destination_image_path)
                print(f"图片已成功复制到 {destination_image_path}")
                # 更改代码中文件指向
                img_tag['src'] = 'assets/img/blog/' + img_name
            except IOError as e:
                print(f"无法复制文件。{e}")
        else:
            print("Can't find image tag!")

    def write(self):
        # 将修改后的HTML内容写入到新文件中
        with open(self.obj_path, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))
        print(f"File has been modified and saved to {self.obj_path}")
