EBS Volume Autoscale Function
=============================
EBS Volume 사용률이 일정 수준이 넘어갈 경우 자동으로 볼륨을 확장해주는 람다 함수
* Python으로 작성
* Version : `python 3.11.6`

### 작업 절차
#### 1. 2개의 SNS Topic 생성
- trigger : cloudwatch 알람의 action으로 지정될 sns.
  - trigger의 subscription은 람다 함수를 지정
- alert : 람다 함수 실행 후 결과를 전송 받을 sns.
  - alert의 subscription은 이메일, 슬랙 등이 될 수 있음.

#### 2. Lambda 구성
- layer 배포
  - 파이썬 패키지 배포
  - `$ bash -x ./deploy/pubilsh-layer.sh`
- function 생성
  - `$ bash -x ./deploy/create-lambda-function.sh [account id] [region]`
- 이후 코드 변경 사항 배포
  - `$ bash -x ./deploy/update-function-code.sh`

#### 3. 스크립트 동작 원리
- cloudwatch 알람 발생
- sns trigger 실행(람다 함수에 event 전달)
- 알람이 발생한 대상 인스턴스와 볼륨을 검색하여 해당 볼륨의 사이즈 5% 증설
- 인스턴스 내 파티션 크기, 파일사이즈 확장
- 메일, 슬랙 등으로 결과 전달

#### TODO
- 범용적으로 사용할 수 있도록
  - 5%의 고정 수치가 아닌 현재 볼륨 사이즈에 따라 탄력적으로 증설 가능하도록 수정
  - root volume 증설도 가능하도록 수정

