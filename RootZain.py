import pyttsx3 
import datetime
import wikipedia
import webbrowser
import os
from os import system
import subprocess
import mysql.connector
import speech_recognition as sr
import sqlite3
import requests, json
import wolframalpha
import functools
import string
import random
import smtplib 
import bday
from newsapi.newsapi_client import NewsApiClient
from twilio.rest import Client 
appid="2GVJK5-X9GEAPP933"
client = wolframalpha.Client(appid)
#SQLite Connection
litecon = sqlite3.connect("myAsstDb.db")
sqlitecurs = litecon.cursor()

#Create Table #
sqlitecurs.execute("""CREATE TABLE IF NOT EXISTS mydb(
			  id integer PRIMARY KEY,
	          name text,
	          iplteam text,
	          voice integer
	          age integer)""")
#DB Connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=""
)
r = sqlitecurs.execute("SELECT voice FROM mydb WHERE id=1")
voice = r.fetchone()
voice = functools.reduce(lambda sub, ele: sub * 10 + ele, voice)
v=(int(voice))
mycursor = mydb.cursor()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[v].id)
engine.setProperty('rate',170)		


def speak(audio):
	engine.say(audio)
	engine.runAndWait()
	pass

def wishme():
	hour = int(datetime.datetime.now().hour)
	if(hour>=0 and hour<12):
		speak("Good Morning Sir")

	elif(hour>=12 and hour<18):
		print("Good Afternoon Sir")
		speak("Good Afternoon Sir")
	elif(hour>=18 and hour<20):
		print("Good Evening Sir")
		speak("Good Evening Sir")	               
	else:
		print("Good Night Sir")
		speak("Good Night Sir")


def takeCommand():
	#it takes audio input from mic and outputs the string
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.adjust_for_ambient_noise(source)
		audio = r.listen(source)
	try:
		print("Recognising Audio...")
		query = r.recognize_google(audio)
		print('Did you said ?...',format(query))

	except Exception as e:
		print("Please say that again")
		return "None"
	return query

def newsreport():
	main_url = " https://newsapi.org/v2/top-headlines?source=ndtv&q=ipl&country=in&apiKey=b186ef2f62a843b7b5de158944aef758"

	# fetching data in json format 
	open_bbc_page = requests.get(main_url).json() 

	# getting all articles in a string article 
	article = open_bbc_page["articles"] 

	# empty list which will  
	# contain all trending news 
	results = [] 
	  
	for ar in article: 
	    results.append(ar["title"]) 
	    
	for i in range(len(results)):
		# printing all trending news 
	    print(i + 1, results[i])
	    speak(i + 1, results[i])
	return results
def changeVoice(v):
	v=str(v)
	sql = "UPDATE mydb SET voice="+v+" WHERE id ='1'"
	sqlitecurs.execute(sql)
	litecon.commit()

def weathereport(CITY):
	URL = "http://api.openweathermap.org/data/2.5/weather?q="+CITY+"&appid=542ffd081e67f4512b705f89d2a611b2"
	# HTTP request
	response = requests.get(URL)
	# checking the status code of the request
	if response.status_code == 200:
	   # getting data in the json format
	   data = response.json()
	   # getting the main dict block
	   main = data['main']
	   # getting temperature
	   temperature = main['temp']
	   temperature = round(temperature-273)
	   # getting the humidity
	   humidity = main['humidity']
	   # getting the pressure
	   pressure = main['pressure']
	   # weather report
	   report = data['weather']
	   print(f"In {CITY},")
	   print(f"The Temperature is {temperature} degree celcius")
	   print(f"Humidity is {humidity}")
	   print(f"Today, you can expect{report[0]['description']} in {CITY}")
	   speak(f"In {CITY},")
	   speak(f"The Temperature is {temperature} degree celcius")
	   speak(f"Humidity is {humidity}")
	   speak(f"Today, you can expect {report[0]['description']} in {CITY}")
	else:
	   # showing the error message
	   print("Error in the HTTP request")

