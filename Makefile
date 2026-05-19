.PHONY: run demo docker-build docker-run clean

run:
	python3 src/main.py

demo:
	python3 src/main.py --demo

docker-build:
	docker build -t opspilot-ai .

docker-run:
	docker run -it --rm -v $(PWD):/app opspilot-ai

clean:
	rm -rf data/reports/*.txt
	rm -f data/opspilot_history.log