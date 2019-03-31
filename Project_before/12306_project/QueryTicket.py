from Login import Login
from Const import API
from json import loads
import urllib3

urllib3.disable_warnings()

class query(object):

    def __init__(self):
        self.session = Login.session
        self.from_station = '漠河' #input('请输出出发地：')
        self.to_station = '古莲' #input('请输入到达地：')
        self.traindate = '2019-03-30' #input('请输入出发时间：')

    def ticket_list(self):
        req7 = self.session.get(url=API.station_url)
        t = req7.text.split('|')
        t.pop(0)
        dict1 = {}
        for i in range(len(t)):
            if i % 5 == 0:
                dict1[t[i]] = t[i + 1]
        return dict1

    def query_ticket(self):

        param8 = {
            'leftTicketDTO.train_date': self.traindate,
            'leftTicketDTO.from_station': self.ticket_list()[self.from_station],
            'leftTicketDTO.to_station': self.ticket_list()[self.to_station],
            'purpose_codes': 'ADULT'
        }
        req8 = self.session.get(url=API.query_url, params=param8)
        res8 = loads(req8.text)['data']['result']  # 查票接口
        train_dict = {}
        train_dict_query = {}
        # print(res8)
        for m in res8:
            fuck = m.split('|')
            if fuck[11] == 'Y':
                train_dict['secretStr'] = fuck[0]
                train_dict['train_no'] = fuck[2]
                train_dict['车次'] = fuck[3]
                train_dict['from_station_code'] = fuck[6]
                train_dict['to_station_code'] = fuck[7]
                train_dict['start_time'] = fuck[8]
                train_dict['end_time'] = fuck[9]
                train_dict['duration'] = fuck[10]
                train_dict['leftTicket'] = fuck[12]
                train_dict['trainDate'] = self.traindate
                train_dict['train_location'] = fuck[15]
                train_dict['from_station_no'] = fuck[16]
                train_dict['to_station_no'] = fuck[17]
                train_dict['高级软卧'] = fuck[21]
                train_dict['Other_type_seats'] = fuck[22]
                train_dict['软卧'] = fuck[23]
                train_dict['无座'] = fuck[26]
                train_dict['硬卧'] = fuck[28]
                train_dict['硬座'] = fuck[29]
                train_dict['二等座'] = fuck[30]
                train_dict['一等座'] = fuck[31]
                train_dict['商务座'] = fuck[32]
                train_dict['动卧'] = fuck[33]
                train_dict['type_seat'] = fuck[35]
                train_dict['出发地'] = self.from_station
                train_dict['目的地'] = self.to_station
            train_dict_query[fuck[3]] = train_dict
        return train_dict_query