#####################################   M A I N    P R O G R A M   ##########################################
if __name__ == '__main__':
	wishme()
	print("Your RootZain is here. How may I help you?")
	speak("Your RootZain is here. How may I help you?")
	while True:
		query = takeCommand().lower()
		if(len(query)==0):
			print('Say Something Sir')
		elif 'send whatsapp message' in query or 'send a whatsapp message' in query:
			account_sid = 'AC487e941ef9f0c6366199fc403212d824' 
			auth_token = '19b8b56b54c45166c1be8aadfb66d4a2' 
			client = Client(account_sid, auth_token)
			speak('to Whom shall I send Sir ?')
			to = takeCommand().lower()
			if 'mum' in to:
				to = '8073532016'
			elif 'dad' in to:
				to = '8722430959'
			else:
				speak('I didnt know the person, can you input the number?') 
				to = input()
			to='whatsapp:+91'+to
			speak('What is the message to be sent Sir?')
			body = takeCommand()
			speak(f'{body} shall I send?')
			ans = takeCommand()
			if 'no' in ans or "don't" in ans:
				speak('Please Type the message Sir')
				body = input()
			speak('Sending message in whatsapp...')
			message = client.messages.create( 
			                              from_='whatsapp:+14155238886',  
			                              body=body,      
			                              to=to 
			                          )
			speak('Sent Message')
		elif 'wikipedia' in query:
			print('What should I search in WikiPedia?')
			speak('What should I search in WikiPedia?')
			ans = takeCommand()
			try:
				results = wikipedia.summary(ans,sentences = 2)
				speak("According to WikiPedia...")
				print(results)
				speak(results)
			except Exception as e:
				try:
					res = client.query(ans)
					speak('According to wolframalpha,')
					print((next(res.results).text))
					speak(next(res.results).text)
				except Exception as e:
					speak('Sorry Sir there are no results found for')
					speak(ans)
   # Change my Name ----------####################################################################
		elif 'change my name' in query:
			speak('Ok Sir what should I call you?')
			myname = takeCommand()
			myname = myname.replace(" ","")
			speak(myname)
			speak('Is this correct Sir?')
			ans = takeCommand()
			if 'no' in ans:
				print('Please type your name Sir!')
				speak('Please type your name Sir!')
				myname = input()
				myname = myname.replace(" ","")
			print(myname)
			print('I hope its fine Sir')
			speak('I hope its fine Sir')
			try:
				sql = "UPDATE mydb SET name = '"+myname+"'"+" WHERE id=1"
				sqlitecurs.execute(sql)
				litecon.commit()
				print('Changed Successfully! ')
				speak('Ok Sir I will call you '+myname)
			except Exception as e:
				speak('Sorry Sir there is some error')
				speak(e)
	#Change my age -----------------------#######################################

		elif 'change my age' in query:
			speak('Ok Sir how old are you?')
			myage = takeCommand()
			myage = myage.replace(" ","")
			speak(myage)
			speak('Is this correct Sir?')
			ans = takeCommand()
			if 'no' in ans:
				print('Please type your Age Sir!')
				speak('Please type your Age Sir!')
				myage = int(input())
			print(myage)
			print('I hope its fine Sir')
			speak('I hope its fine Sir')
			try:
				sql = "UPDATE mydb SET age = '"+myage+"'"+" WHERE id=1"
				sqlitecurs.execute(sql)
				litecon.commit()
				print('Changed Successfully! ')
				speak('I have updated your age,Sir')
			except Exception as e:
				speak('Sorry Sir there is some error')
				print(e)
				speak(e)
				#-----------------------------------------------------------
	#What is my age  ###############################################################
		elif 'what is my age' in query or 'old iam' in query or 'how old' in query or 'my age' in query:
			r = sqlitecurs.execute("SELECT age FROM mydb WHERE id=1")
			age = r.fetchone()
			if ',' in age:
				age = age.replace(",","")
			print(f"Sir you are {age} year old")
			speak(f"Sir you are {age} year old")
		elif 'call me' in query:
			query = query.replace("call me","")
			sql = "UPDATE mydb SET name = '"+query+"'"+" WHERE id=1"
			sqlitecurs.execute(sql)
			litecon.commit()
			#speak('Sir,Your Name is,')
			#speak(r.fetchone())
			speak(f"Sure Sir I will call you {query}")

	#What is my name   ###################################################################
		elif 'what is my name' in query or 'my name' in query:
			r = sqlitecurs.execute("SELECT name FROM mydb WHERE id =1")
			speak(f"Sir your name is {r.fetchone()}")
			speak('You are LEGEND')

        #Who is Search  ######################################################################################
		elif 'who' in query or 'what' in query or 'distance between' in query or 'when is' in query or 'where is' in query or 'how' in query or 'which' in query:
			try:
				res = client.query(query)
				print((next(res.results).text))
				speak(next(res.results).text)
			except Exception as e:
				try:
					if 'who is ' in query:
						query = query.replace("who is ","")
					elif 'what is ' in query:
						query = query.replace("what is ","")
					elif 'when is ' in query:
						query = query.replace("when is ","")
					elif 'where is ' in query:
						query = query.replace("where is ","")
					elif 'which is ' in query:
						query = query.replace("which is ","")	
					results = wikipedia.summary(query,sentences = 2)
					speak("According to WikiPedia...")
					print(results)
					speak(results)
				except Exception as e:
					speak(f'Sorry Sir there are no results found in web for {query}')
 # YouTube Search ######################################################################################
		elif 'youtube' in query:
			print('What should I search in youtube?')
			speak('What should I search in youtube?')
			ans = takeCommand()
			qry = "https://www.youtube.com/results?search_query="+ans
			speak('Opening in youtube')
			webbrowser.open(qry)
		elif 'search' in query or 'search for' in query:
			query = query.replace("search for","")
			speak('Searching...')
			qry = "https://www.google.com/search?q="+query
			webbrowser.open(qry)
  #Google Search ########################################################################################
  
		elif 'play music' in query or 'play songs' in query or 'songs' in query or 'music' in query:
			dir = 'E:\\SONGS\\'
			songs = os.listdir(dir)
			x = random.choice(songs)
			print('Playing from local songs')
			speak('Sure Sir , I will play for you.')
			try:
				os.startfile(dir+x)
			except Exception as e:
				print(e)
				speak('Sorry Sir,there was some error Playing songs')

	#introduce Assistant   ################################################################################
		elif 'who are you' in query or 'what is your name' in query:
		    speak('Iam your Assistant Sir! My name is RootZain!')


	# Exit   #######################################################################################
		elif 'exit' in query or 'bye' in query or 'turn off' in query or 'quit' in query:
			speak('Do you really want to exit ,Sir?')
			ans = takeCommand()
			if 'no' in ans or 'dont' in ans or "don't" in ans:
				speak('Okay what can I do for you Sir?')
			elif 'yes' in query or 'ya' in query or 'yeah' in query or 'exit' in query:
				speak('Exiting Sir..ByeBye')
				exit()
			else:
				hour = int(datetime.datetime.now().hour)
				if(hour>=20 and hour<=24):
					speak('Exiting Sir..ByeBye, Good Night, Take Care')
					exit()
				else:
					speak('Exiting Sir..ByeBye, Take Care')
					exit()
  # Create Database   ##########################################################################################
		elif 'create a database' in query or 'create database' in query:
			speak('Sure! Sir, I will create for you')
			speak('What is name of Database ?')
			dbname = takeCommand()
			dbname = dbname.replace(" ","")
			speak(dbname)
			speak('Is this correct Sir?')
			ans = takeCommand()
			if 'no' in ans:
				print('Please type the DATABASE name Sir!')
				speak('Please type the DATABASE name Sir!')
				dbname = input()
			print(dbname)
			print('I hope its fine Sir')
			speak('I hope its fine Sir')
			dbqry = "CREATE DATABASE "+dbname
			mycursor.execute(dbqry)
			print('Sir,I have created database successfully!')
			speak('Sir,I have created database successfully!')

  # Dropping a Database   #################################################################################
		elif 'drop database' in query or 'drop a database' in query:
			speak('Ok Sir, I will drop.')
			speak('What is name of Database Sir?')
			dbname = takeCommand()
			dbname = dbname.replace(" ","")
			speak(dbname)
			speak('Is this correct Sir?')
			ans = takeCommand()
			if 'no' in ans:
				print('Please type the DATABASE name Sir!')
				speak('Please type the DATABASE name Sir!')
				dbname = input()
			print(dbname)
			print('I hope its fine Sir')
			try:
				print("Dropping...")
				speak('Dropping')
				dbqry =  "DROP DATABASE "+dbname
				mycursor.execute(dbqry)
				speak('I found that !')
				print('Sir,I have dropped database successfully!')
				speak('Sir,I have dropped database successfully!')
				print('Did you said ?...',format(dbqry))
			except Exception as e:
				speak('Sorry Sir database not found !')
