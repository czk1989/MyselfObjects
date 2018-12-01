
import re

def crm_change_customer(request, *args, **kwargs):
    url=request.path
    customer_id=re.search('\d+',re.search('\/\d+\/',url).group()).group()
    customer_list=request.user.customer_set.all()
    count=False
    for customer in customer_list:
        if customer.id==int(customer_id):
            count = True
    if count:
        return True
    else:
        return False
