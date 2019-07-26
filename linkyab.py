# importing libraries
from tkinter import *
from tkinter.ttk import Progressbar
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import threading 
import time


#creat window
window = Tk()
window.title("بررسی لینک")
window.config(bg="white")


#run selenium
options = webdriver.ChromeOptions()   
options.add_argument('--headless')
Windows_driverPath = r'file/chromedriver_win32.exe'


#founctions
def popupmsg(msg):
    try:
        t_check.join()
    except:
        pass
    #global popup
    popup = Tk()
    popup.wm_title("توجه")
    NORM_FONT = ("IRANSans 10")
    global po_label
    po_label = Label(popup, text=msg, font=NORM_FONT,fg="gray25",bg="white")
    po_label.pack(side=TOP, fill="x",padx=10,pady=10)
    global B1
    B1 = Button(popup,bd=1, font=NORM_FONT, text="باشه",fg="white",bg="gray25", command = popup.destroy)
    B1.pack(side=TOP,padx=10,pady=10)
    #popup.geometry("260x100")
    popup.config(bg="white")
    try:
        popup.wm_iconbitmap(r'file/link_0Z3_icon.ico')
    except:
        pass
    popup.resizable(width=False, height=False)
    popup.mainloop()

def check_link():
    get_name.config(text=":نام",fg="gray60")
    get_ip.config(text=":ای پی",fg="gray60")
    get_resident.config(text=":محل سرور",fg="gray60")
    get_traffic.config(text=":تعرفه ترافیک",fg="gray60")
    site = name_site.get()

    if site == "":
        popupmsg("ابتدا نام سایت را وارد کنید")

    else:
        '''try:
            t_check.join()
        except:
            pass
        try:
            driver.close()
        except:
            pass
        try:
            popup.quit()
        except:
            pass'''
        progress.start()
        global driver
        driver = webdriver.Chrome(executable_path=Windows_driverPath,chrome_options=options)
        try:
            driver.get("http://linkirani.ir/?url={}".format(site))
        except:
            popupmsg("تلاش مجدد")
        try:
            url = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#link"))).text
            ip_url = driver.find_element_by_css_selector('#ips').text
        except (TimeoutError) :
            url = "time out"
            pass
        except :
            url = "not found"
            pass
        try:
            ip_ = str(ip_url).replace("IP: ","")
        except:
            pass
        '''file_ = open('filename.png', 'wb')
        file_.write(driver.find_element_by_css_selector('.flag').screenshot_as_png)
        file_.close()
        img = ImageTk.PhotoImage(Image.open("./filename.png"))'''
        
        if url == "لینک ایرانی است و ترافیک آن داخلی حساب می‌شود":
            progress.stop()
            get_name.config(text="{} :نام سایت".format(site),fg="gray25")
            get_ip.config(text="{} :ای پی".format(ip_),fg="gray25")
            get_resident.config(fg="spring green4",text="محل سرور: داخل ایران")
            get_traffic.config(fg="spring green4",text="تعرفه ترافیک: ترافیک نیم بها")
            
        elif url == "لینک خارجی است و ترافیک آن داخلی حساب نمی‌شود":
            progress.stop()
            get_name.config(text="{} :نام سایت".format(site),fg="gray25")
            get_ip.config(text="{} :ای پی".format(ip_),fg="gray25")
            get_resident.config(fg="red",text="محل سرور: خارج از ایران")
            get_traffic.config(fg="red",text="تعرفه ترافیک: ترافیک عادی")
            
        elif url == "لینک ایرانی است ولی ترافیک آن داخلی حساب نمی‌شود":
            progress.stop()
            get_name.config(text="{} :نام سایت".format(site),fg="gray25")
            get_ip.config(text="{} :ای پی".format(ip_),fg="gray25")
            get_resident.config(fg="spring green4",text="محل سرور: داخل ایران")
            get_traffic.config(fg="red",text="تعرفه ترافیک: ترافیک عادی")
            
        elif url == "not found":
            progress.stop()
            popupmsg("لینک وجود ندارد")

        elif url == "time out":
            progress.stop()
            popupmsg("مدت زمان تمام شد")
        else:
            progress.stop()
            popupmsg("ارور نامعلوم دوباره تلاس کنید")
        driver.close()
        try:
            driver.close()
            progress.stop()
        except:
            pass
        try:
            t_check.join()
            progress.stop()
        except:
            pass

def t_check_link():
    if(name_site.get() != ""):
        global t_check
        t_check = threading.Thread(target=check_link)
        t_check.start()
    else:
        popupmsg("ابتدا نام سایت را وارد کنید")

