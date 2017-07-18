#-*- coding: utf-8 -*-
import urllib, time, sys, re

from os import listdir, getcwd
from os.path import isfile, join
from bs4 import BeautifulSoup

# 카테고리:단어 파일이 있는 디렉토리.
dictionary_file_path = './dictionary'


def word_collect(letter, group):
    print letter,group
    # 한글을 주소값에 적합한 형식으로 인코딩.
    quoted_letter = urllib.quote(letter)
    quoted_group = urllib.quote(group)

    # 페이지는 1부터 시작
    page = 1

    # 1페이지부터 마지막 페이지까지 파싱.
    while True:
        try:
            # 10 페이지마다 3초씩 휴식.
            if page % 10 == 0:
                time.sleep(3)
            # 한 글자당 100페이지까지만 파싱
            # if page >= 100:
            #     break

            # url 렌더링.
            url = "http://krdic.naver.com/list.nhn?letter=%s&group=%s&kind=index&page=%d" % (quoted_letter, quoted_group, page)

            # 해당 url의 html을 읽어서 임시로 저장할 파일 포인터 생성.
            fp = urllib.urlopen(url)

            # 변수에 복사
            source = fp.read()
            fp.close()

            # 파싱을 위한 BeatifulSoup 객체 생성.
            soup = BeautifulSoup(source, "html.parser")

            # 어휘 리스트
            voca_list = soup.find('ul', 'lst3').find_all("li")

            # while문 종결 조건: 해당 페이지에 어휘가 없을 경우. 즉 범위를 넘어간 페이지의 경우 종료.
            if len(voca_list) == 0:
                break

            # 단어 리스트가 있다면 하나씩 탐색.
            for voca in voca_list:
                # 어휘 자체.
                string_node = voca.find('a')
                # 어휘 의미.
                meaning_node = voca.find('p')

                # 어휘와 의미 모두 온전히 있다면.
                if string_node is not None and meaning_node is not None:
                    # 어휘 부분의 노드.
                    string_node_text = string_node.text

                    # 뒤에 붙어있는 숫자 제거
                    string_node_text = re.sub("\d+", "", string_node_text)

                    # 의미 부분의 노드.
                    meaning_node_text = meaning_node.text

                    # 범주 체크.
                    cat = re.search("<(.{1,5})>", meaning_node_text)
                    # try:
                    # 범주가 존재하고 단어의 길이가 2글자 이상인 경우에만 파싱.
                    if cat and len(string_node_text) > 1:
                        # 해당 디렉토리에 있는 파일들의 경로를 리스트로 가져온다.
                        file_name_list = listdir(dictionary_file_path)

                        # file_name_list = [f for f in file_name_list]
                        category_string = cat.group(1)

                        with open(dictionary_file_path + '/' + category_string, "a") as f:
                            f.write(string_node_text.encode('utf-8') + "\n")

                        # print category_string
            print letter, group, " page: ", page

                    # except:
                    #     print '파싱 중 에러 발생.'
                    #     pass

            page = page + 1
        except:
            break

if __name__ == "__main__":
    indexes = [
            {
                "letter": "ㄱ",
                "groups": ["가", "갸", "거", "겨", "고", "교", "구", "규", "그", "기"]
             },
            {
                "letter": "ㄴ",
                "groups": ["나", "냐", "너", "녀", "노", "뇨", "누", "뉴", "느", "니"]
            },
            {
                "letter": "ㄷ",
                "groups": ["다", "댜", "더", "뎌", "도", "됴", "두", "듀", "드", "디"]
            },
            {
                "letter": "ㄹ",
                "groups": ["라", "랴", "러", "려", "로", "료", "루", "류", "르", "리"]
            },
            {
                "letter": "ㅁ",
                "groups": ["마", "먀", "머", "며", "모", "묘", "무", "뮤", "므", "미"]
            },
            {
                "letter": "ㅂ",
                "groups": ["바", "뱌", "버", "벼", "보", "뵤", "부", "뷰", "브", "비"]
            },
            {
                "letter": "ㅅ",
                "groups": ["사", "샤", "서", "셔", "소", "쇼", "수", "슈", "스", "시"]
            },
            {
                "letter": "ㅇ",
                "groups": ["아", "야", "어", "여", "오", "요", "우", "유", "으", "이"]
            },
            {
                "letter": "ㅈ",
                "groups": ["자", "쟈", "저", "져", "조", "죠", "주", "쥬", "즈", "지"]
            },
            {
                "letter": "ㅊ",
                "groups": ["차", "챠", "처", "쳐", "초", "쵸", "추", "츄", "츠", "치"]
            },
            {
                "letter": "ㅋ",
                "groups": ["카", "캬", "커", "켜", "코", "쿄", "쿠", "큐", "크", "키"]
            },
            {
                "letter": "ㅌ",
                "groups": ["타", "탸", "터", "텨", "토", "툐", "투", "튜", "트", "티"]
            },
            {
                "letter": "ㅎ",
                "groups": ["하", "햐", "허", "혀", "호", "효", "후", "휴", "흐", "히"]
            }
    ]

    for x in indexes:
        for group in x["groups"]:
            word_collect(x["letter"], group)
