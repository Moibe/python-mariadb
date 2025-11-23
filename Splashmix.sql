CREATE TABLE `conjunto` (
  `id` integer PRIMARY KEY,
  `sitio` varchar(255),
  `nombre` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `producto` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `cantidad` int,
  `unidad_general` varchar(255),
  `precio_base` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `linea` (
  `id` integer PRIMARY KEY,
  `id_conjunto` integer NOT NULL,
  `id_producto` integer NOT NULL,
  `created_at` timestamp
);

CREATE TABLE `pais` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `unidad` varchar(255),
  `unidades` varchar(255),
  `moneda` varchar(255),
  `moneda_tic` varchar(255),
  `simbolo` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `precio` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `id_linea` integer NOT NULL,
  `id_pais` integer NOT NULL,
  `price_id` varchar(255),
  `cantidad_precio` int,
  `ratio_imagen` int,
  `status` varchar(255),
  `created_at` timestamp
);

ALTER TABLE `linea` ADD FOREIGN KEY (`id_conjunto`) REFERENCES `conjunto` (`id`);

ALTER TABLE `linea` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

ALTER TABLE `precio` ADD FOREIGN KEY (`id_linea`) REFERENCES `linea` (`id`);

ALTER TABLE `precio` ADD FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id`);
