from pprint import pformat
import pandas as pd
import requests

all_station_id = ['93t','89t','62t','43t','63t','78t','44t','80t','42t']
Province = ["Trang","Nakhon_Si_Thammarat","Narathiwat","Phuket","Mueang_Yala","Betong_Yala","Songkhla","Satun","Surat_Thani"]
param = "PM25,PM10,O3,CO,NO2,SO2,WS,TEMP,RH,WD"
data_type = "hr"
start_date = "2024-01-01"
end_date = "2024-03-12"
start_time = "00"
end_time = "23"
count = 0

for station_id in all_station_id:
    url = f"http://air4thai.com/forweb/getHistoryData.php?stationID={station_id}&param={param}&type={data_type}&sdate={start_date}&edate={end_date}&stime={start_time}&etime={end_time}"
    response = requests.get(url)
    response_json = response.json()

    pd_from_dict = pd.DataFrame.from_dict(response_json["stations"][0]["data"])
    print(pformat(pd_from_dict))
    pd_from_dict.to_csv(f"website/data/before_clean/{Province[count]}.csv")
    count+=1




