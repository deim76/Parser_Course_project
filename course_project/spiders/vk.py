# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy import FormRequest
from course_project.items import CourseProjectItem


class VkSpider(scrapy.Spider):
    name = 'vk'
    allowed_domains = ['vk.com']
    parse_urls = 'al_friends.php'
    start_urls = ['https://vk.com']
    id_search ='277722' #'2155572'  # '378994962' '1002216''378994962'
    id_start = '519629375''174156122'
    vk_login = '*********'
    vk_password = '********'
    find_user=100
    list_url = []

    vk_login_page = 'https://vk.com/login?u=2&to=ZnJpZW5kcz9pZD0xOTE2MzQ5JnNlY3Rpb249YWxs'

    def parse(self, response):
        lg_h = response.xpath('//input[@name="lg_h"]/@value').extract_first()
        ip_h = response.xpath('//input[@name="ip_h"]/@value').extract_first()

             # todo Authentication

        yield FormRequest(
            "https://login.vk.com/?act=login",
            method='POST',
            callback=self.parse_user,
            formdata={'_origin': 'https%3A%2F%2Fvk.com',
                      'act': 'login',
                      "email": self.vk_login,
                      'expire': '',
                      'ip_h': ip_h,
                      "lg_h": lg_h,
                      'pass': self.vk_password,
                      'role': 'al_frame',
                      'ul': ''}

        )

    def parse_user(self, response):
        if response.text.find('Не удаётся войти.') + 1:
            print('Не удаётся войти.')
        else:
            print('its ok')

            yield FormRequest(
                "https://vk.com/al_friends.php",
                method='POST',
                callback=self.userdata_parse,
                cb_kwargs={'user_id': self.id_start,
                           's': '','level':0},
                formdata={'act': 'load_friends_silent',
                          'al': '1',
                          'gid': '0',
                          'id': self.id_start}
            )

    def userdata_parse(self, response, user_id, s,level):
        start_url=self.start_urls[0]
        list_friends = s.split(';')[1:]
        if response.text.find('Ошибка доступа') + 1:
            print('ошибка Доступа', user_id)  ## страницы с закрытыми друзьями
            return
        if self.find_user > len(list_friends):
            friends = json.loads(json.loads(response.text[4:])['payload'][1][0])['all']
            list_id = []
            for i in friends[:10]:  #Ограниченно 10 первыми друзьями для проверки глубинных уровней
                list_id.append(i[0])

            if self.id_search in list_id:
                self.find_user = len(list_friends)
                list_friends.append(f'{start_url}/{user_id}')
                self.crawler.stop()
                print("find", list_friends)

                yield CourseProjectItem(

                    person_a=f'{start_url}/id{self.id_start}',

                    person_b=f'{start_url}/id{self.id_search}',

                    chain=list_friends[1:]

                )

            else:
                s = s + ";" + f'{start_url}/id{user_id}'
                level+=1
                for i in list_id:

                    if (i in self.list_url) == False:
                        self.list_url.append(i)
                        yield FormRequest(
                            "https://vk.com/al_friends.php",
                            method='POST',
                            callback=self.userdata_parse,
                            cb_kwargs={'user_id': i,
                                       's': s,
                                       'level':level

                                       },
                            formdata={'act': 'load_friends_silent',
                                      'al': '1',
                                      'gid': '0',
                                      'id': str(i)},priority=(20-level))#

