from bs4 import BeautifulSoup
from datetime import datetime

# ################ blogdetails 开始编辑 ###############################
# 指定原始文件路径
original_file_path = "D:/GitHub/morethan987.github.io/blogdetail/2024/07/local_overleaf/index.html"
# 指定新文件的存储路径
new_file_path = 'D:/blog_writer/new_blog/index_mod.html'

# 读取原始文件内容
with open(original_file_path, 'r', encoding='utf-8') as file:
    original_content = file.read()

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(original_content, 'lxml')
if soup:
    print("已成功获取blogdetails模板！开始编辑blogdetails")

# 定位meta标签
mata_tag = soup.find('meta', attrs={'name': 'keyword'})
# 检查是否找到了标签并修改内容
if mata_tag:
    print("original tag: " + str(mata_tag))
    new_content = input("input your new content: ")
    mata_tag['content'] = new_content
else:
    print("No such tag!")

# 定位网页title标签
title_tag = soup.find('title')
# 检查是否找到了标签并修改内容
if title_tag:
    print("original web title: " + str(title_tag))
    new_content = input("input your new web title: ")
    title_tag.string = new_content
else:
    print("No such tag!")

# 定位文章标题
h2_tag = soup.find("h2", attrs={
    'class': 'text-2xl font-semibold leading-normal text-black dark:text-white mt-7 lg:mt-10 article-title lg:text-3xl lg:leading-normal'})
# 检查是否找到了标签并修改内容
if h2_tag:
    print("original detail title: " + str(h2_tag.string))
    new_content = input("input your new detail title: ")
    h2_tag.string = new_content
else:
    print("No such tag!")

# 定位文章类别
if soup.find('h6', string='CATEGORY:'):
    p_tag = soup.find('h6', string='CATEGORY:').find_next_sibling('p')
    # 检查是否找到了标签并修改内容
    if p_tag:
        print("original category: " + str(p_tag.string))
        new_content = input("input your new content: ")
        p_tag.string = new_content
    else:
        print("No such tag!")

# 定位发布时间
new_post_date = ""  # 存储新博客发布时间
if soup.find('h6', string='POSTED ON:'):
    p_tag = soup.find('h6', string='POSTED ON:').find_next_sibling('p')
    # 检查是否找到了标签并修改内容
    if p_tag:
        print("original post date: " + str(p_tag.string))
        new_content = input("input your new post date: ")
        p_tag.string = new_content
        new_post_date = p_tag.string
    else:
        print("No such tag!")
else:
    print("No such tag!")

tag_names = []  # 存储新输入的标签
# 定位tags
target_div = soup.find('div', attrs={'class': 'flex flex-wrap items-center gap-2.5'})
if target_div:
    # 先删除所有原有内容
    for child in target_div.find_all(True):
        child.extract()
    # 再写入新的内容
    print("请输入你的新标签，输入ok完成编辑")
    while True:
        new_tag_name = input("Your new tag:")
        if new_tag_name != "ok":
            new_tag = soup.new_tag('a', attrs={'href': "https://morethan987.github.io/tags/#" + new_tag_name.lower(),
                                               'class': "inline-block border border-dashed border-greyBlack rounded-md text-sm py-1.5 px-2 transition-all hover:text-theme dark:hover:text-white"})
            new_tag.string = new_tag_name
            target_div.append(new_tag)
            tag_names.append(new_tag_name)
        else:
            break
else:
    print("No such tag!")

# 将修改后的HTML内容写入到新文件中
with open(new_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"File has been modified and saved to {new_file_path}")
# ################ blogdetails 结束编辑 ###############################

# ################ blogpages 开始编辑 ###############################
# 指定原始文件路径
original_file_path = "D:/GitHub/morethan987.github.io/blogpages/index.html"
# 指定新文件的存储路径
new_file_path = 'D:/blog_writer/new_page/index_mod.html'
# 读取原始文件内容
with open(original_file_path, 'r', encoding='utf-8') as file:
    original_content = file.read()

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(original_content, 'lxml')
if soup:
    print("已成功获取blogpages模板！开始编辑blogpages")

