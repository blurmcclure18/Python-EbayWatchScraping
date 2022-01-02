import undetected_chromedriver as uc

driver = uc.Chrome()
test_sold_url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1312.R1.TR11.TRC2.A0.H0.XIp.TRS1&_nkw=(291)+elgin&LH_Complete=1&LH_Sold=1&_oac=1"

driver.get(test_sold_url)
