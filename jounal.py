import json

sample_json = """{
    "credit": {"建物": 100000},
    "debit":  {"現金": 100000},
    "issued by": "bgnori@gmail.com",
    "date": 1439517320
}"""

print json.loads(sample_json)





