CREATE TABLE IF NOT EXISTS  project(
   project_id SERIAL PRIMARY KEY,
   project_name text NOT NULL
);

CREATE TABLE IF NOT EXISTS objective(
   objective_id SERIAL PRIMARY KEY,
   objective_name text NOT NULL,
   project_id serial REFERENCES project
);

CREATE TABLE IF NOT EXISTS keyResult(
   keyResult_id SERIAL PRIMARY KEY,
   keyResult_definition text NOT NULL,
   keyResult_status text NOT NULL,
   objective_id serial REFERENCES objective
);