# Whatsapp Web

		elif 'whatsapp' in query:
			speak('Opening Whatsapp Web')
			webbrowser.open('https://web.Whatsapp.com')
# Thanking Assistant  ###########################################################################
		elif 'thank' in query in query or 'good job' in query or 'smart' in query or 'well done' in query or 'good' in query or 'amazing' in query or 'intelligent' in query:
			print('Haha , all credit goes to your Coding skills ,Sir . Iam proud of you')
			speak('Haha , all credit goes to your Coding skills ,Sir . Iam proud of you.')
# Browsing URL ########################################################################################
		elif 'browse' in query:
			query = query.replace("browse ","")
			url = "https://"+query
			speak(f"Browsing {query}")
			webbrowser.open(url)
#######################################################################################################################
# Creating Tables in Db
		elif 'create table' in query or 'create a table' in query:
			print('Sure Sir I will create for you, could you provide Database name Sir?')
			speak('Sure Sir I will create for you, could you provide Database name Sir?')
			dbname = takeCommand().lower()
			dbname = dbname.replace(" ","")
			speak(dbname)
			speak('Is this correct Sir?')
			ans = takeCommand().lower()
			if 'no' in ans:
				print('Please type the DATABASE name Sir!')
				speak('Please type the DATABASE name Sir!')
				dbname = input()
			print(dbname)
			print('I hope its fine Sir')
			speak('I hope its fine Sir')
			speak(dbname)
			qry = "CREATE DATABASE IF NOT EXISTS "+dbname
			mycursor.execute(qry) 
			try:
				print("Redirecting to GUI Page of Localhost")
				speak('Redirecting to GUI Page of Localhost')
				dbqry =  "http://localhost/phpmyadmin/db_structure.php?db="+dbname
				webbrowser.open(dbqry)
				speak('Sir,I have opened the GUI successfully!')

			except Exception as e:
				print('Iam sorry Sir I could not find your database can you type it please')
				speak('Iam sorry Sir I could not find your database can you type it please')
				dbname = input()
				try:
					print('I found that!.Finally')
					speak("I found that!.Finally")
					dbqry =  "DROP DATABASE "+dbname
					mycursor.execute(dbqry)
					speak('Sir,I have dropped database successfully!')
				except Exception as e:
					speak("Sorry Sir the Database not found")
