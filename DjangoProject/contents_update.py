import os
import django
from django.db import transaction
import requests
from bs4 import BeautifulSoup

# django setting 파일 설정하기 및 장고 셋업
cur_dir = os.path.dirname(__file__)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MypreciousWebtoon.settings")
django.setup()

# 모델 임포트는 django setup이 끝난 후에 가능하다. 셋업 전에 import하면 에러난다. db connection 정보가 없어서......
from contentsApp.models import *

@transaction.atomic
def set_content_providers():
    providers_list = ["네이버웹툰", "다음웹툰", "레진", "미소설", "미스터블루", "배틀코믹스", "저스툰", "케이툰", "탑툰", "투믹스"]
    
    for i in providers_list:
        try:
            ContentProvider.objects.get(name=i)
        except:
            provider = ContentProvider()
            provider.name = i
            provider.save()


@transaction.atomic
def set_rating_systems():
    # http://www.zdnet.co.kr/view/?no=20190517090610
    ratings_list = ["미등록", "전체연령가", "12세 이상 이용가", "15세 이상 이용가", "18세 이상 이용가"] # 만나이?, 한국나이?      네이버는 만나이https://m.help.naver.com/support/contents/contentsView.help?contentsNo=1766&lang=ko
    
    for i in ratings_list:
        try:
            AgeRatingSystem.objects.get(rating=i)
        except:
            rating = AgeRatingSystem()
            rating.rating = i
            rating.save()
    
@transaction.atomic
def update_new_cartoon():
    update_naver()
    update_daum()
    update_lezhin()

@transaction.atomic
def update_naver():
    # naver = 'https://comic.naver.com/webtoon/weekday.nhn'
    naver = 'https://comic.naver.com/webtoon/creation.nhn?view=list'
    naver_cartoon_urls = []
    res = requests.get(naver)

    soup = BeautifulSoup(res.content, 'html.parser')
    li = soup.select('#content > div.all_list.all_text > div > ul > li > a')


    for i in li:
        naver_cartoon_urls.append('https://comic.naver.com' + i.get('href'))
    
    provider_naver = ContentProvider.objects.get(name='네이버웹툰')
    
    for i in naver_cartoon_urls:
        res = requests.get(i)
        soup = BeautifulSoup(res.content, 'html.parser')
        so = soup.select_one('div.comicinfo > div.detail > h2')
        cartoon_name = str(so).split('<')[1].split('\t')[-1].strip()
        print("cartoon_name: ", cartoon_name)
        cartoonists = soup.select_one('#content > div.comicinfo > div.detail > h2 > span.wrt_nm').get_text().strip().split(' / ')
        description = soup.select_one('div.comicinfo > div.detail > p:nth-child(2)')
        try:
            age = soup.select_one('div.comicinfo > div.detail > p.detail_info > span.age').get_text()
        except:
            age = None
        tags = []
        try:
            tags = soup.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').get_text().split(', ')
        except:
            print()
            print()
        image = soup.select_one('#content > div.comicinfo > div.thumb > a > img').get('src')

        try:
            this_cartoon = Webtoon.objects.get(name=cartoon_name, content_provider=provider_naver)
        except:
            this_cartoon = Webtoon()
            this_cartoon.content_provider = provider_naver
        this_cartoon.name = cartoon_name
        this_cartoon.description = str(description)
        this_cartoon.url = i
        this_cartoon.save()

        for cartoonist_name in cartoonists:
            try:
                cartoonist_obj = Cartoonist.objects.get(name=cartoonist_name)
            except:
                print("new cartoonist", cartoonist_name)
                cartoonist_obj = Cartoonist()
                cartoonist_obj.name = cartoonist_name
                cartoonist_obj.save()
            this_cartoon.cartoonists.add(cartoonist_obj)
        this_cartoon.save()

        for tag in tags:
            try:
                tag_obj = Tag.objects.get(tag_name=tag)
            except:
                print("new tag", tag)
                tag_obj = Tag()
                tag_obj.tag_name = tag
                tag_obj.save()
            this_cartoon.tags.add(tag_obj)
        this_cartoon.save()

        if age is not None:
            if age == '전체연령가':
                age = '전체연령가'
            elif age == '12세 이용가':
                age = '12세 이상 이용가'
            elif age == '15세 이용가':
                age = '15세 이상 이용가'
            elif age == '18세 이용가':
                age = '18세 이상 이용가'

            this_cartoon.age_rating = AgeRatingSystem.objects.get(rating=age)
        this_cartoon.save()
        
        # print("cartoon_name: ", cartoon_name)
        print("cartoonists: ", cartoonists)
        # print(description)
        print(age)
        print(tags)
        # print(image)

        print()
    #Todo: 까뱅 등 일부 태그 가져오기 안됌, 컷툰 스마트툰과 같은 요소 태그로만들기, 유료화수, 이미지 리소스 url을 다운받아서 디비에 업로드, 요일과 연재중인지


