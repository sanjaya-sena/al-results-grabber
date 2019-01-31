from selenium import webdriver
from selenium.webdriver.common.by import By;
import pymysql.cursors

browser = webdriver.Chrome("c:\\Users\\UCSC\\Desktop\\sel\\chromedriver")


connection1 = pymysql.connect(host='localhost',
                             port=3307,
                             user='root',
                             password='1234',
                             db='aptitude-test',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection1.cursor() as cursor:
        # Read a single record
        sql = "SELECT `index_number` FROM `register`"
        cursor.execute(sql)
        for row in cursor:
            indexnumber = row['index_number']
            try:
                browser.get('https://www.doenets.lk/result/alresult.jsf');
                elem.send_keys(indexnumber)
                elem.send_keys('\n')
            except:
                browser.get('https://www.doenets.lk/result/alresult.jsf');
                elem = browser.find_element_by_name('frm:username');
                elem.send_keys(indexnumber)
                elem.send_keys('\n')

            try:
                err = browser.find_element_by_id('j_idt11:j_idt13_content').get_attribute("innerHTML");
            except:
                err = 'false'
            if err=='Invalid Index Number. Please check your index number and try again.':
                browser.get('https://www.doenets.lk/result/alresult.jsf');
                continue
            else:
                table = browser.find_element(By.ID, "j_idt16:j_idt26_data")
                rows = table.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    sub = row.find_elements(By.TAG_NAME, "td")[0]
                    grd = row.find_elements(By.TAG_NAME, "td")[1]
                    connection = pymysql.connect(host='localhost',
                                                 port=3307,
                                                 user='root',
                                                 password='1234',
                                                 db='py',
                                                 charset='utf8mb4',
                                                 cursorclass=pymysql.cursors.DictCursor)
                    try:
                        with connection.cursor() as cursor:
                            # Create a new record
                            sql = "INSERT INTO `results` (`index_number`,`subject_1`, `mark_1`) VALUES (%s,%s, %s)"
                            cursor.execute(sql, (indexnumber, sub.text, grd.text))

                        # connection is not autocommit by default. So you must commit to save
                        # your changes.
                        connection.commit()
                    finally:
                        connection.close()
                    print(sub.text)
                    print(grd.text)
finally:
    connection1.close()

