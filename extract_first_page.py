import os
from pypdf import PdfReader, PdfWriter

def merge_first_pages(pdf_files, output_path):
    # 创建一个PdfWriter对象来保存合并后的PDF
    pdf_writer = PdfWriter()

    for pdf_file in pdf_files:
        # 创建一个PdfReader对象来读取PDF文件
        pdf_reader = PdfReader(pdf_file)
        
        # 提取第一页并添加到PdfWriter对象中
        first_page = pdf_reader.pages[0]
        pdf_writer.add_page(first_page)

        second_page = pdf_reader.pages[1]
        pdf_writer.add_page(second_page)
    
    # 将合并后的内容写入到输出文件
    with open(output_path, 'wb') as output_pdf:
        pdf_writer.write(output_pdf)

# 获取当前目录下所有PDF文件
pdf_directory = './ICLR_2024_Papers/accept-oral'  # 替换为你的PDF文件所在目录
pdf_files = [os.path.join(pdf_directory, f) for f in os.listdir(pdf_directory) if f.endswith('.pdf')]

# 输出合并后的PDF文件路径
if not os.path.exists("merge_output"):
    os.makedirs("merge_output", exist_ok=True)
output_pdf_path = './merge_output/merged_first_pages.pdf'  # 替换为你想保存合并后的PDF文件路径

# 合并PDF文件的第一页
merge_first_pages(pdf_files, output_pdf_path)

print(f"Merged PDF saved to {output_pdf_path}")