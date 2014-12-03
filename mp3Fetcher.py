from bs4 import BeautifulSoup
import StringIO
import urllib2
import requests
import zipfile
import os
import sys


#Progress bar found on this Stack Overflow question
#http://stackoverflow.com/questions/5783517/downloading-progress-bar-urllib2-python
def chunk_report(bytes_so_far, chunk_size, total_size):
   percent = float(bytes_so_far) / total_size
   percent = round(percent*100, 2)
   sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
       (bytes_so_far, total_size, percent))

   if bytes_so_far >= total_size:
      sys.stdout.write('\n')

def chunk_read(response, chunk_size=8192, report_hook=None):
   total_size = response.info().getheader('Content-Length').strip()
   total_size = int(total_size)
   bytes_so_far = 0
   data = []

   while 1:
      chunk = response.read(chunk_size)
      bytes_so_far += len(chunk)

      if not chunk:
         break

      data += chunk
      if report_hook:
         report_hook(bytes_so_far, chunk_size, total_size)

   return "".join(data)

if __name__ == '__main__':

    base = "http://www.songspk.name/indian-mp3-songs/"
    movie = raw_input("Enter the movie name\t").lower()
    year = raw_input("Enter the year of release\t")
    try:
        print "Songs will be downloaded to " + os.getcwd() + '/' + movie 
        os.mkdir(movie)
        os.chdir(movie)
    except:
        pass

    toAppend = '-'.join(movie.split()) + '-' + year + '-mp3-songs.html'
    songsPKUrl = base + toAppend
    sourceSite = urllib2.urlopen(songsPKUrl)
    soup = BeautifulSoup(sourceSite)
    zipLinks = []
    
    for link in soup.find_all('a'):
        href = link.get('href')
        try:
            if href.endswith('.zip'):
                zipLinks.append(href)
        except:
            pass
            
    print "The following links have been discovered"
    counter = 1
    for zip in zipLinks:
        print str(counter) + "\t" + str(zip)
        counter += 1
    
    choice = int(raw_input("Which of the above do you wish to download?")) - 1
    downloadInfo = requests.head(zipLinks[choice]).headers
    downloadSize = downloadInfo['content-length']
    print str(int(downloadSize) / (1024 * 1024)) + "MB to be downloaded."
    print "Press y/n to continue"
    proceed = raw_input().lower()
    if proceed == 'n':
        print "Exiting."
        sys.exit(1)
    
    print "Downloading...Please wait"
    downloadFileReq = urllib2.Request(zipLinks[choice], headers={'User-Agent': "Magic"})
    downloadFile = urllib2.urlopen(downloadFileReq)
    downloaded = chunk_read(downloadFile, report_hook=chunk_report)
    zipFile = zipfile.ZipFile(StringIO.StringIO(downloaded))
    print "The following songs have been downloaded."
    try:
        for song in zipFile.namelist():
            print song
    except:
        pass
    
    print "Extracting all songs to the directory " + os.getcwd()     
    zipFile.extractall()
    
    print "Download successful."

