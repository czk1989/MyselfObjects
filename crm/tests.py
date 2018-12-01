from django.test import TestCase

# Create your tests here.
import re
# 123
a='acoout/233/dfdf'

print(re.search('\d+',re.search('\/\d+\/',a).group()).group())