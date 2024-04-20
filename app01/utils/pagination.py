import copy
import urllib.parse
from django.utils.safestring import mark_safe
import json


class Pagination(object):
    def __init__(self, request, queryset, page_parm='page', page_size=10, page_plus=2):
        page = request.GET.get(page_parm, '1')
        if page.isdecimal():
            page = int(page)
        else:
            page = 1
        query_dict = copy.deepcopy(request.GET)
        query_dict.mutable = True
        self.query_dict = query_dict
        self.page = page
        self.page_parm = page_parm
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count = (total_count - 1) // page_size + 1
        self.total_page_count = total_page_count
        self.page_plus = page_plus

    def html(self):
        datastr = ','.join(eval(self.query_dict["datalist"]))
        if self.total_page_count >= 2 * self.page_plus + 1:
            if self.page <= self.page_plus:
                start_page = 1
                end_page = 2 * self.page_plus + 1
            elif self.page + self.page_plus > self.total_page_count:
                start_page = self.total_page_count - (2 * self.page_plus)
                end_page = self.total_page_count
            else:
                start_page = self.page - self.page_plus
                end_page = self.page + self.page_plus
        else:
            start_page = 1
            end_page = self.total_page_count

        page_str_list = []
        self.query_dict.setlist(self.page_parm, [1])
        first_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>首页</a></li>"
        page_str_list.append(first_ele)

        if self.page - 1 <= 0:
            up_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>上一页</a></li>"
        else:
            self.query_dict.setlist(self.page_parm, [self.page - 1])
            up_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>上一页</a></li>"
        page_str_list.append(up_ele)

        for i in range(start_page, end_page + 1):
            self.query_dict.setlist(self.page_parm, [i])
            if i == self.page:
                ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>" + str(i) + "</a></li>"
            else:
                ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>" + str(i) + "</a></li>"
            page_str_list.append(ele)

        if self.page + 1 > self.total_page_count:
            self.query_dict.setlist(self.page_parm, [self.total_page_count])
            down_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>下一页</a></li>"
        else:
            self.query_dict.setlist(self.page_parm, [self.page + 1])
            down_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>下一页</a></li>"
        page_str_list.append(down_ele)
        self.query_dict.setlist(self.page_parm, [self.total_page_count])

        last_ele = "<li><a onclick='fun(\"" + datastr + "\",\"" + str(self.query_dict["page"]) + "\")'>尾页</a></li>"
        page_str_list.append(last_ele)

        search_string = """
            <form method="get" style="display: inline-block">
                <input style="display: inline-block;width: 100px;border-radius: 0" type="text"
                       class="form-control" id="exampleInputEmail3" placeholder="输入页码"
                       name="page">
                <span>
                    <button style="float:left;border-radius: 0" type="submit" class="btn btn-info">跳转</button>
                </span>
            </form>
        """

        # page_str_list.append(search_string)

        page_string = mark_safe(''.join(page_str_list))

        return page_string
