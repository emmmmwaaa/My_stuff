from selenium import webdriver
import time

options = webdriver.ChromeOptions()
options.add_argument('user-agent="Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"')
#模拟手机登陆，手机上的页面更好操作
driver = webdriver.Chrome(chrome_options = options)
driver.get('https://wenku.baidu.com/view/aa31a84bcf84b9d528ea7a2c.html')
page = driver.find_element_by_xpath("//div[@class='foldpagewg-text']")
#利用xpath搜索HTML元素，此处采用相对路径定位
page.click()
time.sleep(0.5)
#在click之后等待网页进行加载的时间
target = driver.find_element_by_xpath("//div[@class='btn-join-vip-super btn-nine-year-join stop-propagation']")
#这里有多种定位方法，by_id什么的也可以
driver.execute_script('arguments[0].scrollIntoView(false);', target)
#拖动到可见的元素去
#注意上述语法，以及elements和element的区别，driver.find_elements输出结果是一个list，无法用click()
#execute_script括号内是js脚本，我真滴佛
target = driver.find_element_by_xpath("//div[@class='pagerwg-button']")
target.click()
time.sleep(0.5)
target = driver.find_element_by_xpath("//div[@class='btn-join-vip-super btn-nine-year-join stop-propagation']")
driver.execute_script('arguments[0].scrollIntoView(false);', target)
target = driver.find_element_by_xpath("//div[@class='pagerwg-button']")
target.click()

from bs4 import BeautifulSoup
html = driver.page_source
bf1 = BeautifulSoup(html, 'lxml')
soup = bf1.find_all('p', class_='txt')
for s in soup:
    print(s.text.replace(' ', ''))
	
'''
操纵浏览器的方法：【即对webdriver对象的方法】
set_window_size()	设置浏览器的大小
back()	控制浏览器后退
forward()	控制浏览器前进
refresh()	刷新当前页面
clear()	清除文本
send_keys (value)	模拟按键输入
click()	单击元素
submit()	用于提交表单
get_attribute(name)	获取元素属性值
is_displayed()	设置该元素是否用户可见
size	返回元素的尺寸
text	获取元素的文本

鼠标事件：在Webdriver中，将这些关于鼠标操作的方法封装在 ActionChains 类提供。
ActionChains(driver)	构造ActionChains对象
context_click()	执行鼠标悬停操作
move_to_element(above)	右击
double_click()	双击
drag_and_drop()	拖动
move_to_element(above)	执行鼠标悬停操作
context_click()	用于模拟鼠标右键操作， 在调用时需要指定元素定位
perform()	执行所有 ActionChains 中存储的行为，可以理解成是对整个操作的提交动作

键盘事件:Selenium中的Key模块为我们提供了模拟键盘按键的方法，那就是send_keys()方法。它不仅可以模拟键盘输入，也可以模拟键盘的操作。
send_keys(Keys.BACK_SPACE)	删除键（BackSpace）
send_keys(Keys.SPACE)	空格键(Space)
send_keys(Keys.TAB)	制表键(Tab)
send_keys(Keys.ESCAPE)	回退键（Esc）
send_keys(Keys.ENTER)	回车键（Enter）
send_keys(Keys.CONTROL,‘a’)	全选（Ctrl+A）
send_keys(Keys.CONTROL,‘c’)	复制（Ctrl+C）
send_keys(Keys.CONTROL,‘x’)	剪切（Ctrl+X）
send_keys(Keys.CONTROL,‘v’)	粘贴（Ctrl+V）
send_keys(Keys.F1…Fn)	键盘 F1…Fn

设置元素等待：http://www.testclass.net/selenium_python/element-wait/
定位一组元素：上述有提及，不赘述
'''

