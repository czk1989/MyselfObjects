from django.core.paginator import Paginator
import re


class TuPian(object):

    def __init__(self,request,choice_dir,role):
        self.request=request
        self.choice_dir=choice_dir
        self.role=role

    def page_info(self):
        menu = {}
        search_info = str(self.request.GET.get('_q', '')).strip()
        for i in self.choice_dir:
            x,imgurl_list=str(i).split(':')
            urlid,name=str(x).split('--')
            img_list = re.findall(r"['](.*?)[']",imgurl_list)
            menu[name]=img_list

        if search_info:
            temp={}
            for item in menu:
                if re.search("%s"%search_info,item):
                    temp[item]=menu[item]
            menu=temp
        obj=[]
        for i in menu:
            temp=[]
            temp.append(i)
            temp.append(menu[i][0])
            obj.append(temp)
        paginator = Paginator(obj, 12)
        page = self.request.GET.get('page')
        query_sets = paginator.get_page(page)
        panduan=False
        if self.role=='meinv':
            panduan=True
        data={'query_sets': query_sets,'search_key': search_info,"role":self.role,'panduan':panduan}
        return data

