
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import InputMediaPhoto
import requests
from datetime import datetime
import json
import schedule
import time
from unidecode import unidecode
from datetime import datetime
from collections import deque
payload1 = {
        "operationName": "SearchQuery",
        "variables": {
            "mediaSize": "MEDIUM",
            "q": None,
            "filter": {
                "categorySlug": "automobiles",
                "origin": None,
                "connected": False,
                "delivery": None,
                "regionIds": [],
                "cityIds": [],
                "priceRange": [None, None],
                "exchange": False,
                "hasPictures": False,
                "hasPrice": False,
                "priceUnit": None,
                "fields": [],#{key: "marque-voiture", value: "audi"}{'key': "marque-voiture", 'value': "skoda"},{'key': "modele", 'value': "skoda-octavia"}
                "page": 1,
                "count": 48
            }
        },
        "query": "query SearchQuery($q: String, $filter: SearchFilterInput, $mediaSize: MediaSize = MEDIUM) {\n  search(q: $q, filter: $filter) {\n    announcements {\n      data {\n        ...AnnouncementContent\n        smallDescription {\n          valueText\n          __typename\n        }\n        noAdsense\n        __typename\n      }\n      paginatorInfo {\n        lastPage\n        hasMorePages\n        __typename\n      }\n      __typename\n    }\n    active {\n      category {\n        id\n        name\n        slug\n        icon\n        delivery\n        deliveryType\n        priceUnits\n        children {\n          id\n          name\n          slug\n          icon\n          __typename\n        }\n        specifications {\n          isRequired\n          specification {\n            id\n            codename\n            label\n            type\n            class\n            datasets {\n              codename\n              label\n              __typename\n            }\n            dependsOn {\n              id\n              codename\n              __typename\n            }\n            subSpecifications {\n              id\n              codename\n              label\n              type\n              __typename\n            }\n            allSubSpecificationCodenames\n            __typename\n          }\n          __typename\n        }\n        parentTree {\n          id\n          name\n          slug\n          icon\n          children {\n            id\n            name\n            slug\n            icon\n            __typename\n          }\n          __typename\n        }\n        parent {\n          id\n          name\n          icon\n          __typename\n        }\n        __typename\n      }\n      count\n      __typename\n    }\n    suggested {\n      category {\n        id\n        name\n        slug\n        icon\n        __typename\n      }\n      count\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AnnouncementContent on Announcement {\n  id\n  title\n  slug\n  createdAt: refreshedAt\n  isFromStore\n  isCommentEnabled\n  userReaction {\n    isBookmarked\n    isLiked\n    __typename\n  }\n  hasDelivery\n  deliveryType\n  likeCount\n  description\n  status\n  cities {\n    id\n    name\n    slug\n    region {\n      id\n      name\n      slug\n      __typename\n    }\n    __typename\n  }\n  store {\n    id\n    name\n    slug\n    imageUrl\n    isOfficial\n    isVerified\n    __typename\n  }\n  user {\n    id\n    __typename\n  }\n  defaultMedia(size: $mediaSize) {\n    mediaUrl\n    mimeType\n    thumbnail\n    __typename\n  }\n  price\n  pricePreview\n  priceUnit\n  oldPrice\n  oldPricePreview\n  priceType\n  exchangeType\n  category {\n    id\n    slug\n    __typename\n  }\n  __typename\n}\n"
    }
def make_request(url, data):
    # Convert the data dictionary to a JSON string
    data_json = json.dumps(data)

    # Send a POST request with the data
    response = requests.post(url, data=data_json, headers={'Content-Type': 'application/json'})

    # Check the response status code and content
    datas = response.json()
    print(datas)
    return datas
url = "https://api.ouedkniss.com/graphql"

datas = make_request(url, payload1)
