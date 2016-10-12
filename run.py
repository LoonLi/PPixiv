#coding=UTF-8
from spider import Spider

if __name__ == "__main__":
	s = Spider('艦これ')
	b = s.parse()
	for item in b:
		print item[0],"|||",item[1]
