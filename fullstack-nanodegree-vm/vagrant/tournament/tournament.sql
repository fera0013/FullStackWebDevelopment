-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

 \c tournament

CREATE TABLE players ( name TEXT,
                     id SERIAL PRIMARY KEY);

-- Warning: this database structure doesn't consider draws
CREATE TABLE matches ( winner INTEGER references players(id),
	                   loser INTEGER references players(id),
                       match_number SERIAL PRIMARY KEY );

CREATE VIEW win_table AS
SELECT players.id, players.name, wins 
FROM (SELECT players.id,COUNT(*) AS wins 
FROM players,matches 
WHERE players.id = matches.winner GROUP BY players.id) as games_wins,players 
WHERE players.id=games_wins.id;

CREATE VIEW full_win_table AS
SELECT players.id,players.name,COALESCE(wins,0) as wins 
FROM win_table FULL OUTER JOIN players 
ON players.id=win_table.id;

CREATE VIEW losses_table AS
SELECT players.id, players.name, losses
FROM (SELECT players.id,COUNT(*) AS losses 
FROM players,matches 
WHERE players.id = matches.loser GROUP BY players.id) as games_losses,players 
WHERE players.id=games_losses.id;

CREATE VIEW full_losses_table AS
SELECT players.id,players.name,COALESCE(losses,0) as losses 
FROM losses_table FULL OUTER JOIN players 
ON players.id=losses_table.id;

CREATE VIEW win_loss_table AS
SELECT  full_win_table.id, full_win_table.name,wins,losses,(wins+losses) as matches
FROM full_win_table,full_losses_table
WHERE  full_win_table.id=full_losses_table.id;

