FROM ubuntu:latest

RUN apt update
RUN apt install -y git python-is-python3 graphviz libgraphviz-dev pkg-config pip
RUN apt install -y texlive-latex-base

RUN pip install pygraphviz~=1.10
RUN pip install -i https://test.pypi.org/simple/ figureast==0.0.1

RUN git clone https://github.com/Anvarka/Python_advance.git
RUN cd Python_advance/hw_2/ && git checkout hw_2

WORKDIR /root/Python_advance/hw_2
COPY . .
RUN python latex_generator.py
RUN pdflatex -output-directory artifacts artifacts/latex.tex