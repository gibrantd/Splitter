FROM python:3
WORKDIR /PROSA/Lab/
COPY  *.py /PROSA/Lab/
#COPY  *.sh /PROSA/Lab/
#VOLUME /Users/interware/Documents/IW/PROSA/Match-Interredes/Lab 
RUN pip install pika==0.13.1 
#RUN pip install pymongo==3.7.2
#RUN chmod a+X diff-command.sh
#RUN chmod 777 diff-command.sh
#COPY . .
CMD [ "python", "/PROSA/Lab/splitter_multiprocessing.py"]
