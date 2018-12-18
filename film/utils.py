from django.core.paginator import Paginator
import re


class DianYing(object):

    def __init__(self,request,choice_dir,role):
        self.request=request
        self.choice_dir=choice_dir
        self.role=role

    def page_info(self):
        menu = self.choice_dir
        search_info = str(self.request.GET.get('_q', '')).strip()

        if search_info:
            temp=[]
            for item in menu:
                if re.search("%s"%search_info,item[1]):
                    temp.append(item)
            menu=temp
        obj=menu
        paginator = Paginator(obj, 12)
        page = self.request.GET.get('page')
        query_sets = paginator.get_page(page)
        data={'query_sets': query_sets,'search_key': search_info,"role":self.role}
        return data

    def kankan_page(self):
        menu = self.choice_dir
        search_info = str(self.request.GET.get('_q', '')).strip()
        obj=menu
        if search_info.isdigit():
            for item in menu:
                if item == int(search_info):
                    obj=[item]
        paginator = Paginator(obj, 12)
        page = self.request.GET.get('page')
        query_sets = paginator.get_page(page)
        data={'query_sets': query_sets,'search_key': search_info}
        return data

