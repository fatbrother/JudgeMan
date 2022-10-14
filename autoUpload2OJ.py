from selenium import webdriver
from selenium.webdriver.common.by import By
from rich.progress import track
from pathlib import Path

driver = webdriver.Firefox()
driver.get("https://judge.kulimi.tw/")
input("please logging as root")

output_dir = Path('output_dir')
problem_list = [x for x in output_dir.iterdir() if x.is_dir()]

xpath_dict = {
    "id": "/html/body/div/div/div[3]/div[1]/div/div/form/div[1]/div[1]/div/div/div[1]/input",
    "title": "/html/body/div/div/div[3]/div[1]/div/div/form/div[1]/div[2]/div/div/div[1]/input",
    "description": "/html/body/div/div/div[3]/div[1]/div/div/form/div[2]/div/div/div/div/div[1]/div[4]",
    "input_description": "/html/body/div/div/div[3]/div[1]/div/div/form/div[3]/div[1]/div/div/div/div[1]/div[4]",
    "output_description": "/html/body/div/div/div[3]/div[1]/div/div/form/div[3]/div[2]/div/div/div/div[1]/div[4]",
    "time_limit": "/html/body/div/div/div[3]/div[1]/div/div/form/div[4]/div[1]/div/div/div/input",
    "memory_limit": "/html/body/div/div/div[3]/div[1]/div/div/form/div[4]/div[1]/div/div/div/input",
    "diff": "/html/body/div/div/div[3]/div[1]/div/div/form/div[4]/div[1]/div/div/div/input",
    "tag": "/html/body/div[1]/div/div[3]/div[1]/div/div/form/div[5]/div[3]/div/div/div/div[1]/input",
    
}


for i in track(range(5)):
    driver.get("https://judge.kulimi.tw/admin/problem/create")
    for k in xpath_dict:

        driver.find_element(By.XPATH, xpath_dict[k]).send_keys(k)
        input()
    