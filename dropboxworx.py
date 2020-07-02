import dropbox
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

# LOGIN STEP #
dbx = dropbox.Dropbox('insert token here')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get('https://www.label-worx.com/labelmanager/index.php?option=demos#')
time.sleep(1)
driver.find_element_by_id('myusername').send_keys('insert username here')
driver.find_element_by_id('mypassword').send_keys('insert password here')
driver.find_element_by_class_name('lw_login_button').click()

# COLLECTING SONGS INTO AN ARRAY #
page = driver.page_source
soup = BeautifulSoup(page, 'lxml')
demos = soup.select("tr[class^=row]")
for demo in demos:
    info = demo.find_all('td')
    track = info[2].string
    contact = info[4].string
    link = 'https://www.label-worx.com/labelmanager/'+info[8].select_one("a[href*=edit]")['href']
    try:
        dbx.files_save_url('/demodownloads/' + track + ' - ' + contact + '.wav', link)
    except dropbox.exceptions.ApiError:
        dbx.files_save_url('/demodownloads/' + contact + '.wav', link)
    print('uploaded '+track+' by '+contact+' to dropbox')
    time.sleep(4)
print("finished moving, don't forget to delete the audio in labelworx!")
