import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
# Define the URL
url = "https://dwaprices.com/med.php?id=15"

# Send a GET request to the URL
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
}
#response = requests.get(url, headers=headers)
#print(response.content)
# Check if the request was successful

def save_dataframe(df, base_filename):
    """Saves a Pandas DataFrame to both XLS (Excel) and CSV files.

    Args:
        df: The Pandas DataFrame to save.
        base_filename: The base filename (without extension) to use for both files.
                       The files will be named base_filename.xls and base_filename.csv.
    """

    try:
        # Save to Excel (xls)
        # df.to_excel(f"{base_filename}.xls", index=False)  # index=False prevents saving the DataFrame index
        # print(f"DataFrame saved to {base_filename}.xls")

        # Save to CSV
        df.to_csv(f"{base_filename}.csv", index=False, encoding='utf-8')  # UTF-8 encoding handles most characters
        print(f"DataFrame saved to {base_filename}.csv")

    except Exception as e:
        print(f"An error occurred while saving the DataFrame: {e}")

barcodes = []
names = []
num= []
manufacture = []
scientific_name = []
price=[]
update=[]
lastID=2000
for i in range(1000, lastID):
    print(i)
    product_url = f"https://dwaprices.com/med.php?id={i}"
    product_page = requests.get(product_url , headers=headers)
    time.sleep(0.000000001)
    product_soup = BeautifulSoup(product_page.content, "html.parser")
    table = product_soup.find("table", class_ = "newwtbl")
    if table:
        table_rows = table.find_all("tr")
        barcodes.append(table_rows[7].text.replace("الباركود الدولي ", " "))
        update.append(table_rows[6].text.replace("تحديث السعر ", " "))
        price.append(table_rows[5].text.replace("السعر القديم ", " "))
        num.append(table_rows[3].text.replace("عدد الوحدات", " "))
        names.append(table_rows[0].text.replace("الاسم التجاري", " "))
        manufacture.append(table_rows[2].text.replace("الشركة ", " "))
        scientific_name.append(table_rows[1].text.replace("الاسم العلمي", " "))

columns = {
    'name': names,
    'scientific_name': scientific_name,
    'num' : num ,
    'price' : price ,
    'update ' : update ,
    'barcodes' : barcodes,
    'manufacture' : manufacture}
df = pd.DataFrame(columns)
save_dataframe(df, f"my_data{lastID}s") 