
import time,requests,datetime,json
from common.mysql_pub import MysqlUtil
from os import environ

host = environ.get('host')
user = environ.get('user')
passwd = environ.get('passwd')
sql_folder = environ.get('sql_folder')

# host = "http://192.168.1.15:8080"
# user = "jizhen1"
# passwd = "111111"
# sql_folder = r"C:\\Users\\Administrator\\PycharmProjects\\ecs_test\sql\\"


mysql_db = MysqlUtil()
s = requests.session()

def sleep(n_secs):
    time.sleep(n_secs)


def hook_sql(filename):
    sql_path = sql_folder + filename
    # 读取 sql 文件文本内容
    sql = open(sql_path, 'r', encoding='utf8')

    sqltxts = sql.readlines()
    sqltxts = [x.strip() for x in sqltxts]  # 去除换行符\n

    # 读取之后关闭文件
    sql.close()

    # list 转 str
    for sqltxt in sqltxts:
        mysql_db.mysql_execute(sqltxt)


def hook_print(str):
    print(str)


# 返回测试用户的userid
def get_login_userid():

    # 查询登录测试用户userid
    SQL = "select tu_id from stt_user  where loginname = " + "\"" + user + "\"" +";"
    mysqlutil = MysqlUtil()

    userid = mysqlutil.mysql_getstring(SQL)
    return str(userid)


# 用户登录ecs
def userlogin():
    # 调用登录接口
    login_url = host + "/sso/login"
    login_data = {"username": user, "password": passwd, "mac": ""}
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/74.0.3729.131 Safari/537.36"
    }
    r = s.post(login_url, data=login_data, headers=headers)

# 预检分诊工作台，返回登录用户的cookies
def triage_cookies():
    # 用户登录ecs
    userlogin()
    # 访问预检分诊首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triage/index"
    r = s.get(triageindex)

    cookies = s.cookies
    foo = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sid=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    bar = "".join(foo)
    return bar


# 预检分诊工作台，返回登录用户的cookies
def triage_cookies2():
    # 用户登录ecs
    userlogin()
    # 访问预检分诊首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triage/index"
    r = s.get(triageindex)

    cookies = s.cookies
    return cookies


# 医生站，返回登录用户的cookies
def triagedoctor_cookies():
    # 用户登录ecs
    userlogin()

    # 访问医生站首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triagedoctor/index"
    r = s.get(triageindex)

    cookies = s.cookies
    foo = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sid=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    bar = "".join(foo)
    return bar


# 抢救站，返回登录用户的cookies，给yaml用例中使用
def triagerescue_cookies():
    # 用户登录ecs
    userlogin()

    # 访问医生站首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triagerescue/index"
    r = s.get(triageindex)

    cookies = s.cookies
    foo = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sid=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    bar = "".join(foo)
    return bar




# 抢救站，返回登录用户的cookies，给其他debugtalk方法使用中使用
def triagerescue_cookies2():
    # 用户登录ecs
    userlogin()

    # 访问医生站首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triagerescue/index"
    r = s.get(triageindex)

    cookies = s.cookies
    return cookies


# 留观站，返回登录用户的cookies，给yaml用例中使用
def triageobserve_cookies():
    # 用户登录ecs
    userlogin()

    # 访问医生站首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triageobserve/index"
    r = s.get(triageindex)

    cookies = s.cookies
    foo = []
    # 遍历 cookies 拆分 dict 并拼接为特定格式的 str
    # 如: server=xxxxx; sid=xxxxxx; track=xxxxx;
    for k, v in cookies.items():
        foo.append(k + '=' + v + '; ')
    bar = "".join(foo)
    return bar


# 留观站，返回登录用户的cookies，给其他debugtalk方法使用中使用
def triageobserve_cookies2():
    # 用户登录ecs
    userlogin()

    # 访问医生站首页，如果不访问，直接调用接口会报重定向次数过多
    triageindex = host + "/triageobserve/index"
    r = s.get(triageindex)

    cookies = s.cookies
    return cookies


