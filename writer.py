from bs4 import BeautifulSoup

# ################ blogpages 开始编辑 ###############################
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
    print("已成功获取blogpages模板！")

# 定位meta标签
mata_tag = soup.find('meta', attrs={'name': 'keyword'})
# 检查是否找到了标签并修改内容
if mata_tag:
    print("original tag: "+str(mata_tag))
    new_content = input("input your new content: ")
    mata_tag['content'] = new_content
else:
    print("No such tag!")

# 定位title标签
title_tag = soup.find('title')
# 检查是否找到了标签并修改内容
if title_tag:
    print("original tag: "+str(title_tag))
    new_content = input("input your new title: ")
    title_tag.string = new_content
else:
    print("No such tag!")

# 定位文章标题
h2_tag = soup.find("h2", attrs={'class': 'text-2xl font-semibold leading-normal text-black dark:text-white mt-7 lg:mt-10 article-title lg:text-3xl lg:leading-normal'})
# 检查是否找到了标签并修改内容
if h2_tag:
    print("original content: "+str(h2_tag.string))
    new_content = input("input your new content: ")
    h2_tag.string = new_content
else:
    print("No such tag!")

# 定位文章类别
if soup.find('h6', string='CATEGORY:'):
    p_tag = soup.find('h6', string='CATEGORY:').find_next_sibling('p')
    # 检查是否找到了标签并修改内容
    if p_tag:
        print("original category: "+str(p_tag.string))
        new_content = input("input your new content: ")
        p_tag.string = new_content
    else:
        print("No such tag!")

# 定位发布时间
if soup.find('h6', string='POSTED ON:'):
    p_tag = soup.find('h6', string='POSTED ON:').find_next_sibling('p')
    # 检查是否找到了标签并修改内容
    if p_tag:
        print("original post date: "+str(p_tag.string))
        new_content = input("input your new post date: ")
        p_tag.string = new_content
    else:
        print("No such tag!")

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
            new_tag = soup.new_tag('a', attrs={'href': "https://morethan987.github.io/tags/#"+new_tag_name.lower(),
                                               'class': "inline-block border border-dashed border-greyBlack rounded-md text-sm py-1.5 px-2 transition-all hover:text-theme dark:hover:text-white"})
            new_tag.string = new_tag_name
            target_div.append(new_tag)
        else:
            break
else:
    print("No such tag!")

# 将修改后的HTML内容写入到新文件中
with open(new_file_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"File has been modified and saved to {new_file_path}")
# ################ blogpages 结束编辑 ###############################

