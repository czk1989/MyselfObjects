
import re


def return_t_or_f(data_list, num):
    count = False
    for data in data_list:
        if data.id == int(num):
            count = True
    if count:
        return True
    else:
        return False


class PermFunc(object):
    def __init__(self, request):
        self.request = request
        self.url = request.path

    def crm_change_customer(self):
        customer_id = re.search('\d+', re.search('\/\d+\/', self.url).group()).group()
        customer_list = self.request.user.customer_set.all()
        return return_t_or_f(customer_list, customer_id)

    def limit_class_list_(self):
        classlist_id = re.search('\d+', re.search('\/\d+\/', self.url).group()).group()
        class_list=self.request.user.classlist_set.all()
        return return_t_or_f(class_list, classlist_id)



