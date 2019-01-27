# Hangang-coin-Refactor

Hackerton-Coin을 리팩토링

## 개발환경 소개

```text
서비스 개발: python, django
서비스 호스팅: AWS
데이터베이스: Postgresql
배포: AWS ECS
버그 레포팅: Sentry
브로커 및 백엔드: ElastiCache (Redis)
개발 방법론: TDD (Code Coverage: 95%)
CI / CD: Travis CI (Docker Hub에 Image를 푸시하는것과 ECS를 Blue/Green Deployment 방식으로 무중단 자동배포하는 CD 포함)
프로젝트 관리: Trello
```


## 개발 기간

```text
2019-01-11 ~ 2019-01-27
```

## Travis 

`https://travis-ci.org/teachmesomething2580/Hangang-coin-Refactor`

## CodeCov

`https://codecov.io/gh/teachmesomething2580/Hangang-coin-Refactor`

## Trello

`https://trello.com/b/j9qKKAGF/hangang-coin-planning`

## 문제점

1. AWS EC2 free tier micro환경에서는 Selenium을 동작시킬 수 없다.

> 확신하지는 못하지만 firefox esr, PhantomJS 모두 안됬었다..

2. Functional_test에서 setUp 데이터를 공유하고싶은데 어떻게 안될까?

3. Trello를 어떻게 작성해야할지 아직 잘 모르겠다..
