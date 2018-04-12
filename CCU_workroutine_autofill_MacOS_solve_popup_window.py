from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, calendar, os, sys
from selenium.common.exceptions import NoAlertPresentException,UnexpectedAlertPresentException

choose_browser=int(input("請選擇你常使用的瀏覽器(GoogleChrome請選 1 ,Firefox請選2)："))

path = os.getcwd()
print(path)

if os.path.exists(str(path)+r'/information.html'):
    print ("將自動登入")
    with open('information.html','r') as test:
        ID_number=test.readline().rstrip()
        password=test.readline().rstrip()
        job=test.readline().rstrip()
else:
    # Login information
    ID_number = str(input('請輸入帳號：'))
    password = str(input("請輸入密碼："))
    job = "'" + str(input('請輸入登入身分 (兼任助理為3)：')) + "'"
    print('下次將自動登入')
    with open('information.html','w') as Login:
        Login.write(ID_number+'\n')
        Login.write(password+'\n')
        Login.write(job+'\n')

num_proj =int(input('你要填幾個計畫:'))

if num_proj == 0:
    print('沒有計畫要填，還來亂!!!!!!')
    #driver.quit()
    sys.exit()
elif num_proj == 1:
    if os.path.exists(str(path)+r'/routine_list.html'):
        print('將套用上次你所輸入之工作資訊與工作項目')
        with open('routine_list.html','r') as inf:
            projtype = inf.readline().rstrip()
            workhour = inf.readline().rstrip()
            workroutine = []
            while '' not in workroutine:
                workroutine.append(inf.readline().rstrip())
            workroutine.remove('')
            i = len(workroutine)
    else:
        projtype = "'" + str(input('請輸入計畫代碼 ex:105-00018：')) + "'"
        workhour=str(input('請輸入工作時數：')) #input workhour
        workroutine = []
        print('請輸入工作項目 輸入0則結束輸入')
        i = 0
        while True:
            print ('第',i+1,'項')
            workroutine.append(str(input("請輸入工作項目："))) #input workroutine
            if '0' not in workroutine:
                i +=1
            else:
                del workroutine[-1]
                workroutine_2 = workroutine.copy()
                break
        with open('routine_list.html','w') as routine_inf:
            routine_inf.write(projtype+'\n')
            routine_inf.write(workhour+'\n')
            while len(workroutine_2) != 0:
                routine_inf.write(workroutine_2.pop()+'\n')

else:
    print('系統建構中')
    '''if os.path.exists(str(path)+r'multi_proj'):



    else:
        os.mkdir(r'multi_proj')'''

year = str(input('請輸入年份：'))
month = str(input('請輸入月份：'))

if choose_browser == 2:
    driver = webdriver.Firefox(executable_path="/usr/local/bin/geckodriver")
elif choose_browser == 1:
    driver = webdriver.Chrome()
else:
    print("鬧屁鬧")

driver.get('https://miswww1.ccu.edu.tw/pt_proj/index.php')
driver.set_page_load_timeout(50)
driver.implicitly_wait(30)
user = driver.find_element_by_name("staff_cd").send_keys(ID_number)
passwd = driver.find_element_by_name("passwd").send_keys(password)
driver.find_element_by_xpath(("//select[@name='proj_type']/option[@value=%s]") % job).click()
driver.find_element_by_xpath("/html/body/center/form/input[1]").click()
print("已進入工作日誌系統")
time.sleep(1)  # delay seconds

#Enter Workroutine Space & write in

date = calendar.monthcalendar((int(year)+1911),int(month))
workday = set()
for everyweek in date:
        del everyweek[-1]
        del everyweek[-1]
        for day in everyweek:
            workday.add(day)
workday.remove(0)
workday = list(workday)

print ('你的工作項目有',workroutine,'共', i,'項工作將隨機分布填入')
print(month,'月有 ' ,workday, '日為工作日')

s = 0

# popup window resolve
try:
    alert = driver.switch_to_alert()
    alert.accept()
except UnexpectedAlertPresentException:
    pass
except NoAlertPresentException:
    pass


for eachday in workday:
    driver.get("https://miswww1.ccu.edu.tw/pt_proj/main2.php")
    driver.find_element_by_xpath(("//select[@name='type']/option[@value=%s]")%(projtype)).click()

    y = driver.find_element_by_name('yy')
    y.send_keys(Keys.BACK_SPACE*10)
    y.send_keys(year)

    m = driver.find_element_by_name('mm')
    m.send_keys(Keys.BACK_SPACE*10)
    m.send_keys(month)

    d = driver.find_element_by_name('dd')
    d.send_keys(Keys.BACK_SPACE*10)
    d.send_keys(str(eachday))

    driver.find_element_by_name('hrs').send_keys(workhour)
#   driver.find_element_by_name('workin').send_keys(random.choice(workroutine))                    #隨機填入工作內容
    driver.find_element_by_name('workin').send_keys(workroutine[s%len(workroutine)])               #依序填入工作內容
    driver.find_element_by_xpath("/html/body/form/center/input[1]").click()
    s+=1
    print ('以輸入',year,' 年 ',month, ' 月 ', eachday, '日  工作',workhour,' 小時' )


#Finish & Save
time.sleep(2)
driver.get("https://miswww1.ccu.edu.tw/pt_proj/main2.php")
time.sleep(5)
driver.find_element_by_xpath("/html/body/form/center/input[2]").click()
print('全數輸入完畢')
driver.find_element_by_xpath("/html/body/center[2]/input").click()
print (year,' 年 ',month, ' 月 的工作日誌已全數填寫完畢 並 儲存於資料庫')
print ('請自行產生批號')