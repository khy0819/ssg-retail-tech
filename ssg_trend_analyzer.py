# 이 파일은 온라인 쇼핑몰의 상품 데이터를 수집, 분석, 시각화하는 프로그램입니다.
# 웹 스크래핑, 데이터 분석, 시각화 능력을 보여주는 포트폴리오 예시로 활용할 수 있습니다.
# 이 코드는 가상의 SSG.COM 상품 데이터를 기반으로 작성되었습니다.

# --- 0. 라이브러리 설치 확인 및 불러오기 ---
# 필요한 라이브러리가 없으면 자동으로 설치하는 코드입니다.
# 파이썬 3.4 이상 버전에서 pip가 기본으로 설치되어 있어야 합니다.
import subprocess
import sys

def install_and_import(package):
    """
    Checks if a package is installed. If not, it installs it.
    """
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    finally:
        globals()[package] = __import__(package)

install_and_import('requests')
install_and_import('bs4')
install_and_import('pandas')
install_and_import('matplotlib')

# 이제 필요한 라이브러리를 불러옵니다.
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# --- 1. 데이터 수집 (웹 스크래핑) ---
# 실제 웹사이트의 HTML 구조가 아닌, 포트폴리오용 가상 데이터를 사용합니다.
# 이 코드는 신세계 리테일테크에 대한 이해도를 보여주기 위해 가상 상품을 포함합니다.
# SSG.COM의 '피코크', '노브랜드', '자주' 등의 상품명을 포함했습니다.

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>가상 SSG.COM 상품 목록</title>
</head>
<body>
    <div class="product_item">
        <h2 class="product_name">피코크 초코라떼</h2>
        <span class="price">3,500원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">노브랜드 버터쿠키</h2>
        <span class="price">1,980원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">노브랜드 무선이어폰</h2>
        <span class="price">19,800원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">자주 에어 서큘레이터</h2>
        <span class="price">69,900원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">노브랜드 계란 한 판</h2>
        <span class="price">7,980원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">피코크 닭가슴살 샐러드</h2>
        <span class="price">4,900원</span>
    </div>
    <div class="product_item">
        <h2 class="product_name">자주 침구세트</h2>
        <span class="price">99,000원</span>
    </div>
</body>
</html>
"""

try:
    # BeautifulSoup으로 HTML 파싱하기
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # 'class="product_item"'과 같이 상품 정보가 담긴 태그를 찾아서 가져옵니다.
    products_html = soup.find_all('div', class_='product_item')

    if not products_html:
        print("상품 정보를 찾을 수 없습니다. HTML 태그를 다시 확인하세요.")
        sys.exit()
    
    product_data = []

    # 각 상품에서 이름과 가격 정보 추출
    for product in products_html:
        try:
            name = product.find('h2', class_='product_name').text.strip()
            price_str = product.find('span', class_='price').text.strip()
            
            # 가격 문자열에서 숫자만 추출 (쉼표, '원' 등 불필요한 문자 제거)
            price = int(price_str.replace(',', '').replace('원', ''))

            product_data.append({'name': name, 'price': price})
        except (AttributeError, ValueError) as e:
            # 데이터 추출 중 오류가 발생하면 오류를 출력하고 다음 상품으로 넘어갑니다.
            print(f"데이터 추출 중 오류 발생: {e}. 이 상품은 건너뜁니다.")
            continue
except Exception as e:
    print(f"데이터 파싱 중 오류 발생: {e}")
    sys.exit()

# --- 2. 데이터 분석 및 처리 (Pandas) ---
df = pd.DataFrame(product_data)

if df.empty:
    print("수집된 데이터가 없습니다. 프로그램을 종료합니다.")
    sys.exit()

print("--- 데이터 분석 결과 ---")
print(f"총 상품 수: {len(df)}개")
print(f"상품 평균 가격: {df['price'].mean():.0f}원")

# --- 3. 데이터 시각화 (Matplotlib) ---
# 아래 코드 실행 ---> 'price_distribution.png' 파일 생성
try:
    # 한글 폰트 설정 (Mac과 Windows에서 모두 작동하도록 설정)
    if sys.platform == 'darwin': # Mac
        plt.rcParams['font.family'] = 'AppleGothic'
    elif sys.platform == 'win32': # Windows
        plt.rcParams['font.family'] = 'Malgun Gothic'
    
    plt.rcParams['axes.unicode_minus'] = False # 마이너스 기호 깨짐 방지
    plt.style.use('seaborn-v0_8-whitegrid') # 그래프 스타일 설정
    
    # 가격대별 상품 수 히스토그램
    plt.figure(figsize=(10, 6))
    plt.hist(df['price'], bins=10, edgecolor='black', alpha=0.7)
    plt.title('가격대별 상품 분포', fontsize=16)
    plt.xlabel('가격 (원)', fontsize=12)
    plt.ylabel('상품 수', fontsize=12)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    plt.savefig('price_distribution.png')
    print("그래프가 'price_distribution.png' 파일로 저장되었습니다.")
    
except Exception as e:
    print(f"그래프 생성 중 오류 발생: {e}")
