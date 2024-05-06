

testfiles := $(shell find example/ -name '*.blang' -type f)

test: $(testfiles)
	@for file in $(testfiles); do \
		echo "\033[1;32mTesting $$file\033[0m"; \
		./blang.py $$file; \
	done