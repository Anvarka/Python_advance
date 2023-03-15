FROM ubuntu:latest as build

RUN apt update
RUN apt install -y git python-is-python3 graphviz libgraphviz-dev pkg-config pip
RUN apt install -y texlive-latex-base

RUN pip install pygraphviz~=1.10
RUN pip install -i https://test.pypi.org/simple/ figureasttree4==0.0.1

RUN git clone https://github.com/Anvarka/Python_advance.git
RUN cd Python_advance/ && git checkout hw_2

WORKDIR /Python_advance/hw_2
RUN python latex_generator.py
RUN pdflatex -output-directory artifacts artifacts/latex.tex

FROM ubuntu:latest
COPY --from=build Python_advance/hw_2 .