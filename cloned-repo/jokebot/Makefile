ondahelp:
	@echo "make"
	@echo "    clean"
	@echo "        Remove Python/build artifacts."
	@echo "    formatter"
	@echo "        Apply black formatting to code."
	@echo "    lint"
	@echo "        Lint code with flake8, and check if black formatter should be applied."
	@echo "    types"
	@echo "        Check for type errors using pytype."
	@echo "    validate"
	@echo "        Runs the rasa data validate to verify data."
	@echo "    test"
	@echo "        Runs the rasa test suite checking for issues."
	@echo "    crossval"
	@echo "        Runs the rasa cross validation tests and creates results.md"
	@echo "    shell"
	@echo "        Runs the rasa train and rasa shell for testing"


clean:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f  {} +
	rm -rf build/
	rm -rf .pytype/
	rm -rf dist/
	rm -rf docs/_build

formatter:
	black actions --line-length 88

lint:
	flake8 actions
	black --check actions

types:
	pytype --keep-going actions

validate:
	rasa train --domain data
	rasa data validate --debug

test:
	rasa train --domain data
	rasa test --fail-on-prediction-errors

push-model:
	echo new model: `find models -type f | sort -n | tail -1`
	mc cp `find models -type f | sort -n | tail -1` server/rasa-models/jokebot.tar.gz

logs:
	# make logs arg=rasa-d988fbb8b-ggkp5
	kubectl logs -n gstephens "$(arg)" > .vscode/risbot.log
	python tests/rasalog.py .vscode/risbot.log > .vscode/summary.md

crossval:
	rasa test nlu -f 5 --cross-validation
	python format_results.py

shell:
	rasa train --domain data
	rasa shell --debug

train:
	time rasa train --domain data

tensorboard:
	time rasa train --domain data --config config_tensorboard.yml
