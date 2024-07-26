from bs4 import BeautifulSoup


class ListWriter:
    # 博客列表编写，管理流程中的第三个
    def __init__(self, manager):
        self.manager = manager
        self.templet_path = self.manager.file_index['list_in']
        self.obj_path = self.manager.file_index['list_out']
        self.soup = None

    def start(self):
        self.init()

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