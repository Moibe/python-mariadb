CREATE TABLE `producto` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `precio_mxn` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `pais` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `moneda` varchar(255),
  `moneda_tic` varchar(255),
  `simbolo` varchar(255),
  `created_at` timestamp
);

CREATE TABLE `precio` (
  `id` integer PRIMARY KEY,
  `nombre` varchar(255),
  `id_producto` integer NOT NULL,
  `id_pais` integer NOT NULL,
  `status` varchar(255),
  `price_id` varchar(255),
  `created_at` timestamp
);

ALTER TABLE `precio` ADD FOREIGN KEY (`id_producto`) REFERENCES `producto` (`id`);

ALTER TABLE `precio` ADD FOREIGN KEY (`id_pais`) REFERENCES `pais` (`id`);
