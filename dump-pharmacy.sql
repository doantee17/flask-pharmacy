-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: crossover.proxy.rlwy.net    Database: railway
-- ------------------------------------------------------
-- Server version	9.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `diseases`
--

DROP TABLE IF EXISTS `diseases`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `diseases` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `symptoms` text,
  `treatment` text,
  `image_url` varchar(255) DEFAULT NULL,
  `category` varchar(255) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `diseases`
--

LOCK TABLES `diseases` WRITE;
/*!40000 ALTER TABLE `diseases` DISABLE KEYS */;
INSERT INTO `diseases` VALUES (37,'Cảm cúm','Cúm (Flu) là một dạng bệnh nhiễm vi rút cấp tính. Bệnh phát triển khi vi rút cúm lây nhiễm và tấn công vào hệ hô hấp đường mũi, cổ họng, các ống phế quản và có thể bao gồm cả phổi. Bệnh phần lớn diễn biến nhẹ và người bệnh có thể tự hồi phục trong khoảng 2-7 ngày. Tuy nhiên ở một số trường hợp đặc biệt như người bị suy giảm miễn dịch, người mắc các bệnh mạn tính,… bệnh có thể trở nên nguy hiểm và gây ra các biến chứng nặng có thể dẫn tới tử vong.','Triệu chứng cúm thường gặp đầu tiên là sốt cao từ 39 đến 41 độ C. Trẻ em nếu mắc bệnh thường sẽ sốt cao hơn so với người lớn. Người bị cúm cũng có thể gặp thêm một hoặc nhiều các dấu hiệu sau: (2)  Cảm thấy ớn lạnh, đổ mồ hôi Ho khan Viêm họng Nghẹt mũi, chảy nước mũi Đau đầu Mệt mỏi, khó thở Nôn mửa, tiêu chảy (thường gặp ở trẻ em hơn người lớn)','Thuốc. Thông thường, người bệnh mắc cúm chỉ cần nghỉ ngơi và uống nhiều nước để điều trị cúm. Nhưng trong một số trường hợp, bác sĩ có thể kê toa một loại thuốc chống vi-rút, chẳng hạn như oseltamivir (Tamiflu) hoặc zanamivir (Relenza). Các thuốc này giúp làm giảm triệu chứng của cúm nhanh hơn và giúp ngăn ngừa các biến chứng nghiêm trọng.; Uống nhiều chất lỏng như nước trái cây và súp ấm để tránh mất nước do sốt.','/static/images/diseases/Benh Cum resize.jpg','respiratory','2025-06-08 23:00:59'),(38,'Cảm lạnh','Cảm lạnh là một bệnh lý phổ biến, thường gặp ở tất cả các đối tượng, đặc biệt là ở trẻ em và người cao tuổi. Đây là một bệnh về đường hô hấp, do bị nhiễm virus đường hô hấp. Tuy mức độ không nặng như cảm cúm nhưng vẫn gây cho người bệnh cảm giác mệt mỏi, thiếu năng lượng cho các sinh hoạt thường ngày.','Bệnh cảm lạnh thông thường sẽ chỉ xuất hiện các triệu chứng nhẹ, bệnh có thể tự khỏi sau 1 tuần xuất hiện triệu chứng. Các triệu chứng có thể khác nhau ở mỗi người bệnh, dưới đây là một số triệu chứng thường gặp nhất có thể kể đến:  Nghẹt mũi, khó thở.  Chảy nhiều nước mũi, nước mắt.  Ho.  Đau họng, viêm họng.  Đau đầu, đau nhức cơ thể.  Hắt hơi.  Sốt nhẹ.  Cảm thấy mệt mỏi trong người.','Cảm lạnh là một bệnh lý không phức tạp, cách điều trị chủ yếu là tập trung vào các triệu chứng của bệnh. Bác sĩ có thể chỉ định cho người bệnh dùng các loại thuốc giảm đau, hạ sốt, thuốc xịt giúp thông mũi, thuốc ho giúp làm giảm bớt các triệu chứng của bệnh.\r\n\r\nNgoài ra, người bệnh cũng có thể áp dụng một số các biện pháp điều trị đơn giản cũng hết sức hiệu quả và đã được áp dụng rất nhiều như vệ sinh mũi, miệng, họng sạch sẽ, uống nhiều nước ấm.','/static/images/diseases/camlanh.jpg','respiratory','2025-06-09 00:12:30'),(39,'Tai biến mạch máu não','Tai biến mạch máu não được xem là yếu tố nguy cơ gây tử vong cao hàng thứ 2 tại Việt Nam và thuộc top 10 thế giới, theo thống kê hàng năm của WHO. Bệnh trở thành mối đe dọa nguy hiểm đối với sức khỏe và tính mạng con người.\r\nTai biến mạch máu não là tình trạng mạch máu não (động mạch, mao mạch hoặc tĩnh mạch) bị tắc nghẽn hoặc vỡ đột ngột mà không do chấn thương sọ não.','Cơ mặt tê cứng, cười méo miệng, nói lắp,Thị lực suy giảm, hoa mắt chóng mặt,','Nguyên tắc chung để điều trị tai biến/đột quỵ chính là cấp cứu sớm và can thiệp chính xác, nhằm hạn chế các biến chứng cũng như giảm tối đa nguy cơ tử vong. Khi thấy người có triệu chứng tai biến nhẹ hay nặng thì cần lập tức gọi xe cấp cứu và hỗ trợ đưa người bệnh đến bệnh viện. Ngoài ra, cũng cần lưu ý giữ cho người bệnh không bị té ngã, đặt người bệnh nằm nghiêng để bảo vệ đường thở.; Trước và trong khi đưa người bệnh đi cấp cứu, tuyệt đối không cho người bệnh ăn uống gì và không tự ý điều trị bằng các biện pháp như châm cứu, bấm huyệt, đánh gió,… Cũng không nên cho người bị tai biến uống thuốc huyết áp hoặc các loại thuốc khác mà chỉ theo dõi biểu hiện xem người bệnh có nôn mửa, co giật, méo miệng,… hay không.; Khi đến bệnh viện, các bác sĩ sẽ chẩn đoán người bệnh có bị tai biến mạch máu não hay không. Theo Tổ chức Y tế Thế giới, để xác định tai biến mạch máu não thì cần có 3 tiêu chuẩn lâm sàng sau đây:; Có triệu chứng thần kinh khu trú; Triệu chứng xảy ra đột ngột; Không có chấn thương sọ não','/static/images/diseases/taibien.jpg','cardiovascular','2025-06-09 00:17:14'),(40,'Táo bón','Táo bón xảy ra khi một người đi đại tiện ít hơn 3 lần trong một tuần. Người bị táo bón thường gặp khó khăn khi đi đại tiện, phân có thể cứng hoặc khô. Các triệu chứng khác có thể bao gồm bụng trướng và có tình trạng chảy máu trong quá trình đi hoặc sau khi đi đại tiện.','Đi đại tiện ít hơn 3 lần/1 tuần  Phân cứng và khó đẩy phân ra ngoài  Phân có đường kính lớn có thể gây tắc nghẽn nhà vệ sinh  Đau khi đi đại tiện  Đau bụng  Máu trên bề mặt phân cứng  Nếu trẻ sợ rằng việc đi đại tiện sẽ bị tổn thương và đau thì bé tránh không đi đại tiện. Phụ huynh có thể nhận thấy trẻ bắt chéo chân, siết chặt mông, vặn vẹo cơ thể hoặc mặt tỏ vẻ khó chịu  khi cố gắng giữ phân.','Tùy thuộc vào từng trường hợp cụ thể, bác sĩ có thể lựa chọn các phương pháp điều trị như sau:\r\n\r\nBổ sung thực phẩm chức năng tạo xơ không kê đơn hoặc chất làm mềm phân. Nếu trẻ ăn được nhiều chất xơ trong chế độ ăn, việc bổ sung chất xơ không cần kê đơn là cần thiết như Metamucil hoặc Citrucel. Tuy nhiên, khi sử dụng các thực phẩm chức năng này, trẻ cần uống ít nhất khoảng 1 lít nước mỗi ngày để các sản phẩm này hoạt động hiệu quả nhất. Xin ý kiến của bác sĩ để tìm ra liều lượng phù hợp với tuổi và cân nặng của trẻ.\r\n\r\nThuốc đạn glycerin có thể được sử dụng để làm mềm phân ở trẻ không thể nuốt thuốc dạng viên.\r\n\r\nThuốc nhuận tràng hoặc thuốc xổ. Nếu sự tích tụ của phân tạo ra tắc nghẽn, bác sĩ có thể đề nghị dùng thuốc nhuận tràng hoặc thuốc xổ để giúp loại bỏ tắc nghẽn. Phụ huynh không được phép cho trẻ uống thuốc nhuận tràng hoặc thuốc xổ mà không có sự đồng ý của bác sĩ và được hướng dẫn về liều lượng thích hợp.\r\n\r\nĐến bệnh viện để thụt tháo. Đôi khi có những trường hợp trẻ bị táo bón lâu ngày và ở mức độ nghiêm trọng đến mức cần phải nhập viện, khi đó sẽ được bác sĩ chỉ định cho thụt tháo để làm sạch đường ruột.','/static/images/diseases/taobon.jpg','digestive','2025-06-09 00:23:52'),(41,'Trào ngược dạ dày thực quản','Trào ngược dạ dày thực quản là một loại bệnh tiêu hóa xảy ra khi cơ trong thực quản mở ra và đóng lại không đúng lúc khi bạn nuốt. Khi đó, thức ăn và dịch tiêu hóa chứa axit, sẽ chảy ngược vào thực quản. Cảm giác nóng rát ở ngực và cổ họng thường được mô tả là chứng ợ nóng, một triệu chứng phổ biến của trào ngược axit dạ dày.','Ợ hơi: Thường xuyên xuất hiện, kể cả khi đói hoặc không ăn gì. Ợ nóng: Cảm giác nóng rát từ dạ dày hoặc vùng ngực dưới, lan lên cổ và đôi khi tới hạ họng hoặc mang tai, đi kèm với vị chua trong miệng. Ợ chua: Thức ăn hoặc chất lỏng có vị chua từ dạ dày trào ngược lên cuống họng, thường xảy ra sau khi ăn và trở nên tồi tệ hơn vào ban đêm. Nôn và buồn nôn: Có thể xảy ra khi ăn quá no, nằm xuống ngay sau khi ăn hoặc không nâng đầu cao khi ngủ. Cảm giác nóng trong ngực, cảm giác tức ngực. Nước bọt tiết nhiều, khó nuốt, cảm giác có vật vướng ở họng.','Điều trị ợ nóng và các triệu chứng khác của trào ngược axit dạ dày thường bắt đầu bằng việc sử dụng các loại thuốc không cần kê đơn để kiểm soát axit. Nếu sau vài tuần sử dụng thuốc mà triệu chứng không cải thiện, bác sĩ có thể đề xuất các phương pháp điều trị khác, bao gồm thuốc kê đơn hoặc phẫu thuật.\r\n\r\nĐiều trị ban đầu để kiểm soát ợ nóng bằng các loại thuốc không kê đơn sau đây:\r\n\r\nThuốc trung hòa axit: Giúp giảm triệu chứng nhanh chóng, nhưng không chữa lành được phần thực quản bị viêm do axit dạ dày. Sử dụng quá nhiều có thể gây tác dụng phụ như tiêu chảy hoặc táo bón.\r\nThuốc giảm sản xuất axit: Tác dụng không nhanh như thuốc trung hòa axit, nhưng giúp giảm triệu chứng đáng kể và có thể giảm sự tạo thành axit lên đến 12 giờ.\r\nThuốc ngăn chặn axit và làm lành thực quản: Mạnh hơn các thuốc giảm sản xuất axit, giúp phục hồi tổn thương ở thực quản.','/static/images/diseases/dau-hieu-trao-nguoc-da-day-thuc-quan.jpg','digestive','2025-06-09 00:26:16'),(42,'Tiểu đường','Tiểu đường xảy ra khi tuyến tụy không còn khả năng sản xuất đủ insulin - hormone điều chỉnh lượng đường trong máu hoặc cơ thể sinh ra kháng thể chống lại insulin. ','Đi tiểu thường xuyên,Khát nước nhiều,Cơ thể mệt mỏi, Hay cảm thấy đói bụng,Lâu lành vết thương','Có chế độ ăn nghiêm ngặt\r\nDùng thảo dược tự nhiên\r\nKiểm soát trọng lượng cơ thể','/static/images/diseases/tieu-duong.jpg','endocrine','2025-06-09 00:36:39'),(44,'Thoái hóa đa khớp','Thoái hóa khớp (Osteoarthritis) là tình trạng mãn tính gây tổn thương sụn khớp và mô xương dưới sụn. Bệnh này phổ biến ở người trên 40 tuổi và thường gây đau, cứng khớp, hạn chế vận động','-Đau và cứng khớp: Các khớp bị thoái hóa sẽ có biểu hiện cứng và đau nhức. Khi vận động thì mức độ đau càng tăng lên và khi nghỉ ngơi, cơn đau sẽ giảm dần. Đây chính là một trong những triệu chứng điển hình của bệnh thoái hóa khớp. - Các khớp bị thoái hóa phát ra âm thanh khi người bệnh vận động: Khi các sụn khớp đã bị bào mòn hoàn toàn, các đầu xương có sẽ bị va vào nhau trong quá trình người bệnh di chuyển, vận động và từ đó tạo ra âm thanh lục khục.   - Giảm phạm vi chuyển động: Khi mắc chứng thoái hóa khớp, phạm vi cũng như cường độ hoạt động của khớp sẽ bị giảm đáng kể. Do đó, người bệnh bị suy giảm khả năng vận động và kéo theo chứng teo cơ.   - Gai xương: Khi các sụn khớp bị tổn thương, bào mòn, gai xương có nguy cơ hình thành, gây sưng đau và biến dạng khớp.   - Da bao quanh khớp đỏ và nóng: Tình trạng mô sụn và xương bị tổn thương có thể là yếu tố gây kích thích các mô mềm xung quanh vùng da bao quanh khớp và gây ra hiện tượng đỏ và nóng da.','Một số phương pháp thường được áp dụng trong quá trình điều trị bệnh có thể kể đến như: \r\n\r\n+ Sử dụng thuốc chẳng hạn như thuốc giảm đau, thuốc chống viêm,…\r\n\r\n+ Hướng dẫn người bệnh tập một số bài tập vật lý trị liệu để giảm đau đồng thời cải thiện, phục hồi chức năng khớp. Tuy nhiên, cần kiên trì tập trong thời gian dài. \r\n\r\n+ Duy trì lối sống khoa học, lành mạnh. \r\n\r\n+ Duy trì cân nặng phù hợp. \r\n\r\n+ Tiêm khớp để cải thiện chức năng hoạt động. \r\n\r\n+ Phẫu thuật loại bỏ gai xương, thay thế bằng khớp nhân tạo, phẫu thuật chỉnh hình,…','/static/images/diseases/thoai-hoa-khop-goi-1.jpg','musculoskeletal','2025-06-09 00:42:40'),(45,'Sốt xuất huyết','Sốt cao mất nước chóng mặt, trên người nổi nhiều chấm li ti','sốt cao; mệt mỏi','Mua thuốc dưới hướng dẫn bác sĩ hoặc ra bệnh viện gần nhất để theo dõi','/static/images/diseases/soi.webp','other','2025-06-09 09:17:12');
/*!40000 ALTER TABLE `diseases` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_items`
--

DROP TABLE IF EXISTS `order_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_items`
--

LOCK TABLES `order_items` WRITE;
/*!40000 ALTER TABLE `order_items` DISABLE KEYS */;
INSERT INTO `order_items` VALUES (1,83,104,1,165000.00),(2,83,107,2,195000.00),(3,83,108,3,360000.00),(4,83,109,4,460000.00),(5,83,110,5,245000.00),(6,83,111,6,180000.00),(7,84,93,2,1090000.00),(8,84,96,1,442000.00),(9,85,92,1,795000.00),(10,86,99,5,250000.00),(11,86,100,4,32000.00),(12,86,101,3,89000.00),(13,86,106,2,600000.00),(14,86,112,1,150000.00),(15,87,90,5,50000.00),(16,87,91,5,130000.00),(17,87,94,5,220000.00),(18,87,113,5,40000.00),(19,87,114,5,75000.00),(20,87,116,5,330000.00),(21,88,112,1,150000.00);
/*!40000 ALTER TABLE `order_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` varchar(50) DEFAULT 'pending',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `admin_notes` text,
  `city` varchar(100) DEFAULT NULL,
  `district` varchar(100) DEFAULT NULL,
  `full_name` varchar(255) DEFAULT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `address` text,
  `payment_method` varchar(50) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=89 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (83,14,NULL,5780000.00,'shipped','2025-06-14 12:47:45','done\n','','','ĐỖ ĐỨC QUÂN','0123456789','doquankhyk35b@gmail.com','pho nguyen xa, phuong minh khai','cod',''),(84,14,NULL,2622000.00,'shipped','2025-06-14 14:52:20',NULL,'','','ĐỖ ĐỨC QUÂN','0123456789','doquankhyk35b@gmail.com','yen khanh ninh binh','bank_transfer',''),(85,14,NULL,795000.00,'cancelled','2025-06-14 19:48:14',NULL,'','','quan','0123456789','ducquan@gmail.com','yen khanh ninh binh','credit_card',''),(86,14,NULL,2995000.00,'shipped','2025-06-14 19:49:23',NULL,'','','quan','0123456789','ducquan@gmail.com','yen khanh ninh binh','momo',''),(87,14,NULL,4225000.00,'shipped','2025-06-14 20:15:29',NULL,'','','ĐỖ ĐỨC QUÂN','0123456789','doquankhyk35b@gmail.com','yen khanh ninh binh','momo',''),(88,14,NULL,150000.00,'shipped','2025-06-14 20:17:30',NULL,'','','ĐỖ ĐỨC QUÂN','0123456789','doquankhyk35b@gmail.com','yen khanh ninh binh','credit_card','');
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `products` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text,
  `image_url` varchar(255) DEFAULT NULL,
  `stock_quantity` int DEFAULT '0',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=117 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES (82,'Vitamin E','thuc_pham_cn',150000.00,'Bổ sung vitamin E','/static/images/products/vitamin_e.jpg',20,'2025-06-07 08:37:10'),(86,'Viên sủi Kudos Bone','thuc_pham_cn',107000.00,'Bổ sung canxi, vitamin K2, vitamin D3 cho cơ thể','/static/images/products/vien_sui.jpg',50,'2025-06-08 12:40:41'),(89,'Viên uống Immuvita Easylife','thuc_pham_cn',312000.00,'Bổ sung vitamin và khoáng chất cho cơ thể, tăng sức khỏe','/static/images/products/muvita.webp',20,'2025-06-08 12:45:34'),(90,'Viên nén Paracetamol Stada 500mg','thuoc',50000.00,'Điều trị các cơn đau đầu, đau thần kinh, đau răng','/static/images/products/paracetamon.webp',20,'2025-06-08 12:47:47'),(91,'Thuốc Glotadol 650 Abbott','thuoc',130000.00,'Hỗ trợ hạ sốt và giảm đau','/static/images/products/glotadol.webp',20,'2025-06-08 12:48:58'),(92,'THỰC PHẨM BẢO VỆ SỨC KHỎE WELSON FOR MEN','thuc_pham_cn',795000.00,'Hỗ trợ tiết testosterone, tăng cường khả năng sinh lý ở nam giới.','/static/images/products/welson.webp',20,'2025-06-08 12:51:24'),(93,'Sữa bột dinh dưỡng PEDIASURE hương vani','thuc_pham_cn',1090000.00,'Bổ sung dinh dưỡng cho bé từ 1-10 tuổi (1.6Kg)','/static/images/products/pediasure.jpg',20,'2025-06-08 12:54:10'),(94,'Viên ngậm ho Bảo Thanh','thuoc',220000.00,'Trừ ho, hoá đờm','/static/images/products/baothanh.webp',20,'2025-06-08 12:55:53'),(95,'Viên uống Bình Vị Thái Minh','thuoc',595000.00,'hỗ trợ giảm acid dịch vị, giúp bảo vệ niêm mạc dạ dày','/static/images/products/thaiminh.webp',20,'2025-06-08 12:58:29'),(96,'Thực phẩm bảo vệ sức khỏe Neubria® Neubiotic Her','thuc_pham_cn',442000.00,'Bổ sung lợi khuẩn hỗ trợ sức khỏe nữ giới','/static/images/products/neu.jpg',21,'2025-06-08 13:00:19'),(99,'Đầu kim tiêm tiểu đường PIC Insupen Original','dung_cu_yt',250000.00,'Đầu kim tiểu đường Insupen được trang bị kim Pic, là kết quả của “trải nghiệm indolor®” (công nghệ không đau). Đường kính ngoài giảm, thành mỏng hơn và xử lý bôi trơn cho phép đầu kim tiểu đường Insupen thực hiện thao tác tiêm thoải mái, giảm đau.','/static/images/products/kim.webp',50,'2025-06-08 13:12:33'),(100,'Túi chườm nóng y tế VGlove','dung_cu_yt',32000.00,'Túi chườm nóng VGlove là sản phẩm giúp chườm nóng lên các vùng đau trên cơ thể như đau lưng, đau cơ, đau vai, đau dây thần kinh, đau bụng... Ngoài ra, bạn có thể sử dụng sản phẩm để chườm lạnh giảm sốt cho cả trẻ em và người lớn hoặc chườm nóng để sưởi ấm trong mùa đông.','/static/images/products/tui.webp',50,'2025-06-08 13:13:28'),(101,'Găng tay cao su y tế có bột phủ Latex Powder Disposable Best Gloves','dung_cu_yt',89000.00,'Găng tay cao su y tế có bột phủ Latex Powder Disposable Best Gloves size M được sản xuất từ cao su tự nhiên, có độ dai và bền. Sản phẩm phù hợp cho việc thăm khám trực tiếp.','/static/images/products/gang.jpg',100,'2025-06-08 13:14:26'),(102,'Máy xông khí dung Omron NE-C106','dung_cu_yt',830000.00,'Máy xông khí dung Omron NE-C106 được trang bị với trọn bộ phụ kiện đi kèm: Ống ngậm, mặt nạ trẻ em và người lớn. Sản phẩm được thiết kế nhỏ gọn, chất liệu cao cấp, dễ dàng vận hành và sử dụng, NE-C106 đang dần trở thành giải pháp tối ưu trong quá trình phòng và điều trị bệnh liên quan đến đường hô hấp.','/static/images/products/may_xong.webp',10,'2025-06-08 13:15:51'),(104,'Sữa rửa mặt On: The Body Rice Therapy Heartleaf Acne Cleanser','duoc_my_pham',165000.00,'Làm sạch sâu không gây khô da','/static/images/products/sua_rua_mat.webp',20,'2025-06-08 13:24:02'),(106,'Máy đo huyết áp','dung_cu_yt',600000.00,'Với thiết kế nhỏ gọn, tiện lợi khi mang theo mà lại dễ dàng sử dụng','/static/images/products/omron.webp',20,'2025-06-08 14:20:09'),(107,'Kem chống nắng kiểm soát nhờn cho da mụn Decumar Advanced 50g','duoc_my_pham',195000.00,'CHỐNG NẮNG MỎNG NHẸ – DA MỤN DÙNG LẸ','/static/images/products/kemcndecumar.png',50,'2025-06-08 14:43:26'),(108,'Kem Trị Mụn Mờ Thâm Trà Nghệ GUO Pro Acne Cream','duoc_my_pham',360000.00,'Kem dưỡng ẩm cho da mụn trà nghệ GUO – GUO Pro Acne Cream chứa thành phần tinh dầu tràm trà nano và chiết xuất nghệ vốn nổi tiếng với công dụng kháng khuẩn, giảm viêm, cải thiện mụn lẫn sẹo thâm sau mụn.','/static/images/products/Kem-tra-nghe-GUO-2024-1024x1024.png',50,'2025-06-08 14:51:55'),(109,'Nước tẩy trang dành cho da nhạy cảm Bioderma Sensibio H20 500ml','duoc_my_pham',460000.00,'Nước tẩy trang Bioderma Sensibio H2O là dung dịch làm sạch và tẩy trang dạng hạt mixen (micelle) dành cho vùng mặt và mắt, dành cho da nhạy cảm.','/static/images/products/taytrangbioderma.webp',30,'2025-06-08 14:53:39'),(110,'Tẩy da chết body Đu Đủ Mela','duoc_my_pham',245000.00,'Skincare giúp loại bỏ tế bào chết và góp phần ngăn ngừa mụn 250g ML52','/static/images/products/taydachetmela.webp',40,'2025-06-08 15:06:11'),(111,'Sữa rửa mặt Nghệ - Nhân Sâm Mela','duoc_my_pham',180000.00,'Skincare giúp sáng da và góp phần ngăn ngừa mụn 200ml ML08','/static/images/products/suaruamatnghenhansam.webp',60,'2025-06-08 15:07:17'),(112,'Đai Thắt Lưng Cao Cấp Olumba','dung_cu_yt',150000.00,'Đai thắt lưng cao cấp Olumba size XXL với hệ thống thanh nẹp hợp kim nhôm định hình được sắp xếp khoa học theo chiều dọc, phần thân được may bằng vải chun đặc biệt có độ bền và đàn hồi cao làm cho sản phẩm nhẹ, thoáng khí, đẹp, tạo ra cảm giác yên tâm và thoải mái cho người sử dụng.','/static/images/products/dai.jpg',20,'2025-06-08 15:27:46'),(113,'Thuốc Cetirizin 10mg Trường Thọ trị ngứa ngoài da do dị ứng (10 vỉ x 10 viên)','thuoc',40000.00,'Thuốc Cetirizin 10mg Trường Thọ được sản xuất bởi Công ty Cổ phần Dược phẩm Trường Thọ, có thành phần chính là Cetirizin, được chỉ định để điều trị triệu chứng viêm mũi dị ứng theo mùa hoặc không theo mùa, các bệnh ngứa ngoài da do dị ứng, nổi mề đay mãn tính, bệnh viêm kết mạc dị ứng.','/static/images/products/00033571_cetirizin_10mg_truong_tho_10x10_7980_622e_large_7b5a214e24.webp',100,'2025-06-08 15:41:45'),(114,'Kem Nizoral Jassen 20mg/g điều trị nhiễm nấm ngoài da (15g)','thuoc',75000.00,'Kem Nizoral chứa tác nhân kháng nấm tổng hợp phổ rộng Ketoconazole điều trị các nhiễm nấm ngoài da: Nhiễm nấm ở thân (lác, hắc lào), nhiễm nấm ở bẹn, nhiễm nấm ở bàn tay và bàn chân do Trichophyton rubrum, Trichophyton mentagrophytes, Microsporum canis và Epidermophyton floccosum, điều trị nhiễm nấm Candida ở da và điều trị bệnh lang ben.','/static/images/products/kemnizoral.webp',40,'2025-06-08 15:42:37'),(115,'Thực phẩm bảo vệ sức khỏe OMEGA 3 PLUS Kenko','thuc_pham_cn',920000.00,'hỗ trợ não bộ, thị lực và sức khoẻ tim mạch','/static/images/products/omega_3.jpg',10,'2025-06-09 10:19:09'),(116,'Thuốc Bonlutin Catalent','thuoc',330000.00,'giảm triệu chứng của thoái hóa khớp gối nhẹ và trung bình','images/products/boluntin.webp',10,'2025-06-09 10:29:49');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `role` varchar(20) DEFAULT 'user',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'jack5tr','admin@pharmacy.com','$2b$12$DP26B7Q.qKxZNIaJGDSH1e5D69MoD/6h/4IGpEVqn/zG1JrPwgzl2','2025-05-31 16:31:05','admin'),(14,'DUC QUAN 2','ducquan@gmail.com','$2b$12$69nY7g9w.7fLNQUYDordhufiHuj4sKkduF5mYp3VZKG7X3vK0sLEq','2025-06-08 14:34:07','user'),(25,'admi1','doantienhd177@gmail.com','$2b$12$MMyHNvUQXUBZabYptb2EGOslldHNRfynpJuiO/Y/pW45.SxuMyxYq','2025-06-15 10:19:57','user');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-15 17:38:46
