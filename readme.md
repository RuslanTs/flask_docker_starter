sudo docker exec -it flaskhello_flask_1 bash

# train and save a model
sudo docker exec -it flaskhello_flask_1 python train_model.py

curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"flower":"1,2,3,7"}' \
  http://localhost:5000/iris_post