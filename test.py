
from app import articles, userInfo

id = 16

data = {}

tempArticle = articles.query.get(id)
tempData = ""
tempData += f'{tempArticle.title}, '
tempData += f'{tempArticle.content}, '
tempData += f'{tempArticle.cover_photo}, '
tempData += f'{userInfo.query.get(int(tempArticle.writer_id)).name}, '
tempData += f'{userInfo.query.get(int(tempArticle.writer_id)).surname}, '
tempData += f'{tempArticle.date_created}'

data[id] = tempData

print(data)