@transaction.atomic
def update_daum():
    provider_obj = ContentProvider.objects.get(name='다음웹툰')
    datas = []

    day = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/'
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    for d in days:
        res = requests.get(day + d).json()
        datas.append(res['data'])

    finish = 'http://webtoon.daum.net/data/pc/webtoon/list_finished/'
    res = requests.get(finish).json()
    print(res['result']['status'])
    datas.append(res['data'])
    
    for data in datas:
        
        for i in data:
            cartoon_name = i['title']
            # print("cartoon_name: ", cartoon_name)
            cartoonists = []
            for j in i['cartoon']['artists']:
                cartoonists.append(j['penName'])
            # print(cartoonists)

            try:
                description = i['introduction']
            except:
                description = ""

            age = i['ageGrade']
            tags = []
            try:
                for j in i['cartoon']['genres']:
                    tags.append(j['name'])
            except:
                pass
            url_name = i['nickname']
            image = i['pcThumbnailImage']['url']

            try:
                this_cartoon = Webtoon.objects.get(name=cartoon_name, content_provider=provider_obj)
                print("new cartoon", cartoon_name)
            except:
                this_cartoon = Webtoon()
                this_cartoon.name = cartoon_name
                this_cartoon.content_provider = provider_obj
            this_cartoon.description = description
            this_cartoon.url = 'http://webtoon.daum.net/webtoon/view/' + url_name
            this_cartoon.save()

            for cartoonist_name in cartoonists:
                try:
                    cartoonist_obj = Cartoonist.objects.get(name=cartoonist_name)
                except:
                    print("new cartoonist", cartoonist_name)
                    cartoonist_obj = Cartoonist()
                    cartoonist_obj.name = cartoonist_name
                    cartoonist_obj.save()
                this_cartoon.cartoonists.add(cartoonist_obj)
            this_cartoon.save()

            for tag in tags:
                try:
                    tag_obj = Tag.objects.get(tag_name=tag)
                except:
                    print("new tag", tag)
                    tag_obj = Tag()
                    tag_obj.tag_name = tag
                    tag_obj.save()
                this_cartoon.tags.add(tag_obj)
            this_cartoon.save()

            if age is not None:
                if age == 0:
                    age = '전체연령가'
                elif age == 12:
                    age = '12세 이상 이용가'
                elif age == 15:
                    age = '15세 이상 이용가'
                elif age == 19:
                    age = '18세 이상 이용가'

                this_cartoon.age_rating = AgeRatingSystem.objects.get(rating=age)
            this_cartoon.save()
            
            # print("cartoon_name: ", cartoon_name)
            # print("cartoonists: ", cartoonists)
            # print(description)
            # print(age)
            # print(this_cartoon.age_rating)
            # print(tags)
            # print(image)

            # print()



