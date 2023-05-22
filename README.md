# Zhihugetpages
# 知乎文章爬取
使用selenium爬取（对抗知乎反爬机制）

依赖chrome


pickle持久化存储已爬取信息


将对知乎推荐的公开收藏夹进行爬取，计算权重（赞数以及评论数[知乎回答可靠性鉴定指南](https://zhuanlan.zhihu.com/p/374034735)）。
![image](https://user-images.githubusercontent.com/73327649/200157741-f620e535-b6be-494b-88a2-72e81f057b96.png)


一次爬取四个收藏夹，筛选并保存高权重的作品（自定义）


可以手动关闭浏览器窗口，点击其他栏目跳出爬取页面等方法结束应用。
