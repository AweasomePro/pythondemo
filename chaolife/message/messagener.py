from .client import post, post_to_business
from chaolifeProject.settings import TEST


def _clientpost(url, params):
    return post(url, params)


def _partnerpost(url, params):
    return post_to_business(url, params)


def get_push_params(data, channels=None, push_time=None, expiration_time=None, expiration_interval=None, where=None,
                    cql=None):
    """
       发送推送消息。返回结果为此条推送对应的 _Notification 表中的对象，但是如果需要使用其中的数据，需要调用 fetch() 方法将数据同步至本地。
       :param channels: 需要推送的频道
       :type channels: list or tuple
       :param push_time: 推送的时间
       :type push_time: datetime
       :param expiration_time: 消息过期的绝对日期时间
       :type expiration_time: datetime
       :param expiration_interval: 消息过期的相对时间，从调用 API 的时间开始算起，单位是秒
       :type expiration_interval: int
       :param where: 一个查询 _Installation 表的查询条件 leancloud.Query 对象
       :type where: leancloud.Query
       :param cql: 一个查询 _Installation 表的查询条件 CQL 语句
       :type cql: string_types
       :param data: 推送给设备的具体信息，详情查看 https://leancloud.cn/docs/push_guide.html#消息内容_Data
       :rtype: Notification
       """
    if push_time and expiration_time:
        raise TypeError('Both expiration_time and expiration_time_interval can\'t be set')
    params = {
        'data': data,
    }
    if channels:
        params['channels'] = channels
    if push_time:
        params['push_time'] = push_time.isoformat()
    if expiration_time:
        params['expiration_time'] = expiration_time.isoformat()
    if expiration_interval:
        params['expiration_interval'] = expiration_interval
    if where:
        params['where'] = where
    if cql:
        params['cql'] = cql
    params['prod'] = 'dev' if TEST else 'prod'

    return params


def push_message(data, channels=None, push_time=None, expiration_time=None, expiration_interval=None, where=None,
                 cql=None):
    params = get_push_params(data, channels, push_time=push_time, expiration_time=expiration_time,
                             expiration_interval=expiration_interval, where=where, cql=cql)
    result = post('/push', params=params).json()
    return result


def push_message_to_partner(data, channels=None, push_time=None, expiration_time=None, expiration_interval=None,
                            where=None, cql=None):
    params = get_push_params(data, channels, push_time=push_time, expiration_time=expiration_time,
                             expiration_interval=expiration_interval, where=where, cql=cql)
    result = _partnerpost('/push', params=params).json()
    print('返回结果{}'.format(result))
    return result


def push_message_to_client(data, channels=None, push_time=None, expiration_time=None, expiration_interval=None,
                           where=None, cql=None):
    return push_message(
        data=data,
        channels=channels,
        push_time=push_time,
        expiration_time=expiration_time,
        expiration_interval=expiration_interval,
        where=where,
        cql=cql
    )


class MessageSender(object):
    """
    """

    def send(self):
        pass


class PushMessageBuilder(object):
    def build(self):
        pass


