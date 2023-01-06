from django.shortcuts import render
import string

# Create your views here.


def get_html_content(request):
    import requests
    name = request.GET.get('name')
    name1=string.capwords(name)
    lst_name=name1.split()
    fnl_name='_'.join(lst_name)
    url="https://en.wikipedia.org/wiki/"+fnl_name
    # USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    # LANGUAGE = "en-US,en;q=0.5"
    # session = requests.Session()
    # session.headers['User-Agent'] = USER_AGENT
    # session.headers['Accept-Language'] = LANGUAGE
    # session.headers['Content-Language'] = LANGUAGE
    # html_content = session.get(url).text
    html_content = requests.get(url).text
    return html_content


def home(request):
    result = None
    lst=None
    l=None
    a=None
    if 'name' in request.GET:
        # fetch the weather from Google.
        html_content = get_html_content(request)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        result = dict()
        result['name'] = request.GET.get('name')
        result['short_description']=soup.find('div',class_='shortdescription nomobile noexcerpt noprint searchaux').text
        details=soup.find_all('table',class_='infobox')
        if details is not None:
            list1=[]
            list2=[]
            for detail in details:
                h=detail.find_all('tr')
                for j in h:
                    heading=j.find_all('th')
                    description=j.find_all('td')
                    if heading is not None:
                        for x in heading:
                            list1.append(x.text)
                    if description is not None:
                        for y in description:
                            list2.append(y.text)
                        # result['b']=f"{x.text} :: {y.text} \n"
                l=tuple(zip(list1,list2))
                a=[]
                for i in range(len(l)):
                    a.append("::".join(l[i]))
                a="\n".join(a)
        else:
            l="no information available"
        try:    
            lst=[]
            for k in range(1,16):
                c=soup.find_all('p')[k].text
                lst.append(c)
        except IndexError as e:
            print("search result not available")

        # lst=[]
        # for k in range(1,16):
        #     c=soup.find_all('p')[k].text
        #     lst.append(c)
    return render(request, 'core/home.html', {'result': result,"lst":lst,"l":a})