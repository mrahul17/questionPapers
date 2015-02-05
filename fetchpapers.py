#will be using BeautifulSoup

import os
from bs4 import BeautifulSoup as soup
import urllib2
import re
proxy_support = urllib2.ProxyHandler({})
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

owd = os.getcwd()  #saved the original woring directory 
os.chdir("/home/rahul/Rahul/X/webscraping/qPapers") #I'll download the papers here
homeUrl = "http://10.17.32.9/peqp"
homeData = urllib2.urlopen(homeUrl)
sip = soup(homeData)

#now fetching links for all the years

allYears = sip.find_all("a")
allYears = allYears[1:] #the firs link is the link to parent directory

#allYears has the <a> tags stored. We want only the links

#I love list comprehensions!!
allYears = [year.get("href") for year in allYears]

#now allyears hrefas the partial urls, we'll construct the entire url
allYears = ["http://10.17.32.9"+url for url in allYears]

#print allYears
#the loop for the years will begin now
#till 2008 year/department then we get pdf
#after this year/phase/department/courses
for year in allYears:
	# i need to get the directory name from the url, regexp to the rescue
	yearPattern = re.compile(r"/peqp/(\d{4})/")
	yearString = yearPattern.search(year).groups()[0]
	

	print yearString
	if int(yearString) <= 2007: 
		mainfolder = os.getcwd()
		if not os.path.exists(yearString):
			os.makedirs(yearString)
		os.chdir(os.path.realpath(yearString))

		yearData = urllib2.urlopen(year)
		sipYear = soup(yearData)

		allDepartments = sipYear.find_all("a")[1:]
		allDepartments = [department.get("href") for department in allDepartments]
		allDepartments = ["http://10.17.32.9"+url for url in allDepartments]
		#print allDepartments
		

		for department in allDepartments:
			departmentPattern = re.compile(r"/peqp/"+yearString+"/"+r"(\w*\s*\w*\s*\w*\s*)/")
			departmentString = departmentPattern.search(urllib2.unquote(department)).groups()[0]
			#print department
			departmentData = urllib2.urlopen(department)
			if not os.path.exists(departmentString):
			 	os.makedirs(departmentString)
			os.chdir(departmentString)
			sipDepartment = soup(departmentData)
			allCourses = sipDepartment.find_all("a")[1:]
			allCourses = [course.get("href") for course in allCourses]
			allCourses = ["http://10.17.32.9"+url for url in allCourses]

			#print allCourses
			for course in allCourses:
				coursePattern = re.compile(r"/peqp/"+yearString+"/"+departmentString+"/"+r"(\w*\s*\w*\s*\w*\s*)")
				courseString = coursePattern.search(urllib2.unquote(course)).groups()[0]
				#print courseString
				pdf = urllib2.urlopen(course).read()
			 	filename = courseString+".pdf"
			 	with open(filename,'wb') as f:
					f.write(pdf)
			os.chdir('..')#one department over, now go back one directory		
		os.chdir('..')#one year over,again go back one directory
	

		


