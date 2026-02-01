import pathlib
import pytest
import dotenv

from google.adk.evaluation.agent_evaluator import AgentEvaluator

dotenv.load_dotenv()


@pytest.mark.asyncio
async def test_interview_simulator():
    print("Starting evaluation of Interview Simulator agent...")

    agent_module = "Interview_simulator.agent"

    eval_set_file = pathlib.Path(__file__).parent / "data" / "interview_simulator.test.json"
    assert eval_set_file.exists(), f"Eval set file not found: {eval_set_file}"

    await AgentEvaluator.evaluate(
        agent_module=agent_module,
        eval_dataset_file_path_or_dir=str(eval_set_file),
        num_runs=3,
        print_detailed_results=True
    )

    print("Evaluation finished. Check terminal output for scores and details.")




















