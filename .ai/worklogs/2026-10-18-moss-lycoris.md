# MOSS Image LyCORIS 체크포인트 연결

- 사용자 승인 범위: 기존 native MOSS 구현과 표준 loader에 sd-scripts/LyCORIS 결과를 연결한다. 새 커밋·푸시·서버 재시작은 수행하지 않는다.
- 기존 HEAD `a639f187a`에서 작업. 기존 WORKFLOW/, input.old/, output 계열 등 untracked 데이터는 유지했다.
- `comfy/lora.py`: MOSS의 generic lycoris_ 이름을 추가했다. fused QKV에는 q/k/v별 slice alias를 추가했다. 기존 lora_unet_ alias와 노드 이름은 유지했다.
- `comfy/weight_adapter/base.py`: 출력축 DoRA 분모가 업데이트 방향 대신 기본 weight norm을 사용하던 문제를 수정했다. 입력축 구현은 유지했다.
- `tests-unit/weight_adapter_test/test_dora_norm.py`: Linear/Conv, 두 norm축, strength 0/0.5/1의 독립 수식 비교12개 통과.
- 기존 `nodes_lora_stack_test.py`의13개 회귀도 통과했다. 두 선택 합계25개 통과.
- sd-scripts `tests/test_moss_comfy.py`에서 실제 loader/patch engine으로 252/269개 대상 alias, 두 prefix, fused QKV, 표준 LoRA/LoKR/LoKR+DoRA의 효과를 비교했다.
- native workflow 예제는 sd-scripts의 `examples/moss/comfyui_workflow.json`에 있고 구조를 검사했다. TXT와 caption JSON 문장, layout JSON 입력 방법은 그 저장소의 `docs/moss_train_network.md`를 참조한다.
- 전체 pretrained 모델의 UI 로딩·실제 이미지 생성·양자화 모델 patch 실행·Windows/MPS는 미검증이다. 새 outbound network 경로는 추가하지 않았다.
- 이후 사용자가 커밋·푸시를 요청했다. upstream master와 구분할 로컬 `codex/moss-lycoris-compatibility` 브랜치에 이번4개 파일만 커밋한다. 기존 origin은 comfyanonymous/ComfyUI이므로 게시 가능한 사용자 소유 원격을 확인해야 한다.
