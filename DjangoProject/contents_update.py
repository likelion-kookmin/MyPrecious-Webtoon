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
        provider = ContentProvider()
        provider.name = i
        provider.save()


@transaction.atomic
def set_rating_systems():
    # http://www.zdnet.co.kr/view/?no=20190517090610
    ratings_list = ["전체연령가", "12세 이상 이용가", "15세 이상 이용가", "18세 이상 이용가"] # 만나이?, 한국나이?      네이버는 만나이https://m.help.naver.com/support/contents/contentsView.help?contentsNo=1766&lang=ko
    
    for i in ratings_list:
        rating = RatingSystem()
        rating.rating = i
        rating.save()
    
@transaction.atomic
def update_new_cartoon():
    naver = 'https://comic.naver.com/webtoon/weekday.nhn'
    naver_cartoon_urls = []
    res = requests.get(naver)

    soup = BeautifulSoup(res.content, 'html.parser')
    li = soup.select('div.list_area.daily_all > div > div > ul > li > a')


    for i in li:
        naver_cartoon_urls.append('https://comic.naver.com' + i.get('href')[:-12])
    
    for i in naver_cartoon_urls:
        res = requests.get(i)
        soup = BeautifulSoup(res.content, 'html.parser')
        so = soup.select_one('div.comicinfo > div.detail > h2')
        cartoon_name = str(so).split('<')[1].split('\t')[-1].strip()
        cartoonists = soup.select_one('#content > div.comicinfo > div.detail > h2 > span.wrt_nm').get_text().strip().split(' / ')
        description = soup.select_one('div.comicinfo > div.detail > p:nth-child(2)')
        try:
            age = soup.select_one('div.comicinfo > div.detail > p.detail_info > span.age').get_text()
        except:
            age = ""
        tags = soup.select_one('#content > div.comicinfo > div.detail > p.detail_info > span.genre').get_text().split(', ')
        image = soup.select_one('#content > div.comicinfo > div.thumb > a > img').get('src')

        print("cartoon_name: ", cartoon_name)
        print("cartoonists: ", cartoonists)
        # print(description)
        # print(age)
        # print(tags)
        # print(image)

        try:
            this_cartoon = Webtoon.objects.get(name=cartoon_name)
        except:
            this_cartoon = Webtoon()
        this_cartoon.name = cartoon_name
        this_cartoon.description = str(description)
        this_cartoon.content_provider = ContentProvider.objects.get(name='네이버웹툰')
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

        if age:
            if age == '전체연령가':
                age = '전체연령가'
            elif age == '12세 이용가':
                age = '12세 이상 이용가'
            elif age == '15세 이용가':
                age = '15세 이상 이용가'
            elif age == '18세 이용가':
                age = '18세 이상 이용가'

            this_cartoon.age_rating = RatingSystem.objects.get(rating=age)
        

        print()



@transaction.atomic
def update_my_model_data():
    datas = MyModel.objects.all()
    for data in datas:
        # 하고 싶은거 하고 
        data.save()


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
    # set_content_providers()
    # set_rating_systems()
    update_new_cartoon()
    # update_my_model_data()
    # test()