@transaction.atomic
def update_lezhin():
    provider_obj = ContentProvider.objects.get(name='다음웹툰')
    datas = []

    day = 'http://webtoon.daum.net/data/pc/webtoon/list_serialized/'
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

    for d in days:
        res = requests.get(day + d).json()
        datas.append(res['data'])

    finish = 'http://webtoon.daum.net/data/pc/webtoon/list_finished/'
    res = requests.get(finish).json()
    print(res['result']['status'])
    datas.append(res['data'])
    
    for data in datas:
        
        for i in data:
            cartoon_name = i['title']
            # print("cartoon_name: ", cartoon_name)
            cartoonists = []
            for j in i['cartoon']['artists']:
                cartoonists.append(j['penName'])
            # print(cartoonists)

            try:
                description = i['introduction']
            except:
                description = ""

            age = i['ageGrade']
            tags = []
            try:
                for j in i['cartoon']['genres']:
                    tags.append(j['name'])
            except:
                pass
            url_name = i['nickname']
            image = i['pcThumbnailImage']['url']

            try:
                this_cartoon = Webtoon.objects.get(name=cartoon_name, content_provider=provider_obj)
                print("new cartoon", cartoon_name)
            except:
                this_cartoon = Webtoon()
                this_cartoon.name = cartoon_name
                this_cartoon.content_provider = provider_obj
            this_cartoon.description = description
            this_cartoon.url = 'http://webtoon.daum.net/webtoon/view/' + url_name
            this_cartoon.save()

            for cartoonist_name in cartoonists:
                try:
                    cartoonist_obj = Cartoonist.objects.get(name=cartoonist_name)
                except:
                    print("new cartoonist", cartoonist_name)
                    cartoonist_obj = Cartoonist()
                    cartoonist_obj.name = cartoonist_name
                    cartoonist_obj.save()
                this_cartoon.cartoonists.add(cartoonist_obj)
            this_cartoon.save()

            for tag in tags:
                try:
                    tag_obj = Tag.objects.get(tag_name=tag)
                except:
                    print("new tag", tag)
                    tag_obj = Tag()
                    tag_obj.tag_name = tag
                    tag_obj.save()
                this_cartoon.tags.add(tag_obj)
            this_cartoon.save()

            if age is not None:
                if age == 0:
                    age = '전체연령가'
                elif age == 12:
                    age = '12세 이상 이용가'
                elif age == 15:
                    age = '15세 이상 이용가'
                elif age == 19:
                    age = '18세 이상 이용가'

                this_cartoon.age_rating = AgeRatingSystem.objects.get(rating=age)
            this_cartoon.save()
            
            # print("cartoon_name: ", cartoon_name)
            # print("cartoonists: ", cartoonists)
            # print(description)
            # print(age)
            # print(this_cartoon.age_rating)
            # print(tags)
            # print(image)

            # print()



@transaction.atomic
def test():
    # try:
    #     ContentProvider.objects.get(name='네이버웹툰')
    # except:
    #     print("no")
    i = 'https://comic.naver.com/webtoon/list.nhn?titleId=651673&weekday=sat'

    res = requests.get(i)
    soup = BeautifulSoup(res.content, 'html.parser')
    so = soup.select_one('#content > div.comicinfo > div.detail > h2')

    so = str(so).split('<')[1].split('\t')[-1].strip()
    print(so)
    # cartoon_name = so[1].strip()
    # cartoonists = so[2].strip().split(' / ')
    # description = soup.select_one('div.comicinfo > div.detail > p:nth-child(2)')
    # try:
    #     age = soup.select_one('div.comicinfo > div.detail > p.detail_info > span.age').get_text()
    # except:
    #     age = ""
    # tags = soup.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').get_text().split(', ')
    # image = soup.select_one('#content > div.comicinfo > div.thumb > a > img').get('src')
    # print(so)



if __name__ == "__main__":
    set_content_providers()
    set_rating_systems()
    update_new_cartoon()
    # update_naver()
    # update_daum()
    # update_lezhin()
    # update_my_model_data()
    # test()