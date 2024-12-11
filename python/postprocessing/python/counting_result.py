import os
import glob
import subprocess

# 기준 디렉토리 설정
base_dir = "/cms/ldap_home/seungjun/CMSSW_13_0_10/src/PhysicsTools/NanoAODTools/python/postprocessing/python"

# 결과 저장
results = []

# "run_analysis_*"로 시작하는 디렉토리 탐색
run_analysis_dirs = glob.glob(os.path.join(base_dir, "run_analysis_*/HTCondor_run"))
total_mc_files = 0
total_files = 0

for run_dir in run_analysis_dirs:
    # 부모 디렉토리
    parent_dir = os.path.dirname(run_dir)

    # 디렉토리 이름에서 키워드 추출
    keyword = os.path.basename(parent_dir).replace("run_analysis_", "")

    # MC*.sh 파일 갯수 세기
    mc_files = glob.glob(os.path.join(run_dir, "MC*.sh"))
    mc_count = len(mc_files)
    total_mc_files += mc_count

    # output 디렉토리 탐색
    output_dir = os.path.join(base_dir, "output_nominal")
    #output_dir = os.path.join(base_dir, "output_correction")

    # 조건 구성
    keyword_upto_2018 = "_2018".join(keyword.split("_2018")[:1]) + "_2018"
    correction = keyword.split("_")[-2]
    target = keyword.split("_")[-1]

    # `ls | grep` 방식으로 파일 리스트 가져오기
    #cmd = f"ls {output_dir} | grep '{keyword_upto_2018}' | grep '{correction}_{target}' | wc -l"
    #file_count = int(subprocess.check_output(cmd, shell=True, text=True).strip())
    #cmd = f"ls {output_dir} | grep '{keyword_upto_2018}' | grep '{correction}_{target}' | uniq | wc -l"
    cmd = f"find {output_dir} -type f -name '*{keyword_upto_2018}*{correction}_{target}*' | wc -l"
    file_count = int(os.popen(cmd).read().strip())

    matching_files_count = int(file_count)
    if file_count // 2 == mc_count:  # 정수 나눗셈으로 비교
        file_count = file_count // 2  # 정수 나눗셈으로 재설정

    total_files += file_count

    # 결과 저장
    results.append({
        "run_analysis_dir": parent_dir,
        "keyword": keyword,
        "MC_files_count": mc_count,
        "matching_files_count": file_count#matching_files_count
    })

# 결과 출력
for result in results:
    print(f"Directory: {result['run_analysis_dir']}")
    print(f"  Keyword: {result['keyword']}")
    print(f"  MC*.sh files: {result['MC_files_count']}")
    print(f"  Matching files in output: {result['matching_files_count']}")
    print("-" * 40)

# 총 MC 파일 수 출력
print(f"Total MC*.sh files: {total_mc_files}")
print(f"Total MC*.sh files: {total_files}")

