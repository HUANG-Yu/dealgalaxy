import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

try:
    # api = Connection(domain='svcs.sandbox.ebay.com', appid='YuHUANG-insightd-SBX-5ab9522e2-5c2b72d2', config_file=None)
    api = Connection(appid='YuHUANG-insightd-PRD-04d8cb02c-4739185d', config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'Lowe Gift Card'})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    print item
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)

except ConnectionError as e:
    print(e)
    print(e.response.dict())