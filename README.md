![image](https://github.com/CJY1018/online-registration-and-score-inquiry-system/assets/90013748/83c1f445-9f1d-4a71-91d0-407ca18876fb)

## 设计说明与心路历程

本次课程设计由我和队友**独立**完成，完全没有在其他网站搬运代码，整体开发时长约25天，实际总代码量6000余行，全部为自己手敲。

时间安排上，前5天我们学习了FastAPI框架，这是一个基于Python的后端开发框架。我个人先前学过Java的后端框架SSM（Spring、Spring MVC 、和Mybatis），本次课程设计后端使用Python语言特别是FastAPI开发主要出于以下原因：

1. 今后我保研想选择人工智能方向，使用Python语言。目前国外人工智能应用（AIGC：文字、图像、音频生成等）非常多地使用到了FastAPI这个框架。目前国内相关应用还不是太多，主要是大厂开始在尝试应用，相信随着人工智能的发展FastAPI也会逐渐被国内人工智能公司所广泛应用。
2. 在Github上，诞生于2018年的FastAPI的Star（71.1k）已经超过了传统的Python后端框架Flask(66.4k),直逼传统框架django（76.8k），多次登上Trending周榜。
3. 正如其名，FastAPI速度较快，技术上对标Java的Spring Boot，且学习成本较低，还支持自动生成规范的接口说明文档，比较适合本项目的快速敏捷开发。

 

此外，由于前端框架Vue.js我在大二时自学学过，且大一学过Java的后端框架SSM。项目起初时放弃Java选择Python的FastAPI框架时我的心情还是很恐慌的，怕在规定时间内完不成学习和开发，但在学习的过程中，我发现很多原理都是相通的，有一定基础，所以自学不用花费太多时间。我预计在规定时间能完成项目开发，故打算自己从零开始，独立完成。

 

## 设计感想

通过参与本次《计算机网络课程设计》，我深刻体会到了计算机网络知识与实际应用之间的紧密联系。在设计和实现网上报名及查分系统的过程中，我不仅巩固了对HTTP/HTTPS协议、RESTful API设计、身份验证与授权等计算机网络基础知识的理解，还提升了我在系统分析、设计、开发和测试等方面的实践能力。

在项目开发过程中，我负责了注册登录模块、报名模块、支付模块、查分模块以及管理员操作面板等关键功能的开发。这些模块的设计和实现让我深入理解了前后端分离架构的优势，以及如何使用Vue3、FastAPI等现代技术栈来构建高效、安全且用户友好的Web应用程序。

安全性设计是本次课程设计中的一个重点，我学习了如何使用JWT进行安全的用户身份认证和权限管理，并通过SHA-256哈希加盐技术来存储用户密码，增强了系统的安全性。此外，通过抓包分析“掌上高考”网站，我掌握了如何合法合规地获取和使用第三方数据，解决了高校信息获取的问题，这一过程锻炼了我的网络分析和数据处理能力。

在实现支付功能时，我了解了公网环境下安全支付的重要性，并基于爱发电API实现了支付功能，这一过程让我认识到了PCI-DSS等支付行业安全标准的必要性。

团队合作是项目成功的关键。在项目中，我与队友们进行了明确的分工，定期进行交流和讨论，确保每个模块都能按时完成并顺利集成。我们通过Git进行版本控制，有效管理了代码变更和团队协作。

时间管理上，我通过制定详细的开发计划，并严格遵循既定的时间节点，确保了项目能够按期交付。在这个过程中，我学会了如何平衡学习和项目开发，提高了自我管理的能力。

非常感谢学校和老师们能提供这次课程设计的平台和机会！这次课设不仅增强了我的技术能力，还提高了我的团队协作和问题解决能力。我深刻体会到了不断学习和实践的重要性，以及在实际项目中运用所学知识解决问题的成就感。
