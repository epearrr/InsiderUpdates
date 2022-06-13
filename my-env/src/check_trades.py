from bs4 import BeautifulSoup
import requests


# returns dictionary trade_info
def get_trade_info():
    # this url shows purchases and sales made by CEOs and COOs
    url = 'http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=730&fdr=&td=0&tdr=&fdlyl=&fdlyh=&daysago=&xp=1&xs=1&vl=25&vh=&ocl=&och=&sic1=-1&sicl=100&sich=9999&isceo=1&iscoo=1&grp=0&nfl=&nfh=&nil=&nih=&nol=&noh=&v2l=&v2h=&oc2l=&oc2h=&sortcol=0&cnt=100&page=1'
    trade_info = {}

    page_source = requests.get(url, 'html.parser').text
    soup = BeautifulSoup(page_source)

    table = soup.find('table', {'class' : 'tinytable'})
    recent_trade = table.find_all('tr')[2]
    
    # changing the index of the 'tr' changes the row. changing the index of the 'td' changes the column
    trade_info['filing_date'] = recent_trade.find_all('td')[1].find('a').text
    trade_info['trade_date'] = recent_trade.find_all('td')[2].text
    trade_info['ticker'] = recent_trade.find_all('td')[3].find('a').text
    trade_info['company_name'] = recent_trade.find_all('td')[4].find('a').text
    trade_info['insider_name'] = recent_trade.find_all('td')[5].find('a').text
    trade_info['title'] = recent_trade.find_all('td')[6].text
    trade_info['trade_type'] = recent_trade.find_all('td')[7].text
    trade_info['price'] = recent_trade.find_all('td')[8].text
    trade_info['quantity'] = recent_trade.find_all('td')[9].text
    trade_info['ownership_change_pct'] = recent_trade.find_all('td')[11].text
    trade_info['value'] = recent_trade.find_all('td')[12].text

    return trade_info


def download_graph(trade_info):
    url = f"https://www.profitspi.com/stock/stock-charts.ashx?chart={trade_info['ticker']}"
    req = requests.get(url)
    
    file = open("images/stock_graph.png", "wb")
    file.write(req.content)
    file.close()
    
    
if __name__ == '__main__':
    download_graph(get_trade_info())