original_tag_names = []
# 定位tags Section
target_div = soup.find('div', attrs={'class': 'inline-flex flex-wrap items-center gap-2 mb-5 text-sm md:gap-4'})
if target_div:
    # 获取原标签
    for child in target_div.find_all(True):
        original_tag_names.append(child.string)

    # 标签查重
    for tag_name in tag_names:
        if tag_name not in original_tag_names:
            new_tag = soup.new_tag('a', attrs={'href': "https://morethan987.github.io/tags/#" + tag_name.lower(),
                                               'class': "inline-block px-3.5 py-2 transition duration-300 border border-dashed text-black dark:text-white/70 border-platinum dark:border-greyBlack rounded-3xl md:px-5 md: md:py-2 hover:text-theme dark:hover:text-white"})
            new_tag.string = tag_name
            target_div.append(new_tag)
            print("Already add a new tag!")

else:
    print("No such tag!")

# 轮换最新blog
target_div = soup.find('div', attrs={'class': 'blog-list md:space-y-7.5 space-y-5'})
if target_div:
    # 获取最后一个子标签
    last_child_copy = target_div.find_all('div', attrs={'class': 'grid md:gap-2 grid-cols-12 overflow-hidden article group bg-flashWhite dark:bg-metalBlack items-center rounded-2xl p-3.5'})[-1]

    # 更改链接地址信息
    print("chang file name, you need to new a file in GitHub.io/blogdetail")
    print("the year and month is your current year and month")
    print("you'd better do it now!")
    print("your original file address: ../blogdetail/2024/07/<local_overleaf>")
    new_file_name = input("your new file name: ")
    parent_div = last_child_copy.find('div', attrs={'class': 'flex col-span-12 overflow-hidden thumbnail sm:col-span-6 md:col-span-5'})
    new_address = '../blogdetail/'+f"{datetime.now().year}/{datetime.now().month:02d}/"+new_file_name
    parent_div.find('a')['href'] = new_address
    last_child_copy.find('div', attrs={'class': 'read-details'}).find('a')['href'] = new_address

    # 更改标签内容
    cover_tag = last_child_copy.find('div', attrs={'class': 'text-sm font-medium tags'})
    a_tag = cover_tag.find('a')
    a_tag['href'] = 'https://morethan987.github.io/tags/#' + tag_names[0].lower()
    a_tag.string = tag_names[0]
    cover_tag.find('span').string = new_post_date

    # 更改封面标题
    new_cover_title = input("your new cover title: ")
    cover_title = last_child_copy.find('div', attrs={'class': 'post-title mt-3 md:mt-4.5 mb-6 md:mb-8'}).find('a')
    cover_title.string = new_cover_title
    cover_title['href'] = new_address

    # 将复制的内容插入到标签的开头
    target_div.insert(0, last_child_copy)

else:
    print("No such tag!")

# 将修改后的HTML内容写入到新文件中
with open(new_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))
# ################ blogpages 结束编辑 ###############################

# ################ list 开始编辑 ###############################
# 指定原始文件路径
original_file_path = "D:/GitHub/morethan987.github.io/list/index.html"
# 指定新文件的存储路径
new_file_path = 'D:/blog_writer/new_list/index_mod.html'
# 读取原始文件内容
with open(original_file_path, 'r', encoding='utf-8') as file:
    original_content = file.read()

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(original_content, 'lxml')
if soup:
    print("已成功获取list模板！开始编辑blogpages")

# ################ list 结束编辑 ###############################

# ################ tags 开始编辑 ###############################

# ################ tags 结束编辑 ###############################


# ################ 所有关联文件编辑结束 ###############################
print("Now you need to write your bolg content in new_blog")
print("And add your new picture in the reference position")