# ZAIN LOVES YOU #####################################################################
		elif 'love you' in query:
			r =sqlitecurs.execute("SELECT name FROM mydb")
			name = r.fetchone()
			speak(f"I LOVE YOU TOOO{name}")
			print(f'I LOVE YOU TOOO{name}')
			print("WILL YOU MARRY ME? I can't be single anymore now")
			speak("WILL YOU MARRY ME? I can't be single anymore now")
			ans = takeCommand()
			if 'yes' in ans:
				speak("please marry me as soon as possible!")
			elif 'no' in ans or 'sorry' in ans or 'possible' in query:
				print(f"Ohhh No, I WILL REALLY MISS YOU {name}")
				speak(f"Ohhh No, I WILL REALLY MISS YOU {name}")
# RCB EE SALA CUP NAMDE ####################################################################
		elif 'rcb' in query:
			speak("EE SALA CUP Nam dee")
# Multiplication Tables #####################################################################
		elif 'multiplication tables' in query:
			speak('Sure Sir, which one? say number.')
			try:
				ans = takeCommand()
				ans = int(ans)
				if 'xx' in ans:
					ans = 20
				speak(ans)
			except Exception as e:
				speak("I didn't got that, Please type the number Sir!")
				print('Please type the number Sir!')
				ans = takeCommand()
			try:
				i=1
				while i<11:
					print(f"{ans} * {i} = {ans*i}")
					if i == 6:
						speak(f"{ans} {i}  are {ans*i}")
						i=7
						print(f"{ans} * {i} = {ans*i}")
					speak(f"{ans} {i}s  are {ans*i}")
					i+=1
			except Exception as e:
				speak('Sorry Sir there is an Error.')

