from selenium import webdriver as wd

fp = wd.FirefoxProfile('/home/alec/.mozilla/firefox/87syjf8o.default-release')
wd = wd.Firefox(fp)

wd.implicitly_wait(10)

url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw=grade+303+elgin&LH_Complete=1&LH_Sold=1"

wd.get(url)
pagesource = wd.page_source
