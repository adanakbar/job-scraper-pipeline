-- 1️ Create database
CREATE DATABASE job_pipeline;
GO

USE job_pipeline;
GO

-- 2️ Dimension tables
CREATE TABLE dim_company (
    company_id INT IDENTITY(1,1) PRIMARY KEY,
    company_name VARCHAR(255) UNIQUE
);
GO

CREATE TABLE dim_skills (
    skill_id INT IDENTITY(1,1) PRIMARY KEY,
    skill_name VARCHAR(255) UNIQUE
);
GO

-- 3️ Fact table
CREATE TABLE fact_jobs (
    job_id INT IDENTITY(1,1) PRIMARY KEY,
    job_title VARCHAR(255),
    company_id INT,
    date_posted DATE,
    job_link VARCHAR(MAX),
    scrape_date DATE,
    CONSTRAINT FK_fact_jobs_company FOREIGN KEY (company_id)
        REFERENCES dim_company(company_id)
);
GO

-- 4️ Bridge table for many-to-many
CREATE TABLE job_skills (
    job_id INT,
    skill_id INT,
    PRIMARY KEY (job_id, skill_id),
    CONSTRAINT FK_job_skills_job FOREIGN KEY (job_id)
        REFERENCES fact_jobs(job_id),
    CONSTRAINT FK_job_skills_skill FOREIGN KEY (skill_id)
        REFERENCES dim_skills(skill_id)
);
GO