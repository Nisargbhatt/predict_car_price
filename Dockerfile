FROM python:3.7.5
COPY . /temp
WORKDIR /temp/Price_Prediction_car

RUN pip install -r requirements.txt
# EXPOSE 5000
# ENV FLASK_APP=app.py

# ENTRYPOINT [ "python" ] 
# i get ip address of the docker's localhost by "docker exec -it 106c380dff2f ip addr"
#and run it by combining with the port and ip with your browser.
CMD [ "python","./app.py"]
# CMD ["flask", "run", "--host", "0.0.0.0", "-p", "5000"] 