def bind_t_check_link(event):
    if(name_site.get() != ""):
        global t_check
        t_check = threading.Thread(target=check_link)
        t_check.start()
    else:
        popupmsg("ابتدا نام سایت را وارد کنید")

def exit_event(event):
    
    try:
        t_check.join()
    except:
        pass
    try:
        driver.close()
    except:
        pass
    try:
        popup.quit()
    except:
        pass
    window.quit()

def t_whois():
    if(name_site.get() != ""):
        global t_who
        t_who = threading.Thread(target=whois)
        t_who.start()
    else:
        popupmsg("ابتدا نام سایت را وارد کنید")

def whois():
    progress.start()
    driver = webdriver.Chrome(executable_path=Windows_driverPath,chrome_options=options)
    driver.get("https://www.whois.net/")
    name = driver.find_element_by_css_selector("#domain_search")
    name.send_keys(name_site.get())
    try:
        driver.find_element_by_css_selector("#searchBox > table > tbody > tr > td > a").click()
    except:
        time.sleep(5)
        driver.find_element_by_css_selector("#searchBox > table > tbody > tr > td > a").click()
    try:
        result = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#whois_result_data"))).text
    except:
        time.sleep(5)
        result = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,"#whois_result_data"))).text
    text_whois = open(r"./whois/{}.txt".format(name_site.get()),"w")
    text_whois.write(result)
    text_whois.close()
    progress.stop()
    popupmsg("اطلاعات دامنه ثبت شد")
    driver.close()

#desigen application
frame1 = LabelFrame(window,bd=0,text="",fg="spring green4",font="IRANSans 10",bg="lightyellow3")
frame1.pack(padx=(5,5),pady=(5,5),fill=BOTH)
frame2 = LabelFrame(window,bd=0,font="IRANSans 10",bg="lightyellow3")
frame2.pack(padx=(5,5),pady=(0,0),fill=BOTH, expand=1)

Label(window,bg="white",fg="gray25",text="_______________________________________________________________________________").pack(side=TOP,padx=5)
Label(window,text="hamids نوشته شده توسط",bg="white",fg="gray25", font="IRANSans 8").pack(side=RIGHT,padx=5,pady=(0,5))
Label(window,text="نسخه آلفا ورژن 0.0.1",bg="white",fg="gray25", font="IRANSans 8").pack(side=LEFT,padx=5,pady=(0,5))

Label(frame1,text=":سایت",fg="gray25",bg="lightyellow3",font='IRANSans 10').pack(side=RIGHT,anchor=W,padx=(0,5),pady=(5,5))
name_site = Entry(frame1,font="IRANSans 12",fg="gray25",bd=1)
name_site.pack(side=RIGHT,anchor=W,padx=(0,5),pady=(5,5),fill=BOTH,expand=1)

btn = Button(frame1,text="بررسی",command=t_check_link,width=8,fg="white",bg="gray30",font='IRANSans 10',bd=1)
btn.pack(side=LEFT,padx=(5,5),pady=(5,5),fill=BOTH)
btn_whois = Button(frame1,text="اطلاعات",command=t_whois,width=8,fg="white",bg="gray30",font='IRANSans 10',bd=1)
btn_whois.pack(side=LEFT,padx=(5,5),pady=(5,5),fill=BOTH)
progress = Progressbar(frame2, orient=VERTICAL,  mode='indeterminate')
progress.pack(side=LEFT,anchor=W,padx=(5,5),pady=(5,5),fill=BOTH)
get_name = Label(frame2,text=":نام سایت",fg="gray60",bg="lightyellow3",font='IRANSans 10')
get_name.pack(side=TOP,padx=(5,5),pady=(5,5),anchor=E)
get_ip = Label(frame2,text=":ای پی",fg="gray60",bg="lightyellow3",font='IRANSans 10')
get_ip.pack(side=TOP,padx=(5,5),pady=(5,5),anchor=E)
get_resident = Label(frame2,text=":محل سرور",fg="gray60",bg="lightyellow3",font='IRANSans 10')
get_resident.pack(side=TOP,padx=(5,5),pady=(5,5),anchor=E)
get_traffic = Label(frame2,text=":تعرفه ترافیک",fg="gray60",bg="lightyellow3",font='IRANSans 10')
get_traffic.pack(side=TOP,padx=(5,5),pady=(5,5),anchor=E)

#windows bind
window.bind('<Return>',bind_t_check_link)
window.bind('<Escape>',exit_event)

# finish run application
window.geometry("400x273")
window.protocol("WM_DELETE_WINDOW", exit_event(event = 1))
window.resizable(width=False, height=False)
try:
    window.wm_iconbitmap(r'./file/link_0Z3_icon.ico')
except:
    pass

if __name__ == "__main__":
    window.mainloop()