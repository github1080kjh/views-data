from django.shortcuts import render, HttpResponse
import os
# Create your views here.
from django.db.models import Count
from computing import models
import matplotlib.pyplot as plt
from django.forms.models import model_to_dict


# 保存数据
def save_data(req):
    if req.method == 'POST':
        user_status = req.POST.get('event')
        if user_status == 'confirm':

            # 将文件中结构化的数据存入数据库中
            with open('static/structure_data.txt', 'r') as file:
                # 从文件中读取出来的所有数据
                data = eval(file.read())
                for logging_dict in data:
                    # 这时候的logging_dict是存储着每一条日志记录的字典
                    # print(logging_dict['ip'])
                    # 请求ip
                    ip = logging_dict['ip']
                    # 时间
                    request_time = logging_dict['request_time']
                    # 请求方式
                    resquest_type = logging_dict['request_type']
                    # 请求地址
                    resquest_url = logging_dict['request_url']
                    # 服务器响应状态码
                    status_code = logging_dict['status_code']

                    # 将数据写入数据库
                    models.Logging.objects.create(
                        ip=ip,
                        request_time=request_time,
                        request_type=resquest_type,
                        request_url=resquest_url,
                        status_code=status_code
                    )
                # print(len(data))
            return HttpResponse('ok!')
    return render(req, 'save_data.html')


# 对数据进行可视化
def data_display(req):
    # 从数据库查询出有多少种url地址
    path_list = models.Logging.objects.values('request_url').annotate(url=Count('request_url')).values('request_url')
    path_list = list(path_list)   # 将queryset对象转换为list对象
    # print(type(path_list))

    # 存储路径的类型列表 还可以 用来存储饼状图中的标签（饼状图的绘制）
    path_kinds = []
    for path_dict_index in range(len(path_list)):
        # print(path_dict_index)
        # path_dict_index 是每个path字典在列表中的索引
        # print(path_list[path_dict_index]['request_url'])
        # 只将各种类型的路径存储在列表中
        path_kinds.append(path_list[path_dict_index]['request_url'])
    # print(path_kinds)

    # 获得总的日志数据个数
    comprehensive = len(models.Logging.objects.all().values('id'))
    # print(comprehensive)

    # 这个字典用来存储路径和路径和在全部路径中所占的比例
    proportion = {}

    # 对每个路径在数据库中进行检索，查询每个路径对应的出现了多少次
    for per_path in path_kinds:
        num = models.Logging.objects.filter(request_url=per_path).count()
        # print(num)

        # 在可视化数据中每个种类所占的大小
        angle = num/comprehensive*100
        finally_angle = int(angle)    # 两位精确度
        # print(finally_angle)

        # 将对应的数据存储在proportion字典中
        proportion[per_path] = finally_angle
    # print(proportion)

    # num = models.Logging.objects.filter(request_url='/data/attachment/common/c8/common_2_verify_icon.png').count()
    # num = models.Logging.objects.filter()
    # print(num)

    # 可视化数据的绘制

    # 存储每个路径所占的比例
    sizes = []
    # 循环遍历存有path的列表，取出每个路径对应的比例
    for single_path in path_kinds:
        per_size = proportion[single_path]
        sizes.append(per_size)
    print(sizes)
    explode = (0, 0, 0, 0)  # 0.1表示将Hogs那一块凸显出来
    plt.pie(sizes,autopct='%1.1f%%', labels=path_kinds, shadow=False, startangle=90)
    #  startangle表示饼图的起始角度
    # base_dir = os.path.dirname(os.getcwd())
    # print(base_dir)
    # result_dir = os.path.join(base_dir, 'static\imgs\data.png')
    # 将回执好的可视化数据存入static/imgs/data.png文件夹中
    result_dir = 'H:\project coding\Django\logging_analyze\static\imgs\data.png'
    plt.savefig('H:\project coding\Django\logging_analyze\static\imgs\data.png')

    return render(req, 'data_display.html', {'img_dir': result_dir, 'url_list': path_list})