'''
在Web应用中经常会遇到frame/iframe表单嵌套页面的应用，
WebDriver只能在一个页面上对元素识别与定位，
对于frame/iframe表单内嵌页面上的元素无法直接定位。
这时就需要通过switch_to.frame()方法将当前定位的主体
切换为frame/iframe表单的内嵌页面中。
switch_to.frame()	将当前定位的主体切换为frame/iframe表单的内嵌页面中
switch_to.default_content()	跳回最外层的页面
举例：

from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://www.126.com")

driver.switch_to.frame('x-URS-iframe')
driver.find_element_by_name("email").clear()
driver.find_element_by_name("email").send_keys("username")
driver.find_element_by_name("password").clear()
driver.find_element_by_name("password").send_keys("password")
driver.find_element_by_id("dologin").click()
driver.switch_to.default_content()

driver.quit()
'''

'''
多窗口切换：在页面操作过程中有时候点击某个链接会弹出新的窗口，
这时就需要主机切换到新打开的窗口上进行操作。
WebDriver提供了switch_to.window()方法，可以实现在不同的窗口之间切换。
current_window_handle	获得当前窗口句柄
window_handles	返回所有窗口的句柄到当前会话
switch_to.window()	用于切换到相应的窗口，与上一节的switch_to.frame()类似，前者用于不同窗口的切换，后者用于不同表单之间的切换。
from selenium import webdriver
import time
driver = webdriver.Chrome("F:\Chrome\ChromeDriver\chromedriver")
driver.implicitly_wait(10)
driver.get("http://www.baidu.com")

#1.获得百度搜索窗口句柄
sreach_windows = driver.current_window_handle

driver.find_element_by_link_text('登录').click()
driver.find_element_by_link_text("立即注册").click()

#1.获得当前所有打开的窗口的句柄
all_handles = driver.window_handles

#3.进入注册窗口
for handle in all_handles:
    if handle != sreach_windows:
        driver.switch_to.window(handle)
        print('跳转到注册窗口')
        driver.find_element_by_name("account").send_keys('123456789')
        driver.find_element_by_name('password').send_keys('123456789')
        time.sleep(2)
    
driver.quit()
'''

#警告框处理，这个我懒得写了，自己去找资料8

#下拉框选择操作：导入选择下拉框Select类，使用该类处理下拉框操作。
from selenium.webdriver.support.select import Select
#select_by_value(“选择值”)	相当于我们使用鼠标选择下拉框的值
#可以通过send_keys()的方法实现文件上传

'''
cookie操作:有时候我们需要验证浏览器中cookie是否正确，因为基于真实cookie的测试是无法通过白盒和集成测试进行的。
WebDriver提供了操作Cookie的相关方法，可以读取、添加和删除cookie信息。
get_cookies()	获得所有cookie信息
get_cookie(name)	返回字典的key为“name”的cookie信息
add_cookie(cookie_dict)	添加cookie。“cookie_dict”指字典对象，必须有name 和value 值
delete_cookie(name,optionsString)	删除cookie信息。“name”是要删除的cookie的名称，“optionsString”是该cookie的选项，目前支持的选项包括“路径”，“域”
delete_all_cookies()	删除所有cookie信息
from selenium import webdriver
import time
browser = webdriver.Chrome("F:\Chrome\ChromeDriver\chromedriver")
browser.get("http://www.youdao.com")

#1.打印cookie信息
print('=====================================')
print("打印cookie信息为：")
print(browser.get_cookies)

#2.添加cookie信息
dict={'name':"name",'value':'Kaina'}
browser.add_cookie(dict)

print('=====================================')
print('添加cookie信息为：')
#3.遍历打印cookie信息
for cookie in browser.get_cookies():
    print('%s----%s\n' %(cookie['name'],cookie['value']))
    
#4.删除一个cookie
browser.delete_cookie('name')
print('=====================================')
print('删除一个cookie')
for cookie in browser.get_cookies():
    print('%s----%s\n' %(cookie['name'],cookie['value']))

print('=====================================')
print('删除所有cookie后：')
#5.删除所有cookie,无需传递参数
browser.delete_all_cookies()
for cookie in browser.get_cookies():
    print('%s----%s\n' %(cookie['name'],cookie['value']))

time.sleep(3)
browser.close()
'''
#来源：https://blog.csdn.net/weixin_36279318/article/details/79475388