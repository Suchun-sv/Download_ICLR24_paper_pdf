import requests
from bs4 import BeautifulSoup
import tqdm
import os, re

# Function to sanitize and format the title
def sanitize_title(title):
    # Remove special characters
    sanitized_title = re.sub(r'[^\w\s]', '', title)
    # Replace spaces with underscores
    formatted_title = re.sub(r'\s+', '_', sanitized_title)
    return formatted_title

def parse():
    # 创建一个文件夹保存下载的论文
    if not os.path.exists("ICLR_2024_Papers"):
        os.makedirs("ICLR_2024_Papers")

    # 指定本地HTML文件的路径
    file_path = "./pages/oral.html"

    # 读取本地HTML文件内容
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(html_content, "html.parser")

    # 解析页面内容，获取所有论文链接
    paper_list = [ _ for _ in soup.find_all("div", class_="note undefined")]
    paper_list_info = []
    for paper in tqdm.tqdm(paper_list):
        # paper_url = paper_link["href"]
        # paper_title = paper_link.get_text().strip()
        # paper_contents = [_ for _ in paper.children]
        # Keywords = paper_contents[1].get_text().strip()
        # Abstract = paper_contents[3].get_text().strip()

        # 提取信息
        paper_info = {}

        # 提取标题和链接
        import re
        title_link = paper.find("h4").find("a")
        paper_info["title"] = re.sub(r'\s+', ' ', title_link.text.strip())
        paper_info["link"] = title_link["href"]

        # 提取PDF下载链接
        pdf_link = paper.find("a", class_="pdf-link")
        if pdf_link:
            paper_info["pdf_link"] = pdf_link["href"]

        # 提取作者信息
        authors = []
        for author in paper.find("div", class_="note-authors").find_all("a"):
            authors.append(re.sub(r'\s+', ' ', author.text.strip()))
        paper_info["authors"] = ", ".join(authors)

        # 提取元信息（发布日期、修改日期等）
        # meta_info = paper.find("ul", class_="note-meta-info").find_all("li")
        # published_info = meta_info[0].text.strip()
        # paper_info["published_date"] = published_info.split(',')[0].replace("Published:", "").strip()
        # paper_info["last_modified_date"] = published_info.split(',')[1].replace("Last Modified:", "").strip()
        # paper_info["presentation_type"] = meta_info[1].text.strip()
        # paper_info["readers"] = meta_info[2].text.strip().replace("Readers: ", "")
        # paper_info["replies"] = meta_info[3].text.strip()

        # 提取更多详细信息
        # details_div = paper.find("div", class_="collapse-indent")
        # if details_div:
        #     details = details_div.find_all("div", class_="note-content")
        #     for detail in details:
        #         field_name = detail.find("strong", class_="note-content-field").text.strip(":")
        #         field_value = detail.find("span", class_="note-content-value").text.strip()
        #         paper_info[field_name] = field_value

        # 提取摘要
        abstract_div = paper.find("div", class_="note-content-value markdown-rendered")
        if abstract_div:
            abstract = " ".join([re.sub(r'\s+', ' ', p.get_text().strip()) for p in abstract_div.find_all("p")])
            paper_info["abstract"] = abstract
        paper_list_info.append(paper_info)

    # 下载
    error_list = []
    for paper_info in paper_list_info:
        try:
            # 格式化标题
            formatted_title = sanitize_title(paper_info["title"])
            # 构建保存路径
            save_path = os.path.join("ICLR_2024_Papers", f"{formatted_title}.pdf")
            # 下载PDF文件
            if os.path.exists(save_path):
                print(f"Already downloaded: {formatted_title}.pdf")
                continue
            response = requests.get(paper_info["pdf_link"], stream=True)
            with open(save_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)
            print(f"Downloaded: {formatted_title}.pdf")
        except KeyError:
            print(f"PDF link not found for {paper_info['title']}")
            error_list.append(paper_info['title'])
    print("The total number of papers is: ", len(paper_list_info), "The number of papers downloaded successfully is: ", len(paper_list_info) - len(error_list), "The number of papers failed to download is: ", len(error_list))
    # 再度显示下载失败的论文
    print("The following papers failed to download:")
    for i, error in enumerate(error_list):
        print(f"#{i}/{len(error_list)}", error)
    # save error list to txt
    with open("error_list.txt", "w") as f:
        for item in error_list:
            f.write("%s\n" % item)

if __name__ == "__main__":
    parse()