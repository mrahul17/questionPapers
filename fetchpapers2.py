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
		pass
	elif int(yearString)>=2011:
		if not os.path.exists(yearString):
			os.makedirs(yearString)
		os.chdir(yearString)
		yearData = urllib2.urlopen(year)
		sipYear = soup(yearData)

		allPhases = sipYear.find_all("a")[1:]
		allPhases = [phase.get("href") for phase in allPhases]
		allPhases = ["http://10.17.32.9"+url for url in allPhases]

		#print allPhases
		for phase in allPhases:
			phasePattern = re.compile(r"/peqp/"+yearString+"/"+r"([a-zA-Z0-9& _/,()]*)/")
			phaseString = phasePattern.search(urllib2.unquote(phase)).groups()[0]
			#print phaseString
			if not os.path.exists(phaseString):
				os.makedirs(phaseString)
			os.chdir(phaseString)

			phaseData = urllib2.urlopen(phase)
			sipPhase = soup(phaseData)
			allDepartments = sipPhase.find_all("a")[1:]
			allDepartments = [department.get("href") for department in allDepartments]
			allDepartments = ["http://10.17.32.9"+url for url in allDepartments]

			for department in allDepartments:
				departmentPattern = re.compile(r"/peqp/"+yearString+"/"+phaseString+"/"+r"([a-zA-Z0-9& _,()]*)")
				departmentString = departmentPattern.search(urllib2.unquote(department)).groups()[0]
				print department
				departmentData = urllib2.urlopen(department)
				if not os.path.exists(departmentString):
				 	os.makedirs(departmentString)
				os.chdir(departmentString)
				sipDepartment = soup(departmentData)
				allCourses = sipDepartment.find_all("a")[1:]
				allCourses = [course.get("href") for course in allCourses]
				
				count = 0 
				for course in allCourses:
					try:
						course = "http://10.17.32.9" + course
						#print course
						count+=1
					except TypeError:
						with open("unableToDownload.txt",'w') as f:
							f.write(departmentString+"  "+str(count))
							count+=1
							allCourses.remove(course)
			

				#print allCourses

				for course in allCourses:

					try:
						coursePattern = re.compile(r"/peqp/"+yearString+"/"+phaseString+"/"+departmentString+"/"+r"([a-zA-Z0-9& _,\(\)]*)")
						courseString = coursePattern.search(urllib2.unquote(course)).groups()[0]
					except AttributeError:
						print "OOps! something to work upon"
					#print courseString
					try:
						pdf = urllib2.urlopen("http://10.17.32.9"+course).read()
				 		filename = courseString+".pdf"
				 		with open(filename,'wb') as f:
					 		f.write(pdf)
					except UnicodeEncodeError:
						with open("unableToDownload.txt",'w') as f:
							f.write("yet another")
					except TypeError:
						"Oops!!"

				os.chdir('..')

			os.chdir('..')

		os.chdir('..')
		


