import argparse
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

def plot_bar(df, title, y_col, color):
    plt.figure(figsize=(10, 6))
    plt.barh(df['영화'], df[y_col], color=color)
    plt.title(title)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def top10_domestic():
    data = [
        ("극한직업", 16265969), ("명량", 17614354), ("신과함께-죄와 벌", 14411152),
        ("국제시장", 14263954), ("어벤져스: 엔드게임", 13936649), ("겨울왕국 2", 13746761),
        ("베테랑", 13414000), ("아바타", 13338178), ("도둑들", 12983738), ("7번방의 선물", 12811054),
    ]
    df = pd.DataFrame(data, columns=["영화", "관객수"])
    plot_bar(df, "역대 박스오피스 TOP10 (국내)", "관객수", "#7600FF")

def marvel_rank():
    data = [
        ("어벤져스: 엔드게임", 13936649), ("어벤져스: 인피니티 워", 11211880), ("어벤져스: 에이지 오브 울트론", 10494499),
        ("아이언맨 3", 9001309), ("캡틴 아메리카: 시빌 워", 8677249), ("스파이더맨: 파 프롬 홈", 7960094),
        ("스파이더맨: 홈커밍", 7258678), ("어벤져스", 7074867), ("캡틴 마블", 5801070), ("앤트맨과 와스프", 5447826),
    ]
    df = pd.DataFrame(data, columns=["영화", "관객수"])
    plot_bar(df, "마블 영화 국내 관객 수 순위", "관객수", "#FF6666")

def monthly_korean():
    data = [
        ("서울의 봄", 10042000), ("싱글 인 서울", 2100000), ("3일의 휴가", 1800000),
        ("노량: 죽음의 바다", 1600000), ("괴물", 1500000), ("목호", 1200000),
        ("잠", 1000000), ("보호자", 980000), ("스마트폰을 떨어뜨렸을 뿐인데", 920000), ("비공식작전", 880000),
    ]
    df = pd.DataFrame(data, columns=["영화", "관객수"])
    plot_bar(df, "2024년 12월 한국 영화 흥행 순위", "관객수", "#00A6FF")

def highly_rated():
    data = [
        ("박하사탕", 5.0), ("살인의 추억", 5.0), ("비밀은 없다", 5.0), ("밀양", 5.0),
        ("버닝", 5.0), ("올드보이", 5.0), ("마더", 5.0), ("건축학개론", 5.0),
        ("기생충", 5.0), ("우리들", 5.0),
    ]
    df = pd.DataFrame(data, columns=["영화", "평점"])
    plot_bar(df, "20대에게 좋은 평을 받은 한국 영화", "평점", "#00C49F")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="영화 순위 시각화")
    parser.add_argument("--category", choices=["domestic", "marvel", "monthly", "rating"], required=True,
                        help="카테고리 선택: domestic | marvel | monthly | rating")
    args = parser.parse_args()

    if args.category == "domestic":
        top10_domestic()
    elif args.category == "marvel":
        marvel_rank()
    elif args.category == "monthly":
        monthly_korean()
    elif args.category == "rating":
        highly_rated()
