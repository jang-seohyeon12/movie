import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time # 요청 사이에 지연 시간을 주기 위함

# User-Agent 설정: 웹사이트가 봇으로 인식하지 않도록 브라우저처럼 보이게 합니다.
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# 1. 역대 박스오피스 TOP 10 (Box Office Mojo)
def get_all_time_top10():
    print("--- 역대 전 세계 박스오피스 TOP 10 (Box Office Mojo) ---")
    url = "https://www.boxofficemojo.com/chart/top_lifetime_gross/"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status() # HTTP 오류 발생 시 예외 발생
        soup = BeautifulSoup(response.text, 'html.parser')

        # Box Office Mojo의 역대 흥행 순위 테이블 클래스 확인 (변경될 수 있음)
        table = soup.find('table', class_='a-bordered a-horizontal-stripes a-size-base a-span12 imdb-chart-table')
        if not table:
            print("오류: 역대 박스오피스 TOP 10 테이블을 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
            return

        # 첫 번째 행은 헤더이므로 제외하고 상위 10개 행만 가져옴
        rows = table.find_all('tr')[1:11]

        data = []
        for row in rows:
            cols = row.find_all('td')
            # Box Office Mojo 테이블 구조에 따라 인덱스 조정이 필요할 수 있습니다.
            # 순위(0), 영화제목(1), 스튜디오(2), 전세계수익(5) (가정)
            if len(cols) > 5: # 필요한 컬럼의 최소 개수 확인
                rank = cols[0].text.strip()
                title = cols[1].text.strip()
                worldwide_gross = cols[5].text.strip()
                data.append([rank, title, worldwide_gross])

        df = pd.DataFrame(data, columns=['순위', '영화 제목', '전세계 수익'])
        print(df.to_string(index=False)) # 인덱스 없이 출력
        print("\n" + "="*50 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"웹 요청 오류 발생 (역대 박스오피스): {e}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생 (역대 박스오피스): {e}")
    time.sleep(1) # 다음 요청 전 잠시 대기

# 2. 마블 영화 수익 순위 (Box Office Mojo 검색 기반)
def get_marvel_movie_rank():
    print("--- 마블 영화 수익 순위 (Box Office Mojo) ---")
    # 정확한 데이터를 위해 Box Office Mojo에서 검색 가능한 마블 영화 목록을 수동으로 입력
    # 이 목록은 시간이 지남에 따라 업데이트될 수 있습니다.
    marvel_movies = [
        "Avengers: Endgame", "Avatar", "Spider-Man: No Way Home", "Avengers: Infinity War",
        "The Avengers", "Avengers: Age of Ultron", "Black Panther", "Captain America: Civil War",
        "Iron Man 3", "Captain Marvel", "Spider-Man: Far From Home", "Guardians of the Galaxy Vol. 2",
        "Thor: Ragnarok", "Spider-Man: Homecoming", "Doctor Strange", "Ant-Man and the Wasp",
        "Iron Man 2", "Iron Man", "Ant-Man", "Thor: The Dark World", "Captain America: The Winter Soldier",
        "Guardians of the Galaxy", "Thor", "The Incredible Hulk", "Eternals", "Black Widow",
        "Shang-Chi and the Legend of the Ten Rings", "Doctor Strange in the Multiverse of Madness",
        "Thor: Love and Thunder", "Black Panther: Wakanda Forever", "Ant-Man and the Wasp: Quantumania",
        "Guardians of the Galaxy Vol. 3"
    ]

    data = []
    for movie_title in marvel_movies:
        # Box Office Mojo 검색 URL 인코딩 (한글 또는 특수문자 고려)
        search_url = f"https://www.boxofficemojo.com/search/?q={requests.utils.quote(movie_title)}"
        try:
            response = requests.get(search_url, headers=HEADERS)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # 검색 결과에서 가장 상단에 있는 영화의 링크를 찾습니다.
            # string 인자를 사용하면 DeprecationWarning을 피할 수 있습니다.
            movie_link_tag = soup.find('a', class_='a-link-normal', href=True, string=movie_title)
            if movie_link_tag:
                movie_detail_url = "https://www.boxofficemojo.com" + movie_link_tag['href']
                detail_response = requests.get(movie_detail_url, headers=HEADERS)
                detail_response.raise_for_status()
                detail_soup = BeautifulSoup(detail_response.text, 'html.parser')

                # 상세 페이지에서 'Worldwide' 수익 정보 찾기 (클래스나 구조가 변경될 수 있음)
                # 'text' 대신 'string' 인자 사용 권장
                worldwide_gross_span = detail_soup.find('span', string='Worldwide')
                if worldwide_gross_span and worldwide_gross_span.find_next_sibling('span'):
                    worldwide_gross = worldwide_gross_span.find_next_sibling('span').text.strip()
                    data.append([movie_title, worldwide_gross])
                else:
                    data.append([movie_title, "수익 정보 없음"])
            else:
                data.append([movie_title, "검색 결과 없음"])

        except requests.exceptions.RequestException as e:
            print(f"{movie_title} 웹 요청 오류 발생: {e}")
            data.append([movie_title, "오류 발생"])
        except Exception as e:
            print(f"{movie_title} 데이터 처리 중 오류 발생: {e}")
            data.append([movie_title, "오류 발생"])
        time.sleep(0.5) # 각 영화 검색 사이에 짧은 대기 시간

    # 수익을 숫자로 변환하여 정렬
    df = pd.DataFrame(data, columns=['영화 제목', '전세계 수익'])
    # 'N/A', '검색 결과 없음', '오류 발생' 등 숫자로 변환할 수 없는 값은 처리하지 않음
    df['전세계 수익 (숫자)'] = df['전세계 수익'].replace({r'[$,]': ''}, regex=True).astype(float, errors='coerce')
    df_sorted = df.sort_values(by='전세계 수익 (숫자)', ascending=False).drop(columns=['전세계 수익 (숫자)'])

    print(df_sorted.to_string(index=False))
    print("\n" + "="*50 + "\n")
    time.sleep(1)

# 3. 한국 영화 흥행 순위 (KOBIS - 영화진흥위원회)
def get_korean_box_office_rank():
    print("--- 한국 영화 흥행 순위 (KOBIS 역대 박스오피스) ---")
    # KOBIS 역대 박스오피스 페이지 URL
    url = "http://www.kobis.or.kr/kobis/business/stat/boxs/findFormerBoxOfficeList.do"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # KOBIS 페이지의 테이블 클래스 확인 (HTML 분석 결과 'tbl_comm'으로 확인됨)
        table = soup.find('table', class_='tbl_comm')
        if not table:
            print("오류: 한국 영화 흥행 순위 테이블을 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
            return

        # 첫 번째 행은 헤더이므로 제외하고 데이터 행들을 가져옴
        rows = table.find_all('tr')[1:]

        data = []
        for row in rows:
            # HTML 분석 결과에 따라 각 td 태그의 id를 사용하여 데이터 추출
            rank_tag = row.find('td', id='td_rank')
            movie_title_tag = row.find('td', id='td_movie')
            audience_tag = row.find('td', id='td_audiAcc') # 누적 관객수

            if rank_tag and movie_title_tag and audience_tag:
                rank = rank_tag.text.strip()
                # 영화 제목은 td_movie 안에 있는 a 태그의 텍스트를 가져와야 합니다.
                title = movie_title_tag.find('span', class_='ellip').find('a').text.strip()
                audience = audience_tag.text.strip()
                data.append([rank, title, audience])

        df = pd.DataFrame(data, columns=['순위', '영화 제목', '누적 관객수'])
        print(df.to_string(index=False))
        print("\n" + "="*50 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"웹 요청 오류 발생 (한국 영화 흥행): {e}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생 (한국 영화 흥행): {e}")
    time.sleep(1)

# 4. 영화 평점 높은 국내 영화 순위 (네이버 영화)
def get_korean_movie_rating_rank():
    print("--- 영화 평점 높은 국내 영화 순위 (네이버 영화) ---")
    # 네이버 영화 평점 순위 페이지 URL (현재 날짜로 업데이트)
    # 네이버 영화는 날짜 파라미터를 사용하므로 매일 업데이트 가능
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur&date={today}"

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # 네이버 영화 평점 순위 테이블 클래스 확인 (변경될 수 있음)
        table = soup.find('table', class_='list_ranking')
        if not table:
            print("오류: 영화 평점 순위 테이블을 찾을 수 없습니다. 웹사이트 구조가 변경되었을 수 있습니다.")
            return

        # 모든 tr 태그를 찾음 (첫 번째 tr은 보통 헤더가 아님)
        rows = table.find_all('tr')

        data = []
        for row in rows:
            # 영화 제목과 평점을 포함하는 td 태그 찾기
            title_tag = row.find('div', class_='tit5')
            rating_tag = row.find('td', class_='point')

            if title_tag and rating_tag:
                title = title_tag.find('a').text.strip()
                rating = rating_tag.text.strip()
                data.append([title, rating])

        # 평점(float) 기준으로 정렬 (네이버는 이미 정렬되어 있지만, 확인 차)
        df = pd.DataFrame(data, columns=['영화 제목', '평점'])
        df['평점 (숫자)'] = pd.to_numeric(df['평점'], errors='coerce') # 숫자로 변환할 수 없는 값은 NaN으로
        df_sorted = df.sort_values(by='평점 (숫자)', ascending=False).drop(columns=['평점 (숫자)'])

        print(df_sorted.to_string(index=False))
        print("\n" + "="*50 + "\n")

    except requests.exceptions.RequestException as e:
        print(f"웹 요청 오류 발생 (영화 평점): {e}")
    except Exception as e:
        print(f"데이터 처리 중 오류 발생 (영화 평점): {e}")
    time.sleep(1)

# 모든 함수 실행
if __name__ == '__main__':
    print("영화 박스오피스 및 평점 순위 정보 수집 시작...\n")
    get_all_time_top10()
    get_marvel_movie_rank()
    get_korean_box_office_rank() # KOBIS HTML 구조를 반영하여 수정된 함수
    get_korean_movie_rating_rank()
    print("모든 영화 순위 정보 수집 완료.")
    