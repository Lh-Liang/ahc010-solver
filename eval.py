"""
AHC010 评测脚本（边跑边打印）
用法：
  python eval.py              # full 版，50 个 case
  python eval.py --workers 4  # 并行 worker 数（默认 8）

注意：ahc010 无 lite 版本，--lite 参数不可用。
"""

import argparse
import time
import ale_bench


def main():
    parser = argparse.ArgumentParser(description="AHC010 Evaluator")
    parser.add_argument("--workers", type=int, default=8, help="并行 worker 数（默认 8）")
    args = parser.parse_args()

    total_cases = 50

    print(f"=== AHC010 Evaluation (full) ===")
    print(f"Workers: {args.workers}  Cases: {total_cases}\n")

    with open("solution.py", "r", encoding="utf-8") as f:
        solution_code = f.read()

    print("Starting session...")
    session = ale_bench.start(
        problem_id="ahc010",
        lite_version=False,
        num_workers=args.workers,
    )
    print("Session started. Running cases...\n")

    scores = []
    start_time = time.time()

    print(f"[{time.strftime('%H:%M:%S')}] Submitting to public eval (this may take a while)...")
    t0 = time.time()
    result = session.public_eval(solution_code, code_language="python")
    t1 = time.time()

    print(f"[{time.strftime('%H:%M:%S')}] Done in {t1-t0:.1f}s\n")

    for i, case in enumerate(result.case_results):
        score = case.absolute_score
        scores.append(score)
        status = "✓" if score > 0 else "✗"
        judge = case.judge_result.value if hasattr(case.judge_result, 'value') else str(case.judge_result)
        print(f"  {status} case[{i:2d}/{total_cases}]: {score:>10,}  [{judge}]")

    elapsed = time.time() - start_time
    nonzero = sum(1 for s in scores if s > 0)

    print(f"\n{'='*50}")
    print(f"Overall score  : {result.overall_absolute_score:,}")
    print(f"Non-zero cases : {nonzero}/{len(scores)}")
    if scores:
        print(f"Max score      : {max(scores):,}")
        print(f"Min score      : {min(scores):,}")
        print(f"Avg score      : {sum(scores)/len(scores):,.1f}")
    print(f"Total time     : {elapsed:.1f}s")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
