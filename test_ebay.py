import datetime
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection

try:
    api = Connection(appid='AkioKaki-507final-PRD-4132041a0-57ec3f09', config_file=None)
    response = api.execute('findItemsAdvanced', {'keywords': 'headphone'})

    assert(response.reply.ack == 'Success')
    assert(type(response.reply.timestamp) == datetime.datetime)
    assert(type(response.reply.searchResult.item) == list)

    item = response.reply.searchResult.item[0]
    assert(type(item.listingInfo.endTime) == datetime.datetime)
    assert(type(response.dict()) == dict)
    # print(response.dict())
    # print(type(response.dict()))
    with open("cache_thing.html", 'w') as f:
        key = response.dict().key()
        value = response.dict().value()
        f.write()


    # print(response.dict().get("searchResult"))
    for i in response.dict(): 
        print("{}, which is a type {}".format(i, type(i)))

except ConnectionError as e:
    print(e)
    print(e.response.dict())