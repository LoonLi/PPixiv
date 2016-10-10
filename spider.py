# -*- coding: utf-8 -*-
import urllib2
import urllib
import time
from bs4 import BeautifulSoup

def makeRequest(url):
	request = urllib2.Request(url)
	request.add_header('Accept-Language','zh;q=0.8')
	# request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	# request.add_header('Accept-Encoding','gzip, deflate, sdch')
	# request.add_header('Connection','keep-alive')
	# request.add_header('Cookie','p_ab_id=9; login_ever=yes; stacc_mode=unify; a_type=0; is_sensei_service_user=1; bookmark_tag_type=count; bookmark_tag_order=desc; _ga=GA1.2.744023963.1467183331; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_t=1467183360295%3B1476055411949%3B1476097632750%3B15%3B28; ki_r=; PHPSESSID=14695102_c391ab8482a4da2d71713de84b831752; __utmt=1; __utma=235335808.744023963.1467183331.1476078305.1476096197.34; __utmb=235335808.73.9.1476097675591; __utmc=235335808; __utmz=235335808.1474680004.24.7.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/u/2032349783/home; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=14695102=1')
	# request.add_header('Host','www.pixiv.net')
	# request.add_header('Upgrade-Insecure-Requests','1')
	request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
	return urllib2.urlopen(request)


#construct a url
tag = "ナネットさん"
origin_url = 'http://www.pixiv.net/search.php?s_mode=s_tag&word='
url = origin_url+urllib2.quote(tag,"!")
#print tag
#print url
#print "http://www.pixiv.net/search.php?s_mode=s_tag&word=%E3%81%BE%E3%81%A3%E3%81%9F%E3%81%8F%E3%80%81%E9%A7%86%E9%80%90%E8%89%A6%E3%81%AF%E6%9C%80%E9%AB%98%E3%81%A0%E3%81%9C!!"
resp = makeRequest(url)
#print urllib2.unquote("%E3%81%BE%E3%81%A3%E3%81%9F%E3%81%8F%E3%80%81%E9%A7%86%E9%80%90%E8%89%A6%E3%81%AF%E6%9C%80%E9%AB%98%E3%81%A0%E3%81%9C!!")
#print resp.url

item_urls = []
next_url = url
page_count = 1

while True:
	soup = BeautifulSoup(resp.read(),'html.parser')
	#get this page items
	items=soup.select('li[class="image-item"]')
	for item in items:
		item_url = "http://www.pixiv.net"+item.a['href']
		item_urls.append(item_url)
	print next_url,"has finished.This is no.",page_count,"."
	#get next page url
	# a=soup.select('a[r/el="next"]')
	
	#limit the pages
	# if page_count%5==0:
	# 	print "Let me have a rest..."
	# 	time.sleep(5)

	if page_count>100:
		break
	page_count+=1

	# if len(a)!=0:
	# 	a=a[0]
	# 	href=a['href']
	# 	next_url="http://www.pixiv.net/search.php"+href
	# 	resp=makeRequest(next_url)
	# else:
	# 	break
	if len(items)<10:
		break
	#print len(items)
	next_url = url+"&p="+str(page_count)
	resp = makeRequest(next_url)



print "Finished!!"
# print "we get these urls:"
# for x in item_urls:
# 	print x
# print len(item_urls)
print "-------------------------------------------------"
print "Staring scores collecting."

scores_board = {}

for item_url in item_urls:
	resp = makeRequest(item_url)
	soup = BeautifulSoup(resp.read(),'html.parser')
	span = soup.select('span[class="views"]')
	scores = int(span[1].string)
	scores_board[item_url] = scores
	print item_url,"has [[[",scores,"]]] scores."

scores_board = sorted(scores_board.iteritems(), key=lambda d:d[1], reverse = True)

print ""
print "Finished!!"
print " "

for item in scores_board:
	print item[0],"|||||",item[1]