
DROP TABLE IF EXISTS `produtos`;

CREATE TABLE `produtos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(256) DEFAULT NULL,
  `descricao` text,
  `preco` decimal(10,2) DEFAULT NULL,
  `quantidade` int DEFAULT NULL,
  PRIMARY KEY (`id`)
)

INSERT INTO `produtos` 
VALUES (1,'Teclado Mecânico RGB','Teclado com iluminação RGB e switches azuis.',249.90,13),
(2,'Mouse Gamer 7200 DPI','Mouse com ajuste de DPI, 6 botões programáveis e LED vermelho',200.00,7),
(3,'Monitor 24 Full HD','Tela LED 1080p com borda fina e entrada HDMI',809.99,6),
(5,'Webcam Full HD','Webcam 1080p com microfone embutido e clip universal',255.80,33),
(6,'Headset Gamer Rgb','Som surround 7.1, microfone com cancelamento de ruído, led rgb customizável',314.99,13),
(7,'Ssd Nvme Tb','Alta velocidade, leitura até 3500mb/s, perfeito para games e edição de vídeo',451.16,0),
(11,'Alexa Echo 5° G','Smart com som aprimorado, display led com hora, temperatura e timers. integração total e automação residencial.',569.05,18),(12,'Óculos Tcl Nxt Xr','Óculos que simula uma tela de cinema 130°. conecta com vrlular, notebook ou console via usb-c.',4899.00,5);


