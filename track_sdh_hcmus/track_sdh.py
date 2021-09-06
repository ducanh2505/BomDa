import requests
from bs4 import BeautifulSoup
import datetime
import os

print('requests version: ',requests.__version__)
## DECLARE 
PAGE = 'https://sdh.hcmus.edu.vn/tuyen-sinh-cao-hoc/'
PROJ_DIR = 'track_sdh_hcmus'
RECORD_FILE = os.path.join(PROJ_DIR,'newest_post.txt')
DATETIME_FORMAT = r'%d/%m/%Y  %I:%M %p'
print("RECORD_FILE: ",RECORD_FILE)

# Def functions
def record_post(post_name,date_post,RECORD_FILE = RECORD_FILE):
    with open(RECORD_FILE,'w') as f:
        f.writelines(f'{post_name}\n{date_post}')
def read_recorded(RECORD_FILE):
    with open(RECORD_FILE,'r') as f:
        name,date = f.readlines()
    return name[:-1],date 
def main():
    r = requests.get(PAGE)
    soup = BeautifulSoup(r.text, 'html.parser')
    posts = soup.find_all("li", class_="cat-post-item")
    newest_post = posts[0]
    newest_name,newest_date = newest_post.text.split('\n')


    # check record is exist
    
    if not os.path.exists(RECORD_FILE):
        record_post(newest_name,newest_date,RECORD_FILE)
    else:
        recored_name,recored_date = read_recorded(RECORD_FILE)
        recored_date = datetime.datetime.strptime(recored_date,DATETIME_FORMAT)
        newest_date = datetime.datetime.strptime(newest_date,DATETIME_FORMAT)
        if newest_date > recored_date:
            print("!!!!!!!!!! NEW POST !!!!!!!!! ")
            record_post(newest_name,newest_date,RECORD_FILE)
        else:
            print("====>NOTHING CHANGE")

if __name__ == "__main__":
    main()