from bs4 import BeautifulSoup


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

    def insert_blog(self):
        pass

    def write(self):
        # 将修改后的HTML内容写入到新文件中
        with open(self.obj_path, 'w', encoding='utf-8') as file:
            file.write(str(self.soup))
        print(f"File has been modified and saved to {self.obj_path}")
