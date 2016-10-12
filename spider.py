# -*- coding:UTF-8 -*-
import urllib2
import urllib
import time
from bs4 import BeautifulSoup


# for item in scores_board:
# 	print item[0],"|||||",item[1]


class Spider:
	def __init__(self,tag):
		self.tag = tag
		origin_url = 'http://www.pixiv.net/search.php?s_mode=s_tag&word='
		self.url = origin_url+urllib2.quote(tag,"!")


	def makeRequest(self,url):
		Cookie = 'p_ab_id=9; login_ever=yes; _ga=GA1.2.744023963.1467183331; stacc_mode=unify; bookmark_tag_type=count; bookmark_tag_order=desc; a_type=0; is_sensei_service_user=1; PHPSESSID=14695102_c391ab8482a4da2d71713de84b831752; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_t=1467183360295%3B1476281904178%3B1476281904178%3B18%3B40; ki_r=; __utma=235335808.744023963.1467183331.1476273994.1476281883.39; __utmb=235335808.3.10.1476281883; __utmc=235335808; __utmz=235335808.1476273994.38.8.utmcsr=t.co|utmccn=(referral)|utmcmd=referral|utmcct=/Il6fcnFBn9; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=14695102=1'
		req = urllib2.Request(url)
		#request.add_header('Accept-Language','zh;q=0.8')
		req.add_header('Cookie',Cookie)
		# request.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
		# request.add_header('Accept-Encoding','gzip, deflate, sdch')
		# request.add_header('Connection','keep-alive')
		# request.add_header('Cookie','p_ab_id=9; login_ever=yes; stacc_mode=unify; a_type=0; is_sensei_service_user=1; bookmark_tag_type=count; bookmark_tag_order=desc; _ga=GA1.2.744023963.1467183331; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; ki_t=1467183360295%3B1476055411949%3B1476097632750%3B15%3B28; ki_r=; PHPSESSID=14695102_c391ab8482a4da2d71713de84b831752; __utmt=1; __utma=235335808.744023963.1467183331.1476078305.1476096197.34; __utmb=235335808.73.9.1476097675591; __utmc=235335808; __utmz=235335808.1474680004.24.7.utmcsr=weibo.com|utmccn=(referral)|utmcmd=referral|utmcct=/u/2032349783/home; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=14695102=1')
		# request.add_header('Host','www.pixiv.net')
		# request.add_header('Upgrade-Insecure-Requests','1')
		# request.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36')
		return urllib2.urlopen(req)

	def parse(self):
		resp = self.makeRequest(self.url)

		item_urls = []
		scores_board = {}
		next_url = self.url
		page_count = 1

		while True:
			soup = BeautifulSoup(resp.read(),'html.parser')
			#get this page items
			items=soup.select('li[class="image-item"]')
			for item in items:
				item_url = "http://www.pixiv.net"+item.a['href']
				a_count = item.select('a[class="bookmark-count _ui-tooltip"]')
				if len(a_count)!=0:
					item_count = int(a_count[0].text)
				else:
					item_count = 0
				scores_board[item_url] = item_count
			print next_url,"has finished.This is no.",page_count,"."			
			if page_count>100:
				break
			page_count+=1
			if len(items)<10:
				break
			next_url = self.url+"&p="+str(page_count)
			resp = self.makeRequest(next_url)

		print "-------------------------------------------------"
		print "Staring scores collecting."
		scores_board = sorted(scores_board.iteritems(), key=lambda d:d[1], reverse = True)
		print ""
		print "Finished!!"
		print " "
		return scores_board