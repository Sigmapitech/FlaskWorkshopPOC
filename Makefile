APP = app

VENV = venv
VBIN = $(VENV)/bin

all: $(VBIN)/$(APP)

$(VBIN)/activate:
	python3 -m venv $(VENV)

$(VBIN)/$(APP): $(VENV)
	$(VBIN)/pip install -e .

$(VENV): $(VBIN)/activate
	chmod +x $(VBIN)/activate
	./$(VBIN)/activate

clean:
	find . | grep -E "(__pycache__|.pyc|.pyo)" | xargs rm -rf

fclean: clean
	rm -rf $(VENV)

re: fclean all

.PHONY: clean fclean re
