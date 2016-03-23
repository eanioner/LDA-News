import lxml.html
import requests
import codecs
import os
import time

main_path = u"http://www.fontanka.ru"
path_for_saving_news = u'./all_news/'
number_of_news_downloaded = 0

cnt = 0
threshold = 47121
with codecs.open('news_category_links', 'r', encoding='utf8') as inf:
    for line in inf:
        cnt += 1
        print cnt, 
        if cnt < threshold:
            continue
	
        category, link = line.split('\t')
        link = link.strip()
        try:
            response = requests.get(main_path + link)
        except:
            print "Something bad (no response) with %s"%link
            continue
        
        if category not in os.listdir(path_for_saving_news):
            os.mkdir(path_for_saving_news + category)
        
        path_for_news = path_for_saving_news[2:] + category + '/'
        
        if response.status_code == 200:
            
            try:
                number_of_news_downloaded += 1
                html = response.content
                tree = lxml.html.document_fromstring(html)
                txt = tree.xpath("//div[@class='article']/div[@class='article_desc']/div[@class='article_fulltext']/p/text()")
                filename = link.replace("/", "_")
                with codecs.open(path_for_news+filename, 'w', encoding="utf8") as ouf:
                    for t in txt:
                        ouf.write(t)
            except:
                print "Something bad with %s"%link
                    
        else:
            print "Something bad with %s"%link
        if (number_of_news_downloaded + threshold) % 10 == 1:
            print "%d \n"%(number_of_news_downloaded + threshold),
            time.sleep(0.5)
        
        
        



