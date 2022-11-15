.PHONY: all
all:
	virtualenv-3 ./venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python ./generate.py


.PHONY: clean
clean:
	find docs/modules -type f -exec rm -f {} +
	rm -rf docs/modules.md

.PHONY: update
update:all
	git add --all .
	git commit -m "up"
	git push
