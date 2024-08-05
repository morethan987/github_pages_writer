from bs4 import BeautifulSoup
import os
import shutil
import copy


class ListWriter:
    # 博客列表编写，管理流程中的第三个
    def __init__(self, manager):
        self.manager = manager
        self.templet_path = self.manager.file_index['list_in']
        self.obj_path = self.manager.file_index['list_out']
        self.soup = None

    def start(self):
        self.init()
        self.add_blog()
        self.add_image()
        self.write()

    def init(self):
        print("开始编辑bloglist，读取list模板中......")

        # 读取原始文件内容
        with open(self.templet_path, 'r', encoding='utf-8') as file:
            original_content = file.read()
        # 使用BeautifulSoup解析HTML内容
        self.soup = BeautifulSoup(original_content, 'lxml')
        if self.soup:
            print("已成功获取bloglist模板！开始编辑bloglist")
        else:
            print("获取模板失败，请重新指定路径！")

    def add_blog(self):
        # 检测是否存在当前月份
        month_div = self.soup.find('div', attrs={'py-5 xl:py-3.5 max-w-content xl:max-2xl:max-w-50rem max-xl:mx-auto '
                                                 'xl:ml-auto'})
        if month_div.get('id') == self.manager.cover_information['post_month']:
            cover_soup = self.get_templet()
            source_div = cover_soup.find_all('div', class_='grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack items-center rounded-2xl p-3.5')[0]
            target_div = month_div.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
            # 将 source_div 复制并插入到 target_div 的第一个位置
            if source_div and target_div:
                target_div.insert(0, source_div)
        else:
            month_div_copy = copy.copy(month_div)
            # 更改容器标签信息
            month_div_copy['id'] = self.manager.cover_information['post_month']
            month_div_copy.find('div', attrs={'class': 'inline-flex items-center gap-2 px-4 py-2 text-xl '
                                                       'tracking-wide text-black dark:text-white border lg:px-5 '
                                                       'section-name border-platinum dark:border-greyBlack200 '
                                                       'rounded-4xl'}).string = '<i class="fal fa-calendar text-theme">' + month_div_copy['id']
            # 更改内容信息
            target_div = month_div_copy.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
            # 先删除所有原有内容
            for child in target_div.find_all(True):
                child.extract()
            # 获取模板
            cover_soup = self.get_templet()
            source_div = cover_soup.find_all('div', attrs={
                'class': 'grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack '
                         'items-center rounded-2xl p-3.5'})[0]
            # 将 source_div 复制并插入到 target_div 的第一个位置
            if source_div and target_div:
                target_div.insert(0, source_div)
            # 完成修改并插入
            month_div.parent.insert(0, month_div_copy)

    def add_image(self):
        img_name = self.manager.cover_information['cover_image_name']
        # 实际复制图片到指定目录
        # 指定源图片文件的路径
        source_image_path = 'D:/blog_writer/image/' + img_name

        # 指定目标文件夹的路径
        destination_folder_path = 'D:/GitHub/morethan987.github.io/list/assets/img/blog'

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
