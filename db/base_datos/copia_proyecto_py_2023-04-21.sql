# ************************************************************
# Sequel Pro SQL dump
# Versión 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.5.5-10.4.21-MariaDB)
# Base de datos: copia_proyecto_py
# Tiempo de Generación: 2023-04-22 02:49:29 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Volcado de tabla calificacion
# ------------------------------------------------------------

DROP TABLE IF EXISTS `calificacion`;

CREATE TABLE `calificacion` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_solicitud` int(11) unsigned NOT NULL,
  `id_usuario` int(11) unsigned NOT NULL,
  `observaciones` varchar(50) DEFAULT NULL,
  `numero_estrellas` int(11) DEFAULT NULL,
  `registro` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_solicitud` (`id_solicitud`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `calificacion_ibfk_4` FOREIGN KEY (`id_solicitud`) REFERENCES `solicitud` (`id`),
  CONSTRAINT `calificacion_ibfk_5` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `calificacion` WRITE;
/*!40000 ALTER TABLE `calificacion` DISABLE KEYS */;

INSERT INTO `calificacion` (`id`, `id_solicitud`, `id_usuario`, `observaciones`, `numero_estrellas`, `registro`)
VALUES
	(1,3,1,'todo bien',5,'2023-04-04 09:33:15'),
	(3,9,2,'excelente',5,'2023-04-04 10:30:10'),
	(4,9,1,'bien',4,'2023-04-04 11:23:15'),
	(5,15,1,'Buen servicio',4,'2023-04-04 12:00:15'),
	(6,24,2,'muy amable',3,'2023-04-04 12:33:15'),
	(7,37,46,'mal',1,'2023-04-04 13:00:00'),
	(8,26,1,'b',5,'2023-04-04 13:33:15'),
	(9,7,1,'todo muy agradable',4,'2023-04-04 15:13:43'),
	(10,6,1,'regular',3,'2023-04-05 15:19:56'),
	(11,27,2,'muy bien, pero le falto mas',4,'2023-04-05 21:09:01'),
	(12,37,1,'muy amable',4,'2023-04-13 21:27:33'),
	(13,23,2,'bien',3,'2023-04-21 18:30:19'),
	(14,30,20,'',4,'2023-04-21 18:49:51');

/*!40000 ALTER TABLE `calificacion` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla documento
# ------------------------------------------------------------

DROP TABLE IF EXISTS `documento`;

CREATE TABLE `documento` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `tipo_documento` char(4) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `documento` WRITE;
/*!40000 ALTER TABLE `documento` DISABLE KEYS */;

INSERT INTO `documento` (`id`, `tipo_documento`)
VALUES
	(1,'C.C'),
	(2,'C.E');

/*!40000 ALTER TABLE `documento` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla estado
# ------------------------------------------------------------

DROP TABLE IF EXISTS `estado`;

CREATE TABLE `estado` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `estado` WRITE;
/*!40000 ALTER TABLE `estado` DISABLE KEYS */;

INSERT INTO `estado` (`id`, `nombre`)
VALUES
	(1,'Pendiente'),
	(2,'Aceptada'),
	(3,'Cancelada'),
	(4,'Finalizada');

/*!40000 ALTER TABLE `estado` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla ocupacion
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ocupacion`;

CREATE TABLE `ocupacion` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `ocupacion` WRITE;
/*!40000 ALTER TABLE `ocupacion` DISABLE KEYS */;

INSERT INTO `ocupacion` (`id`, `nombre`)
VALUES
	(1,'Albañil'),
	(2,'Plomero'),
	(3,'Electricista'),
	(4,'Carpintero');

/*!40000 ALTER TABLE `ocupacion` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla solicitud
# ------------------------------------------------------------

DROP TABLE IF EXISTS `solicitud`;

CREATE TABLE `solicitud` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario_contratista` int(11) unsigned NOT NULL,
  `id_usuario_cliente` int(11) unsigned NOT NULL,
  `id_ocupacion_solicitud` int(11) unsigned NOT NULL,
  `horario` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `evidencia` varchar(300) DEFAULT NULL,
  `descripcion` varchar(300) DEFAULT NULL,
  `id_estado` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_usuario_cliente` (`id_usuario_cliente`),
  KEY `id_usuario_ocupaciones` (`id_usuario_contratista`),
  KEY `id_estado` (`id_estado`),
  KEY `id_ocupacion` (`id_ocupacion_solicitud`),
  CONSTRAINT `solicitud_ibfk_2` FOREIGN KEY (`id_usuario_cliente`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `solicitud_ibfk_5` FOREIGN KEY (`id_estado`) REFERENCES `estado` (`id`),
  CONSTRAINT `solicitud_ibfk_6` FOREIGN KEY (`id_usuario_contratista`) REFERENCES `usuarios` (`id`),
  CONSTRAINT `solicitud_ibfk_7` FOREIGN KEY (`id_ocupacion_solicitud`) REFERENCES `ocupacion` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `solicitud` WRITE;
/*!40000 ALTER TABLE `solicitud` DISABLE KEYS */;

INSERT INTO `solicitud` (`id`, `id_usuario_contratista`, `id_usuario_cliente`, `id_ocupacion_solicitud`, `horario`, `hora`, `evidencia`, `descripcion`, `id_estado`)
VALUES
	(3,1,15,2,'2023-09-21','00:00:00','68b0b622-b8ba-4d9f-800d-16c63208227c.jpeg','no me prende el televisor',4),
	(6,1,35,1,'2023-04-11','00:00:00','732adf3a-b69d-4c6a-ab68-158c245b9712.png','no me sirve el reloj',4),
	(7,1,30,2,'2023-06-23','00:00:00','64841395-f76f-47a6-b498-b33cdbead52a.jpg','se me apago',4),
	(8,1,15,2,'2023-03-23','00:00:00','d856b906-6b4b-413b-9536-715cdea078e5.jpg','probando 1',4),
	(9,1,2,1,'2023-04-03','00:00:00','d7ba8b5f-1bed-436b-9609-a0ccfbd5d2ec.png','prueba 2',4),
	(15,1,2,1,'2023-03-28','00:00:00','834721f4-a89f-45fb-b0a0-cba762216bc2.png','dd',1),
	(19,20,2,2,'2023-03-23','00:00:00','333d2b04-5c7b-4824-977e-9499f1fabc60.png','a',3),
	(20,21,2,3,'2023-03-29','00:00:00','d20bd077-0c97-460b-953c-7517c0ab1767.png','1',2),
	(21,21,2,3,'2023-03-28','00:00:00','45fe2352-2be1-4d58-aa37-8e057871ccf2.png','no hay luz',3),
	(22,21,2,4,'2023-04-14','09:00:01','168bdf56-1ddf-4b66-b8af-6a3dd1e293a7.png','a',2),
	(23,1,2,1,'2023-03-24','00:00:00','8c541d65-29b5-4e70-b124-c6a180bc5731.png','prueba 2',4),
	(24,20,46,2,'2023-03-27','00:00:00','55c921aa-444a-4abe-9c3e-66feb1a506f1.png','prueba de solicitud plomero ',4),
	(25,1,2,2,'2023-03-30','00:00:00','5b61e802-6991-4625-abe8-2dffe988b85f.png','prueba',4),
	(26,1,2,1,'2023-03-29','00:00:00','d6eb7077-89de-4876-bc8e-6b5c6ac61067.png','prubea 3',4),
	(27,21,2,3,'2023-03-29','00:00:00','1fd1cbfb-9d5c-4e97-a867-af24428a7f1b.jpeg','gh',4),
	(28,1,2,2,'2023-03-29','00:00:00','24aeb07f-42a4-4cf1-9246-a4eb7b1667ee.jpeg','prueba de problemas ',3),
	(29,1,2,2,'2023-03-30','00:00:00','68dba5b6-236d-418e-a4aa-8c50d50e3cf8.png','11',3),
	(30,20,2,2,'2023-03-30','00:00:00','a990e8f8-5c9d-4da0-9ce4-8eba6e993172.jpg','juj',4),
	(31,1,2,2,'2023-03-31','00:00:00','055ce593-e4d2-4a8d-b944-c2566fd660b4.jpg','kkk',3),
	(32,1,2,2,'2023-04-12','00:00:00','8c541d65-29b5-4e70-b124-c6a180bc5731.png','11',3),
	(33,1,2,2,'2023-04-05','07:00:00','8c541d65-29b5-4e70-b124-c6a180bc5731.png','aa',4),
	(34,20,2,2,'2023-03-31','00:00:00','d4832579-b2e8-4d52-ae13-ad5dca7d8aae.png','sdfsdf',3),
	(35,20,46,1,'2023-04-01','00:00:00','e0c7dec6-fd30-4fd2-8735-d60ab6b6b903.png','sss',3),
	(36,20,46,2,'2023-04-08','00:00:00','2d49fdce-f41a-413b-8873-32579b0ed3c0.png','hola',4),
	(37,1,46,2,'2023-04-26','00:00:00','c0ae2b46-9c0a-43a3-b667-f16891bf2ad2.png','un m',4),
	(38,47,2,1,'2023-04-19','20:00:29','','problema abanico',2),
	(39,21,2,3,'2023-04-28','10:00:54','087938d5-7787-4337-92d7-78669f7da7fd.jpg','prueba proyecto',1),
	(40,1,2,2,'2023-04-21','10:00:00','3bfa4dd2-0493-4191-b02e-0167b94ae776.png','prueba',2),
	(41,1,2,2,'2023-04-27','11:00:29','','pruebas',1),
	(42,1,2,2,'2023-04-28','12:00:18','6684b0f8-fee2-45ba-a2a4-0232ecc17800.png','pruebas',1),
	(43,20,51,1,'2023-04-21','20:00:00','b9b5054c-99a1-475b-974c-d7868bf5f89b.png','test',2);

/*!40000 ALTER TABLE `solicitud` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla tipo_usuario
# ------------------------------------------------------------

DROP TABLE IF EXISTS `tipo_usuario`;

CREATE TABLE `tipo_usuario` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `tipo_usuario` WRITE;
/*!40000 ALTER TABLE `tipo_usuario` DISABLE KEYS */;

INSERT INTO `tipo_usuario` (`id`, `nombre`)
VALUES
	(1,'Admin'),
	(2,'Contratista'),
	(3,'Cliente');

/*!40000 ALTER TABLE `tipo_usuario` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla usuario_datos_personales
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usuario_datos_personales`;

CREATE TABLE `usuario_datos_personales` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_documento` int(11) unsigned DEFAULT NULL,
  `nombre_completo` varchar(30) DEFAULT NULL,
  `numero_documento` int(11) NOT NULL,
  `numero_celular` int(30) DEFAULT 0,
  `direccion` varchar(20) DEFAULT 'DEFAULT ''''',
  `descripcion` varchar(60) DEFAULT 'DEFAULT ''''',
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_documento` (`numero_documento`),
  KEY `id_documento` (`id_documento`),
  CONSTRAINT `usuario_datos_personales_ibfk_2` FOREIGN KEY (`id_documento`) REFERENCES `documento` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `usuario_datos_personales` WRITE;
/*!40000 ALTER TABLE `usuario_datos_personales` DISABLE KEYS */;

INSERT INTO `usuario_datos_personales` (`id`, `id_documento`, `nombre_completo`, `numero_documento`, `numero_celular`, `direccion`, `descripcion`)
VALUES
	(1,1,'ENE WOLFF',1002932882,300898975,'calle 95 #43-21','PRUEBA'),
	(2,1,'LUIS',1352423325,300272671,'calle 20 # 23-12',''),
	(3,1,'WOlferm Alpha',4352425,301928291,'cra 43 #20-10',''),
	(4,1,'Jessica Morris',109292002,320191912,'cra 90 #22-1',''),
	(5,1,'Jessica Paola De Alba',1001781662,304392892,'calle 92#90-10',''),
	(6,1,'SONIA LOPEZ',100920109,32038838,'calle 30',''),
	(7,1,'Otto Gomez',109838392,0,'',''),
	(8,1,'juan esteban',1098282992,0,'',''),
	(9,1,'daniela cabo',10002929,0,'',''),
	(12,1,'Laura Villa',1092292,0,'',''),
	(14,1,'JAZLPALO0',10029929,309484,'calle 20','prueba'),
	(15,2,'camila suarez',1092992992,0,'',''),
	(17,1,'eyner schoonewolff',1000292839,300049499,'calle 89 #23-45',''),
	(18,1,'bryan schoonewolff',102092992,1002992992,'calle 48 # 43',''),
	(20,1,'Dayana Mosquera',100092929,30949494,'calle 20',''),
	(21,1,'ola mundo',1002992,3004994,'calle',''),
	(22,1,'luiz diaz',1002929,30949494,'calle 100',''),
	(23,1,'eyner wolff',100299292,0,'',''),
	(24,1,'juan esteban ',1009292992,0,'',''),
	(25,1,'Elsa Velandia',100929928,30499993,'calle 20 #20-1',''),
	(26,1,'luis suarez',100282,3094948,'calle 828',''),
	(27,1,'luis Diego Mora',109282,30949499,'calle 90#23-12',''),
	(28,1,'pacheco ',102883839,3094949,'call 1002',''),
	(30,1,'Juan Esteban Montes',1038748383,30949493,'calle 20#12-12',''),
	(31,1,'German Garmendia',10929929,0,'',''),
	(32,1,'kevin turizo',4738929,30949494,'Calle 31 #34-58',''),
	(33,1,'LOLA FRENCH',98397937,300949949,'calle 20',''),
	(34,2,'EYNER ALFONSO',109282828,3092772,'calle 15',''),
	(35,1,'CARLOS MONTES',109299,3093993,'call 30',''),
	(37,1,'KAROLL DURAN',1093837738,309499494,'calle 99',''),
	(38,1,'prueba de repaso',10939939,0,'DEFAULT \'\'',''),
	(39,1,'Nestor',1143271197,0,'DEFAULT \'\'','');

/*!40000 ALTER TABLE `usuario_datos_personales` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla usuario_ocupaciones
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usuario_ocupaciones`;

CREATE TABLE `usuario_ocupaciones` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `id_usuario` int(11) unsigned NOT NULL,
  `id_ocupacion` int(11) unsigned NOT NULL,
  `eliminado` int(11) DEFAULT 0,
  PRIMARY KEY (`id`),
  KEY `id_ocupacion` (`id_ocupacion`),
  KEY `id_usuario` (`id_usuario`),
  CONSTRAINT `usuario_ocupaciones_ibfk_1` FOREIGN KEY (`id_ocupacion`) REFERENCES `ocupacion` (`id`),
  CONSTRAINT `usuario_ocupaciones_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `usuario_ocupaciones` WRITE;
/*!40000 ALTER TABLE `usuario_ocupaciones` DISABLE KEYS */;

INSERT INTO `usuario_ocupaciones` (`id`, `id_usuario`, `id_ocupacion`, `eliminado`)
VALUES
	(1,1,1,1),
	(2,1,2,0),
	(5,20,1,0),
	(6,20,2,0),
	(7,21,3,0),
	(8,21,4,0),
	(9,1,3,1),
	(10,1,3,1),
	(11,1,4,0),
	(12,47,1,0),
	(13,47,2,0),
	(14,27,3,0);

/*!40000 ALTER TABLE `usuario_ocupaciones` ENABLE KEYS */;
UNLOCK TABLES;


# Volcado de tabla usuarios
# ------------------------------------------------------------

DROP TABLE IF EXISTS `usuarios`;

CREATE TABLE `usuarios` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `email` varchar(50) NOT NULL DEFAULT '',
  `contraseña` varchar(100) NOT NULL DEFAULT '',
  `id_tipo_usuario` int(11) unsigned NOT NULL,
  `id_usuario_datos_personales` int(11) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `id_usuario_datos_personales` (`id_usuario_datos_personales`),
  KEY `id_tipo_usuario` (`id_tipo_usuario`),
  CONSTRAINT `usuarios_ibfk_2` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`id`),
  CONSTRAINT `usuarios_ibfk_3` FOREIGN KEY (`id_usuario_datos_personales`) REFERENCES `usuario_datos_personales` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;

