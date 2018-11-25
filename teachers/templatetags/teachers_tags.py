#!/usr/bin/env python
# -*- coding:utf-8 -*-
# _Auther_:Xiao Zhi
# Date:2018/10/22
from django import template
from king_admin import tag_base
from django.utils.safestring import mark_safe
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Sum
from crm import models
register=template.Library()

@register.simple_tag
def get_course_grades(class_obj):
    '''返回整个班级的成绩'''


    return dict(models.StudyRecord.objects.filter(course_record__from_class=class_obj).\
                values_list('student').annotate(Sum('score')) )


@register.simple_tag
def get_course_ranking(class_grade_dic):
    '''返回整个班级的排名数据'''
    ranking_dic = {}
    ranking_list = sorted(class_grade_dic.items(),key=lambda x:x[1])
    for item in ranking_list:
        ranking_dic[item[0]] = [item[1], ranking_list.index(item)+1]
    return ranking_dic


@register.simple_tag
def get_study_record_count(enroll_obj):
    study_records = []
    course_records = enroll_obj.enrolled_class.courserecord_set.select_related()
    for obj in course_records:
        study_records.extend(obj.studyrecord_set.select_related().filter(student=enroll_obj.customer))
    return study_records

@register.simple_tag
def fetch_stu_course_score(class_grade_dic, enroll_obj ):
    print(class_grade_dic,enroll_obj.customer.id )
    return class_grade_dic.get(enroll_obj.customer.id)

@register.simple_tag
def get_stu_grade_ranking(course_ranking_dic,enroll_obj):
    '''返回这个学员在本班的成绩排名'''

    score = course_ranking_dic.get(enroll_obj.customer.id)
    if score:
        return score[1]