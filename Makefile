.PHONY: run run-rule run-llm run-react demo demo-rule demo-llm docker-build docker-run clean

run:
	python3 main.py

run-rule:
	python3 main.py --rule

run-llm:
	python3 main.py --llm

run-react:
	python3 main.py --react

demo:
	python3 main.py --demo

demo-rule:
	python3 main.py --demo --rule

demo-llm:
	python3 main.py --demo --llm

docker-build:
	docker build -t opspilot-ai .

docker-run:
	docker run -it --rm -v $(PWD):/app opspilot-ai

clean:
	rm -rf reports/*.txt
	rm -f opspilot_history.log