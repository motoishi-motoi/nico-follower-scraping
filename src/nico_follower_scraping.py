import chromedriver_binary
from selenium import webdriver
import time
import csv
import datetime

def init_settings():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage') # メモリ改善
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')               
    options.add_argument('--proxy-server="direct://"')         
    options.add_argument('--proxy-bypass-list=*')              
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--lang=ja')                          
    options.add_argument("--log-level=3")
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(375,812)
    driver.implicitly_wait(3) # 秒

    return driver

def follower_list(driver, url):
    driver.get(url)
    follower_list = []

    while True:
        try:
            # さらに表示のクリック前で読み込んで、部分的に読み込まれない仕様に対応
            for follower in get_url_list(driver, follower_list):
                follower_list.append(follower)
            more = driver.find_element_by_xpath("//button[@class='ShowMoreList-more']")
            # より正確に読み込みたい場合、下3行のコメントアウトも解除すると良いです（ただしさらに処理が重くなる）
            # time.sleep(1)
            # for follower in get_url_list(driver, get_follower_list):
            #     follower_list.append(follower)
            more.click()
            print('clicked')
            time.sleep(3)
        except:
            print('click comp')
            break

    return follower_list

def get_url_list(driver, follower_list):
    follower_url = []
    for follower in follower_list:
        follower_url.append(follower.get_attribute("href"))
    return follower_url

def dup_delete(list_data):
    list_to_set = set(list_data)
    set_to_list = list(list_to_set)
    return set_to_list

def get_user_data(follower_url_list):

    print(f"取得データ数 : {len(follower_url_list)}")

    follower_datas = []
    data = []

    for follower_url in follower_url_list:
        driver.get(follower_url)

        data = []

        username = driver.find_element_by_xpath("//h3[@class='UserDetailsHeader-nickname']").text
        follow = driver.find_element_by_xpath("//div[@class='UserDetailsStatusItem UserDetailsStatus-item'][1]/a").text
        follower = driver.find_element_by_xpath("//div[@class='UserDetailsStatusItem UserDetailsStatus-item'][2]/a").text
        userpage = follower_url

        data.append(str(username))
        data.append(k_convert(follow.replace('Following', '').replace('\n', '')))
        data.append(k_convert(follower.replace('Followers', '').replace('\n', '')))
        data.append(userpage)

        follower_datas.append(data)

        progress = f"{len(follower_datas)} / {len(follower_url_list)}"
        if(len(follower_datas) % 10 == 0 or len(follower_datas) == len(follower_url_list)):
            print(progress)

        time.sleep(10)

    return follower_datas

def create_csv(follower_datas):
    
    csvDate = datetime.datetime.today().strftime("%Y%m%d_%H%M")

    csvFileName = 'csv/follower_list' + csvDate + '.csv'
    f = open(csvFileName, 'w', encoding='utf-8', errors='ignore')
    writer = csv.writer(f, lineterminator='\n')

    csv_header = ['ユーザー名', 'フォロー数', 'フォロワー数', 'ユーザーページ']
    writer.writerow(csv_header)

    for follower_data in follower_datas:
        writer.writerow(follower_data)

def k_convert(string):
    if('K' in string):
        number = string.replace('K', '')
        number = float(number) * 1000
        return int(number)
    else:
        return string

driver = init_settings()
tmp_follower_url_list = follower_list(driver, 'https://www.nicovideo.jp/user/2090155/follow/follower?ref=pc_userpage_top')
follower_url_list = dup_delete(tmp_follower_url_list)
follower_datas = get_user_data(follower_url_list)
create_csv(follower_datas)

driver.quit()