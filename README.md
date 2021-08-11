# zoom-attendance

Windows 이외의 운영체제 지원은 고려하지 않았습니다.

## 설치 및 설정하기

이 과정은 python3이 설치되었고, 사용할 수 있다는 가정 하에 작성되었습니다.

1. 이 리포지토리를 복사합니다. (또는 Code → Download ZIP으로 다운로드 하고 압축을 풉니다.)

    ```sh
    git clone https://github.com/nutyworks/zoom-attendance
    cd zoom-attendance
    ```

2. `InstallRequirements.bat`을 실행합니다.
3. `format.txt`를 열고 포맷을 설정합니다.
    * `{serial}` 자리는 0을 포함한 두 자리 숫자로 대체됩니다. (e. g. `10{serial}` → `1001`)
    * `{name}` 자리는 이름으로 대체됩니다.
4. `members.txt`를 열고 줄바꿈(`\n`)으로 구분하여 이름을 작성합니다.

## 사용하기

1. `Run.bat`을 실행합니다.

2. 명령 프롬프트의 안내에 따릅니다.
