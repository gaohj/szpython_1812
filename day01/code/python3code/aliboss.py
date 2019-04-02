import json
import urllib.request
import urllib.parse
headers = {
"User-Agent":"User-Agent, Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
}

url = "https://job.alibaba.com/zhaopin/socialPositionList/doList.json"
for i in range(1,6):
    params = {
        "pageSize": 10,
        "t": '0.8752307723219721',
        "keyWord": "python",
        "location": "深圳",
        "pageIndex": i
    }
    data = urllib.parse.urlencode(params).encode()

    req = urllib.request.Request(url,headers=headers,data=data)
    responses = urllib.request.urlopen(req)
    content = responses.read().decode()
    print(content)

    data_dict = json.loads(content)

    job_list = data_dict['returnValue']['datas']

    for job in  job_list:
        degree = job.get('degree')
        departmentName = job.get('departmentName')
        requirement = job.get('requirement')
        firstCategory = job.get('firstCategory')
        workExperience = job.get('workExperience')

        with open('ali.txt','a+',encoding='utf-8') as fp:
            fp.write(degree+departmentName+requirement+firstCategory+workExperience+ "\n")
            fp.flush() #write 必须回车才写 flush 能够不回车也往里写