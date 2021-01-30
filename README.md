# weatherCN
The most simple way to get China city weather through python.
一行代码查询近7日天气，pip一键安装，数据来源于中国天气网

Install
---
```shell script
pip3 install weatherCN
```

Usage
---
**demo:**
```python
import weatherCN
# 快速使用
# 主城区
weather=weatherCN.getWeatherByNames('上海','上海')
weather=weatherCN.getWeatherByNames('安徽','合肥','合肥')

# 其它
weather=weatherCN.getWeatherByNames('上海','浦东')
weather=weatherCN.getWeatherByNames('西藏','日喀则','萨迦')
#
print(weather)


# 查看所有地区、以及每个区域的id信息
regionData=weatherCN.getRegionData()
print(regionData)

# 查询地区的id
regionId=weatherCN.getRegionId('北京','朝阳')
regionId=weatherCN.getRegionId('安徽','合肥','合肥')
print(regionId)

# 根据id查询近7日天气
weather=weatherCN.getWeatherById(regionId)
print(weather)
# {'lowTemp': ['3', '5', '0', '1', '3', '4', '2'], 'highTemp': ['14', '15', '10', '9', '14', '17', '18'], 'detail': ['多云', '小雨', '小雨转晴', '晴', '多云转晴', '晴', '晴']}

```
