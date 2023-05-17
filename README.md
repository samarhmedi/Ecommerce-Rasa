# Ecommerce Rasa
 Rasa chatbot for ecommerce websites. This chatbot is able to check inventory , cancel status , start a return , answer FAQ , take order and take customer feedback. 
# To start the project 
make sure you have docker  correctly installed 
```
pip install -r requirements.txt
```
```
rasa run actions
```
```
docker run -p 8000:8000 rasa/duckling
```
```
rasa train
```
```
rasa shell 
```
