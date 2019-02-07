import hashlib
import os
import shutil

from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


class VCSMixin:

    @staticmethod
    def calc_commit_hash(tracked_file, now):
        full_str = tracked_file.managed_file.name + str(now)
        return hashlib.sha1(str.encode(full_str)).hexdigest()

    @classmethod
    def commit(cls, *args, tracked_file, new_file, **kwargs):
        def file_hash(file):
            """
            새 파일 내용의 Hash값을 검사하는 메서드
            """
            BLOCKSIZE = 65536
            hasher = hashlib.sha1()
            for chunk in file.chunks(chunk_size=BLOCKSIZE):
                hasher.update(str(chunk).encode('utf-8'))
            return hasher.hexdigest()

        def save_temp_file(new_file, repository_dir, original_file):
            """
            쉘에서의 파일 비교를위해 새 파일을 저장하는 함수
            """
            vcs_dir = os.path.join(repository_dir, '.vcs')
            temp_file = os.path.join(vcs_dir, 'temp_file')
            shutil.copyfile(original_file, temp_file)
            if isinstance(new_file, str):
                with open(original_file, 'w') as f:
                    f.write(new_file)
            elif isinstance(new_file, InMemoryUploadedFile):
                with open(original_file, 'wb') as f:
                    for chunk in new_file.chunks(chunk_size=65536):
                        f.write(chunk)
            return temp_file

        now = timezone.now()  # PATCH파일 이름 저장, Commit의 저장시간을 동일하게 가져가기위해 여기서 now()
        repository_dir = tracked_file.managed_file.get_root_dir(
            tracked_file.managed_file).root_repository.get_repository_dir
        file_content_hash = file_hash(new_file)

        if not tracked_file.head or tracked_file.head != file_content_hash:
            # 기존 head가 없거나, 기존 내용과 동일하지 않다면 새 Commit을 생성하기위한 PATCH 파일을 생성
            tracked_file.head = file_content_hash  # Head를 새 파일의 해쉬로 지정
            origin_file = os.path.join(settings.ROOT_DIR, tracked_file.managed_file.file.path)  # 파일 비교를위해 원 파일의 위치를 지정
            temp_file = save_temp_file(new_file, repository_dir, origin_file)  # 파일 비교를위해 temp_file을 저장

            patch_dir = os.path.join(repository_dir, '.vcs', 'patch')  # 해당 레포지토리의 patch_dir를 찾음
            patch_file = os.path.join(patch_dir, cls.calc_commit_hash(tracked_file, now))  # patch_file 를 지정

            os.system('diff ' + temp_file + ' ' + origin_file + ' > ' + patch_file)  # diff 파일 생성
            tracked_file.save()

            os.remove(temp_file)
        elif tracked_file.head == file_content_hash:
            # 기존 커밋과 비교하고 같으면 실패
            raise ValueError('바뀐 내용이 없습니다.')

        kwargs['tracked_file'] = tracked_file
        kwargs['created_at'] = now
        obj = cls(*args, **kwargs)
        obj.save()
        return obj
