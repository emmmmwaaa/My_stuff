import requests, time

class utility(object):
    @classmethod
    def getSession(self):
        session = requests.session()  # 创建session会话
        session.headers = {
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Host': 'kyfw.12306.cn',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3719.0 Safari/537.36'
        }
        session.verify = False  # 跳过SSL验证
        return session

    @classmethod
    def formatDate(self, date):
        year = time.strptime(date, '%Y%m%d').tm_year
        month = time.strptime(date, '%Y%m%d').tm_mon
        day = time.strptime(date, '%Y%m%d').tm_mday
        return '%04d-%02d-%02d' % (year, month, day)

    # 检查购票日期是否合理
    @classmethod
    def checkDate(self, date):

        localTime = time.localtime()

        localDate = '%04d-%02d-%02d' % (localTime.tm_year, localTime.tm_mon, localTime.tm_mday)

        # 获得当前时间时间戳
        currentTimeStamp = int(time.time())
        # 预售时长的时间戳
        deltaTimeStamp = '2505600'
        # 截至日期时间戳
        deadTimeStamp = currentTimeStamp + int(deltaTimeStamp)
        # 获取预售票的截止日期时间
        deadTime = time.localtime(deadTimeStamp)
        deadDate = '%04d-%02d-%02d' % (deadTime.tm_year, deadTime.tm_mon, deadTime.tm_mday)
        # print(Colored.red('请注意合理的乘车日期范围是:{} 至 {}'.format(localDate, deadDate)))

        # 判断输入的乘车时间是否在合理乘车时间范围内
        # 将购票日期转换为时间数组
        trainTimeStruct = time.strptime(date, "%Y-%m-%d")
        # 转换为时间戳:
        trainTimeStamp = int(time.mktime(trainTimeStruct))
        # 将购票时间修改为12306可接受格式 ，如用户输入2018-8-7则格式改为2018-08-07
        trainTime = time.localtime(trainTimeStamp)
        trainDate = '%04d-%02d-%02d' % (trainTime.tm_year, trainTime.tm_mon, trainTime.tm_mday)
        # 比较购票日期时间戳与当前时间戳和预售截止日期时间戳
        if currentTimeStamp <= trainTimeStamp and trainTimeStamp <= deadTimeStamp:
            return trainDate
        else:
            print('Error:您输入的乘车日期:{}, 当前系统日期:{}, 预售截止日期:{}'.format(trainDate, localDate, deadDate))
            return False

    @classmethod
    def getTrainDate(self, dateStr):
        # 返回格式 Wed Aug 22 2018 00: 00:00 GMT + 0800 (China Standard Time)
        # 转换成时间数组
        timeArray = time.strptime(dateStr, "%Y-%m-%d")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        # 转换成localtime
        timeLocal = time.localtime(timestamp)
        # 转换成新的时间格式
        GMT_FORMAT = '%a %b %d %Y 00:00:00 GMT+0800'
        timeStr = time.strftime(GMT_FORMAT, timeLocal)
        timeStr = timeStr + ' (中国标准时间)'
        return timeStr

    @classmethod
    def now(cls):
        localTime = time.localtime()
        localDate = '%04d-%02d-%02d' % (localTime.tm_year, localTime.tm_mon, localTime.tm_mday)
        return localDate



