import requests

url_transactions = "https://www.philippe-fournier-viger.com/spmf/datasets/fruithut_original.txt"
url_taxonomy = "https://www.philippe-fournier-viger.com/spmf/datasets/Fruithut_taxonomy_data.txt"

response_transations = requests.get(url_transactions)
transactions = response_transations.text

response_taxonomy = requests.get(url_taxonomy)
taxonomy = response_taxonomy.text