# 返回当前时间，作为接诊时间
def get_currenttime():
    nowtime = datetime.datetime.now()
    currenttime = nowtime.strftime('%Y-%m-%d %H:%M')
    return currenttime



# 获取抢救室床位，并且取空的一个床位id
def get_rescue_bedid():
    # 调用抢救工作站，返回登录时的cookies
    cookies = triagerescue_cookies2()

    s = requests.session()
    # 请求查询抢救室床位信息接口，获取所有床位信息
    url = host + "/triagerescue/index/seachBedInfo"
    data = {'department':'抢救室1'}
    r = s.post(url=url,data=data,cookies=cookies)
    # response = r.json()
    response = json.loads(r.text)

    # 获取一个空的床位id
    for i in response['rows']:
        if i['patient_id'] == None:
            bed_id = i['bed_id']
            break
    return bed_id



# 获取留观室床位，并且取空的一个床位id
def get_observe_bedid():
    # 调用留观工作站，返回登录时的cookies
    cookies = triageobserve_cookies2()

    s = requests.session()
    # 请求查询抢救室床位信息接口，获取所有床位信息
    url = host + "/triageobserve/index/seachBedInfo"
    data = {'department':'留观室1'}
    r = s.post(url=url,data=data,cookies=cookies)
    # response = r.json()
    response = json.loads(r.text)

    # 获取一个空的床位id
    for i in response['rows']:
        if i['patient_id'] == None:
            bed_id = i['bed_id']
            break
    return bed_id

def add_patients(fullname,cardnum,bornday,gender,tel,idcard,age,sg,tz,autograde,dividtime):
    # 调用预检分诊工作站，返回登录时的cookies
    cookies = triage_cookies2()

    s = requests.session()
    # 请求查询抢救室床位信息接口，获取所有床位信息
    url = host + "/triage/divid/save"
    data = {"id":"","fullname":fullname,"cardnum":cardnum,
            "bornday":bornday,"gender":gender,"tel":tel,"card_type":"01","parenttel":"15721028988",
            "reason":'发烧3天，高烧不退',"idcard":idcard,"address":'江苏省南京市江宁区双龙大道1088号明月新寓花园',"memberstel":'夏东海',"category":'1',
            "admission":'步行',"GreenChFlag":'N',"ThreeNoFlag":'N',"others":"","consciousness":'模糊',
            "anamnesis":'无',"status":'未接诊',"source":'自行来院',"age":age,"registertime":"","sg":sg,"tz":tz,"il6":"","crp":"",
            "cea":"","afp":"","myo":"","ddimer":"",
            "fer":"","ntprobnp":"","hsctnl":"","ckmb":"","ctnt":"","ca":"","sighid":"","handleid":"","autograde":autograde,
            "finalgrade":"",
            "changereason":'选择修改原因',"reasondetail":'修改原因:',"hljl":'已测体温超过38度，患者先要挂水退烧',"nurse":'高博',"nurseid":'10062',
            "deptment":'39',"deptmentname":'急诊内科',
            "symtpomid":"15948114482","symtpomzdyvalue":"","symtpomzdygrade":"","edts_ids":"","edts_ids_qitastatus":"false",
            "edts_ids_qita":"","mews_ids":"","mews_score":"","edts_score":"",
            "pain_score":'2',"fast_score":'A',
            "gcs_score":'14',"sign_grade":"","dividtime":dividtime,"signurl":"","xgpj":"","cixu":'1',"maxcixu":'1',"feijz":'1',
            "hisid":"","PAADMVisitNumber":"",
            "savestatus":'save',"allergic_history":'不详',
            "supplement":"","events_id":"","events_name":"","remark":"",
            "go_rct":'0',"GCS_xq":'4,5,5',
            "isFuzhen":'N',"isLiuguan":'N',"is_changegrade":0}

    r = s.post(url=url,data=data,cookies=cookies)



# add_patients('张晨阳','1234','1992-02-01','男','13925123600','365014199202012362','28岁','182','68','1002','2020-11-5 10:00')