################### Change Assistant Voice ############################################3
		elif 'change your voice' in query:
			speak("Sure Sir I will.")
			print("Sure Sir I will.")
			if 'boy' in query:
				engine.setProperty('voice',voices[0].id)
				v=1
				changeVoice(v)
				speak('Changed to Boys Voice')
			elif 'girl' in query:
				engine.setProperty('voice',voices[1].id)
				v=0
				changeVoice(v)
				speak('Changed to Girls Voice')
			else:
				speak('Girls voice or boys voice?')
				ans = takeCommand()
				if 'girl' in ans:
					engine.setProperty('voice',voices[1].id)
					v=0
					changeVoice(v)
					speak('Changed to Girls Voice')
				elif 'boy' in ans:
					engine.setProperty('voice',voices[0].id)
					v=1
					changeVoice(v)
					speak("Changed to Boy's Voice")
				else:
					speak(f'Sorry Sir there is no voice called {ans}')

#########S U B L I M E EDITOR OPEN ##################################################################
		elif 'sublime' in query:
			try:
				os.startfile("D:\Sublime Text 3\sublime_text.exe")
				speak('Here it is, SUBLIME')
			except Exception as e:
				print('The File is not present in system !')
				speak('The File is not present in system !')
#########C M D OPEN ####################################################################################
		elif 'cmd' in query:
			try:
				os.startfile("C:\\WINDOWS\\system32\\cmd.exe")
				speak("Here's your CMD Sir")
			except Exception as e:
				speak("I'm Sorry CMD cant be opened Sir")
##########V S CODE ##########################################################################################
		elif 'code' in query:
			try:
				os.startfile("C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe")
				speak("Here's your VS Code Sir")
			except Exception as e:
				speak("Sorry Sir there was some error opening VS CODE")
		elif 'install' in query:
				print(query)
				speak(query)
				speak('is this correct Sir?')
				ans = takeCommand()
				if 'no' in ans or 'not' in query:
					speak('Please type the Command Sir.')
					query = input()
				try:
					speak('Executing Command in Terminal!')
					os.system(f'{query}')
				except Exception as e:
					speak(f'Sorry Sir there was some error in executing {query}')
########### W E A T H E R   F O R E C A S T ####################################################################
		elif 'weather' in query :
				if 'weather in ' in query:
					CITY = query.replace("weather in ","")
				else:
					CITY = takeCommand()
				weathereport(CITY)
		elif 'clear' in query:
			system('cls')
			speak('Screen Cleared')
		elif 'shutdown' in query or 'turn off' in query:
			speak('Do you really want to shut down the Computer?')
			ans = takeCommand()
			if 'yes' in ans or 'yeah' in ans or 'ya' in ans:
				speak('Ok Sir, shutting down Bye Bye, Take Care')
				try:
					system('shutdown /s /t 1')
				except Exception as e:
					speak('Code to shut down isnt worked!')
		elif 'send an email' in query or 'send email' in query:
		    speak('What is the subject?')
		    subject = takeCommand()
		    speak('What is the message?')
		    message = takeCommand()
		    content = 'Subject: {}\n\n{}'.format(subject, message)
		    #init gmail SMTP
		    mail = smtplib.SMTP('smtp.gmail.com', 587)

		    #identify to server
		    mail.ehlo()

		    #encrypt session
		    mail.starttls()

		    #login
		    try:
		    	mail.login('yourgmail@gmail.com', 'password')
		    except Exception as e:
		    	speak('Error in Login')

		    #send message
		    speak('Please type Whom to Send :')
		    to = input('To:')
		    try:
		    	mail.sendmail('yourgmail@gmail.com', to, content)
		    except Exception as e:
		    	speak('Error in sending Email')

		    #end mail connection
		    mail.close()
		    speak('Email Sent')

		elif 'start my day' in query:
			speak("I wish you'll have a beautiful day Sir")
			CITY = 'bangalore'
			weathereport(CITY)
			newsreport()
		elif 'happy birthday' in query:
			bday.bday()
