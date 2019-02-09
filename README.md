# Study-Planing
공부기록 사이트

## 기능 마인드맵
[MindMeister](https://www.mindmeister.com/1208278042?t=ZaUE9Qsx9R)

## API

[Swagger HUB]()

## 핵심 라이브러리
[Simple Text Version Control System](https://github.com/KapiteinRo/muq)

## 커밋 작성법

[Udacity Git Commit Message Style Guide](https://udacity.github.io/git-styleguide/)를 따른다.

### 제목 

`Type: 제목`

Type은 아래의 종류가 있다.

```text
Feat: 새로운 기능을 추가할 경우
Fix: 버그를 고친 경우
Docs: 문서를 수정한 경우
Style: 코드 포맷 변경, 세미콜론 누락, 코드 수정이 없는 경우
Refactor: 프로덕션 코드 리팩터링
Test: 테스트 추가, 테스트 리팩터링 (프로덕션 코드 변경 없음)
Chore: 빌드 태스트 업데이트, 패키지 매니저를 설정할 경우 (프로덕션 코드 변경 없음)
```

### 본문 (선택)

한 줄에 72자 이내로 작성한다.

### 꼬리말 (선택)

이슈 트래커 ID를 추가한다.

# 하면서 찾아본 것

## AbstractBaseUser

[네가지 User 구현법](https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html#abstractbaseuser)

#### 추가

REUQIRED_FIELDS는 CLI로 `createsuperuser`할 때 입력하여야할 필드를 나타낸다.

`USERNAME_FIELD`와 `password`는 기본적으로 포함되어있고 추가로 필요한것만 넣어주면 된다.



## Simple Text Version Control System

[muq](https://github.com/KapiteinRo/muq)



## File관련

1. upload_to는 함수를 받을 수 있다.
2. FileField는 사용자가 올린 파일, FilePathField는 시스템에 존재하는 파일을 가르키기위해 사용된다.
3. File관련 저장을할 때 upload_to의 함수를 적용시키고싶다면 아래와 같이 저장해야한다.

```python
# ManagedFile.objects.create() 로 생성하면 upload_to가 적용되지 않더라..

myfile = ContentFile('hello World')
obj = ManagedFile(
	...
)
obj.file.save('file_name', myfile)
```



## InMemoryUploadedFile

1. 한번 닫으면 다시 못연다.. (open, read, 등등 안되더라..)
2. `with open` 구문 대신 `for chunk in file.chunks()`를 사용하여 데이터를 가져오자.



## DRF Permission

[원문](https://stackoverflow.com/a/49626193/9583961)

- `def has_permission(self, request, view)`
- `def has_object_permission(self, request, view, obj)`

두가지 메서드는 권한이 없는 사용자가 데이터를 조작하는 것을 제한하기 위해 사용된다.

`has_permission`은 모든 HTTP 요청에 호출되는 반면,

`has_object_permission`은 DRF 메서드인 `def get_object(self)`에 의해 호출된다.

`has_object_permission` 메서드는 `GET, PUT, DELETE`에만 작동하고 `POST`에는 작동하지 않는다.



__정리__

- `permission_classes`에 정의된 리스트를 루프하며 권한을 확인한다.
- `has_permission` 메서드 뒤에 호출되는 `has_object_permission` 메서드는 POST 메서드를 제외하고 `True`를 반환한다. (POST 메서드는 `has_permission`에서만 실행된다.)
- `permission_classes` 메서드가 `False`를 반환할 때, permission내 메서드는 더이상 호출되지 않으며 이외의 경우 모든 permission을 확인한다.
- `has_permission`은 모든 HTTP request 요청에 대해 호출된다.
- `has_object_permission`는 `POST` 요청에 호출되지 않는다.



## 비교

`is` 연산자는 `Object Identity`를 비교한다. 같은 메모리를 참조하고있는지 비교한다.

`==`는 `Object equality`를 비교한다. 두 객체가 참조하고 있는 메모리는 신경쓰지 않고 두 객체가 같은 객체인가를 비교한다. `__eq__`나 `__cmp__`에 의해 결정된다.



## Dulwich

### ObjectStore로 Commit하기

1. blob 생성 (파일의 메타데이터를 제외한 데이터만을 담고있는 객체)
2. tree 생성 (디렉터리에 해당한다. 이는 Tree와 Blob를 가질 수 있다.)
3. Commit 생성
4. repository의 `object_store`에 blob, tree, commit을 담음
5. repo.refs에 commit.id를 담음

> blob만으로 커밋을 생성하면 파일은 생성되지 않음에 주의하자.



