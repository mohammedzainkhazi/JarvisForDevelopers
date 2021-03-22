from aicommunication import speak
import requests, json
from newsapi.newsapi_client import NewsApiClient
def newsreport():
	main_url = "https://newsapi.org/v2/top-headlines?source=ndtv&q=cricket&country=in&apiKey=b186ef2f62a843b7b5de158944aef758"

	# fetching data in json format 
	open_bbc_page = requests.get(main_url).json() 

	# getting all articles in a string article 
	article = open_bbc_page["articles"] 

	# empty list which will  
	# contain all trending news 
	results = article 
	  
	for ar in article: 
	    results.append(ar["title"]) 
	    
	for i in range(len(results)):
		# printing all trending news 
	    print(i + 1, results[i])
	    # speak(i + 1, results[i])
	return results

if __name__ == '__main__':
	n = newsreport()
	print(n)
	speak(n)
