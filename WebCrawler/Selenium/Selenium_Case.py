from selenium import webdriver
from selenium.common.exceptions import TimeoutException



#-----------------------------------------------元素查找相关
    #两种find  :  find_element  find_elements
    #多种选择渠道 ： by_id | by_class_name | by_tag_name(比如Span) | by_name
    inputElement = driver.find_element_by_name("q")

    #by_link_text("cheese")  根据文本值找href的内容  | by_partial_link_text("cheese") 根据部份文本值找href的内容
    #他也支持css selectors  by_css_selector("#food span.dairy.aged")
    
    # by_xpath("//input")
    # 默认使用浏览器自带的XPath，假如浏览器没有就用Selenium带的。标准可能不同，返回的结果会不同（比如是否敏感大小写）。

    #一次放多个条件
    from selenium.webdriver.common.by import By
    element = driver.find_element(by=By.ID, value="AA")
    element = driver.find_elements(By.CLASS_NAME, "cheese")
    element = driver.find_element(By.TAG_NAME, "button")  #就是HTML的标签
    #多种选择 ： By.NAME  
    # By.LINK_TEXT（是填文本值找href）  By.PARTIAL_LINK_TEXT（同前，但是只需要部分文本值）
    # By.CSS_SELECTOR  By.XPATH

#-----------------------------------------------元素操作
    #一个元素包含的文本值 
    element.text
    #拿一个属性
    element.get_attribute("value")

    #点击按钮 | 多选
    select = driver.find_element_by_tag_name("select")
    allOptions = select.find_elements_by_tag_name("option")
    for option in allOptions:
        print ("Value is: " + option.get_attribute("value"))
        option.click()
    #多选的别的方式
    from selenium.webdriver.support.ui import Select
    select = Select(driver.find_element_by_tag_name("select"))
    select.deselect_all()
    select.select_by_visible_text("Edam")

    #element.submit()  不确定用法。好像是提交表单的。
    #inputElement.send_keys("cheese!")  发送要填的内容？



#-------------浏览器

#-----------------------------执行一段JS   
    labels = driver.find_elements_by_tag_name("label")
    inputs = driver.execute_script(
        "var labels = arguments[0], inputs = []; for (var i=0; i < labels.length; i++){" +
        "inputs.push(document.getElementById(labels[i].getAttribute('for'))); } return inputs;", labels)
 #-----------------------------窗口操作

    driver = webdriver.Chrome('E:\Python\chromedriver\chromedriver')
    driver.get("http://www.google.com")
    print(driver.title)  #标题
    driver.quit()
    
    #窗口切换
    driver.switch_to.window("windowName")
    #名字来源 <a href="somewhere.html" target="windowName">Click here to open a new window</a> 中的windowName

    for handle in driver.window_handles:  #每个打开的窗口里互切
        driver.switch_to.window(handle)

    #同样的 标签切换
    driver.switch_to.frame("frameName")

    #处理各种弹出的各种对话框，提示
        alert = driver.switch_to.alert
        # usage: alert.dismiss(), etc.
    #前进后退
    driver.forward()
    driver.back()

    #------------------------------------------cookie
        driver.add_cookie({'name':'key', 'value':'value'})
        #一次加入一个字典，一个字典代表一项Cookie
        # 可选项：optional keys - “path”, “domain”, “secure”, “expiry”

        for cookie in driver.get_cookies():
            print "%s -> %s" % (cookie['name'], cookie['value'])

        #删Cookies
        driver.delete_cookie("CookieName")
        driver.delete_all_cookies()

#拖放操作
from selenium.webdriver.common.action_chains import ActionChains
element = driver.find_element_by_name("source")
target =  driver.find_element_by_name("target")
ActionChains(driver).drag_and_drop(element, target).perform()

#显示等待
        WebDriverWait(driver, 10).until(EC.title_contains("cheese!"))
        print (driver.title) 

ff.get("http://somedomain/url_that_delays_loading")
try:
    element = WebDriverWait(ff, 10).until(EC.presence_of_element_located((By.ID, "myDynamicElement")))
finally:
    ff.quit()
#10秒后报错TimeoutException 否则就是10秒内找到了目标点。每0.5秒检查一次

#可以点了吗？
from selenium.webdriver.support import expected_conditions as EC
wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.ID,'someid')))

#隐式等待
ff = webdriver.Firefox()
ff.implicitly_wait(10) # seconds
ff.get("http://somedomain/url_that_delays_loading") #和显式一样，10秒没拿到，就报错。
myDynamicElement = ff.find_element_by_id("myDynamicElement")
#效果和显示一样。持续整个webdriver的生命周期。


#---------------------------------------------Chrome Driver
chrome://version/ 
可以看到Chrome版本和路径。

#把已存在的Driver实例的options，增加到新实例来
capabilities = DesiredCapabilities.chrome();
capabilities.setCapability(ChromeOptions.CAPABILITY, options);  #
ChromeDriver driver = new ChromeDriver(capabilities);

...弹出窗口？
"profile.default_content_settings.popups", 0

#代理  Proxy
#loggingPrefs Log的设置
#配置文件
    .addArguments("user-data-dir=/path/to/your/custom/profile");
#最大化      "start-maximized"  
disable-plugins 禁用插件

#-----------------------------ChromeOptions
默认的ChromeDriver使用时会创建一个临时的配置文件

#-----args     
http://peter.sh/experiments/chromium-command-line-switches/  一堆内容
这个网页找到的参数都可以用addArguments来填
    chromedriver --help

#定位一个Chrome可执行路径，不在默认目录的那种
    .setBinary("/path/to/other/chrome/binary");  

#加扩展
    .addExtensions(new File("/path/to/extension.crx"));

#localState 本地设置  Local State是一个文件，在用户文件夹下面，可以打开看看结构
#excludeSwitches  一些设置，开浏览器的时候使用。

#是否分离Driver和Chrome。影响Chrome的清除临时信息的时间。
    detach


--user-agent

opts.add_argument("user-agent="'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36')