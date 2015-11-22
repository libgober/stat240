"""
Download all the data from CA bar

"""
import mechanize
from bs4 import BeautifulSoup
import csv
import re

br = mechanize.Browser()
br.set_handle_robots(False)

def pull_attorneys(url):
    url = "http://members.calbar.ca.gov/fal/MemberSearch/AdvancedSearch?LegalSpecialty=01"
    #pull attorneys
    html = br.open(url)
    soup = BeautifulSoup(html)
    table = soup.findAll('table')[3]
    data = []
    data.append(["URL","Name","Status","Number","City","Admission Date","Randomization"])
    for tr in table.findAll('tr'):
        row  = [] 
        try:
            tds = tr.find_all('td')
            row.append(tds[0].a.get('href'))
            for td in tds:
                row.append(td.text.encode('utf-8','ignore').strip())
            data.append(row)
        except:
            1
    return(data)

def active_span(text):
    """takes a style string like
    <style>#e0{display:none;}#e1{display:none;}#e2{display:none;}#e3{display:none;}#e4{display:none;}#e5{display:none;}#e6{display:none;}#e7{display:none;}#e8{display:none;}#e9{display:none;}#e10{display:none;}#e11{display:inline;}#e12{display:none;}#e13{display:none;}#e14{display:none;}#e15{display:none;}#e16{display:none;}#e17{display:none;}#e18{display:none;}#e19{display:none;}</style>
    
    returns which display is not none
    """
    split.string = re.split("#e(\d*)",text)
    for i in range(len(split.string)):
        if split.string[i] == "{display:inline;}":
            return(split.string[i-1])

        

def read_member_page(url):
    """Read a member page"""
    html = br.open(url)
    soup = BeautifulSoup(html)
    data =[]     
    tablerows = 0
    def read_row(i):
        if len(tablerows[i].findAll('td')) > 1:
            x = [tablerows[i].td.text,tablerows[i].td.next_sibling.next_sibling.text]
            return([i.strip() for i in x])
        else:
            x = tablerows[i].td.text.split(":")
            return([i.strip() for i in x])
    
    if len(soup.select("#moduleAttorneyProvInfo"))>0:
        tableid = 1
        table = soup.findAll('table')[tableid]
        tablerows = table.findAll('tr')
        data.append(read_row(0)) #bar number
        data.append(read_row(1)) #address
        email = active_span(soup.style.text)
        if len(tablerows[2].select("#e"+email)) > 0:
            data.append(["email:",tablerows[2].select("#e"+email)[0].text]) #email
        else:
            print "Email Not Available"
            data.append(["email:",NaN])
        data.append([i.strip() for i in re.split(":",tablerows[3].td.text)]) #undergrad
        data.append([i.strip() for i in re.split(":",tablerows[4].td.text)]) #law school
        
    else:
        tableid = 0
        table = soup.findAll('table')[tableid]
        tablerows = table.findAll('tr')
        data.append(read_row(0)) #bar number
        data.append(read_row(1)) #address
        email = active_span(soup.style.text)
        try: 
            e = tablerows[3].select("#e"+email)[0].text
        except:
            print "Failed to get " + url
            e = NaN
        data.append(["email:",e])#email
        data.append([tablerows[4].findAll('td')[2].text.strip(),tablerows[4].findAll('td')[3].text.strip()]) #undergrad
        data.append([tablerows[6].findAll('td')[2].text.strip(),tablerows[4].findAll('td')[3].text.strip()]) #Law school

    return(data)

dir_url = "http://members.calbar.ca.gov/fal/MemberSearch/AdvancedSearch?LegalSpecialty=01"
data = pull_attorneys(dir_url)
d = data
urls = ["http://members.calbar.ca.gov" + row[0] for row in data]

#now load the member page sand add some details to each entry
data[0] = data[0] + ["Bar Number","Address","Email","Undergrad","Law School"]
for i in range(1,len(urls)):
    data[i] = data[i]  + [j[1] for j in read_member_page(urls[i])]
    print i

df = pd.DataFrame(data[1:],columns=data[0])
df.Email.count()
df.to_csv("California_Criminal_Lawyers.csv")
