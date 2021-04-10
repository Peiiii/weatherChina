import requests
import re
import os
import json
data_path=os.path.dirname(__file__)+'/data/city.json'
with open(data_path,'r',encoding='utf-8') as f:
    regionData=json.load(f)


def parse_county(counties):
    data={}
    for c in counties:
        info = {}
        info['id'] = c['districtId']
        info['name'] = c['districtName']
        info['level'] = 'county'
        info['children'] = {}
        data[info['name']]=info
    return data

def parse_city(cities):
    data={}
    for c in cities:
        info = {}
        info['id'] = c['cityId']
        info['name'] = c['cityName']
        info['level'] = 'city'
        info['children'] = parse_county(c['districtList']) if 'districtList' in c.keys() else {}
        data[info['name']] = info
    return data


def parse_province(provinces):
    data={}
    for p in provinces:
        info = {}
        info['id'] = p['id']
        info['name'] = p['provinceName']
        info['level'] = 'province'
        info['children'] = parse_city(p['cityList'])
        data[info['name']]=info
    return data





class Tree:
    def __init__(self,data):
        self.data= data
    def getRegionId(self,*args):
        node=self.getNode(*args)
        return node['id']
    def getNode(self,*keys):
        assert len(keys)>=1
        rootNode=self.data[keys[0]]

        return self._getNode(rootNode,*keys[1:])

    def _getNode(self,root, *keys):
        for key in keys:
            root = root['children'][key]
        return root

regionTree=Tree(parse_province(regionData))

def getRegionId(*args):
    return regionTree.getRegionId(*args)


def extractNumbers(s):
    s2=''
    for char in s:
        if char.isdigit() or char=='-':
            s2+=char
    return s2
class WeatherApp:
    def __init__(self):
        self.baseUrl = r"http://www.weather.com.cn/weather/"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}

    def getWeather7d(self,regionId):
        PageUrl = self.baseUrl + regionId + ".shtml"
        response=requests.get(PageUrl,headers=self.headers)
        response.encoding='utf-8'
        self.htmlResult = response.text
        highTemp = re.findall(r'<span>(.*?)</span>/<i>', self.htmlResult)
        highTemp=[extractNumbers(x) for x in highTemp]
        lowTemp = re.findall(r'</span>/<i>(.*?)</i>', self.htmlResult)
        lowTemp=[extractNumbers(x) for x in lowTemp]
        detail = re.findall(r'<p title="(.*?)" class="wea">', self.htmlResult)
        return dict(
            lowTemp=lowTemp, highTemp=highTemp, detail=detail)
			
	def getWeather1d(self,regionId):
        PageUrl = self.baseUrl + regionId + ".shtml"
        response=requests.get(PageUrl,headers=self.headers)
        response.encoding='utf-8'
        self.htmlResult = response.text
        data_json = re.findall(r'<script>\nvar hour3data=(.*?)\n</script>', self.htmlResult)
        data_parser = json.loads(data_json[0])
        return data_parser['1d']

app=WeatherApp()
def getWeatherById(regionId):
    return app.getWeather7d(regionId)
def get1dWeatherById(regionId):
	return app.getWeather1d(regionId)
def getWeatherByNames(*names):
    regionId=getRegionId(*names)
    return app.getWeather7d(regionId)
def get1dWeatherByNames(*names):
    regionId=getRegionId(*names)
    return app.get1dWeatherById(regionId)	

def getRegionData():
    return regionData
def demo():
    app=WeatherApp()
    id=getRegionId('青海','海东','民和')
    print(id)
    x=app.getWeather7d(id)
    print(x)
	oneDayWeather = app.getWeather7d(id)
	print(oneDayWeather)
	

if __name__ == '__main__':
    demo()