from Login import Login
from Const import API
from json import loads
import urllib3
import re
from QueryTicket import query
from Utility import utility
from urllib import parse

urllib3.disable_warnings()


class BuyTicket(object):

    def __init__(self):
        self.session = Login.session
        self.trainname = '6245'  # input('请输入你想要的车次：')
        self.seatType = '1'  # input('请输入你想要的座位类型,
        # WZ无座,F动卧,M一等座,O二等座,1硬座,3硬卧,4软卧,6高级软卧,9商务座:\n')
        self.username = '官笑尘'  # input('请输入你的名字，确保你的名字要在12306里面哦:')

    def buyticket(self):

        train_dict_query1 = query().query_ticket()

        train_dict_query = train_dict_query1[self.trainname]
        data9 = {'_json_att': ''}
        req9 = self.session.post(url=API.check_user_url, data=data9)
        data10 = {
            'secretStr': parse.unquote(train_dict_query['secretStr']),
            'train_date': train_dict_query['trainDate'],
            'back_train_date': utility.now(),
            'tour_flag': 'dc',
            'purpose_codes': 'ADULT',
            'query_from_station_name': train_dict_query['出发地'],
            'query_to_station_name': train_dict_query['目的地'],
            'undefined': ''
        }
        req10 = self.session.post(url=API.order_url, data=data10)
        if loads(req10.text)['status']:
            print('系统提交订单请求成功')

        data11 = {'_json_att': ''}
        req11 = self.session.post(url=API.init_url, data=data11)
        REPEAT_SUBMIT_TOKEN = re.findall("globalRepeatSubmitToken = '(.*?)';", req11.text)[0]
        # print(re.findall(r"key_check_isChange':'(.*?)'", req11.text))
        keyCheckIsChange = re.findall(r"key_check_isChange':'(.*?)'", req11.text)[0]

        data12 = {
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
        }
        req12 = self.session.post(url=API.getDTO_url, data=data12)
        passengers = loads(req12.text)['data']['normal_passengers']
        for passenger in passengers:
            if passenger['passenger_name'] == self.username:
                passengerTicketStr = '{},{},{},{},{},{},{},N'.format(self.seatType, passenger['passenger_flag'],
                                                                     passenger['passenger_type'],
                                                                     passenger['passenger_name'],
                                                                     passenger['passenger_id_type_code'],
                                                                     passenger['passenger_id_no'],
                                                                     passenger['mobile_no'])
                oldPassengerStr = '{},{},{},3_'.format(passenger['passenger_name'], passenger['passenger_id_type_code'],
                                                       passenger['passenger_id_no'])
                self.checkOrder(passengerTicketStr, oldPassengerStr, train_dict_query, REPEAT_SUBMIT_TOKEN, keyCheckIsChange)
            else:
                print('无法购票')


    def checkOrder(self, passengerTicketStr, oldPassengerStr, train_dict_query, REPEAT_SUBMIT_TOKEN, keyCheckIsChange):
        data13 = {
            'cancel_flag': '2',
            'bed_level_order_num': '000000000000000000000000000000',
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldPassengerStr,
            'tour_flag': 'dc',
            'randCode': '',
            'whatsSelect': '1',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
        }
        req13 = self.session.post(url=API.checkOrder_url, data=data13)
        dict = req13.json()
        if dict['data']['submitStatus']:
            print('系统校验订单信息成功')
            if dict['data']['ifShowPassCode'] == 'Y':
                print('需要再次验证')
            if dict['data']['ifShowPassCode'] == 'N':
                print('那你没了呀')
        else:
            print('系统校验订单信息失败')
        data14 = {
            'train_date': utility.getTrainDate(train_dict_query['trainDate']),
            'train_no': train_dict_query['train_no'],
            'stationTrainCode': train_dict_query['车次'],
            'seatType': self.seatType,
            'fromStationTelecode': train_dict_query['from_station_code'],
            'toStationTelecode': train_dict_query['to_station_code'],
            'leftTicket': train_dict_query['leftTicket'],
            'purpose_codes': '00',
            'train_location': train_dict_query['train_location'],
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
        }
        req14 = self.session.post(url=API.getQ_url, data=data14)

        if req14.json()['status']:
            print('系统获取队列信息成功')

        else:
            print('系统获取队列信息失败')

        data15 = {
            'passengerTicketStr': passengerTicketStr,
            'oldPassengerStr': oldPassengerStr,
            'randCode': '',
            'purpose_codes': '00',
            'key_check_isChange': keyCheckIsChange,
            'leftTicketStr': train_dict_query['leftTicket'],
            'train_location': train_dict_query['train_location'],
            'choose_seats': '',
            'seatDetailType': '000',
            'whatsSelect': '1',
            'roomType': '00',
            'dwAll': 'N',
            '_json_att': '',
            'REPEAT_SUBMIT_TOKEN': REPEAT_SUBMIT_TOKEN
        }
        req15 = self.session.post(url=API.confirmQ_url, data=data15)
        print(req15)
        if req15.json()['status']['submitStatus'] == True:
            print('已完成订票，请前往12306进行支付')
        else:
            print('订票失败,请稍后重试!')


Login().login()
a = BuyTicket()
a.buyticket()