INSERT INTO `usuarios` (`id`, `email`, `contraseña`, `id_tipo_usuario`, `id_usuario_datos_personales`)
VALUES
	(1,'enewolff@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,1),
	(2,'jh@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',3,2),
	(5,'luis@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',1,3),
	(15,'enewolff2015@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',3,4),
	(19,'Jdealbad30@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',3,5),
	(20,'sonyapsicologa@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,6),
	(21,'perroktrehp@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,7),
	(22,'juan@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',3,8),
	(24,'daniela@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,9),
	(26,'laura03@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,12),
	(27,'jazl.palomb@diaperstack.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,14),
	(28,'cammcf@egl-inc.info','$2b$12$g17vRMilj9qnBJcYR4pBjOkYvk4JQc1mSPkiTGxyexcwDWpxoK9vC',2,15),
	(29,'mariaAngel@gmail.com','$2b$12$eVsL3jJx3QDfmXcDakSSwOGSSOXO0cZg.zI9GalUWSSaAQumlbkAa',3,17),
	(30,'schoonewolff@gmail.com','$2b$12$OWOTfvq5Gqrck/LmVrvr3.uAvoWCnu6aEc2BjJ3ArwhwJpMgJf1Re',3,18),
	(32,'dayana@gmail.com','$2b$12$iJDyoNaH1KNJzID2qUp67OXmrYyWrWC65F2S7kVKc5f.gFbRPahtC',2,20),
	(33,'hola@gmai.com','$2b$12$vORjBFwbroBIJFQfLqSn9O.g.jt99htDGOq.1//Rq1b7JI61yfLXe',2,21),
	(34,'luchodiaz@gmail.com','$2b$12$vY/kyHjmWTFHN21o99pdyuQEiPOjlRWpEUC6xGkLfZfKjCUcz.TMq',2,22),
	(35,'enewolff2014@gmail.com','$2b$12$lQtKqRz6kRDVap5zGizHK.kHGur9uX2zQMwE/6EsA/ftbWF.pk0/6',3,23),
	(36,'juan@gmail.coms','$2b$12$iUSVGLp89iI34FSlmx2kW.XlX7XNnVxoFz.fnNDu6fjj7VQKSzdoa',2,24),
	(37,'elsaVelandia@gmail.com','$2b$12$Qa66VORqin/KHG6iC8AUWumyDbGnQXCXfn/h8OydpapxbKak1NLVG',2,25),
	(38,'luisSuarez@gmail.com','$2b$12$PVkG/nPdQaNXLd5OYdwVSupn/1U/Bbgxig/X6g0qw1v1n5V.83odS',2,26),
	(39,'LuisDiego@gmail.com','$2b$12$4/U0SWgxmWearlHlVbc3v.mWOBaP/egPDfdvg2PwtfHiT24SsNrSW',3,27),
	(40,'pachequito@gmail.com','$2b$12$nu5k/AajY.e1LNGKMOqSKOSGCa1L4gRyI3D.xkVqrqK8hB.HGhmiq',2,28),
	(42,'juanMontes@gmail.com','$2b$12$0kstPWh.zVh6rgo6/oHQr.tmbx.p54dqY8.HweGbpU0Jg2V4sDWn6',2,30),
	(43,'holaSoyGerman@gmail.com','$2b$12$UhmV6MhPJU2ygFqGiTeW.OSZzM4/T5NZDDte1J6MSmOpUc3ona7Ee',2,31),
	(44,'maybelle_veum@hotmail.com','$2b$12$ii/ytucB8tOtU5nulvWhIOn9f6gFVt0V64zCiqKW1qnnIyIvKJImu',2,32),
	(45,'lolawolff@gmail.com','$2b$12$/tt45S.XBzV9hXsJoZ0QUeUVbBguKQGGVGlykcV6zfpYt.06O0Fvm',2,33),
	(46,'eynerschoonewolff@gmail.com','$2b$12$yhS8Qm/NFIdx3pn8X3PSAejiOHZVwk8.l3nZeceYvJJa2AkrWXAI2',3,34),
	(47,'carlos99@gmail.com','$2b$12$RALR8ADswcXxnvU4jGZBRuki7J8l40.Bk8LoxDUfxxNtHVWyLEGtq',2,35),
	(49,'karolcita@gmail.com','$2b$12$5OvVIk9IoDPRlG7vwBfwPueBjk7psvEsFTmiBJvZLqYomdBveLXQO',3,37),
	(50,'n@gmail.com','$2b$12$Y6gWLaTduXeiCSogYn1nBenCYs0E/T7edemSwg8KuCjFwZe.oh2qq',3,38),
	(51,'junior@gmail.com','$2b$12$RzSOAFU3ZSDVCg/kUYBcyudnfi7DmVpwwfbHsSs30oDHyl5WT9P/q',3,39);

/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;



/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
