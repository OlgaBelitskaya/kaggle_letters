# -*- coding: utf-8 -*-
"""grayscaled-handwritten-letters-r.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iuO75CenXoGJja8p7watQ8VTjoo2T6Au

<h1 class='font-effect-3d-float' style='font-family:Akronim; color:#FF9966; font-size:250%;'>Styling, Links, Helpful Functions, & Code Modules</h1>
#### [Github Repository](https://github.com/OlgaBelitskaya/deep_learning_projects/tree/master/DL_PP2) & [Full Version. Python](https://olgabelitskaya.github.io/kaggle_letters.html) & [Full Version. R](https://olgabelitskaya.github.io/kaggle_letters_R.html)
"""

library(IRdisplay); library(repr)
library(tensorflow); library(keras)
library(imager); library(R6)
keras_backend<-backend()

display_html("<style> 
@import url('https://fonts.googleapis.com/css?family=Akronim|Roboto&effect=3d-float');
body {background-color:#AAF0D1;} 
a,h4 {color:#FF9966; font-family:Roboto;}
span {color:black; text-shadow:4px 4px 4px #aaa;}
div.output_prompt {color:#FF9966;} 
div.input_prompt {color:#66FF66;} 
div.output_area pre,div.output_subarea {font-size:15px; color:#FF9966;}
div.output_stderr pre {background-color:#AAF0D1;}
</style>")

fw<-"best_letters.h5"
gray_image_loading<-function(image_path) {
    image<-keras::image_load(image_path,
                             target_size=c(32,32),
                             grayscale=T)
    image<-image_to_array(image)/255
    image<-array_reshape(image,c(1,dim(image)))
    return(image) }

"""<h1 class='font-effect-3d-float' style='font-family:Akronim; color:#FF9966; font-size:250%;'> Data Loading and Exploring </h1>"""

letters1<-read.csv("../input/letters.csv")
letters2<-read.csv("../input/letters2.csv")
letters3<-read.csv("../input/letters3.csv")
image_paths1<-list.files("../input/letters",recursive=TRUE,full.names=TRUE)
image_paths1<-image_paths1[1:(length(image_paths1))]
image_paths2<-list.files("../input/letters2",recursive=TRUE,full.names=TRUE)
image_paths2<-image_paths2[1:(length(image_paths2))]
image_paths3<-list.files("../input/letters3",recursive=TRUE,full.names=TRUE)
image_paths3<-image_paths3[1:(length(image_paths3))]
letter_labels1<-as.matrix(letters1["label"])
letter_labels2<-as.matrix(letters2["label"])
letter_labels3<-as.matrix(letters3["label"])
cletter_labels1<-keras::to_categorical(letter_labels1-1,33)
cletter_labels2<-keras::to_categorical(letter_labels2-1,33)
cletter_labels3<-keras::to_categorical(letter_labels3-1,33)
letter_images1<-lapply(image_paths1,gray_image_loading)
letter_images2<-lapply(image_paths2,gray_image_loading)
letter_images3<-lapply(image_paths3,gray_image_loading)
letter_images1<-array_reshape(letter_images1,c(-1,32*32))
letter_images2<-array_reshape(letter_images2,c(-1,32*32))
letter_images3<-array_reshape(letter_images3,c(-1,32*32))

head(letters3,3); head(image_paths3,3);
c(dim(letter_images1),dim(letter_labels1),dim(cletter_labels1),
  dim(letter_images2),dim(letter_labels2),dim(cletter_labels2),
  dim(letter_images3),dim(letter_labels3),dim(cletter_labels3))

letter_images<-rbind(letter_images1,letter_images2)
letter_images<-rbind(letter_images,letter_images3)
letter_labels<-rbind(letter_labels1,letter_labels2)
letter_labels<-rbind(letter_labels,letter_labels3)
cletter_labels<-rbind(cletter_labels1,cletter_labels2)
cletter_labels<-rbind(cletter_labels,cletter_labels3)
c(dim(letter_images),dim(cletter_labels))
df<-data.frame(letter_images,cletter_labels)
df<-df[sample(nrow(df)),]; dim(df)

options(repr.plot.width=6,repr.plot.height=3)
par(mar=c(2,2,2,2))
letter_labels %>% 
    table() %>% barplot(col=rainbow(33,start=.1,end=.45))

im<-load.image("../input/letters/01_05.png")
options(repr.plot.width=3,repr.plot.height=3)
par(mar=c(2,2,2,2))
dim(im); plot(im)

options(repr.plot.width=3,repr.plot.height=3)
par(mar=c(1,1,1,1))
image_example<-df[100,1:1024]
image_example<-array_reshape(as.matrix(df[100,1:1024]),c(32,32))
c(dim(image_example),which(df[100,1025:1057]==1))
plot(as.raster(image_example))

train_indices<-1:round(0.8*nrow(df))
valid_indices<-(round(0.8*nrow(df))+1):round(0.9*nrow(df))
test_indices<-(round(0.9*nrow(df))+1):nrow(df)
x_train<-as.matrix(df[train_indices,1:1024])
y_train<-as.matrix(df[train_indices,1025:1057])
x_valid<-as.matrix(df[valid_indices,1:1024])
y_valid<-as.matrix(df[valid_indices,1025:1057])
x_test<-as.matrix(df[test_indices,1:1024])
y_test<-as.matrix(df[test_indices,1025:1057])
c(dim(x_train),dim(x_valid),dim(x_test),
  dim(y_train),dim(y_valid),dim(y_test))

"""<h1 class='font-effect-3d-float' style='font-family:Akronim; color:#FF9966; font-size:250%;'> One-Label Classification Models</h1>"""

gray_cnn_model<-keras_model_sequential()
gray_cnn_model %>%  
layer_conv_2d(filter=32,kernel_size=c(5,5),padding="same",
              input_shape=c(32,32,1) ) %>%  
layer_activation_leaky_relu(alpha=.02) %>%  
layer_max_pooling_2d(pool_size=c(2,2)) %>%  
layer_dropout(.2) %>%
layer_conv_2d(filter=256,kernel_size=c(5,5)) %>% 
layer_activation_leaky_relu(alpha=.02) %>%  
layer_max_pooling_2d(pool_size=c(2,2)) %>%  
layer_dropout(.2) %>%
layer_global_max_pooling_2d() %>%  
layer_dense(1024) %>%  
layer_activation_leaky_relu(alpha=.02) %>%  
layer_dropout(.5) %>%  
layer_dense(33) %>%    
layer_activation("softmax")
gray_cnn_model %>%
  compile(loss="categorical_crossentropy",
          optimizer="rmsprop",metrics="accuracy")

d<-c(-1,32,32,1)
cb<-list(callback_model_checkpoint(fw,save_best_only=T),
         callback_reduce_lr_on_plateau(monitor="val_loss",
                                       factor=.8))
gray_cnn_fit<-gray_cnn_model %>%
    fit(x=array_reshape(x_train,d),y=y_train,
        validation_data=list(array_reshape(x_valid,d),y_valid),
        shuffle=T,batch_size=64,epochs=100,callbacks=cb)

options(warn=-1,repr.plot.width=7,repr.plot.height=7)
plot(gray_cnn_fit)

gray_cnn_fit_df<-as.data.frame(gray_cnn_fit)
gray_cnn_fit_df[201:250,1:4]

load_model_weights_hdf5(gray_cnn_model,fw)
gray_cnn_model %>% 
    evaluate(array_reshape(x_test,d),y_test)

gray_mlp_model<-keras_model_sequential()
gray_mlp_model %>%  
layer_dense(128,input_shape=c(32*32)) %>%  
layer_activation("relu") %>%  
layer_batch_normalization() %>%  
layer_dense(256) %>%  
layer_activation("relu") %>%  
layer_batch_normalization() %>%
layer_dense(512) %>%  
layer_activation("relu") %>%  
layer_batch_normalization() %>%
layer_dense(1024) %>%  
layer_activation("relu") %>%  
layer_dropout(.25) %>% 
layer_dense(33) %>%    
layer_activation("softmax")
gray_mlp_model %>%
    compile(loss="categorical_crossentropy",
            optimizer="nadam",metrics="accuracy")

cb<-list(callback_model_checkpoint(fw,save_best_only=T),
         callback_reduce_lr_on_plateau(monitor="val_loss",
                                       factor=.8))
gray_mlp_fit<-gray_mlp_model %>%
    fit(x=x_train,y=y_train,callbacks=cb,
        validation_data=list(x_valid,y_valid),
        shuffle=T,batch_size=128,epochs=300)

options(warn=-1,repr.plot.width=7,repr.plot.height=7)
plot(gray_mlp_fit)

load_model_weights_hdf5(gray_mlp_model,fw)
gray_mlp_model %>% 
    evaluate(x_test,y_test)