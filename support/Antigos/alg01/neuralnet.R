library("neuralnet")

train <- read.csv("~/Documents/Recomender/alg01/train.txt", sep=";")
get_rate <- function(pred){
  
  correct_previtions <- 0
  
  for(i in 1:length(pred[,1])){
    
    if (pred[,1][i] == pred[,2][i]){
      correct_previtions <- correct_previtions + 1
    }
  }
  
  return (correct_previtions/(length(pred[,1]))*100)
}

run_nnet <- function(train_file, test_file, results_file, maxiterat,neurons ){
  
  train_ <- read.csv(file=train_file,head=TRUE,sep=";")
  train <- train_[2:7]
  
  test_ <- read.csv(file=test_file,head=TRUE,sep=";")
  test <- test_[2:7]
  
  
  
  length_d <- length(train[,1]) - 1
  length_t <- length(test[,1]) - 1
  
  iTrainData = sample(1:length_d,length_d)
  iValidData = sample(1:length_t,length_t)
  
  
  
  ideal <- class.ind(train$target)
  
  # 5 Train the model, -5 because you want to leave out the class attribute , the dataset had a total of 5 attributes with the last one as the predicted one
  
  moviesNN = nnet(train[iTrainData,-5], ideal[iTrainData,], size=neurons, softmax=TRUE, maxit=maxiterat)
  
  # 6 Predict on testset
  
  #predict(winesANN, winesdata[iValidData,-5], type="class")
  
  # 7 Calculate Classification accuracy
  
  pred <- cbind(predict(moviesNN, test, type="class"),test$target)
  print(get_rate(pred))
  t <- data.frame(test_$name,pred)
  print(t)
  return (pred)
}


result <- run_nnet("~/Documents/Recomender/alg01/train.txt","~/Documents/Recomender/alg01/test.txt","x",4000,20)
print(result)

# form.in <- as.formula('target~ 
#                           GAP_min+
#                           GAP_max+
#                           SPEECH_min+
#                           SPEECH_max+
#                           TotalGap+
#                           TotalSpeech+
#                           AVG_gap+
#                           AVG_speech+
#                           ratio')
# 
# 
# mod2<-neuralnet(form.in,data=train,hidden=10)
# net.results <- compute(mod2, test)
# 
# # test <- tests[2:11]
# # 
# #net.sqrt <- neuralnet(
# #                           ,trains, hidden=10, threshold=0.01)
# # 
# # net.results <- compute(net.sqrt, test)
# # result = data.frame(tests$name,net.results$net.result,tests$target)
# # print(result)
# # print(tests$name)
# # 
# # # trainX = train[,0:8]
# # # trainY = train[,9]
# # # 
# # # net.sqrt <- neuralnet(train$V9~train$V1+
# # #                         train$V2+
# # #                         train$V3+
# # #                         train$V4+
# # #                         train$V5+
# # #                         train$V6+
# # #                         train$V7+
# # #                         train$V8,train, hidden=10, threshold=0.01)
# # # print(net.sqrt)
# # # 
# # # net.results <- compute(net.sqrt, test) #Run them through the neural network
# # # print(net.results$net.result)
