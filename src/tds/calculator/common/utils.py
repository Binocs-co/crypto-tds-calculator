from uuid import uuid4
from datetime import datetime


def generate_unique_account_id():
    account_id = str(uuid4())
    return account_id


def current_time_epoch():
    utc_time = datetime.utcnow()
    epoch = datetime.utcfromtimestamp(0)
    epoch_time = (utc_time - epoch).total_seconds() * 1000.0
    return int(epoch_time)


def get_india_fy(start_time, end_time):
    current_time = current_time_epoch()
    FYs = [
        {'start': 1112293800000, 'end': 1143829799999, 'label': 'FY2005-06'},
        {'start': 1143829800000, 'end': 1175365799999, 'label': 'FY2006-07'},
        {'start': 1175365800000, 'end': 1206988199999, 'label': 'FY2007-08'},
        {'start': 1206988200000, 'end': 1238524199999, 'label': 'FY2008-09'},
        {'start': 1238524200000, 'end': 1270060199999, 'label': 'FY2009-10'},
        {'start': 1270060200000, 'end': 1301596199999, 'label': 'FY2010-11'},
        {'start': 1301596200000, 'end': 1333218599999, 'label': 'FY2011-12'},
        {'start': 1333218600000, 'end': 1364754599999, 'label': 'FY2012-13'},
        {'start': 1364754600000, 'end': 1396290599999, 'label': 'FY2013-14'},
        {'start': 1396290600000, 'end': 1427826599999, 'label': 'FY2014-15'},
        {'start': 1427826600000, 'end': 1459448999999, 'label': 'FY2015-16'},
        {'start': 1459449000000, 'end': 1490984999999, 'label': 'FY2016-17'},
        {'start': 1490985000000, 'end': 1522520999999, 'label': 'FY2017-18'},
        {'start': 1522521000000, 'end': 1554056999999, 'label': 'FY2018-19'},
        {'start': 1554057000000, 'end': 1585679399999, 'label': 'FY2019-20'},
        {'start': 1585679400000, 'end': 1617215399999, 'label': 'FY2020-21'},
        {'start': 1617215400000, 'end': 1648751399999, 'label': 'FY2021-22'},
        {'start': 1648751400000, 'end': 1680287399999, 'label': 'FY2022-23'},
        {'start': 1680287400000, 'end': 1711909799999, 'label': 'FY2023-24'}
    ]

    filters = []
    for fy in FYs:
        if fy['end'] > start_time and fy['start'] < end_time:
            filters.append(fy)
    if len(filters) >= 2:
        default_selection = filters[-2]
    else:
        default_selection = filters[-1]
    default_selection['default'] = True
    return filters
