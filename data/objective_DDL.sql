CREATE TABLE IF NOT EXISTS  project(
   project_id SERIAL PRIMARY KEY,
   project_name text NOT NULL,
  CONSTRAINT project_name_unique UNIQUE (project_name)
);

CREATE TABLE IF NOT EXISTS objective(
   objective_id SERIAL PRIMARY KEY,
   objective_name text NOT NULL,
   project_id serial
);

CREATE TABLE IF NOT EXISTS keyResult(
   keyResult_id SERIAL PRIMARY KEY,
   keyResult_definition text NOT NULL,
   keyResult_status text NOT NULL,
   objective_id serial
);

ALTER TABLE objective DROP CONSTRAINT IF EXISTS "objective_project_fk";
ALTER TABLE objective ADD CONSTRAINT "objective_project_fk" FOREIGN KEY(project_id) REFERENCES project ON DELETE CASCADE;
ALTER TABLE keyResult DROP CONSTRAINT IF EXISTS "keyResult_objective_fk";
ALTER TABLE keyResult ADD CONSTRAINT "keyResult_objective_fk" FOREIGN KEY(objective_id) REFERENCES objective ON DELETE CASCADE;
