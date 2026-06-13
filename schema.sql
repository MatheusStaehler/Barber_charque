-- ============================================================
--  Barber Charque – Script de criação do banco de dados
-- ============================================================

CREATE DATABASE IF NOT EXISTS barber_charque
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE barber_charque;

-- Tabela de usuários (clientes + admin)
CREATE TABLE IF NOT EXISTS usuarios (
  id       INT          NOT NULL AUTO_INCREMENT,
  nome     VARCHAR(100) NOT NULL,
  telefone VARCHAR(20)  NOT NULL UNIQUE,
  senha    VARCHAR(255) NOT NULL,
  tipo     VARCHAR(10)  NOT NULL DEFAULT 'cliente',  -- 'cliente' | 'admin'
  PRIMARY KEY (id)
);

-- Horários disponíveis para agendamento
CREATE TABLE IF NOT EXISTS disponibilidade (
  id      INT  NOT NULL AUTO_INCREMENT,
  data    DATE NOT NULL,
  horario TIME NOT NULL,
  PRIMARY KEY (id)
);

-- Agendamentos realizados pelos clientes
CREATE TABLE IF NOT EXISTS agendamentos (
  id         INT  NOT NULL AUTO_INCREMENT,
  data       DATE NOT NULL,
  horario    TIME NOT NULL,
  id_usuario INT  NOT NULL,
  PRIMARY KEY (id),
  FOREIGN KEY (id_usuario) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- ── Usuário administrador padrão ──────────────────────────────
-- Telefone: 51999999999 | Senha: admin123
INSERT INTO usuarios (nome, telefone, senha, tipo)
VALUES ('Administrador', '51999999999', 'admin123', 'admin');
