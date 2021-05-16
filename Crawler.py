
#DCCON
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import sys
import time
import os
path = "C:/Selenium/chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36") 
driver = webdriver.Chrome(path, chrome_options=options)
header={'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"}
filterlist=["짭","카피","열화","트레이싱","문제시","문제 시"]
nowpath=os.getcwd()
def filtering(_string,filterlist):
    for i in filterlist:
        if _string.find(i) != -1:
            return False
    return True
for page in range(1,17):#20210505 기준으로 17페이지인데 더 추가으면 바꾸세용
    print("Page {0}".format(page))
    driver.get("https://dccon.dcinside.com/hot/{0}/title/%EC%AD%90%EC%96%B4".format(str(page)))
    driver.implicitly_wait(5)
    for i in range(15):
        driver.find_elements_by_css_selector("span.dcon_frame.blue_brd")[i].click()
        time.sleep(1)
        dcconname=driver.find_elements_by_css_selector("h4.font_blue")[0].text
        dccondesc=driver.find_elements_by_css_selector("p.inner_txt")[0].text
        if filtering(dcconname, filterlist) and filtering(dccondesc, filterlist):#짭쭐어콘 구분
            img=driver.find_elements_by_css_selector("span.img_dccon")
            if not os.path.exists(dcconname):
                os.makedirs(dcconname)
                print("Checking {0}, found {1} images, Start downloading...".format(dcconname,len(img)))
                for j in range(len(img)):
                    url=img[j].find_element_by_css_selector("img").get_attribute("src")
                    urllib.request.urlretrieve(url, "{0}/{0}_{1}.png".format(dcconname, str(j)))
                    print("{0}_{1} is done!".format(dcconname,str(j)))
                    time.sleep(1)
                print("\n{0} is all done! Checking GIF Format...".format(dcconname))
                for j in range(len(img)):
                    f=open("{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".png"),"rb")
                    data=f.read()
                    if data[0:3].decode(encoding='CP949')=='GIF':
                        f.close()
                        print("{0} seems like GIF file, changing extension...".format(dcconname+"_"+str(j)))
                        os.rename("{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".png"),"{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".gif"))
                    else:
                        f.close()
                print("{0} is all done! Waiting 10 Sec to avoid Trafic detector...".format(dcconname))
                time.sleep(10)
            else:
                filelist = os.listdir(nowpath+"//{0}".format(dcconname))
                if len(filelist)<len(img):
                    print("The folder exists, but there's not enough image in folder({0} Left), Downloading {1}...".format(len(img)-len(filelist),dcconname))
                    for j in range(len(filelist),len(img)):
                        url=img[j].find_element_by_css_selector("img").get_attribute("src")
                        urllib.request.urlretrieve(url, "{0}/{0}_{1}.png".format(dcconname, str(j)))
                        print("{0}_{1} is done!".format(dcconname,str(j)))
                        time.sleep(1)
                    print("\n{0} is all done! Checking GIF Format...".format(dcconname))
                    for j in range(len(img)):
                        f=open("{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".png"),"rb")
                        data=f.read()
                        if data[0:3].decode(encoding='CP949')=='GIF':
                            f.close()
                            print("{0} seems like GIF file, changing extension...".format(dcconname+"_"+str(j)))
                            os.rename("{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".png"),"{0}/{1}/{2}".format(nowpath,dcconname,dcconname+"_"+str(j)+".gif"))
                        else:
                            f.close()
                    print("{0} is all done! Waiting 10 Sec to avoid Trafic detector...".format(dcconname))
                    time.sleep(10)
                else:
                    print("{0} already exists in folder, skipping...".format(dcconname))
                time.sleep(1)
        else:
            print("{0} seems like unoffical dccon, skipping...".format(dcconname))
            time.sleep(1)
        driver.find_element_by_css_selector("em.sp_img.icon_bgblueclose").click()
input()
