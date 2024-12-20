from bs4 import BeautifulSoup
import copy
import shutil
import os


class TagsWriter:
    # 博客标签编写，管理流程中的第四个
    def __init__(self, manager):
        self.manager = manager
        self.templet_path = self.manager.file_index['tags_in']
        self.obj_path = self.manager.file_index['tags_out']
        self.soup = None

    def start(self):
        self.init()
        self.insert_blog()
        self.update_tags()  # insert和update二者顺序不能调换，insert的检查点在tags section
        self.add_image()
        self.write()

    def init(self):
        print("开始编辑blogtags，读取tags模板中......")

        # 读取原始文件内容
        with open(self.templet_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        self.soup = BeautifulSoup(original_content, 'lxml')
        if self.soup:
            print("已成功获取blogtags模板！开始编辑blogtags")
        else:
            print("获取模板失败，请重新指定路径！")

    def update_tags(self):
        original_tag_names = []
        # 定位tags Section
        target_div = self.soup.find('div', attrs={'class': 'inline-flex flex-wrap items-center gap-2 mb-5 text-sm '
                                                           'md:gap-4'})
        if target_div:
            # 获取原标签
            for child in target_div.find_all('a', attrs={'class': 'inline-block px-3.5 py-2 transition duration-300 border border-dashed text-black dark:text-white/70 border-platinum dark:border-greyBlack rounded-3xl md:px-5 md: md:py-2 hover:text-theme dark:hover:text-white'}):
                original_tag_names.append(child.string)

            # 标签查重
            for tag_name in self.manager.detail_information['tag_names']:
                if tag_name not in original_tag_names:
                    last_tag = target_div.find_all('a', attrs={'class': 'inline-block px-3.5 py-2 transition duration-300 border border-dashed text-black dark:text-white/70 border-platinum dark:border-greyBlack rounded-3xl md:px-5 md: md:py-2 hover:text-theme dark:hover:text-white'})[-1]
                    data_scroll_nav = int(last_tag['data-scroll-nav']) + 1
                    new_tag = self.soup.new_tag('a', attrs={
                        'href': "#" + tag_name.lower(),
                        'class': "inline-block px-3.5 py-2 transition duration-300 border "
                                 "border-dashed text-black dark:text-white/70 "
                                 "border-platinum dark:border-greyBlack rounded-3xl md:px-5 "
                                 "md: md:py-2 hover:text-theme dark:hover:text-white",
                        'data-scroll-nav': str(data_scroll_nav)})
                    new_tag.string = tag_name
                    target_div.append(new_tag)
                    print("add a new tag!")

        else:
            print("No such tag!")

    def insert_blog(self):
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
                    temp_div = self.soup.find_all('div', attrs={'class': 'py-5 xl:py-3.5 max-w-content xl:max-2xl:max-w-50rem max-xl:mx-auto xl:ml-auto'})[-1]
                    copy_div = copy.copy(temp_div)
                    # 更改容器标签信息
                    copy_div['id'] = tag_name.lower()
                    copy_div['data-scroll-index'] = str(int(temp_div['data-scroll-index']) + 1)
                    copy_div.find('div', attrs={'class': 'inline-flex items-center gap-2 px-4 py-2 text-xs '
                                                         'tracking-wide text-black dark:text-white border lg:px-5 '
                                                         'section-name border-platinum dark:border-greyBlack200 '
                                                         'rounded-4xl'}).string = tag_name
                    # 定位blog插入母标签
                    obj_div = copy_div.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
                    # 先删除原有内容
                    for child in obj_div.find_all(True):
                        child.extract()
                    # 获取模板
                    cover_soup = self.get_templet()
                    source_div = cover_soup.find_all('div', attrs={
                        'class': 'grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack '
                                 'items-center rounded-2xl p-3.5'})[0]
                    # 将 source_div 复制并插入到 obj_div 的第一个位置
                    if source_div and obj_div:
                        obj_div.insert(0, source_div)
                    # 完成修改并插入
                    self.soup.find('div', attrs={'id': 'blog_container'}).append(copy_div)
                else:
                    # 定位上级标签
                    parent_div = self.soup.find('div', attrs={'class':'py-5 xl:py-3.5 max-w-content xl:max-2xl:max-w-50rem max-xl:mx-auto xl:ml-auto', 'id': tag_name.lower()})
                    # 获取模板
                    cover_soup = self.get_templet()
                    source_div = cover_soup.find_all('div',
                                                     class_='grid md:gap-2 grid-cols-12 overflow-hidden article group '
                                                            'bg-flashWhite dark:bg-metalBlack items-center '
                                                            'rounded-2xl p-3.5')[0]
                    target_div = parent_div.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
                    # 将 source_div 复制并插入到 target_div 的第一个位置
                    if source_div and target_div:
                        target_div.insert(0, source_div)
        else:
            print("No such tag!")

    def add_image(self):
        img_name = self.manager.cover_information['cover_image_name']
        # 实际复制图片到指定目录
        # 指定源图片文件的路径
        source_image_path = 'D:/blog_writer/image/' + img_name

        # 指定目标文件夹的路径
        destination_folder_path = 'D:/GitHub/morethan987.github.io/tags/assets/img/blog'

        # 确保目标文件夹存在
        if not os.path.exists(destination_folder_path):
            os.makedirs(destination_folder_path)

        # 构建目标图片文件的完整路径
        destination_image_path = os.path.join(destination_folder_path, os.path.basename(source_image_path))

        # 复制图片文件
        try:
            shutil.copy(source_image_path, destination_image_path)
            print(f"图片已成功复制到 {destination_image_path}")
        except IOError as e:
            print(f"无法复制文件。{e}")

    def write(self):
        # 将修改后的HTML内容写入到新文件中
        with open(self.obj_path, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))
        print(f"File has been modified and saved to {self.obj_path}")

    def get_templet(self):
        # 获取pages模板,返回soup对象
        cover_path = self.manager.file_index['pages_out']
        # 读取pages文件
        with open(cover_path, 'r', encoding='utf-8') as file:
            cover_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        cover_soup = BeautifulSoup(cover_content, 'lxml')
        return cover_soup
