# RA, 2020-06-27

from tcga.utils import download

url = "https://www.gsea-msigdb.org/gsea/msigdb/download_file.jsp?filePath=/msigdb/release/7.1/msigdb_v7.1_files_to_download_locally.zip"
download(url).to(rel_path="original").now
