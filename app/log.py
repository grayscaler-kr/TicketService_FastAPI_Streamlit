import os
import logging

# 현재 실행 중인 파일의 경로를 바탕으로 로그 파일 경로 설정
def get_log_file_path():
    print(os.path.abspath(__file__))
    # 현재 실행 중인 파일의 경로 (__file__)을 사용하여 디렉토리 경로 추출
    caller_dir = os.path.dirname(os.path.abspath(__file__))
    
    # caller_dir에 'login_front.log'라는 로그 파일을 설정
    log_file = os.path.join(caller_dir, "login_front.log")
    return log_file

# 로그 파일 경로 얻기
log_file = get_log_file_path()

# 로그 설정
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

def log_info(message):
    logging.info(message)

def log_error(message):
    logging.error(message)

def log_warning(message):
    logging.warning(message)

def log_debug(message):
    logging.debug(message)
