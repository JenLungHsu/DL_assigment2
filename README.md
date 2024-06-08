# DL_assigment2

Firstpart為第一題，動態卷積的實現在dynamic_conv.py中，模型實現在vgg.py中，訓練時分別訓練vgg.py中的dy_vgg()和raw_vgg()。測試時也是使用這兩個模型，參數diff_channel中可以調整要輸入的通道數為RGB,RG,GB,R,G,B中任一值，以達成此次任務。

Secondpart為第二題，自定義模型為mymodel.py中的AdvancedTwoLayerCNN()，訓練結果與ResNet34做比較，
