.PHONY: run run-rule run-llm run-lc run-react run-script run-script-approve demo demo-rule demo-llm docker-build docker-run clean

run:
	python3 -m src.main

run-rule:
	python3 -m src.main --rule

run-llm:
	python3 -m src.main --llm

run-lc:
	python3 -m src.main --lc

run-react:
	python3 -m src.main --react

run-script:
	python3 -m src.main --script

demo:
	python3 -m src.main --demo

demo-rule:
	python3 -m src.main --demo --rule

demo-llm:
	python3 -m src.main --demo --llm

docker-build:
	docker build -t opspilot-ai .

docker-run:
	docker run -it --rm -v $(PWD):/app opspilot-ai

run-script-approve:
	python3 -m src.main --script --script-approve

clean:
	rm -rf ops_reports/*.txt
	rm -rf script_audits/*.log
	rm -rf ops_audit_logs/*.log
	rm -rf vector_store
	rm -rf generated_scripts/*.sh
	rm -f data/opspilot_history.log
	rm -f opspilot_memory.db

run-lc-agent:
	python3 main.py --lc-agent