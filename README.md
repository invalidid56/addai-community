# add.ai Community API


## Requirements
- Python 3.11
- Docker & Docker Compose
- (Optional) Postgresql **14.0**
- (Optional) Redis **6.2.5**

## Conventions

### Active Branches
- `dev` (default): 개발용 브랜치입니다
- `feature/{description}`: 새로운 기능이 추가되는 경우에 사용
- `refactor/{description}`: 기능 변경 없이 코드 리팩토링만을 하는 경우에 사용
- `fix/{description}`: `dev` 브랜치로 반영하는 사소한 오류 수정 시에 사용
- `hotfix/{description}`: `prod` 브랜치로 반영하는 긴급한 오류 수정 시에 사용

### PR Merge Rules
  - default: *Squash and merge*


## Dev Guidelines

### Python Dependencies
가상환경을 활성화하고 필요한 패키지를 설치합니다.
```shell
pip install -r requirements.txt
```
`requirements.txt` 파일의 패키지 목록을 변경한 경우, 아래 명령을 통해 `requirements.txt` 파일을 최신화합니다.
```shell
pip freeze > requirements.txt
```

### Server Startup
Docker Compose를 활용하여 Postgresql, Redis 및 FastAPI 서버를 실행합니다.
```shell
docker-compose up
```

### DB Migration
Database에 수정사항이 있는 경우 alembic를 사용하여 migration을 진행합니다.
```shell
alembic revision --autogenerate -m "{description}"
```

이후 docker-compose 실행 시 자동으로 docker-entrypoint를 통해 migration이 진행됩니다

## Security
- [ ] `prod` 브랜치에는 `dev` 브랜치에 존재하지 않는 파일이나 코드가 포함되어서는 안됩니다.
- [ ] `prod` 브랜치에는 `dev` 브랜치에 존재하지 않는 패키지가 포함되어서는 안됩니다.
- [ ] `prod` 브랜치에는 `dev` 브랜치에 존재하지 않는 환경변수가 포함되어서는 안됩니다.
- [ ] 클라이언트 단에 user id와 같은 중요한 정보를 포함시켜서는 안됩니다. (무조건 유저네임을 기반으로 검색하도록)
