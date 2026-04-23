/*
 Navicat Premium Dump SQL

 Source Server         : 47.117.107.23-15431-pg
 Source Server Type    : PostgreSQL
 Source Server Version : 170004 (170004)
 Source Host           : 47.117.107.23:15431
 Source Catalog        : db_dtlms
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 170004 (170004)
 File Encoding         : 65001

 Date: 23/04/2026 16:15:47
*/


-- ----------------------------
-- Sequence structure for dtlms_achievements_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_achievements_id_seq";
CREATE SEQUENCE "public"."dtlms_achievements_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_admission_decisions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_admission_decisions_id_seq";
CREATE SEQUENCE "public"."dtlms_admission_decisions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_advisors_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_advisors_id_seq";
CREATE SEQUENCE "public"."dtlms_advisors_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_application_materials_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_application_materials_id_seq";
CREATE SEQUENCE "public"."dtlms_application_materials_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_data_sync_logs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_data_sync_logs_id_seq";
CREATE SEQUENCE "public"."dtlms_data_sync_logs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_dict_data_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_dict_data_id_seq";
CREATE SEQUENCE "public"."dtlms_dict_data_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_dict_types_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_dict_types_id_seq";
CREATE SEQUENCE "public"."dtlms_dict_types_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_interview_groups_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_interview_groups_id_seq";
CREATE SEQUENCE "public"."dtlms_interview_groups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_interview_schedules_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_interview_schedules_id_seq";
CREATE SEQUENCE "public"."dtlms_interview_schedules_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_interview_scores_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_interview_scores_id_seq";
CREATE SEQUENCE "public"."dtlms_interview_scores_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_login_logs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_login_logs_id_seq";
CREATE SEQUENCE "public"."dtlms_login_logs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_material_scores_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_material_scores_id_seq";
CREATE SEQUENCE "public"."dtlms_material_scores_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_notification_templates_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_notification_templates_id_seq";
CREATE SEQUENCE "public"."dtlms_notification_templates_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_operation_logs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_operation_logs_id_seq";
CREATE SEQUENCE "public"."dtlms_operation_logs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_outbound_studies_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_outbound_studies_id_seq";
CREATE SEQUENCE "public"."dtlms_outbound_studies_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_permissions_id_seq";
CREATE SEQUENCE "public"."dtlms_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_achievement_records_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_achievement_records_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_achievement_records_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_attachments_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_attachments_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_attachments_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_education_experiences_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_education_experiences_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_education_experiences_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_english_proficiencies_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_english_proficiencies_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_english_proficiencies_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_family_members_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_family_members_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_family_members_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_practice_experiences_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_practice_experiences_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_practice_experiences_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_application_preferences_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_application_preferences_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_application_preferences_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_portal_students_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_portal_students_id_seq";
CREATE SEQUENCE "public"."dtlms_portal_students_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_qualification_reviews_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_qualification_reviews_id_seq";
CREATE SEQUENCE "public"."dtlms_qualification_reviews_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_recruitment_applications_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_recruitment_applications_id_seq";
CREATE SEQUENCE "public"."dtlms_recruitment_applications_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_recruitment_plans_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_recruitment_plans_id_seq";
CREATE SEQUENCE "public"."dtlms_recruitment_plans_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_research_fields_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_research_fields_id_seq";
CREATE SEQUENCE "public"."dtlms_research_fields_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_research_projects_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_research_projects_id_seq";
CREATE SEQUENCE "public"."dtlms_research_projects_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_reviewer_assignments_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_reviewer_assignments_id_seq";
CREATE SEQUENCE "public"."dtlms_reviewer_assignments_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_role_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_role_permissions_id_seq";
CREATE SEQUENCE "public"."dtlms_role_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_roles_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_roles_id_seq";
CREATE SEQUENCE "public"."dtlms_roles_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_scientific_reports_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_scientific_reports_id_seq";
CREATE SEQUENCE "public"."dtlms_scientific_reports_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_student_advisor_history_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_student_advisor_history_id_seq";
CREATE SEQUENCE "public"."dtlms_student_advisor_history_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_student_team_history_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_student_team_history_id_seq";
CREATE SEQUENCE "public"."dtlms_student_team_history_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_students_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_students_id_seq";
CREATE SEQUENCE "public"."dtlms_students_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_system_configs_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_system_configs_id_seq";
CREATE SEQUENCE "public"."dtlms_system_configs_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_team_advisors_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_team_advisors_id_seq";
CREATE SEQUENCE "public"."dtlms_team_advisors_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_teams_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_teams_id_seq";
CREATE SEQUENCE "public"."dtlms_teams_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_theses_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_theses_id_seq";
CREATE SEQUENCE "public"."dtlms_theses_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_thesis_reviews_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_thesis_reviews_id_seq";
CREATE SEQUENCE "public"."dtlms_thesis_reviews_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_training_plan_versions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_training_plan_versions_id_seq";
CREATE SEQUENCE "public"."dtlms_training_plan_versions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_training_plans_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_training_plans_id_seq";
CREATE SEQUENCE "public"."dtlms_training_plans_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_user_roles_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_user_roles_id_seq";
CREATE SEQUENCE "public"."dtlms_user_roles_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_users_id_seq";
CREATE SEQUENCE "public"."dtlms_users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_wf_ru_identitylink_id__seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_wf_ru_identitylink_id__seq";
CREATE SEQUENCE "public"."dtlms_wf_ru_identitylink_id__seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for dtlms_written_exam_scores_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."dtlms_written_exam_scores_id_seq";
CREATE SEQUENCE "public"."dtlms_written_exam_scores_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for dtlms_achievements
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_achievements";
CREATE TABLE "public"."dtlms_achievements" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_achievements_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "achievement_type" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "published_at" date,
  "publisher_name" varchar(255) COLLATE "pg_catalog"."default",
  "ranking_text" varchar(64) COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_achievements
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_admission_decisions
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_admission_decisions";
CREATE TABLE "public"."dtlms_admission_decisions" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_admission_decisions_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "decision_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "rank_no" int4,
  "final_score" numeric(5,2),
  "transfer_option" varchar(64) COLLATE "pg_catalog"."default",
  "decision_comment" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_admission_decisions
-- ----------------------------
INSERT INTO "public"."dtlms_admission_decisions" VALUES (1, 27, 'pending', 27, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (2, 26, 'pending', 26, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (3, 16, 'pending', 16, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (4, 17, 'pending', 17, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (5, 19, 'pending', 19, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (6, 15, 'pending', 15, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (7, 14, 'pending', 14, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (8, 13, 'pending', 13, NULL, NULL, '来源计划 5', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (9, 1, 'admitted', 1, 91.00, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (10, 2, 'pre_admit', 2, 88.50, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (11, 3, 'pending', 3, 85.00, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (12, 4, 'pending', 4, NULL, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (13, 5, 'pending', 5, 82.00, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (14, 6, 'pending', 6, NULL, NULL, '来源计划 1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (15, 7, 'pending', 7, NULL, NULL, '来源计划 2', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (16, 8, 'admitted', 8, 93.00, NULL, '来源计划 2', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (17, 9, 'pending', 9, 73.00, NULL, '来源计划 2', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (18, 10, 'pre_admit', 10, 86.00, NULL, '来源计划 2', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (19, 11, 'pending', 11, NULL, NULL, '来源计划 3', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_admission_decisions" VALUES (20, 12, 'pending', 12, NULL, NULL, '来源计划 3', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_advisors
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_advisors";
CREATE TABLE "public"."dtlms_advisors" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_advisors_id_seq'::regclass),
  "advisor_no" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "full_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "title" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "organization_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "research_direction" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "annual_quota" int4 NOT NULL DEFAULT 0,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_advisors
-- ----------------------------
INSERT INTO "public"."dtlms_advisors" VALUES (1, 'ADV001', '刘亚', '教授', '智能制造学院', '智能制造与工业互联网', 7, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_advisors" VALUES (2, 'ADV002', '袁野', '副教授', '智能制造学院', '博士生培养与过程治理', 8, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_advisors" VALUES (3, 'ADV003', '徐素天', '教授', '工业软件学院', '智能制造与工业互联网', 9, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_application_materials
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_application_materials";
CREATE TABLE "public"."dtlms_application_materials" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_application_materials_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "material_type" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "material_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "file_url" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_application_materials
-- ----------------------------
INSERT INTO "public"."dtlms_application_materials" VALUES (2, 26, '报名材料', 'pending', '/materials/ZSLQSP202604230009.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (3, 16, '报名材料', 'pending', '/materials/ZSLQSP202604210004.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (4, 17, '报名材料', 'pending', '/materials/ZSLQSP202604210005.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (5, 19, '报名材料', 'pending', '/materials/ZSLQSP202604210007.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (6, 15, '报名材料', 'approved', 'checklist.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (7, 14, '报名材料', 'approved', 'checklist.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (8, 13, '报名材料', 'approved', 'materials.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (9, 1, '报名材料', 'approved', '/materials/ZSLQSP202604070001.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (10, 2, '报名材料', 'approved', '/materials/ZSLQSP202604070002.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (11, 3, '报名材料', 'approved', '/materials/ZSLQSP202604070003.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (12, 4, '报名材料', 'approved', '/materials/ZSLQSP202604070004.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (13, 5, '报名材料', 'approved', '/materials/ZSLQSP202604070005.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (14, 6, '报名材料', 'pending', '/materials/ZSLQSP202604070006.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (15, 7, '报名材料', 'approved', '/materials/ZSLQSP202604070007.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (16, 8, '报名材料', 'approved', '/materials/ZSLQSP202604070008.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (17, 9, '报名材料', 'approved', '/materials/ZSLQSP202604070009.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (18, 10, '报名材料', 'approved', '/materials/ZSLQSP202604070010.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (19, 11, '报名材料', 'approved', '/materials/ZSLQSP202604070011.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (20, 12, '报名材料', 'pending', '/materials/ZSLQSP202604070012.zip', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_application_materials" VALUES (28, 27, '报名材料', 'pending', '/materials/ZSLQSP202604230010.zip', 'f', '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_data_sync_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_data_sync_logs";
CREATE TABLE "public"."dtlms_data_sync_logs" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_data_sync_logs_id_seq'::regclass),
  "source_system" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "target_system" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "sync_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "record_count" int4 NOT NULL DEFAULT 0,
  "failure_reason" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_data_sync_logs
-- ----------------------------
INSERT INTO "public"."dtlms_data_sync_logs" VALUES (1, '招生系统', 'DTLMS', 'success', 36, NULL, '2026-04-07 05:00:00+08', '2026-04-07 05:00:00+08');
INSERT INTO "public"."dtlms_data_sync_logs" VALUES (2, '飞书', 'DTLMS', 'failed', 4, '回执接口超时，等待补偿重试。', '2026-04-07 06:00:00+08', '2026-04-07 06:00:00+08');
INSERT INTO "public"."dtlms_data_sync_logs" VALUES (3, '实验室OA', 'DTLMS', 'success', 58, NULL, '2026-04-07 07:00:00+08', '2026-04-07 07:00:00+08');

-- ----------------------------
-- Table structure for dtlms_dict_data
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_dict_data";
CREATE TABLE "public"."dtlms_dict_data" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_dict_data_id_seq'::regclass),
  "dict_type_id" int8 NOT NULL,
  "dict_type" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "label" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "value" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "sort_order" int4 NOT NULL DEFAULT 0,
  "status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '启用'::character varying,
  "color_type" varchar(32) COLLATE "pg_catalog"."default",
  "css_class" varchar(128) COLLATE "pg_catalog"."default",
  "remark" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_dict_data
-- ----------------------------
INSERT INTO "public"."dtlms_dict_data" VALUES (69, 19, 'training_report_cycle', '半年度', '半年度', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (74, 20, 'training_report_status', '已通过', '已通过', 20, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (73, 20, 'training_report_status', '退回修改', '退回修改', 30, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (89, 23, 'degree_thesis_status', '待查重', '待查重', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (1, 1, 'system_account_status', '锁定', '锁定', 30, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24550, 6247, 'student_ethnic_group', '汉族', '汉族', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24551, 6247, 'student_ethnic_group', '蒙古族', '蒙古族', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24552, 6247, 'student_ethnic_group', '回族', '回族', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24553, 6247, 'student_ethnic_group', '藏族', '藏族', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24554, 6247, 'student_ethnic_group', '维吾尔族', '维吾尔族', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24555, 6247, 'student_ethnic_group', '苗族', '苗族', 60, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24556, 6247, 'student_ethnic_group', '彝族', '彝族', 70, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24557, 6247, 'student_ethnic_group', '壮族', '壮族', 80, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24558, 6247, 'student_ethnic_group', '布依族', '布依族', 90, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24588, 6247, 'student_ethnic_group', '阿昌族', '阿昌族', 390, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24589, 6247, 'student_ethnic_group', '普米族', '普米族', 400, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24590, 6247, 'student_ethnic_group', '塔吉克族', '塔吉克族', 410, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24591, 6247, 'student_ethnic_group', '怒族', '怒族', 420, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24592, 6247, 'student_ethnic_group', '乌孜别克族', '乌孜别克族', 430, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24593, 6247, 'student_ethnic_group', '俄罗斯族', '俄罗斯族', 440, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24594, 6247, 'student_ethnic_group', '鄂温克族', '鄂温克族', 450, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (60, 17, 'recruitment_application_status', '预录取', '预录取', 60, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (59, 17, 'recruitment_application_status', '同意录取', '同意录取', 70, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (3, 1, 'system_account_status', '启用', '启用', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (2, 1, 'system_account_status', '停用', '停用', 20, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (9, 2, 'system_role_scope', '系统治理', '系统治理', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (8, 2, 'system_role_scope', '招生管理', '招生管理', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (7, 2, 'system_role_scope', '学生管理', '学生管理', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (6, 2, 'system_role_scope', '培养与学位', '培养与学位', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (5, 2, 'system_role_scope', '学位管理', '学位管理', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (4, 2, 'system_role_scope', '跨部门协同', '跨部门协同', 60, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (11, 3, 'system_integration_direction', '双向同步', '双向同步', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (10, 3, 'system_integration_direction', '主数据下发', '主数据下发', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24559, 6247, 'student_ethnic_group', '朝鲜族', '朝鲜族', 100, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24560, 6247, 'student_ethnic_group', '满族', '满族', 110, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24561, 6247, 'student_ethnic_group', '侗族', '侗族', 120, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24562, 6247, 'student_ethnic_group', '瑶族', '瑶族', 130, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24563, 6247, 'student_ethnic_group', '白族', '白族', 140, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24564, 6247, 'student_ethnic_group', '土家族', '土家族', 150, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24565, 6247, 'student_ethnic_group', '哈尼族', '哈尼族', 160, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24566, 6247, 'student_ethnic_group', '哈萨克族', '哈萨克族', 170, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24567, 6247, 'student_ethnic_group', '傣族', '傣族', 180, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24568, 6247, 'student_ethnic_group', '黎族', '黎族', 190, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24569, 6247, 'student_ethnic_group', '傈僳族', '傈僳族', 200, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24570, 6247, 'student_ethnic_group', '佤族', '佤族', 210, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24571, 6247, 'student_ethnic_group', '畲族', '畲族', 220, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24572, 6247, 'student_ethnic_group', '高山族', '高山族', 230, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24573, 6247, 'student_ethnic_group', '拉祜族', '拉祜族', 240, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24574, 6247, 'student_ethnic_group', '水族', '水族', 250, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24575, 6247, 'student_ethnic_group', '东乡族', '东乡族', 260, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24576, 6247, 'student_ethnic_group', '纳西族', '纳西族', 270, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24577, 6247, 'student_ethnic_group', '景颇族', '景颇族', 280, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24578, 6247, 'student_ethnic_group', '柯尔克孜族', '柯尔克孜族', 290, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24579, 6247, 'student_ethnic_group', '土族', '土族', 300, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24609, 12, 'student_political_status', '民革党员', '民革党员', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24610, 12, 'student_political_status', '民盟盟员', '民盟盟员', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24612, 12, 'student_political_status', '民进会员', '民进会员', 70, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24613, 12, 'student_political_status', '农工党党员', '农工党党员', 80, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24614, 12, 'student_political_status', '致公党党员', '致公党党员', 90, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24615, 12, 'student_political_status', '九三学社社员', '九三学社社员', 100, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24616, 12, 'student_political_status', '台盟盟员', '台盟盟员', 110, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24617, 12, 'student_political_status', '无党派人士', '无党派人士', 120, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24582, 6247, 'student_ethnic_group', '羌族', '羌族', 330, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (57, 16, 'recruitment_material_status', '材料齐全', '材料齐全', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (56, 16, 'recruitment_material_status', '待补材料', '待补材料', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (55, 16, 'recruitment_material_status', '已退回修改', '已退回修改', 30, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (65, 17, 'recruitment_application_status', '报名已提交', '报名已提交', 10, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (64, 17, 'recruitment_application_status', '资格审核通过', '资格审核通过', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (58, 17, 'recruitment_application_status', '不录取', '不录取', 80, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (68, 18, 'training_plan_status', '待学生确认', '待学生确认', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (67, 18, 'training_plan_status', '执行中', '执行中', 20, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (66, 18, 'training_plan_status', '已归档', '已归档', 30, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (72, 19, 'training_report_cycle', '月度', '月度', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24583, 6247, 'student_ethnic_group', '布朗族', '布朗族', 340, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24584, 6247, 'student_ethnic_group', '撒拉族', '撒拉族', 350, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24599, 6247, 'student_ethnic_group', '塔塔尔族', '塔塔尔族', 500, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24600, 6247, 'student_ethnic_group', '独龙族', '独龙族', 510, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24601, 6247, 'student_ethnic_group', '鄂伦春族', '鄂伦春族', 520, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24602, 6247, 'student_ethnic_group', '赫哲族', '赫哲族', 530, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24603, 6247, 'student_ethnic_group', '门巴族', '门巴族', 540, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24604, 6247, 'student_ethnic_group', '珞巴族', '珞巴族', 550, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24605, 6247, 'student_ethnic_group', '基诺族', '基诺族', 560, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (71, 19, 'training_report_cycle', '双月', '双月', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (70, 19, 'training_report_cycle', '季度', '季度', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (14, 3, 'system_integration_direction', '主数据导入 / 录取回传', '主数据导入 / 录取回传', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (13, 3, 'system_integration_direction', '考勤 / 门禁 / 请假同步', '考勤 / 门禁 / 请假同步', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (12, 3, 'system_integration_direction', '待办通知 / 审批提醒 / 回执', '待办通知 / 审批提醒 / 回执', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (19, 4, 'system_integration_cadence', '实时', '实时', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (18, 4, 'system_integration_cadence', '实时 + 每日对账', '实时 + 每日对账', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (17, 4, 'system_integration_cadence', '实时事件 + 定时补偿', '实时事件 + 定时补偿', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (16, 4, 'system_integration_cadence', '每小时', '每小时', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (15, 4, 'system_integration_cadence', '每日', '每日', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24580, 6247, 'student_ethnic_group', '达斡尔族', '达斡尔族', 310, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24581, 6247, 'student_ethnic_group', '仫佬族', '仫佬族', 320, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24585, 6247, 'student_ethnic_group', '毛南族', '毛南族', 360, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (22, 5, 'system_integration_status', '正常', '正常', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (21, 5, 'system_integration_status', '告警', '告警', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (20, 5, 'system_integration_status', '停用', '停用', 30, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24, 6, 'system_audit_status', '启用', '启用', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (23, 6, 'system_audit_status', '停用', '停用', 20, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (26, 7, 'system_operation_result', '成功', 'success', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (31, 9, 'student_status', '请假中', '请假中', 40, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (30, 9, 'student_status', '学位论文阶段', '学位论文阶段', 50, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (29, 9, 'student_status', '已毕业', '已毕业', 60, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24586, 6247, 'student_ethnic_group', '仡佬族', '仡佬族', 370, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24587, 6247, 'student_ethnic_group', '锡伯族', '锡伯族', 380, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24595, 6247, 'student_ethnic_group', '德昂族', '德昂族', 460, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24596, 6247, 'student_ethnic_group', '保安族', '保安族', 470, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24597, 6247, 'student_ethnic_group', '裕固族', '裕固族', 480, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24598, 6247, 'student_ethnic_group', '京族', '京族', 490, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (63, 17, 'recruitment_application_status', '材料评分中', '材料评分中', 30, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (62, 17, 'recruitment_application_status', '面试待安排', '面试待安排', 40, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (61, 17, 'recruitment_application_status', '面试完成', '面试完成', 50, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (28, 8, 'system_sync_status', '成功', 'success', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (27, 8, 'system_sync_status', '失败', 'failed', 20, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (24611, 12, 'student_political_status', '民建会员', '民建会员', 60, '启用', NULL, NULL, NULL, 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (51, 14, 'recruitment_plan_stage', '报名配置', '报名配置', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (50, 14, 'recruitment_plan_stage', '资格审核', '资格审核', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (54, 15, 'recruitment_degree', '本科', '本科', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (53, 15, 'recruitment_degree', '硕士', '硕士', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (52, 15, 'recruitment_degree', '博士', '博士', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (93, 24, 'degree_blind_review_status', '未送审', '未送审', 20, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (92, 24, 'degree_blind_review_status', '进行中', '进行中', 30, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (91, 24, 'degree_blind_review_status', '已通过', '已通过', 40, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (90, 24, 'degree_blind_review_status', '未通过', '未通过', 50, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (98, 25, 'degree_defense_status', '未进入', '未进入', 10, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (97, 25, 'degree_defense_status', '待安排', '待安排', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (96, 25, 'degree_defense_status', '预答辩完成', '预答辩完成', 30, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (95, 25, 'degree_defense_status', '正式答辩完成', '正式答辩完成', 40, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (103, 26, 'degree_status', '待申请', '待申请', 10, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (102, 26, 'degree_status', '未授位', '未授位', 20, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (101, 26, 'degree_status', '授位审批中', '授位审批中', 30, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (100, 26, 'degree_status', '待正式答辩', '待正式答辩', 40, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (99, 26, 'degree_status', '已授位', '已授位', 50, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (107, 27, 'degree_review_status', '待反馈', '待反馈', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (106, 27, 'degree_review_status', '已提交', '已提交', 20, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (105, 27, 'degree_review_status', '已通过', '已通过', 30, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (25, 7, 'system_operation_result', '失败', 'failed', 20, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (34, 9, 'student_status', '在校', '在校', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (33, 9, 'student_status', '实习中', '实习中', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (32, 9, 'student_status', '外出研修', '外出研修', 30, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (36, 10, 'student_degree_type', '工程博士', '工程博士', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (35, 10, 'student_degree_type', '学术博士', '学术博士', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (39, 11, 'student_team_status', '启用', '启用', 10, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (38, 11, 'student_team_status', '筹建', '筹建', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (37, 11, 'student_team_status', '停用', '停用', 30, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (43, 12, 'student_political_status', '中共党员', '中共党员', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (42, 12, 'student_political_status', '中共预备党员', '中共预备党员', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (41, 12, 'student_political_status', '共青团员', '共青团员', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (40, 12, 'student_political_status', '群众', '群众', 130, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (45, 13, 'recruitment_semester', '春', '春', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (44, 13, 'recruitment_semester', '秋', '秋', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (88, 23, 'degree_thesis_status', '查重中', '查重中', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (87, 23, 'degree_thesis_status', '查重通过', '查重通过', 30, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (86, 23, 'degree_thesis_status', '退回修改', '退回修改', 40, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (85, 23, 'degree_thesis_status', '盲审通过', '盲审通过', 50, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (94, 24, 'degree_blind_review_status', '待送审', '待送审', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (104, 27, 'degree_review_status', '需修改', '需修改', 40, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (110, 28, 'workflow_priority', '高', '高', 10, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (109, 28, 'workflow_priority', '中', '中', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (108, 28, 'workflow_priority', '低', '低', 30, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (114, 29, 'workflow_status', '待处理', '待处理', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (113, 29, 'workflow_status', '处理中', '处理中', 20, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (112, 29, 'workflow_status', '已通过', '已通过', 30, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (111, 29, 'workflow_status', '已驳回', '已驳回', 40, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (49, 14, 'recruitment_plan_stage', '评分推荐', '评分推荐', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (48, 14, 'recruitment_plan_stage', '材料评分', '材料评分', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (47, 14, 'recruitment_plan_stage', '面试执行', '面试执行', 50, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (46, 14, 'recruitment_plan_stage', '预录取', '预录取', 60, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (75, 20, 'training_report_status', '待导师审阅', '待导师审阅', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (79, 21, 'training_outbound_study_type', '联合培养', '联合培养', 10, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (78, 21, 'training_outbound_study_type', '企业研修', '企业研修', 20, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (77, 21, 'training_outbound_study_type', '访学交流', '访学交流', 30, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (76, 21, 'training_outbound_study_type', '学术会议', '学术会议', 40, '启用', NULL, NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (84, 22, 'training_outbound_approval_status', '审批中', '审批中', 10, '启用', 'warning', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (83, 22, 'training_outbound_approval_status', '已批准', '已批准', 20, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (82, 22, 'training_outbound_approval_status', '研修中', '研修中', 30, '启用', 'success', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (81, 22, 'training_outbound_approval_status', '已结束', '已结束', 40, '启用', 'info', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_data" VALUES (80, 22, 'training_outbound_approval_status', '已驳回', '已驳回', 50, '启用', 'danger', NULL, NULL, 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');

-- ----------------------------
-- Table structure for dtlms_dict_types
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_dict_types";
CREATE TABLE "public"."dtlms_dict_types" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_dict_types_id_seq'::regclass),
  "dict_name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "dict_type" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '启用'::character varying,
  "remark" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_dict_types
-- ----------------------------
INSERT INTO "public"."dtlms_dict_types" VALUES (1, '账号状态', 'system_account_status', '启用', '系统账号状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (2, '角色范围', 'system_role_scope', '启用', '系统角色范围字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (3, '集成方向', 'system_integration_direction', '启用', '系统集成方向字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (4, '集成频率', 'system_integration_cadence', '启用', '系统集成频率字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (5, '集成状态', 'system_integration_status', '启用', '系统集成状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (6, '审计策略状态', 'system_audit_status', '启用', '审计策略状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (7, '操作结果', 'system_operation_result', '启用', '操作日志结果字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (6247, '民族', 'student_ethnic_group', '启用', '学生民族字典', 'f', '2026-04-21 15:35:36.575931+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (29, '流程状态', 'workflow_status', '启用', '审批状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (8, '同步状态', 'system_sync_status', '启用', '同步日志状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (9, '学生状态', 'student_status', '启用', '学生生命周期状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (10, '学位类型', 'student_degree_type', '启用', '博士类型字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (11, '团队状态', 'student_team_status', '启用', '团队状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (12, '政治面貌', 'student_political_status', '启用', '学生政治面貌字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (13, '招生学期', 'recruitment_semester', '启用', '招生学期字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (14, '招生计划阶段', 'recruitment_plan_stage', '启用', '招生计划阶段字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (15, '报考学历', 'recruitment_degree', '启用', '招生学历字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (16, '材料状态', 'recruitment_material_status', '启用', '材料状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (17, '申请状态', 'recruitment_application_status', '启用', '申请状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (18, '培养方案状态', 'training_plan_status', '启用', '培养方案状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (19, '科研报告周期', 'training_report_cycle', '启用', '科研报告周期字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (20, '科研报告状态', 'training_report_status', '启用', '科研报告状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (21, '外出研修类型', 'training_outbound_study_type', '启用', '外出研修类型字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (22, '外出研修审批状态', 'training_outbound_approval_status', '启用', '外出研修审批状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (23, '论文状态', 'degree_thesis_status', '启用', '论文流程状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (24, '盲审状态', 'degree_blind_review_status', '启用', '盲审状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (25, '答辩状态', 'degree_defense_status', '启用', '答辩状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (26, '授位状态', 'degree_status', '启用', '授位状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (27, '评审状态', 'degree_review_status', '启用', '评审状态字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');
INSERT INTO "public"."dtlms_dict_types" VALUES (28, '流程优先级', 'workflow_priority', '启用', '审批优先级字典', 'f', '2026-04-02 17:40:18.854951+08', '2026-04-23 14:49:28.031265+08');

-- ----------------------------
-- Table structure for dtlms_interview_groups
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_interview_groups";
CREATE TABLE "public"."dtlms_interview_groups" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_interview_groups_id_seq'::regclass),
  "plan_id" int8 NOT NULL,
  "group_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "group_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "interview_mode" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'offline'::character varying,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_interview_groups
-- ----------------------------
INSERT INTO "public"."dtlms_interview_groups" VALUES (1, 5, 'G01', '第1面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (2, 5, 'G02', '第2面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (3, 5, 'G03', '第3面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (4, 1, 'G01', '第1面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (5, 1, 'G02', '第2面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (6, 1, 'G03', '第3面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (7, 1, 'G04', '第4面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (8, 2, 'G01', '第1面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (9, 2, 'G02', '第2面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (10, 2, 'G03', '第3面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (11, 3, 'G01', '第1面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (12, 3, 'G02', '第2面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_groups" VALUES (13, 4, 'G01', '第1面试组', 'offline', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_interview_schedules
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_interview_schedules";
CREATE TABLE "public"."dtlms_interview_schedules" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_interview_schedules_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "interview_group_id" int8 NOT NULL,
  "admission_ticket_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "starts_at" timestamptz(6) NOT NULL,
  "ends_at" timestamptz(6) NOT NULL,
  "schedule_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'scheduled'::character varying,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_interview_schedules
-- ----------------------------
INSERT INTO "public"."dtlms_interview_schedules" VALUES (1, 27, 1, 'TKT-ZSLQSP202604230010', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (2, 26, 1, 'TKT-ZSLQSP202604230009', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (3, 16, 1, 'TKT-ZSLQSP202604210004', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (4, 17, 1, 'TKT-ZSLQSP202604210005', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (5, 19, 1, 'TKT-ZSLQSP202604210007', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (6, 15, 1, 'TKT-ZSLQSP202604100004', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (7, 14, 1, 'TKT-ZSLQSP202604100003', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (8, 13, 1, 'TKT-ZSLQSP202604100001', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (9, 1, 4, 'TKT-ZSLQSP202604070001', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (10, 2, 4, 'TKT-ZSLQSP202604070002', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (11, 3, 4, 'TKT-ZSLQSP202604070003', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (12, 4, 4, 'TKT-ZSLQSP202604070004', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (13, 5, 4, 'TKT-ZSLQSP202604070005', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (14, 6, 4, 'TKT-ZSLQSP202604070006', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (15, 7, 8, 'TKT-ZSLQSP202604070007', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (16, 8, 8, 'TKT-ZSLQSP202604070008', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (17, 9, 8, 'TKT-ZSLQSP202604070009', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (18, 10, 8, 'TKT-ZSLQSP202604070010', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'completed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (19, 11, 11, 'TKT-ZSLQSP202604070011', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_schedules" VALUES (20, 12, 11, 'TKT-ZSLQSP202604070012', '2026-04-18 09:00:00+08', '2026-04-18 09:30:00+08', 'scheduled', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_interview_scores
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_interview_scores";
CREATE TABLE "public"."dtlms_interview_scores" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_interview_scores_id_seq'::regclass),
  "schedule_id" int8 NOT NULL,
  "evaluator_username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "single_choice_score" numeric(5,2),
  "fill_blank_score" numeric(5,2),
  "coding_score" numeric(5,2),
  "interview_score" numeric(5,2),
  "ideological_score" numeric(5,2),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_interview_scores
-- ----------------------------
INSERT INTO "public"."dtlms_interview_scores" VALUES (1, 1, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (2, 2, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (3, 3, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (4, 4, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (5, 5, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (6, 6, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (7, 7, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (8, 8, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (9, 9, '何琳', NULL, NULL, NULL, 91.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (10, 10, '何琳', NULL, NULL, NULL, 88.50, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (11, 11, '何琳', NULL, NULL, NULL, 85.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (12, 12, '曹博', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (13, 13, '何琳', NULL, NULL, NULL, 82.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (14, 14, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (15, 15, '何琳', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (16, 16, '何琳', NULL, NULL, NULL, 93.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (17, 17, '曹博', NULL, NULL, NULL, 73.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (18, 18, '何琳', NULL, NULL, NULL, 86.00, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (19, 19, '曹博', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_interview_scores" VALUES (20, 20, 'system.auto', NULL, NULL, NULL, NULL, 95.00, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_login_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_login_logs";
CREATE TABLE "public"."dtlms_login_logs" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_login_logs_id_seq'::regclass),
  "username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "login_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "login_ip" varchar(64) COLLATE "pg_catalog"."default",
  "user_agent" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_login_logs
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_material_scores
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_material_scores";
CREATE TABLE "public"."dtlms_material_scores" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_material_scores_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "reviewer_assignment_id" int8 NOT NULL,
  "material_score" numeric(5,2),
  "recommendation_text" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_material_scores
-- ----------------------------
INSERT INTO "public"."dtlms_material_scores" VALUES (1, 27, 1, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (2, 26, 2, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (3, 16, 3, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (4, 17, 4, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (5, 19, 5, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (6, 15, 6, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (7, 14, 7, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (8, 13, 8, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (9, 1, 9, 91.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (10, 2, 10, 88.50, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (11, 3, 11, 85.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (12, 4, 12, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (13, 5, 13, 82.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (14, 6, 14, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (15, 7, 15, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (16, 8, 16, 93.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (17, 9, 17, 73.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (18, 10, 18, 86.00, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (19, 11, 19, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_material_scores" VALUES (20, 12, 20, NULL, '按模拟数据导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_notification_templates
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_notification_templates";
CREATE TABLE "public"."dtlms_notification_templates" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_notification_templates_id_seq'::regclass),
  "template_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "channel" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "title" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "content_template" text COLLATE "pg_catalog"."default" NOT NULL,
  "variables_schema" jsonb,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_notification_templates
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_operation_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_operation_logs";
CREATE TABLE "public"."dtlms_operation_logs" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_operation_logs_id_seq'::regclass),
  "operator_username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "operator_role" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "module_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "entity_id" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "action" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "old_value" jsonb,
  "new_value" jsonb,
  "request_ip" varchar(64) COLLATE "pg_catalog"."default",
  "result" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'success'::character varying,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_operation_logs
-- ----------------------------
INSERT INTO "public"."dtlms_operation_logs" VALUES (179, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:03:34+08', '2026-04-23 13:03:34+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (178, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:02:58+08', '2026-04-23 13:02:58+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (177, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:01:59+08', '2026-04-23 13:01:59+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (176, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 12:09:15+08', '2026-04-23 12:09:15+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (175, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 12:02:07+08', '2026-04-23 12:02:07+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (174, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 12:01:46+08', '2026-04-23 12:01:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (173, '18615768209', 'runtime_seed', '招生管理', '报名申请', '27', '新增', NULL, '{"summary": "新增报名申请 罗凯"}', '127.0.0.1', 'success', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (172, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 12:01:03+08', '2026-04-23 12:01:03+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (171, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 12:01:02+08', '2026-04-23 12:01:02+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (170, '13521297322', 'runtime_seed', '学生门户', '报名提交', '20', '提交报名', NULL, '{"summary": "学生 李小玉 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 11:51:21+08', '2026-04-23 11:51:21+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (169, '13521297322', 'runtime_seed', '学生门户', '报名提交', '20', '提交报名', NULL, '{"summary": "学生 李小玉 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 11:50:46+08', '2026-04-23 11:50:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (168, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:50:46+08', '2026-04-23 11:50:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (167, '13521297322', 'runtime_seed', '学生门户', '报名提交', '20', '提交报名', NULL, '{"summary": "学生 李小玉 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 11:50:26+08', '2026-04-23 11:50:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (166, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:50:26+08', '2026-04-23 11:50:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (165, '13521297322', 'runtime_seed', '学生门户', '报名提交', '20', '提交报名', NULL, '{"summary": "学生 李小玉 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 11:50:06+08', '2026-04-23 11:50:06+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (164, '13521297322', 'runtime_seed', '学生门户', '报名提交', '20', '提交报名', NULL, '{"summary": "学生 李小玉 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 11:49:45+08', '2026-04-23 11:49:45+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (163, '13521297322', 'runtime_seed', '招生管理', '报名申请', '26', '新增', NULL, '{"summary": "新增报名申请 李小玉"}', '127.0.0.1', 'success', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (162, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:49:14+08', '2026-04-23 11:49:14+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (161, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:49:04+08', '2026-04-23 11:49:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (160, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:47:35+08', '2026-04-23 11:47:35+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (159, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:45:18+08', '2026-04-23 11:45:18+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (158, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 11:44:41+08', '2026-04-23 11:44:41+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (52, '18615768209', 'runtime_seed', '学生门户', '找回密码', '1', '重置密码', NULL, '{"summary": "学生 罗凯 重置门户密码"}', '127.0.0.1', 'success', '2026-04-22 01:55:10+08', '2026-04-22 01:55:10+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (51, '18615768209', 'runtime_seed', '学生门户', '找回密码', '1', '重置密码', NULL, '{"summary": "学生 罗凯 重置门户密码"}', '127.0.0.1', 'success', '2026-04-22 01:53:19+08', '2026-04-22 01:53:19+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (48, 'admin', 'runtime_seed', '个人空间', '个人资料', 'admin', '编辑', NULL, '{"summary": "更新个人资料 系统管理员"}', '127.0.0.1', 'success', '2026-04-21 16:20:42+08', '2026-04-21 16:20:42+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (47, 'admin', 'runtime_seed', '个人空间', '个人资料', 'admin', '编辑', NULL, '{"summary": "更新个人资料 系统管理员"}', '127.0.0.1', 'success', '2026-04-21 16:19:49+08', '2026-04-21 16:19:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (45, '15908833765', 'runtime_seed', '学生门户', '门户注册', '16', '注册', NULL, '{"summary": "学生 王珊 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 11:39:49+08', '2026-04-21 11:39:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (37, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:25:16+08', '2026-04-21 02:25:16+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (36, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:16:01+08', '2026-04-21 02:16:01+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (35, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:15:32+08', '2026-04-21 02:15:32+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (34, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:12:40+08', '2026-04-21 02:12:40+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (33, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '新增研究中心', NULL, '{"summary": "新增研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:12:12+08', '2026-04-21 02:12:12+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (32, '132786107897', 'runtime_seed', '招生管理', '报名申请', '19', '新增', NULL, '{"summary": "新增报名申请 门户联调考生"}', '127.0.0.1', 'success', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (31, '132786107897', 'runtime_seed', '学生门户', '门户注册', '15', '注册', NULL, '{"summary": "学生 门户联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 02:06:08+08', '2026-04-21 02:06:08+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (30, '13100000001', 'runtime_seed', '学生门户', '门户注册', '14', '注册', NULL, '{"summary": "学生 中文考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 02:05:20+08', '2026-04-21 02:05:20+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (29, '131300757986', 'runtime_seed', '学生门户', '门户注册', '13', '注册', NULL, '{"summary": "学生 门户联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 02:03:50+08', '2026-04-21 02:03:50+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (28, '139836871113', 'runtime_seed', '招生管理', '报名申请', '18', '新增', NULL, '{"summary": "新增报名申请 ??????"}', '127.0.0.1', 'success', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (27, '139836871113', 'runtime_seed', '学生门户', '门户注册', '12', '注册', NULL, '{"summary": "学生 ?????? 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 02:01:55+08', '2026-04-21 02:01:55+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (26, '138610893902', 'runtime_seed', '招生管理', '报名申请', '17', '新增', NULL, '{"summary": "新增报名申请 Portal Smoke User"}', '127.0.0.1', 'success', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (25, '138610893902', 'runtime_seed', '学生门户', '门户注册', '11', '注册', NULL, '{"summary": "学生 Portal Smoke User 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:58:09+08', '2026-04-21 01:58:09+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (24, '139602805956', 'runtime_seed', '学生门户', '门户注册', '10', '注册', NULL, '{"summary": "学生 Portal Smoke User 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:57:43+08', '2026-04-21 01:57:43+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (23, '136449765890', 'runtime_seed', '招生管理', '报名申请', '16', '新增', NULL, '{"summary": "新增报名申请 联调考生"}', '127.0.0.1', 'success', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (22, '136449765890', 'runtime_seed', '学生门户', '门户注册', '9', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:53:47+08', '2026-04-21 01:53:47+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (21, '131406454328', 'runtime_seed', '学生门户', '门户注册', '8', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:52:04+08', '2026-04-21 01:52:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (20, '138363035504', 'runtime_seed', '学生门户', '门户注册', '7', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:51:00+08', '2026-04-21 01:51:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (19, '135988852152', 'runtime_seed', '学生门户', '门户注册', '6', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:44:32+08', '2026-04-21 01:44:32+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (18, '135759274417', 'runtime_seed', '学生门户', '门户注册', '5', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:37:03+08', '2026-04-21 01:37:03+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (17, '133972320247', 'runtime_seed', '学生门户', '门户注册', '4', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 01:36:26+08', '2026-04-21 01:36:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (16, '13920260421', 'runtime_seed', '学生门户', '门户注册', '3', '注册', NULL, '{"summary": "学生 联调考生 完成门户注册"}', '127.0.0.1', 'success', '2026-04-21 00:11:54+08', '2026-04-21 00:11:54+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (15, '18615768208', 'runtime_seed', '学生门户', '门户注册', '2', '注册', NULL, '{"summary": "学生 张三 完成门户注册"}', '127.0.0.1', 'success', '2026-04-20 14:13:07+08', '2026-04-20 14:13:07+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (14, '18615768209', 'runtime_seed', '学生门户', '门户注册', '1', '注册', NULL, '{"summary": "学生 罗凯 完成门户注册"}', '127.0.0.1', 'success', '2026-04-13 23:55:00+08', '2026-04-13 23:55:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (13, 'admin', 'runtime_seed', '招生管理', '报名申请', '15', '导入', NULL, '{"summary": "导入报名申请 在线联调0410132736"}', '127.0.0.1', 'success', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (12, 'admin', 'runtime_seed', '招生管理', '报名申请', '14', '导入', NULL, '{"summary": "导入报名申请 联调考生0410132613"}', '127.0.0.1', 'success', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (11, 'admin', 'runtime_seed', '招生管理', '报名申请', '13', '导入', NULL, '{"summary": "导入报名申请 联调考生0410131457"}', '127.0.0.1', 'success', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (10, 'zhou.qing', 'runtime_seed', '流程中心', '论文主档', 'SWSQSP202604090002', '复核通过', NULL, '{"summary": "周晴 执行 学位申请审批 - 复核通过"}', '127.0.0.1', 'success', '2026-04-09 20:15:26+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (9, 'xu.sutian', 'runtime_seed', '流程中心', '论文主档', 'SWSQSP202604090002', '提交送审', NULL, '{"summary": "徐素天 执行 学位申请审批 - 提交送审"}', '127.0.0.1', 'success', '2026-04-09 20:15:15+08', '2026-04-09 20:15:15+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (8, 'xu.sutian', 'runtime_seed', '学位管理', '论文主档', '6', '新增', NULL, '{"summary": "新增论文 沈知遥"}', '127.0.0.1', 'success', '2026-04-09 20:15:05+08', '2026-04-09 20:15:05+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (7, 'zhou.qing', 'runtime_seed', '流程中心', '论文主档', 'SWSQSP202604090001', '复核通过', NULL, '{"summary": "周晴 执行 学位申请审批 - 复核通过"}', '127.0.0.1', 'success', '2026-04-09 20:14:35+08', '2026-04-09 20:14:35+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (6, 'xu.sutian', 'runtime_seed', '流程中心', '论文主档', 'SWSQSP202604090001', '提交送审', NULL, '{"summary": "徐素天 执行 学位申请审批 - 提交送审"}', '127.0.0.1', 'success', '2026-04-09 20:14:25+08', '2026-04-09 20:14:25+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (5, 'xu.sutian', 'runtime_seed', '学位管理', '论文主档', '5', '新增', NULL, '{"summary": "新增论文 沈知遥"}', '127.0.0.1', 'success', '2026-04-09 20:14:15+08', '2026-04-09 20:14:15+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (4, 'admin', 'runtime_seed', '招生管理', '招生计划', '5', '新增', NULL, '{"summary": "新增招生计划 2027 春季招生计划"}', '127.0.0.1', 'success', '2026-04-09 19:48:48+08', '2026-04-09 19:48:48+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (1, 'admin', 'runtime_seed', '系统治理', '角色权限', 'role-2', '授权', NULL, '{"summary": "为导师角色补充流程处理权限。"}', '127.0.0.1', 'success', '2026-04-06 09:00:00+08', '2026-04-06 09:00:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (2, 'liu.ya', 'runtime_seed', '培养管理', '科研报告', 'KYBGSY202604070001', '审阅通过', NULL, '{"summary": "导师完成陈一鸣科研报告审阅。"}', '127.0.0.1', 'success', '2026-04-06 23:00:00+08', '2026-04-06 23:00:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (3, 'zhou.qing', 'runtime_seed', '学位管理', '论文主档', 'SWSQSP202604070002', '复核', NULL, '{"summary": "学位秘书推进论文送审流程。"}', '127.0.0.1', 'success', '2026-04-07 03:00:00+08', '2026-04-07 03:00:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (38, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:27:49+08', '2026-04-21 02:27:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (39, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '7', '新增研究中心', NULL, '{"summary": "新增研究中心 联调研究中心-1776709847"}', '127.0.0.1', 'success', '2026-04-21 02:30:47+08', '2026-04-21 02:30:47+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (40, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '7', '编辑研究中心', NULL, '{"summary": "更新研究中心 联调研究中心-1776709847-更新"}', '127.0.0.1', 'success', '2026-04-21 02:30:48+08', '2026-04-21 02:30:48+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (41, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '7', '删除研究中心', NULL, '{"summary": "删除研究中心 联调研究中心-1776709847-更新"}', '127.0.0.1', 'success', '2026-04-21 02:30:48+08', '2026-04-21 02:30:48+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (42, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:32:22+08', '2026-04-21 02:32:22+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (43, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:32:29+08', '2026-04-21 02:32:29+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (44, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 02:32:33+08', '2026-04-21 02:32:33+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (46, 'admin', 'runtime_seed', '学生管理', '研究中心主数据', '6', '编辑研究中心', NULL, '{"summary": "更新研究中心 人工智能安全研究中心"}', '127.0.0.1', 'success', '2026-04-21 15:40:04+08', '2026-04-21 15:40:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (49, 'admin', 'runtime_seed', '个人空间', '个人资料', 'admin', '编辑', NULL, '{"summary": "更新个人资料 系统管理员"}', '127.0.0.1', 'success', '2026-04-21 16:25:28+08', '2026-04-21 16:25:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (50, 'admin', 'runtime_seed', '个人空间', '个人资料', 'admin', '编辑', NULL, '{"summary": "更新个人资料 系统管理员"}', '127.0.0.1', 'success', '2026-04-21 16:29:39+08', '2026-04-21 16:29:39+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (53, '18615768209', 'runtime_seed', '学生门户', '找回密码', '1', '重置密码', NULL, '{"summary": "学生 罗凯 重置门户密码"}', '127.0.0.1', 'success', '2026-04-22 02:03:56+08', '2026-04-22 02:03:56+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (54, 'admin', 'runtime_seed', '系统治理', '系统用户', '10', '新建账号', NULL, '{"summary": "新建系统账号 性能测试账号"}', '127.0.0.1', 'success', '2026-04-22 02:22:27+08', '2026-04-22 02:22:27+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (55, 'perf.tmp.1776795747', 'runtime_seed', '系统治理', '系统用户', 'perf.tmp.1776795747', '重置密码', NULL, '{"summary": "更新账号 perf.tmp.1776795747 的登录密码"}', '127.0.0.1', 'success', '2026-04-22 02:22:28+08', '2026-04-22 02:22:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (56, 'admin', 'runtime_seed', '系统治理', '系统用户', '10', '删除账号', NULL, '{"summary": "删除系统账号 性能测试账号"}', '127.0.0.1', 'success', '2026-04-22 02:22:28+08', '2026-04-22 02:22:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (57, 'admin', 'runtime_seed', '学生管理', '注册学生', '16', '停用账号', NULL, '{"summary": "停用注册学生账号 王珊"}', '127.0.0.1', 'success', '2026-04-22 02:23:44+08', '2026-04-22 02:23:44+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (58, 'admin', 'runtime_seed', '学生管理', '注册学生', '16', '启用账号', NULL, '{"summary": "启用注册学生账号 王珊"}', '127.0.0.1', 'success', '2026-04-22 02:23:44+08', '2026-04-22 02:23:44+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (59, 'admin', 'runtime_seed', '学生管理', '注册学生', '16', '重置密码', NULL, '{"summary": "重置注册学生密码 王珊"}', '127.0.0.1', 'success', '2026-04-22 02:23:44+08', '2026-04-22 02:23:44+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (60, 'admin', 'runtime_seed', '学生管理', '注册学生', '16', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 王珊"}', '127.0.0.1', 'success', '2026-04-22 02:23:44+08', '2026-04-22 02:23:44+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (61, 'admin', 'runtime_seed', '系统治理', '角色', '8', '新建角色', NULL, '{"summary": "新建角色 性能测试角色"}', '127.0.0.1', 'success', '2026-04-22 02:26:51+08', '2026-04-22 02:26:51+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (62, 'admin', 'runtime_seed', '系统治理', '系统用户', '11', '新建账号', NULL, '{"summary": "新建系统账号 角色联动测试用户"}', '127.0.0.1', 'success', '2026-04-22 02:26:51+08', '2026-04-22 02:26:51+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (63, 'admin', 'runtime_seed', '系统治理', '角色', '8', '调整权限', NULL, '{"summary": "更新角色 性能测试角色V2 的权限配置"}', '127.0.0.1', 'success', '2026-04-22 02:26:51+08', '2026-04-22 02:26:51+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (64, 'admin', 'runtime_seed', '系统治理', '系统用户', '11', '删除账号', NULL, '{"summary": "删除系统账号 角色联动测试用户"}', '127.0.0.1', 'success', '2026-04-22 02:26:52+08', '2026-04-22 02:26:52+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (65, 'admin', 'runtime_seed', '系统治理', '角色', '8', '删除角色', NULL, '{"summary": "删除角色 性能测试角色V2"}', '127.0.0.1', 'success', '2026-04-22 02:26:52+08', '2026-04-22 02:26:52+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (66, 'admin', 'runtime_seed', '审批中心', '审批任务', '38', '新增', NULL, '{"summary": "新增审批任务 性能验证手工任务"}', '127.0.0.1', 'success', '2026-04-22 02:28:10+08', '2026-04-22 02:28:10+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (67, 'admin', 'runtime_seed', '审批中心', '审批任务', '38', '编辑', NULL, '{"summary": "更新审批任务 性能验证手工任务-更新"}', '127.0.0.1', 'success', '2026-04-22 02:28:10+08', '2026-04-22 02:28:10+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (68, 'admin', 'runtime_seed', '审批中心', '审批任务', '38', '删除', NULL, '{"summary": "删除审批任务 性能验证手工任务-更新"}', '127.0.0.1', 'success', '2026-04-22 02:28:11+08', '2026-04-22 02:28:11+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (69, 'admin', 'runtime_seed', '招生管理', '招生计划', '6', '新增', NULL, '{"summary": "新增招生计划 性能验证计划1776796165"}', '127.0.0.1', 'success', '2026-04-22 02:29:25+08', '2026-04-22 02:29:25+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (70, 'admin', 'runtime_seed', '招生管理', '招生计划', '6', '编辑', NULL, '{"summary": "更新招生计划 性能验证计划1776796165-更新"}', '127.0.0.1', 'success', '2026-04-22 02:29:26+08', '2026-04-22 02:29:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (71, 'admin', 'runtime_seed', '培养管理', '培养方案', '19', '登记方案', NULL, '{"summary": "登记培养方案 性能培养方案"}', '127.0.0.1', 'success', '2026-04-22 02:51:49+08', '2026-04-22 02:51:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (72, 'admin', 'runtime_seed', '培养管理', '培养方案', '19', '维护方案', NULL, '{"summary": "维护培养方案 性能培养方案"}', '127.0.0.1', 'success', '2026-04-22 02:51:49+08', '2026-04-22 02:51:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (73, 'admin', 'runtime_seed', '培养管理', '培养方案', '19', '删除方案', NULL, '{"summary": "删除培养方案 性能培养方案"}', '127.0.0.1', 'success', '2026-04-22 02:51:50+08', '2026-04-22 02:51:50+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (74, 'admin', 'runtime_seed', '学位管理', '盲审意见', '5', '新增', NULL, '{"summary": "新增盲审意见 评审专家A"}', '127.0.0.1', 'success', '2026-04-22 02:51:50+08', '2026-04-22 02:51:50+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (75, 'admin', 'runtime_seed', '学位管理', '盲审意见', '5', '编辑', NULL, '{"summary": "更新盲审意见 评审专家A"}', '127.0.0.1', 'success', '2026-04-22 02:51:50+08', '2026-04-22 02:51:50+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (76, 'admin', 'runtime_seed', '培养管理', '科研报告', '8', '维护报告', NULL, '{"summary": "维护科研报告 江若溪"}', '127.0.0.1', 'success', '2026-04-22 02:54:20+08', '2026-04-22 02:54:20+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (77, 'admin', 'runtime_seed', '培养管理', '外出研修', '4', '维护研修', NULL, '{"summary": "维护外出研修 孟书恒"}', '127.0.0.1', 'success', '2026-04-22 02:54:20+08', '2026-04-22 02:54:20+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (78, 'admin', 'runtime_seed', '学位管理', '论文主档', '6', '编辑', NULL, '{"summary": "更新论文 沈知遥"}', '127.0.0.1', 'success', '2026-04-22 02:54:21+08', '2026-04-22 02:54:21+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (79, 'perf.creator', 'runtime_seed', '培养管理', '科研报告', '9', '登记报告', NULL, '{"summary": "登记科研报告 流程性能验证"}', '127.0.0.1', 'success', '2026-04-22 02:57:36+08', '2026-04-22 02:57:36+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (80, 'perf.advisor', 'runtime_seed', '流程中心', '科研报告', 'KYBGSY202604220001', '审阅通过', NULL, '{"summary": "perf.advisor 执行 科研报告审阅 - 审阅通过"}', '127.0.0.1', 'success', '2026-04-22 02:57:37+08', '2026-04-22 02:57:37+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (81, 'admin', 'runtime_seed', '系统治理', '审计策略', '5', '新建策略', NULL, '{"summary": "新建审计策略 性能策略1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:58:59+08', '2026-04-22 02:58:59+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (82, 'admin', 'runtime_seed', '系统治理', '审计策略', '5', '维护策略', NULL, '{"summary": "更新审计策略 性能策略1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:58:59+08', '2026-04-22 02:58:59+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (83, 'admin', 'runtime_seed', '系统治理', '审计策略', '5', '删除策略', NULL, '{"summary": "删除审计策略 性能策略1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:59:00+08', '2026-04-22 02:59:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (84, 'admin', 'runtime_seed', '系统治理', '集成链路', '4', '新建链路', NULL, '{"summary": "新建集成链路 性能链路1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:59:00+08', '2026-04-22 02:59:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (85, 'admin', 'runtime_seed', '系统治理', '集成链路', '4', '维护链路', NULL, '{"summary": "更新集成链路 性能链路1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:59:00+08', '2026-04-22 02:59:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (86, 'admin', 'runtime_seed', '系统治理', '集成链路', '4', '删除链路', NULL, '{"summary": "删除集成链路 性能链路1776797939"}', '127.0.0.1', 'success', '2026-04-22 02:59:01+08', '2026-04-22 02:59:01+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (87, '139be009f7d', 'runtime_seed', '学生门户', '门户注册', '17', '注册', NULL, '{"summary": "学生 性能回归be009f7d 完成门户注册"}', '127.0.0.1', 'success', '2026-04-22 09:24:01+08', '2026-04-22 09:24:01+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (88, '139be009f7d', 'runtime_seed', '学生门户', '申请草稿', '17', '保存草稿', NULL, '{"summary": "学生 性能回归be009f7d 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 09:24:01+08', '2026-04-22 09:24:01+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (89, '139be009f7d', 'runtime_seed', '招生管理', '报名申请', '20', '新增', NULL, '{"summary": "新增报名申请 性能回归be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (90, '139be009f7d', 'runtime_seed', '学生门户', '报名提交', '17', '提交报名', NULL, '{"summary": "学生 性能回归be009f7d 提交报名申请"}', '127.0.0.1', 'success', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (91, 'admin', 'runtime_seed', '招生管理', '报名申请', '21', '新增', NULL, '{"summary": "新增报名申请 直建be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (92, 'admin', 'runtime_seed', '招生管理', '报名申请', '21', '编辑', NULL, '{"summary": "更新报名申请 直建更新be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (93, 'admin', 'runtime_seed', '招生管理', '报名申请', '22', '导入', NULL, '{"summary": "导入报名申请 导入be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (94, 'admin', 'runtime_seed', '招生管理', '报名申请', '21', '删除', NULL, '{"summary": "删除报名申请 直建更新be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (95, 'admin', 'runtime_seed', '招生管理', '报名申请', '22', '删除', NULL, '{"summary": "删除报名申请 导入be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (96, 'admin', 'runtime_seed', '招生管理', '报名申请', '20', '删除', NULL, '{"summary": "删除报名申请 性能回归be009f7d"}', '127.0.0.1', 'success', '2026-04-22 09:24:05+08', '2026-04-22 09:24:05+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (97, '13952d69275', 'runtime_seed', '学生门户', '门户注册', '18', '注册', NULL, '{"summary": "学生 性能回归52d69275 完成门户注册"}', '127.0.0.1', 'success', '2026-04-22 09:25:27+08', '2026-04-22 09:25:27+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (98, '13952d69275', 'runtime_seed', '学生门户', '申请草稿', '18', '保存草稿', NULL, '{"summary": "学生 性能回归52d69275 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 09:25:27+08', '2026-04-22 09:25:27+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (99, '13952d69275', 'runtime_seed', '招生管理', '报名申请', '23', '新增', NULL, '{"summary": "新增报名申请 性能回归52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (100, '13952d69275', 'runtime_seed', '学生门户', '报名提交', '18', '提交报名', NULL, '{"summary": "学生 性能回归52d69275 提交报名申请"}', '127.0.0.1', 'success', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (101, 'admin', 'runtime_seed', '招生管理', '报名申请', '24', '新增', NULL, '{"summary": "新增报名申请 直建52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (102, 'admin', 'runtime_seed', '招生管理', '报名申请', '24', '编辑', NULL, '{"summary": "更新报名申请 直建更新52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (103, 'admin', 'runtime_seed', '招生管理', '报名申请', '25', '导入', NULL, '{"summary": "导入报名申请 导入52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (104, 'admin', 'runtime_seed', '招生管理', '报名申请', '24', '删除', NULL, '{"summary": "删除报名申请 直建更新52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (105, 'admin', 'runtime_seed', '招生管理', '报名申请', '25', '删除', NULL, '{"summary": "删除报名申请 导入52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:31+08', '2026-04-22 09:25:31+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (106, 'admin', 'runtime_seed', '招生管理', '报名申请', '23', '删除', NULL, '{"summary": "删除报名申请 性能回归52d69275"}', '127.0.0.1', 'success', '2026-04-22 09:25:31+08', '2026-04-22 09:25:31+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (107, 'admin', 'runtime_seed', '学生管理', '学生主档', '19', '新增', NULL, '{"summary": "新增学生 性能验证学生"}', '127.0.0.1', 'success', '2026-04-22 09:32:33+08', '2026-04-22 09:32:33+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (108, 'admin', 'runtime_seed', '学生管理', '学生主档', '19', '编辑', NULL, '{"summary": "更新学生 性能验证学生-更新"}', '127.0.0.1', 'success', '2026-04-22 09:32:33+08', '2026-04-22 09:32:33+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (109, 'admin', 'runtime_seed', '学生管理', '学生主档', '19', '删除', NULL, '{"summary": "删除学生 性能验证学生-更新"}', '127.0.0.1', 'success', '2026-04-22 09:32:33+08', '2026-04-22 09:32:33+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (110, 'admin', 'runtime_seed', '学生管理', '学生主档', '20', '新增', NULL, '{"summary": "新增学生 性能验证学生8952d6ab"}', '127.0.0.1', 'success', '2026-04-22 09:33:31+08', '2026-04-22 09:33:31+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (111, 'admin', 'runtime_seed', '学生管理', '学生主档', '20', '编辑', NULL, '{"summary": "更新学生 性能验证学生更新8952d6ab"}', '127.0.0.1', 'success', '2026-04-22 09:33:32+08', '2026-04-22 09:33:32+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (112, 'admin', 'runtime_seed', '学生管理', '学生主档', '20', '删除', NULL, '{"summary": "删除学生 性能验证学生更新8952d6ab"}', '127.0.0.1', 'success', '2026-04-22 09:33:32+08', '2026-04-22 09:33:32+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (113, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 10:06:30+08', '2026-04-22 10:06:30+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (114, 'admin', 'runtime_seed', '个人空间', '个人资料', 'admin', '编辑', NULL, '{"summary": "更新个人资料 系统管理员"}', '127.0.0.1', 'success', '2026-04-22 13:12:05+08', '2026-04-22 13:12:05+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (115, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 13:34:31+08', '2026-04-22 13:34:31+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (116, 'admin', 'runtime_seed', '学生管理', '学生主档', '18', '编辑', NULL, '{"summary": "更新学生 陆承泽"}', '127.0.0.1', 'success', '2026-04-22 13:47:00+08', '2026-04-22 13:47:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (117, 'admin', 'runtime_seed', '学生管理', '学生主档', '18', '编辑', NULL, '{"summary": "更新学生 陆承泽"}', '127.0.0.1', 'success', '2026-04-22 13:47:06+08', '2026-04-22 13:47:06+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (118, '13908237925', 'runtime_seed', '学生门户', '门户注册', '19', '注册', NULL, '{"summary": "学生 罗凯 完成门户注册"}', '127.0.0.1', 'success', '2026-04-22 15:16:42+08', '2026-04-22 15:16:42+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (119, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '重置密码', NULL, '{"summary": "重置注册学生密码 罗凯"}', '127.0.0.1', 'success', '2026-04-22 15:39:34+08', '2026-04-22 15:39:34+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (120, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '重置密码', NULL, '{"summary": "重置注册学生密码 罗凯"}', '127.0.0.1', 'success', '2026-04-22 16:29:37+08', '2026-04-22 16:29:37+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (121, '18615768209', 'runtime_seed', '学生门户', '找回密码', '1', '重置密码', NULL, '{"summary": "学生 罗凯 重置门户密码"}', '127.0.0.1', 'success', '2026-04-22 18:05:59+08', '2026-04-22 18:05:59+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (122, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 18:32:49+08', '2026-04-22 18:32:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (123, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 18:37:05+08', '2026-04-22 18:37:05+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (124, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 19:20:03+08', '2026-04-22 19:20:03+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (125, '132786107897', 'runtime_seed', '学生门户', '申请草稿', '15', '保存草稿', NULL, '{"summary": "学生 门户联调考生 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 19:32:02+08', '2026-04-22 19:32:02+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (126, '13100000001', 'runtime_seed', '学生门户', '申请草稿', '14', '保存草稿', NULL, '{"summary": "学生 中文考生 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 19:32:54+08', '2026-04-22 19:32:54+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (127, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 19:34:17+08', '2026-04-22 19:34:17+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (128, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-22 19:54:29+08', '2026-04-22 19:54:29+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (129, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 01:33:31+08', '2026-04-23 01:33:31+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (130, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 01:34:09+08', '2026-04-23 01:34:09+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (131, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 01:43:21+08', '2026-04-23 01:43:21+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (132, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 01:43:46+08', '2026-04-23 01:43:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (133, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 01:49:04+08', '2026-04-23 01:49:04+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (134, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 01:52:29+08', '2026-04-23 01:52:29+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (135, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 01:53:11+08', '2026-04-23 01:53:11+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (136, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 01:55:42+08', '2026-04-23 01:55:42+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (137, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 01:56:23+08', '2026-04-23 01:56:23+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (138, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 02:00:38+08', '2026-04-23 02:00:38+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (139, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '重置密码', NULL, '{"summary": "重置注册学生密码 罗凯"}', '127.0.0.1', 'success', '2026-04-23 02:00:48+08', '2026-04-23 02:00:48+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (140, '18615768209', 'runtime_seed', '学生门户', '个人空间', '1', '修改密码', NULL, '{"summary": "学生 罗凯 在个人空间修改密码"}', '127.0.0.1', 'success', '2026-04-23 02:01:21+08', '2026-04-23 02:01:21+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (141, 'admin', 'runtime_seed', '学生管理', '注册学生', '1', '发送邮件', NULL, '{"summary": "向注册学生发送邮件 罗凯"}', '127.0.0.1', 'success', '2026-04-23 02:07:10+08', '2026-04-23 02:07:10+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (142, 'admin', 'runtime_seed', '学生管理', '学生主档', '14', '编辑', NULL, '{"summary": "更新学生 江若溪"}', '127.0.0.1', 'success', '2026-04-23 02:07:38+08', '2026-04-23 02:07:38+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (143, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 02:11:11+08', '2026-04-23 02:11:11+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (144, 'admin', 'runtime_seed', '招生管理', '报名申请', '18', '删除', NULL, '{"summary": "删除报名申请 ??????"}', '127.0.0.1', 'success', '2026-04-23 02:12:12+08', '2026-04-23 02:12:12+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (145, 'admin', 'runtime_seed', '招生管理', '报名申请', '18', '删除', NULL, '{"summary": "删除报名申请 ??????"}', '127.0.0.1', 'success', '2026-04-23 02:18:15+08', '2026-04-23 02:18:15+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (146, 'admin', 'runtime_seed', '招生管理', '报名申请', '19', '编辑', NULL, '{"summary": "更新报名申请 门户联调考生"}', '127.0.0.1', 'success', '2026-04-23 02:18:36+08', '2026-04-23 02:18:36+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (147, 'admin', 'runtime_seed', '招生管理', '报名申请', '19', '编辑', NULL, '{"summary": "更新报名申请 门户联调考生"}', '127.0.0.1', 'success', '2026-04-23 02:19:23+08', '2026-04-23 02:19:23+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (148, 'admin', 'runtime_seed', '招生管理', '报名申请', '17', '编辑', NULL, '{"summary": "更新报名申请 Portal Smoke User"}', '127.0.0.1', 'success', '2026-04-23 02:52:45+08', '2026-04-23 02:52:45+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (149, 'admin', 'runtime_seed', '招生管理', '报名申请', '19', '编辑', NULL, '{"summary": "更新报名申请 测试管理保存"}', '127.0.0.1', 'success', '2026-04-23 02:53:39+08', '2026-04-23 02:53:39+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (150, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 03:40:25+08', '2026-04-23 03:40:25+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (151, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 03:40:28+08', '2026-04-23 03:40:28+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (152, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 03:40:33+08', '2026-04-23 03:40:33+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (153, '18615768209', 'runtime_seed', '学生门户', '申请草稿', '1', '保存草稿', NULL, '{"summary": "学生 罗凯 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 03:40:46+08', '2026-04-23 03:40:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (154, '13521297322', 'runtime_seed', '学生门户', '门户注册', '20', '注册', NULL, '{"summary": "学生 李小玉 完成门户注册"}', '127.0.0.1', 'success', '2026-04-23 09:20:19+08', '2026-04-23 09:20:19+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (155, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 09:28:16+08', '2026-04-23 09:28:16+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (156, '13521297322', 'runtime_seed', '学生门户', '申请草稿', '20', '保存草稿', NULL, '{"summary": "学生 李小玉 保存报名草稿"}', '127.0.0.1', 'success', '2026-04-23 09:28:46+08', '2026-04-23 09:28:46+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (157, '18918001537', 'runtime_seed', '学生门户', '门户注册', '21', '注册', NULL, '{"summary": "学生 牟沿霖 完成门户注册"}', '127.0.0.1', 'success', '2026-04-23 10:28:25+08', '2026-04-23 10:28:25+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (180, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:06:49+08', '2026-04-23 13:06:49+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (181, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:07:02+08', '2026-04-23 13:07:02+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (182, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:08:00+08', '2026-04-23 13:08:00+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (189, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:15:08+08', '2026-04-23 13:15:08+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (190, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:15:26+08', '2026-04-23 13:15:26+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (191, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:15:37+08', '2026-04-23 13:15:37+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (192, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:37:54+08', '2026-04-23 13:37:54+08');
INSERT INTO "public"."dtlms_operation_logs" VALUES (193, '18615768209', 'runtime_seed', '学生门户', '报名提交', '1', '提交报名', NULL, '{"summary": "学生 罗凯 提交报名申请"}', '127.0.0.1', 'success', '2026-04-23 13:43:22+08', '2026-04-23 13:43:22+08');

-- ----------------------------
-- Table structure for dtlms_outbound_studies
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_outbound_studies";
CREATE TABLE "public"."dtlms_outbound_studies" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_outbound_studies_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "advisor_id" int8 NOT NULL,
  "study_type" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "destination" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date NOT NULL,
  "approval_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'submitted'::character varying,
  "expected_outcome" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "business_key" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of dtlms_outbound_studies
-- ----------------------------
INSERT INTO "public"."dtlms_outbound_studies" VALUES (1, 7, 1, '联合培养', '新加坡国立大学', '2026-03-01', '2026-08-31', 'submitted', '完成联合培养课题与月度交流汇报。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'WCYXSP202604070001');
INSERT INTO "public"."dtlms_outbound_studies" VALUES (2, 8, 3, '访学交流', '香港科技大学', '2026-02-15', '2026-07-30', 'submitted', '完成知识图谱跨语种研究。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'WCYXSP202604070002');
INSERT INTO "public"."dtlms_outbound_studies" VALUES (3, 3, 2, '企业研修', '中控技术研究院', '2026-05-01', '2026-07-31', 'submitted', '研修目标与阶段任务需进一步明确。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'WCYXSP202604070003');
INSERT INTO "public"."dtlms_outbound_studies" VALUES (4, 15, 2, '学术会议', '深圳', '2026-05-18', '2026-05-22', 'submitted', '参加流程治理与数字教育论坛。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'WCYXSP202604070004');

-- ----------------------------
-- Table structure for dtlms_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_permissions";
CREATE TABLE "public"."dtlms_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_permissions_id_seq'::regclass),
  "permission_code" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "permission_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "module_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_permissions
-- ----------------------------
INSERT INTO "public"."dtlms_permissions" VALUES (1, 'dashboard:read', '查看驾驶舱', 'dashboard', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2, 'recruitment:read', '查看招生工作台', 'recruitment', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (3, 'recruitment:write', '维护招生流程', 'recruitment', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (4, 'students:read', '查看学生主数据', 'students', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (5, 'students:write', '维护学生主数据', 'students', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (6, 'training:read', '查看培养过程', 'training', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (7, 'training:write', '维护培养过程', 'training', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (8, 'degree:read', '查看学位过程', 'degree', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (9, 'degree:write', '维护学位过程', 'degree', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (10, 'audit:read', '查看审计日志与同步策略', 'system', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2181, 'audit:write', '维护审计日志与同步策略', 'system', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2182, 'system:read', '查看系统治理', 'system', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2183, 'system:write', '维护系统治理', 'system', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2184, 'workflow:read', '查看流程中心', 'workflow', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_permissions" VALUES (2185, 'workflow:write', '处理流程任务', 'workflow', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_achievement_records
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_achievement_records";
CREATE TABLE "public"."dtlms_portal_application_achievement_records" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_achievement_records_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "achievement_type" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "paper_title" varchar(255) COLLATE "pg_catalog"."default",
  "author_order" varchar(32) COLLATE "pg_catalog"."default",
  "journal_or_conference" varchar(255) COLLATE "pg_catalog"."default",
  "publish_or_index_month" varchar(16) COLLATE "pg_catalog"."default",
  "award_name" varchar(255) COLLATE "pg_catalog"."default",
  "awarding_organization" varchar(255) COLLATE "pg_catalog"."default",
  "award_level" varchar(128) COLLATE "pg_catalog"."default",
  "award_year" varchar(16) COLLATE "pg_catalog"."default",
  "responsibility_text" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_achievement_records
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_portal_application_attachments
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_attachments";
CREATE TABLE "public"."dtlms_portal_application_attachments" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_attachments_id_seq'::regclass),
  "portal_student_id" int8,
  "application_id" int8,
  "owner_type" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "owner_id" int8,
  "attachment_category" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "file_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "file_url" text COLLATE "pg_catalog"."default" NOT NULL,
  "file_type" varchar(32) COLLATE "pg_catalog"."default",
  "file_size" int8,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_attachments
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (1, 11, 17, 'personal_statement', 17, 'resume', 'resume-75163dc510e24a04b6c90c0eaf77f253.pdf', '/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf', 'pdf', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (2, 9, 16, 'personal_statement', 16, 'resume', 'resume-5221465b8e7d4c1693dd1274df5b6fac.pdf', '/portal-attachments/uploads/student-9/resume/resume-5221465b8e7d4c1693dd1274df5b6fac.pdf', 'pdf', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (3, 15, 19, 'portal_application', 19, 'personal_statement', 'resume-1361bf8942e240b6afa9af9eb42236c5.pdf', '/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf', 'pdf', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (4, 15, 19, 'personal_statement', 19, 'resume', 'resume-1361bf8942e240b6afa9af9eb42236c5.pdf', '/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (5, NULL, 15, 'personal_statement', 15, 'resume', 'ps.pdf', 'ps.pdf', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (6, NULL, 14, 'personal_statement', 14, 'resume', 'ps.pdf', 'ps.pdf', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (7, NULL, 13, 'personal_statement', 13, 'resume', 'statement.pdf', 'statement.pdf', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (8, NULL, 15, 'application', 15, 'material_list', 'checklist.zip', 'checklist.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (9, NULL, 14, 'application', 14, 'material_list', 'checklist.zip', 'checklist.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (10, NULL, 13, 'application', 13, 'material_list', 'materials.zip', 'materials.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (12, 20, 26, 'application_material', 2, '报名材料', 'ZSLQSP202604230009.zip', '/materials/ZSLQSP202604230009.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (13, 9, 16, 'application_material', 3, '报名材料', 'ZSLQSP202604210004.zip', '/materials/ZSLQSP202604210004.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (14, 11, 17, 'application_material', 4, '报名材料', 'ZSLQSP202604210005.zip', '/materials/ZSLQSP202604210005.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (15, 15, 19, 'application_material', 5, '报名材料', 'ZSLQSP202604210007.zip', '/materials/ZSLQSP202604210007.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (16, NULL, 15, 'application_material', 6, '报名材料', 'checklist.zip', 'checklist.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (17, NULL, 14, 'application_material', 7, '报名材料', 'checklist.zip', 'checklist.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (18, NULL, 13, 'application_material', 8, '报名材料', 'materials.zip', 'materials.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (19, NULL, 1, 'application_material', 9, '报名材料', 'ZSLQSP202604070001.zip', '/materials/ZSLQSP202604070001.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (20, NULL, 2, 'application_material', 10, '报名材料', 'ZSLQSP202604070002.zip', '/materials/ZSLQSP202604070002.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (21, NULL, 3, 'application_material', 11, '报名材料', 'ZSLQSP202604070003.zip', '/materials/ZSLQSP202604070003.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (22, NULL, 4, 'application_material', 12, '报名材料', 'ZSLQSP202604070004.zip', '/materials/ZSLQSP202604070004.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (23, NULL, 5, 'application_material', 13, '报名材料', 'ZSLQSP202604070005.zip', '/materials/ZSLQSP202604070005.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (24, NULL, 6, 'application_material', 14, '报名材料', 'ZSLQSP202604070006.zip', '/materials/ZSLQSP202604070006.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (25, NULL, 7, 'application_material', 15, '报名材料', 'ZSLQSP202604070007.zip', '/materials/ZSLQSP202604070007.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (26, NULL, 8, 'application_material', 16, '报名材料', 'ZSLQSP202604070008.zip', '/materials/ZSLQSP202604070008.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (27, NULL, 9, 'application_material', 17, '报名材料', 'ZSLQSP202604070009.zip', '/materials/ZSLQSP202604070009.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (28, NULL, 10, 'application_material', 18, '报名材料', 'ZSLQSP202604070010.zip', '/materials/ZSLQSP202604070010.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (29, NULL, 11, 'application_material', 19, '报名材料', 'ZSLQSP202604070011.zip', '/materials/ZSLQSP202604070011.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (30, NULL, 12, 'application_material', 20, '报名材料', 'ZSLQSP202604070012.zip', '/materials/ZSLQSP202604070012.zip', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_attachments" VALUES (36, 1, 27, 'application_material', 28, '报名材料', 'ZSLQSP202604230010.zip', '/materials/ZSLQSP202604230010.zip', NULL, NULL, '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_declarations
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_declarations";
CREATE TABLE "public"."dtlms_portal_application_declarations" (
  "application_id" int8 NOT NULL,
  "has_read_declaration" bool NOT NULL DEFAULT false,
  "declaration_text" text COLLATE "pg_catalog"."default",
  "progress_snapshot" jsonb,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_declarations
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (17, 't', 'I confirm all submitted information is true.', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (16, 't', '本人承诺以上填写内容真实、准确。', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (19, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (26, 't', '我已同意并仔细阅读使用条款和隐私政策。', '{"family_count": 2, "english_count": 0, "practice_count": 0, "education_count": 1, "preference_count": 2, "achievement_count": 0}', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (27, 't', '我已同意并仔细阅读使用条款和隐私政策。', '{"family_count": 2, "english_count": 0, "practice_count": 0, "education_count": 1, "preference_count": 1, "achievement_count": 0}', '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:22+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (10, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (9, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (8, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (7, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (6, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (5, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (4, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (3, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (2, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (1, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (13, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (14, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (15, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (12, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_declarations" VALUES (11, 'f', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_education_experiences
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_education_experiences";
CREATE TABLE "public"."dtlms_portal_application_education_experiences" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_education_experiences_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "sort_order" int4 NOT NULL DEFAULT 1,
  "education_stage" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "start_month" varchar(16) COLLATE "pg_catalog"."default",
  "end_month" varchar(16) COLLATE "pg_catalog"."default",
  "school_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "major_name" varchar(255) COLLATE "pg_catalog"."default",
  "average_score" varchar(64) COLLATE "pg_catalog"."default",
  "gpa" varchar(32) COLLATE "pg_catalog"."default",
  "ranking" varchar(64) COLLATE "pg_catalog"."default",
  "verifier_name" varchar(128) COLLATE "pg_catalog"."default",
  "verifier_phone" varchar(32) COLLATE "pg_catalog"."default",
  "transcript_attachment_url" text COLLATE "pg_catalog"."default",
  "degree_certificate_attachment_url" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_education_experiences
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_education_experiences" VALUES (1, 17, 1, 'Master', NULL, NULL, 'Jiangnan University', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_education_experiences" VALUES (2, 16, 1, '硕士', NULL, NULL, '江南大学', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_education_experiences" VALUES (3, 26, 1, '硕士', '2017-09', '2020-07', '北京大学', '1', '1', '1', '1', '1', '1', NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_education_experiences" VALUES (8, 27, 1, '硕士', '2018-07', '2022-09', '电子科技大学', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_english_proficiencies
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_english_proficiencies";
CREATE TABLE "public"."dtlms_portal_application_english_proficiencies" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_english_proficiencies_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "exam_name" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "score_text" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "certificate_attachment_url" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_english_proficiencies
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_portal_application_family_members
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_family_members";
CREATE TABLE "public"."dtlms_portal_application_family_members" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_family_members_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "member_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "relation_type" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "employer_name" varchar(255) COLLATE "pg_catalog"."default",
  "job_title" varchar(128) COLLATE "pg_catalog"."default",
  "contact_phone" varchar(32) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_family_members
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (1, 17, 'Parent A', 'Father', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (2, 17, 'Parent B', 'Mother', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (3, 16, '张父', '父亲', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (4, 16, '张母', '母亲', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (5, 26, '1', '父亲', '1', NULL, '1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (6, 26, '1', '母亲', '1', NULL, '1', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (15, 27, '罗道全', '父亲', NULL, NULL, NULL, '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:23.07594+08');
INSERT INTO "public"."dtlms_portal_application_family_members" VALUES (16, 27, '张丛秀', '母亲', NULL, NULL, NULL, '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_personal_statements
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_personal_statements";
CREATE TABLE "public"."dtlms_portal_application_personal_statements" (
  "application_id" int8 NOT NULL,
  "personal_statement_text" text COLLATE "pg_catalog"."default",
  "ai_problem_statement" text COLLATE "pg_catalog"."default",
  "ai_industry_opinion" text COLLATE "pg_catalog"."default",
  "resume_attachment_url" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_personal_statements
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (26, '11', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (16, '真实联调提交', NULL, NULL, '/portal-attachments/uploads/student-9/resume/resume-5221465b8e7d4c1693dd1274df5b6fac.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (17, 'Portal smoke submission', NULL, NULL, '/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (19, '门户联调提交', NULL, NULL, '/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (27, '测试', NULL, NULL, NULL, '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:22+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (15, '个人简介第一段。', '复杂场景下的模型可信推理。', '我不同意仅凭更大规模数据就能解决全部泛化问题。', 'ps.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (14, '个人简介第一段。', '复杂场景下的模型可信推理。', '我不同意仅凭更大规模数据就能解决全部泛化问题。', 'ps.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_personal_statements" VALUES (13, '个人简介第一段。', '面向复杂场景的多模态推理可靠性问题。', '我不同意只要扩大参数规模就必然提升系统可靠性的行业共识。', 'statement.pdf', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_portal_application_practice_experiences
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_practice_experiences";
CREATE TABLE "public"."dtlms_portal_application_practice_experiences" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_practice_experiences_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "start_month" varchar(16) COLLATE "pg_catalog"."default",
  "end_month" varchar(16) COLLATE "pg_catalog"."default",
  "organization_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "position_name" varchar(128) COLLATE "pg_catalog"."default",
  "responsibility_text" text COLLATE "pg_catalog"."default",
  "verifier_name" varchar(128) COLLATE "pg_catalog"."default",
  "verifier_phone" varchar(32) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_practice_experiences
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_portal_application_preferences
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_application_preferences";
CREATE TABLE "public"."dtlms_portal_application_preferences" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_application_preferences_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "preference_order" int4 NOT NULL,
  "research_center_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "advisor_name" varchar(128) COLLATE "pg_catalog"."default",
  "is_optional" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_portal_application_preferences
-- ----------------------------
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (4, 26, 1, '智能制造团队', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (2, 16, 1, '智能制造团队', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (1, 17, 1, '智能制造团队', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (10, 19, 1, '智能制造团队', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (11, 1, 1, '智能制造', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (12, 2, 1, '机器人控制', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (13, 3, 1, '工业互联网', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (14, 4, 1, '视觉检测', '曹博', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (15, 5, 1, '数据智能', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (16, 6, 1, '数字孪生', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (17, 7, 1, '工业软件', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (18, 8, 1, '软件工程', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (19, 9, 1, '模型驱动开发', '曹博', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (5, 26, 2, '机器人应用团队', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (27, 1, 2, '机器学习', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (28, 2, 2, '工业互联网', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (29, 3, 2, '知识图谱', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (30, 4, 2, '数据智能', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (31, 5, 2, '数字孪生', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (32, 6, 2, '软件工程', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (33, 7, 2, '机器学习', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (34, 8, 2, '工业互联网', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (35, 9, 2, '知识图谱', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (36, 10, 2, '数据智能', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (37, 11, 2, '数字孪生', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (375, 27, 1, '智能制造团队', '刘亚', 'f', '2026-04-23 13:43:23.07594+08', '2026-04-23 13:43:22+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (20, 10, 1, '工业数据治理', '何琳', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (21, 11, 1, '知识图谱', '曹博', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (22, 12, 1, '机器学习', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (23, 15, 1, '智能科学', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (24, 14, 1, '智能科学', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (25, 13, 1, '人工智能', '刘亚', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (38, 12, 2, '软件工程', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (39, 15, 2, '模式识别', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (40, 14, 2, '模式识别', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_portal_application_preferences" VALUES (41, 13, 2, '计算机视觉', NULL, 't', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_portal_student_profiles
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_student_profiles";
CREATE TABLE "public"."dtlms_portal_student_profiles" (
  "portal_student_id" int8 NOT NULL,
  "full_name_pinyin" varchar(128) COLLATE "pg_catalog"."default",
  "gender" varchar(16) COLLATE "pg_catalog"."default",
  "birth_date" varchar(32) COLLATE "pg_catalog"."default",
  "ethnic_group" varchar(64) COLLATE "pg_catalog"."default",
  "native_place" varchar(128) COLLATE "pg_catalog"."default",
  "political_status" varchar(64) COLLATE "pg_catalog"."default",
  "marital_status" varchar(32) COLLATE "pg_catalog"."default",
  "religious_belief" varchar(128) COLLATE "pg_catalog"."default",
  "id_type" varchar(64) COLLATE "pg_catalog"."default",
  "mailing_address" text COLLATE "pg_catalog"."default",
  "emergency_contact_name" varchar(128) COLLATE "pg_catalog"."default",
  "emergency_contact_phone" varchar(32) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "profile_photo_url" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_portal_student_profiles
-- ----------------------------
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (13, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (12, NULL, '?', '1999-01-01', NULL, '????', '????', NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (5, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (14, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-22 19:32:54+08', '/portal-attachments/uploads/student-test/profile_photo/test.png');
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (11, NULL, 'Male', '1999-01-01', NULL, 'Wuxi Jiangsu', 'PartyMember', NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (10, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (9, NULL, '男', '1999-01-01', NULL, '江苏无锡', '中共党员', NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (8, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (7, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (6, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (1, 'LUOKAI', '男', NULL, '汉族', NULL, '群众', NULL, NULL, '居民身份证', '上海市浦东新区惠南镇听达路185弄5号304室', '张丛秀', '13682137095', '2026-04-21 16:14:01+08', '2026-04-23 13:43:22+08', '/portal-attachments/uploads/student-1/profile_photo/profile_photo-525a6aaea02a4d0b83bb1b518df91983.png');
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (3, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-21 16:14:01+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (16, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-22 02:23:44+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (17, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-22 09:24:01+08', '2026-04-22 09:24:02+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (18, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-22 09:25:27+08', '2026-04-22 09:25:28+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (19, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-22 15:16:42+08', NULL);
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (15, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-22 19:32:02+08', '/portal-attachments/uploads/student-test/profile_photo/test.png');
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (20, 'li xiaoyu', '女', NULL, '汉族', NULL, '中共党员', NULL, NULL, '居民身份证', '1', '1', '1', '2026-04-23 13:03:35.578384+08', '2026-04-23 12:01:02+08', '/portal-attachments/uploads/student-20/profile_photo/profile_photo-7a069d5d7f0f487e85b05482baf7438e.jpg');
INSERT INTO "public"."dtlms_portal_student_profiles" VALUES (21, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 10:28:25+08', NULL);

-- ----------------------------
-- Table structure for dtlms_portal_students
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_portal_students";
CREATE TABLE "public"."dtlms_portal_students" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_portal_students_id_seq'::regclass),
  "full_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "phone_number" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "id_number" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "graduation_school" varchar(255) COLLATE "pg_catalog"."default",
  "highest_degree" varchar(64) COLLATE "pg_catalog"."default",
  "intended_field" varchar(128) COLLATE "pg_catalog"."default",
  "political_status" varchar(64) COLLATE "pg_catalog"."default",
  "selected_plan_id" int8,
  "selected_team_name" varchar(128) COLLATE "pg_catalog"."default",
  "selected_advisor_name" varchar(128) COLLATE "pg_catalog"."default",
  "self_evaluation" text COLLATE "pg_catalog"."default",
  "submitted_at" timestamptz(6),
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "password_hash" varchar(255) COLLATE "pg_catalog"."default",
  "gender" varchar(16) COLLATE "pg_catalog"."default",
  "birth_date" varchar(32) COLLATE "pg_catalog"."default",
  "ethnic_group" varchar(64) COLLATE "pg_catalog"."default",
  "native_place" varchar(128) COLLATE "pg_catalog"."default",
  "marital_status" varchar(32) COLLATE "pg_catalog"."default",
  "religious_belief" varchar(128) COLLATE "pg_catalog"."default",
  "id_type" varchar(64) COLLATE "pg_catalog"."default",
  "mailing_address" text COLLATE "pg_catalog"."default",
  "english_level" varchar(128) COLLATE "pg_catalog"."default",
  "family_info" text COLLATE "pg_catalog"."default",
  "education_experience" text COLLATE "pg_catalog"."default",
  "practice_experience" text COLLATE "pg_catalog"."default",
  "personal_profile" text COLLATE "pg_catalog"."default",
  "recommendation_notes" text COLLATE "pg_catalog"."default",
  "personal_statement_text" text COLLATE "pg_catalog"."default",
  "signed_agreement" bool NOT NULL DEFAULT false,
  "account_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '启用'::character varying
)
;

-- ----------------------------
-- Records of dtlms_portal_students
-- ----------------------------
INSERT INTO "public"."dtlms_portal_students" VALUES (13, '门户联调考生', '131300757986', 'portal.254277869@example.com', '32000019998800027', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$/R8DYEzJ2TtHCAFA6P3fuw$7zcNBFXV.xuARaL1fU9gJ.Hj66GRNbzirLdAjwi1TAg', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (12, '??????', '139836871113', 'portal.338335439@example.com', '32000019993682138', '????', '??', '智能制造团队', '????', 5, '智能制造团队', '刘亚', NULL, '2026-04-21 02:02:08+08', '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$eq81RsgZA4BQak3JuRdibA$JZbIHUI5.W6kCwIodPwH96wu0z5u8eHGPACZu1b6zx0', '?', '1999-01-01', NULL, '????', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "??", "relation_type": "??"}, {"member_name": "??", "relation_type": "??"}]', '[{"sort_order": 1, "education_stage": "??", "school_name": "????"}]', NULL, NULL, NULL, '??????', 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (5, '联调考生', '135759274417', 'portal.271598992@example.com', '32000019998353673', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$4tw75/wf47z33lvrHQMAYA$xHlSDvoay8SUxvyoX9jlj435woefjRCN6RJxQqSizLA', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (14, '中文考生', '13100000001', 'portal.test@example.com', '3200001999123456', NULL, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-22 19:32:54+08', '$pbkdf2-sha256$29000$nBOidE7J2Vvr3bs3phSiNA$cG.wdf10RyfuzTRKRVLVJ9V9IsnKYOtPZQATe6jSz6Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (11, 'Portal Smoke User', '138610893902', 'portal.520532517@example.com', '32000019994456783', 'Jiangnan University', 'Master', '智能制造团队', 'PartyMember', 5, '智能制造团队', '刘亚', NULL, '2026-04-21 01:58:19+08', '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$gJCyFqL0vnfundOaU4rReg$9242ot2pOB2niZjGxe0wgu6HWQe6m4PQN9QJpU9oQJg', 'Male', '1999-01-01', NULL, 'Wuxi Jiangsu', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "Parent A", "relation_type": "Father"}, {"member_name": "Parent B", "relation_type": "Mother"}]', '[{"sort_order": 1, "education_stage": "Master", "school_name": "Jiangnan University"}]', NULL, NULL, NULL, 'Portal smoke submission', 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (10, 'Portal Smoke User', '139602805956', 'portal.651275151@example.com', '32000019993427012', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$R8g5xxjjfI.xdo6xFmLsPQ$upSLPB/2rlwNk8bPOJue8vLZ.vgl3bwy2K.s1dtae/w', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (9, '联调考生', '136449765890', 'portal.550629792@example.com', '32000019999145401', '江南大学', '硕士', '智能制造团队', '中共党员', 5, '智能制造团队', '刘亚', NULL, '2026-04-21 01:53:57+08', '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$41wrhTBmjNHam7N27j2nlA$p1REy2Vark0YRzS4UkTsNsMD2dkKNU.Nm6lEZLpghk4', '男', '1999-01-01', NULL, '江苏无锡', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "张父", "relation_type": "父亲"}, {"member_name": "张母", "relation_type": "母亲"}]', '[{"sort_order": 1, "education_stage": "硕士", "school_name": "江南大学"}]', NULL, NULL, NULL, '真实联调提交', 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (8, '联调考生', '131406454328', 'portal.157628501@example.com', '32000019995416599', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$kFKK8T4HAICQEoKQslbqPQ$NycXdbcknLzgPWzhsmQsSJX22.Ehwi4jIQbCrzX9STc', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (7, '联调考生', '138363035504', 'portal.150206797@example.com', '32000019998271744', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$H2MsJaSUshbiPEfoXet9Lw$UG4rZF2TosmON0mAFlp7ndThngQGzlCr8i81RzghvA0', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (6, '联调考生', '135988852152', 'portal.863164580@example.com', '32000019991480547', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$fw9BaM2ZU8r5H2Psvfdeiw$dsEp8UNs94xpEFCkzl5417oqMgZMHFMPT9exfEXTtQQ', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (4, '联调考生', '133972320247', 'portal.916429449@example.com', '32000019992615150', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$EoLQOufcm5PSmjPmfE8phQ$XB3Jc/u2Gg5MTPsanc.nCaxclr0ano.3EATmOet3HS4', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (3, '联调考生', '13920260421', 'portal.20260421001153@example.com', '320000199901011234', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$aE3pHQNAiPFe632vNUZISQ$dVvded79NYS4Epe0LAGPTEloO6DRvJdFR/RWC6.9YJs', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (2, '张三', '18615768208', 'zsan@cotong.com', '510104197911301878', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-21 16:14:01+08', '$pbkdf2-sha256$29000$5jznXItRau39vxcCwDhnLA$eSpx40C9plY2DUDXlffwWdwXJUQTLrcoEPZutNidauQ', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (16, '王珊', '15908833765', 'wss@126.com', '510104197910111000', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-21 16:14:01+08', '2026-04-22 02:23:44+08', '$pbkdf2-sha256$29000$sJbSupeyFqLUGoMwRuhd6w$y1xzbm2tUcLMg.mbBw.ASOFAp.3Cy.0lEYbAVEYMZbo', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (17, '性能回归be009f7d', '139be009f7d', 'perf_be009f7d@example.com', '32010119900101be00', '回归测试大学', '硕士', '智能制造团队', NULL, 5, '智能制造团队', '刘亚', NULL, '2026-04-22 09:24:02+08', '2026-04-22 09:24:01+08', '2026-04-22 09:24:02+08', '$pbkdf2-sha256$29000$lFKqda7VWusdY6yV8v7/vw$V5umOb8mauV1s.1V5FW3B33h7cSZSpl05IhRK55L49Y', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (18, '性能回归52d69275', '13952d69275', 'perf_52d69275@example.com', '3201011990010152d6', '回归测试大学', '硕士', '智能制造团队', NULL, 5, '智能制造团队', '刘亚', NULL, '2026-04-22 09:25:28+08', '2026-04-22 09:25:27+08', '2026-04-22 09:25:28+08', '$pbkdf2-sha256$29000$bU3Jea8VgtB6L2XsfS9lbA$JCrgIBI4zU8kjU5M5V/G0rj821L9mF8mTyg98yxyzjw', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (19, '罗凯', '13908237925', 'lkai@cotong.com', '510104197911301877', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-22 15:16:42+08', '2026-04-22 15:16:42+08', '$pbkdf2-sha256$29000$qFXqnVNqjfE.p5RSilHqPQ$Mc26MBjuEeppBozWF8V5muhTxMs9zAU4Q7/5Vm0g4.Q', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (15, '门户联调考生', '132786107897', 'portal.606885427@example.com', '32000019997301982', NULL, NULL, NULL, NULL, 5, NULL, NULL, NULL, '2026-04-21 02:06:20+08', '2026-04-21 16:14:01+08', '2026-04-22 19:32:02+08', '$pbkdf2-sha256$29000$xxiDcE6JEUIoJcR4T8n5vw$1N0V1KgpQscHVLGlATKfVhnrowrjsb2/wYNKbjOBHm4', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (20, '李小玉', '13521297322', 'annieleexy@hotmail.com', '371326199602240040', '北京大学', '硕士', '智能制造团队', '中共党员', 5, '智能制造团队', '刘亚', NULL, '2026-04-23 11:51:21+08', '2026-04-23 09:20:19+08', '2026-04-23 12:01:02+08', '$pbkdf2-sha256$29000$aM35P.ecs5ZSqtWacw7BeA$QpFPFNFwLR3mX2SuNAoNh4k3ckVQEeEwNUMuf3xG1CY', '女', NULL, '汉族', NULL, NULL, NULL, '居民身份证', '1', NULL, '[{"member_name": "1", "relation_type": "父亲", "employer_name": "1", "contact_phone": "1"}, {"member_name": "1", "relation_type": "母亲", "employer_name": "1", "contact_phone": "1"}]', '[{"sort_order": 1, "education_stage": "硕士", "start_month": "2017-09", "end_month": "2020-07", "school_name": "北京大学", "major_name": "1", "average_score": "1", "gpa": "1", "ranking": "1", "verifier_name": "1", "verifier_phone": "1"}]', NULL, NULL, NULL, '11', 't', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (21, '牟沿霖', '18918001537', 'moupengfei11@163.com', '310105201403193216', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2026-04-23 10:28:25+08', '2026-04-23 10:28:25+08', '$pbkdf2-sha256$29000$2huDcE4JofQ.xzgHQAhBCA$COELNy02aDiro5y.abl.5dq.9qXf0OQ/g2TU12rPOkg', NULL, NULL, NULL, NULL, NULL, NULL, '居民身份证', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 'f', '启用');
INSERT INTO "public"."dtlms_portal_students" VALUES (1, '罗凯', '18615768209', 'lk139@126.com', '510104197911301879', '电子科技大学', '硕士', '智能制造团队', '群众', 5, '智能制造团队', '刘亚', '测试', '2026-04-23 13:43:22+08', '2026-04-21 16:14:01+08', '2026-04-23 13:43:22+08', '$pbkdf2-sha256$29000$iRECIOT8vzdGKAWA0Pqfsw$J0FkSN9r6D/JuwE/6LEObp07ar48ImHf1oIFozh3vxc', '男', NULL, '汉族', NULL, NULL, NULL, '居民身份证', '上海市浦东新区惠南镇听达路185弄5号304室', NULL, '[{"member_name": "罗道全", "relation_type": "父亲"}, {"member_name": "张丛秀", "relation_type": "母亲"}]', '[{"sort_order": 1, "education_stage": "硕士", "start_month": "2018-07", "end_month": "2022-09", "school_name": "电子科技大学"}]', NULL, NULL, NULL, '测试', 't', '启用');

-- ----------------------------
-- Table structure for dtlms_qualification_reviews
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_qualification_reviews";
CREATE TABLE "public"."dtlms_qualification_reviews" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_qualification_reviews_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "reviewer_username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "review_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "review_comment" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_qualification_reviews
-- ----------------------------
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (1, 27, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (2, 26, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (3, 16, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (4, 17, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (5, 19, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (6, 15, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (7, 14, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (8, 13, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (9, 1, '何琳', 'pending', '导入状态：同意录取', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (10, 2, '何琳', 'approved', '导入状态：预录取', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (11, 3, '何琳', 'approved', '导入状态：面试完成', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (12, 4, '曹博', 'pending', '导入状态：面试待安排', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (13, 5, '何琳', 'approved', '导入状态：材料评分中', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (14, 6, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (15, 7, '何琳', 'approved', '导入状态：资格审核通过', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (16, 8, '何琳', 'pending', '导入状态：同意录取', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (17, 9, '曹博', 'pending', '导入状态：不录取', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (18, 10, '何琳', 'approved', '导入状态：预录取', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (19, 11, '曹博', 'pending', '导入状态：面试待安排', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_qualification_reviews" VALUES (20, 12, 'system.auto', 'pending', '导入状态：报名已提交', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_recruitment_applications
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_recruitment_applications";
CREATE TABLE "public"."dtlms_recruitment_applications" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_recruitment_applications_id_seq'::regclass),
  "plan_id" int8 NOT NULL,
  "student_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "candidate_no" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "gender" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "graduation_school" varchar(255) COLLATE "pg_catalog"."default",
  "highest_degree" varchar(64) COLLATE "pg_catalog"."default",
  "intended_field_id" int8,
  "application_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'submitted'::character varying,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "business_key" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "review_round" varchar(64) COLLATE "pg_catalog"."default",
  "first_choice" varchar(255) COLLATE "pg_catalog"."default",
  "second_choice" varchar(255) COLLATE "pg_catalog"."default",
  "political_status" varchar(64) COLLATE "pg_catalog"."default",
  "marital_status" varchar(32) COLLATE "pg_catalog"."default",
  "religious_belief" varchar(128) COLLATE "pg_catalog"."default",
  "native_place" varchar(128) COLLATE "pg_catalog"."default",
  "phone_number" varchar(64) COLLATE "pg_catalog"."default",
  "email" varchar(255) COLLATE "pg_catalog"."default",
  "mailing_address" text COLLATE "pg_catalog"."default",
  "id_type" varchar(64) COLLATE "pg_catalog"."default",
  "id_number" varchar(128) COLLATE "pg_catalog"."default",
  "undergraduate_school" varchar(255) COLLATE "pg_catalog"."default",
  "accept_adjustment" varchar(16) COLLATE "pg_catalog"."default",
  "undergraduate_average_score" varchar(64) COLLATE "pg_catalog"."default",
  "undergraduate_gpa" varchar(64) COLLATE "pg_catalog"."default",
  "undergraduate_rank" varchar(64) COLLATE "pg_catalog"."default",
  "undergraduate_major" varchar(255) COLLATE "pg_catalog"."default",
  "graduate_average_score" varchar(64) COLLATE "pg_catalog"."default",
  "graduate_gpa" varchar(64) COLLATE "pg_catalog"."default",
  "graduate_rank" varchar(64) COLLATE "pg_catalog"."default",
  "graduate_major" varchar(255) COLLATE "pg_catalog"."default",
  "intended_advisor_name" varchar(128) COLLATE "pg_catalog"."default",
  "discovery_channel" text COLLATE "pg_catalog"."default",
  "graduate_school" varchar(255) COLLATE "pg_catalog"."default",
  "overseas_university_name" varchar(255) COLLATE "pg_catalog"."default",
  "overseas_master_university_name" varchar(255) COLLATE "pg_catalog"."default",
  "self_evaluation" text COLLATE "pg_catalog"."default",
  "applied_at" timestamptz(6),
  "research_problem" text COLLATE "pg_catalog"."default",
  "research_status_analysis" text COLLATE "pg_catalog"."default",
  "research_impact" text COLLATE "pg_catalog"."default",
  "ai_society_impact" text COLLATE "pg_catalog"."default",
  "dissenting_view" text COLLATE "pg_catalog"."default",
  "family_info" text COLLATE "pg_catalog"."default",
  "education_experience" text COLLATE "pg_catalog"."default",
  "practice_experience" text COLLATE "pg_catalog"."default",
  "personal_statement_text" text COLLATE "pg_catalog"."default",
  "student_activity_experience" text COLLATE "pg_catalog"."default",
  "personal_statement_attachment" text COLLATE "pg_catalog"."default",
  "material_list_attachment" text COLLATE "pg_catalog"."default",
  "supplementary_profile" text COLLATE "pg_catalog"."default",
  "portal_student_id" int8,
  "source_channel" varchar(64) COLLATE "pg_catalog"."default",
  "source_channel_other" varchar(255) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_recruitment_applications
-- ----------------------------
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (26, 5, '李小玉', 'ZSLQSP202604230009', '女', '北京大学', '硕士', 8, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604230009', NULL, '智能制造团队', '机器人应用团队', '中共党员', NULL, NULL, NULL, '13521297322', 'annieleexy@hotmail.com', '1', '居民身份证', '371326199602240040', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '刘亚', '实验室官网', NULL, NULL, NULL, NULL, '2026-04-23 11:51:21+08', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "1", "relation_type": "父亲", "employer_name": "1", "contact_phone": "1"}, {"member_name": "1", "relation_type": "母亲", "employer_name": "1", "contact_phone": "1"}]', '[{"sort_order": 1, "education_stage": "硕士", "start_month": "2017-09", "end_month": "2020-07", "school_name": "北京大学", "major_name": "1", "average_score": "1", "gpa": "1", "ranking": "1", "verifier_name": "1", "verifier_phone": "1"}]', NULL, '11', NULL, NULL, NULL, NULL, 20, '实验室官网', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (16, 5, '联调考生', 'ZSLQSP202604210004', '男', '江南大学', '硕士', 8, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604210004', NULL, '智能制造团队', NULL, '中共党员', NULL, NULL, '江苏无锡', '136449765890', 'portal.550629792@example.com', NULL, NULL, '32000019999145401', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '刘亚', '实验室官网', NULL, NULL, NULL, NULL, '2026-04-21 01:53:57+08', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "张父", "relation_type": "父亲"}, {"member_name": "张母", "relation_type": "母亲"}]', '[{"sort_order": 1, "education_stage": "硕士", "school_name": "江南大学"}]', NULL, '真实联调提交', NULL, '/portal-attachments/uploads/student-9/resume/resume-5221465b8e7d4c1693dd1274df5b6fac.pdf', NULL, NULL, 9, '实验室官网', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (17, 5, 'Portal Smoke User', 'ZSLQSP202604210005', 'Male', 'Jiangnan University', 'Master', 8, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604210005', '', '智能制造团队', '', 'PartyMember', '未婚', '无', 'Wuxi Jiangsu', '138610893902', 'portal.520532517@example.com', NULL, '居民身份证', '32000019994456783', '', '是', NULL, NULL, NULL, NULL, '', '', '', '', '刘亚', 'LabSite', '', '', '', '', '2026-04-21 01:58:19+08', NULL, '', '', '', NULL, '[{"member_name": "Parent A", "relation_type": "Father"}, {"member_name": "Parent B", "relation_type": "Mother"}]', '[{"sort_order": 1, "education_stage": "Master", "school_name": "Jiangnan University"}]', '', 'Portal smoke submission', '', '/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf', '', '', 11, 'LabSite', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (19, 5, '测试管理保存', 'ZSLQSP202604210007', '男', '江南大学', '硕士', 8, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604210007', '', '智能制造团队', '', '中共党员', '未婚', '无', '江苏无锡', '132786107897', 'portal.606885427@example.com', NULL, '居民身份证', '32000019997301982', '', '是', NULL, NULL, NULL, NULL, '', '', '', '', '刘亚', '实验室官网', '', '', '', '', '2026-04-21 02:06:20+08', NULL, '', '', '', NULL, '[{"member_name": "张父", "relation_type": "父亲"}, {"member_name": "张母", "relation_type": "母亲"}]', '[{"sort_order": 1, "education_stage": "硕士", "school_name": "江南大学"}]', '', '门户联调提交', '', '/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf', '', '', 15, '实验室官网', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (1, 1, '吴启程', 'ZSLQSP202604070001', '未知', '东南大学', '硕士', 7, 'admitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070001', '1轮次', '智能制造', '机器学习', '中共党员', '未婚', '无', '待补充', '13900020001', 'candidate01@mail.example.com', '待补充', '居民身份证', NULL, '东南大学', '是', NULL, NULL, NULL, '智能制造', NULL, NULL, NULL, '智能制造', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (2, 1, '沈清禾', 'ZSLQSP202604070002', '未知', '同济大学', '硕士', 10, 'pre_admitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070002', '1轮次', '机器人控制', '工业互联网', '共青团员', '未婚', '无', '待补充', '13900020002', 'candidate02@mail.example.com', '待补充', '居民身份证', NULL, '同济大学', '是', NULL, NULL, NULL, '机器人控制', NULL, NULL, NULL, '机器人控制', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (3, 1, '顾明睿', 'ZSLQSP202604070003', '未知', '华中科技大学', '硕士', 2, 'interviewed', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070003', '1轮次', '工业互联网', '知识图谱', '群众', '未婚', '无', '待补充', '13900020003', 'candidate03@mail.example.com', '待补充', '居民身份证', NULL, '华中科技大学', '是', NULL, NULL, NULL, '工业互联网', NULL, NULL, NULL, '工业互联网', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (4, 1, '周亦凡', 'ZSLQSP202604070004', '未知', '哈尔滨工业大学', '硕士', 14, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070004', '1轮次', '视觉检测', '数据智能', '中共预备党员', '未婚', '无', '待补充', '13900020004', 'candidate04@mail.example.com', '待补充', '居民身份证', NULL, '哈尔滨工业大学', '是', NULL, NULL, NULL, '视觉检测', NULL, NULL, NULL, '视觉检测', '曹博', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (27, 5, '罗凯', 'ZSLQSP202604230010', '男', '电子科技大学', '硕士', 8, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:43:22+08', 'ZSLQSP202604230010', NULL, '智能制造团队', NULL, '群众', NULL, NULL, NULL, '18615768209', 'lk139@126.com', '上海市浦东新区惠南镇听达路185弄5号304室', '居民身份证', '510104197911301879', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '刘亚', '实验室官网', NULL, NULL, NULL, '测试', '2026-04-23 13:43:22+08', NULL, NULL, NULL, NULL, NULL, '[{"member_name": "罗道全", "relation_type": "父亲"}, {"member_name": "张丛秀", "relation_type": "母亲"}]', '[{"sort_order": 1, "education_stage": "硕士", "start_month": "2018-07", "end_month": "2022-09", "school_name": "电子科技大学"}]', NULL, '测试', NULL, NULL, NULL, NULL, 1, '实验室官网', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (5, 1, '李静姝', 'ZSLQSP202604070005', '未知', '浙江大学', '硕士', 6, 'scoring', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070005', '1轮次', '数据智能', '数字孪生', '中共党员', '未婚', '无', '待补充', '13900020005', 'candidate05@mail.example.com', '待补充', '居民身份证', NULL, '浙江大学', '是', NULL, NULL, NULL, '数据智能', NULL, NULL, NULL, '数据智能', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (6, 1, '陈思远', 'ZSLQSP202604070006', '未知', '北京航空航天大学', '硕士', 5, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070006', '1轮次', '数字孪生', '软件工程', '共青团员', '未婚', '无', '待补充', '13900020006', 'candidate06@mail.example.com', '待补充', '居民身份证', NULL, '北京航空航天大学', '是', NULL, NULL, NULL, '数字孪生', NULL, NULL, NULL, '数字孪生', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (7, 2, '赵安歌', 'ZSLQSP202604070007', '未知', '南京大学', '硕士', 4, 'qualified', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070007', '2轮次', '工业软件', '机器学习', '群众', '未婚', '无', '待补充', '13900020007', 'candidate07@mail.example.com', '待补充', '居民身份证', NULL, '南京大学', '是', NULL, NULL, NULL, '工业软件', NULL, NULL, NULL, '工业软件', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (8, 2, '林知夏', 'ZSLQSP202604070008', '未知', '上海交通大学', '硕士', 15, 'admitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070008', '2轮次', '软件工程', '工业互联网', '中共预备党员', '未婚', '无', '待补充', '13900020008', 'candidate08@mail.example.com', '待补充', '居民身份证', NULL, '上海交通大学', '是', NULL, NULL, NULL, '软件工程', NULL, NULL, NULL, '软件工程', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (9, 2, '钱北辰', 'ZSLQSP202604070009', '未知', '西安交通大学', '硕士', 12, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070009', '2轮次', '模型驱动开发', '知识图谱', '中共党员', '未婚', '无', '待补充', '13900020009', 'candidate09@mail.example.com', '待补充', '居民身份证', NULL, '西安交通大学', '是', NULL, NULL, NULL, '模型驱动开发', NULL, NULL, NULL, '模型驱动开发', '曹博', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (10, 2, '韩知遇', 'ZSLQSP202604070010', '未知', '天津大学', '硕士', 3, 'pre_admitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070010', '2轮次', '工业数据治理', '数据智能', '共青团员', '未婚', '无', '待补充', '13900020010', 'candidate10@mail.example.com', '待补充', '居民身份证', NULL, '天津大学', '是', NULL, NULL, NULL, '工业数据治理', NULL, NULL, NULL, '工业数据治理', '何琳', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (11, 3, '朱安宁', 'ZSLQSP202604070011', '未知', '武汉大学', '硕士', 13, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070011', '3轮次', '知识图谱', '数字孪生', '群众', '未婚', '无', '待补充', '13900020011', 'candidate11@mail.example.com', '待补充', '居民身份证', NULL, '武汉大学', '是', NULL, NULL, NULL, '知识图谱', NULL, NULL, NULL, '知识图谱', '曹博', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (12, 3, '谢明远', 'ZSLQSP202604070012', '未知', '北京理工大学', '硕士', 11, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604070012', '3轮次', '机器学习', '软件工程', '中共预备党员', '未婚', '无', '待补充', '13900020012', 'candidate12@mail.example.com', '待补充', '居民身份证', NULL, '北京理工大学', '是', NULL, NULL, NULL, '机器学习', NULL, NULL, NULL, '机器学习', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (15, 5, '在线联调0410132736', 'ZSLQSP202604100004', '男', '浙江大学', '硕士', 9, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604100004', '第11轮', '智能科学', '模式识别', '中共党员', '未婚', '无', '上海', '13710132736', 'web_0410132736@example.com', '上海市徐汇区联调路11号', '居民身份证', '310115199901012736', '浙江大学', '是', '90.1', '3.88', '8/200', '计算机科学与技术', '92.3', '3.95', '3/80', '人工智能', '刘亚', '官网报名', '复旦大学', NULL, NULL, '具备扎实的研究训练基础。', '2026-04-10 15:00:00+08', '复杂场景下的模型可信推理。', '当前多集中于离线评测，真实世界泛化不足。', '将提升高风险行业的智能辅助可靠性。', 'AI 会深刻改变知识工作与流程自动化。', '我不同意仅凭更大规模数据就能解决全部泛化问题。', '家庭支持继续深造。', '本科浙江大学，硕士复旦大学。', '参与过科研项目与工程落地。', '个人简介第一段。', '组织过多次学术活动。', 'ps.pdf', 'checklist.zip', '个人简介第二段。', NULL, '官网报名', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (14, 5, '联调考生0410132613', 'ZSLQSP202604100003', '男', '浙江大学', '硕士', 9, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604100003', '第10轮', '智能科学', '模式识别', '中共党员', '未婚', '无', '上海', '13810132613', 'online_0410132613@example.com', '上海市浦东新区联调路10号', '居民身份证', '310115199901012613', '浙江大学', '是', '90.1', '3.88', '8/200', '计算机科学与技术', '92.3', '3.95', '3/80', '人工智能', '刘亚', '官网报名', '复旦大学', NULL, NULL, '具备扎实的研究训练基础。', '2026-04-10 15:00:00+08', '复杂场景下的模型可信推理。', '当前多集中于离线评测，真实世界泛化不足。', '将提升高风险行业的智能辅助可靠性。', 'AI 会深刻改变知识工作与流程自动化。', '我不同意仅凭更大规模数据就能解决全部泛化问题。', '家庭支持继续深造。', '本科浙江大学，硕士复旦大学。', '参与过科研项目与工程落地。', '个人简介第一段。', '组织过多次学术活动。', 'ps.pdf', 'checklist.zip', '个人简介第二段。', NULL, '官网报名', NULL);
INSERT INTO "public"."dtlms_recruitment_applications" VALUES (13, 5, '联调考生0410131457', 'ZSLQSP202604100001', '女', '东南大学', '硕士', 1, 'submitted', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'ZSLQSP202604100001', '第9轮', '人工智能', '计算机视觉', '共青团员', '未婚', '无', '江苏无锡', '13910131457', 'jointest_0410131457@example.com', '江苏省无锡市滨湖区测试路9号', '居民身份证', '320211199901011457', '东南大学', '是', '89.5', '3.82', '12/180', '软件工程', '91.2', '3.91', '5/60', '人工智能', '刘亚', '导师推荐', '上海交通大学', NULL, NULL, '具备较强科研潜力与工程落地能力。', '2026-04-10 14:00:00+08', '面向复杂场景的多模态推理可靠性问题。', '当前研究已覆盖通用基准，但在真实场景稳健性方面仍有明显短板。', '若能解决，将提升智能系统在教育与工业领域的可信应用水平。', 'AI 将持续影响高风险决策支持与知识生产流程。', '我不同意只要扩大参数规模就必然提升系统可靠性的行业共识。', '家庭稳定，支持继续攻读博士。', '2018-2022 东南大学 软件工程 本科；2022-2025 上海交通大学 人工智能 硕士。', '曾参与科研项目、企业联合课题与开源社区维护。', '个人简介第一段。', '担任研究生会学术部负责人，组织多场学术活动。', 'statement.pdf', 'materials.zip', '个人简介第二段。', NULL, '导师推荐', NULL);

-- ----------------------------
-- Table structure for dtlms_recruitment_plans
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_recruitment_plans";
CREATE TABLE "public"."dtlms_recruitment_plans" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_recruitment_plans_id_seq'::regclass),
  "plan_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "plan_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "academic_year" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "semester" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "start_date" timestamptz(6) NOT NULL,
  "end_date" timestamptz(6) NOT NULL,
  "target_quota" int4 NOT NULL DEFAULT 0,
  "plan_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'draft'::character varying,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "brochure_image_url" varchar(255) COLLATE "pg_catalog"."default",
  "plan_description" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_recruitment_plans
-- ----------------------------
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (5, 'PLAN-005', '2027 春季招生计划', '2027', '春', '2027-03-01 08:00:00+08', '2027-10-31 18:00:00+08', 30, 'admitting', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (1, 'PLAN-001', '2026 秋季博士招生', '2026', '秋', '2026-03-01 08:00:00+08', '2026-10-31 18:00:00+08', 36, 'published', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (2, 'PLAN-002', '2026 工程博士专项', '2026', '秋', '2026-03-01 08:00:00+08', '2026-10-31 18:00:00+08', 28, 'published', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (3, 'PLAN-003', '2026 智能制造联合培养', '2026', '秋', '2026-03-01 08:00:00+08', '2026-10-31 18:00:00+08', 18, 'admitting', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (4, 'PLAN-004', '2025 春季补录', '2025', '春', '2025-03-01 08:00:00+08', '2025-10-31 18:00:00+08', 8, 'closed', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, NULL);
INSERT INTO "public"."dtlms_recruitment_plans" VALUES (6, 'PLAN-006', '性能验证计划1776796165-更新', '2026-2027', '秋季学期', '2026-03-01 08:00:00+08', '2026-10-31 18:00:00+08', 0, 'admitting', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', NULL, '仅验证增量持久化-更新');

-- ----------------------------
-- Table structure for dtlms_research_fields
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_research_fields";
CREATE TABLE "public"."dtlms_research_fields" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_research_fields_id_seq'::regclass),
  "field_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "field_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_research_fields
-- ----------------------------
INSERT INTO "public"."dtlms_research_fields" VALUES (1, 'FIELD001', '人工智能', '人工智能方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (2, 'FIELD002', '工业互联网', '工业互联网方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (3, 'FIELD003', '工业数据治理', '工业数据治理方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (4, 'FIELD004', '工业软件', '工业软件方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (5, 'FIELD005', '数字孪生', '数字孪生方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (6, 'FIELD006', '数据智能', '数据智能方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (7, 'FIELD007', '智能制造', '智能制造方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (8, 'FIELD008', '智能制造团队', '智能制造团队方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (9, 'FIELD009', '智能科学', '智能科学方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (10, 'FIELD010', '机器人控制', '机器人控制方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (11, 'FIELD011', '机器学习', '机器学习方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (12, 'FIELD012', '模型驱动开发', '模型驱动开发方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (13, 'FIELD013', '知识图谱', '知识图谱方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (14, 'FIELD014', '视觉检测', '视觉检测方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_research_fields" VALUES (15, 'FIELD015', '软件工程', '软件工程方向', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_research_projects
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_research_projects";
CREATE TABLE "public"."dtlms_research_projects" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_research_projects_id_seq'::regclass),
  "project_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "project_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "principal_advisor_id" int8,
  "funding_amount" numeric(12,2),
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_research_projects
-- ----------------------------

-- ----------------------------
-- Table structure for dtlms_reviewer_assignments
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_reviewer_assignments";
CREATE TABLE "public"."dtlms_reviewer_assignments" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_reviewer_assignments_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "reviewer_username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "reviewer_role" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "assignment_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'assigned'::character varying,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_reviewer_assignments
-- ----------------------------
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (1, 27, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (2, 26, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (3, 16, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (4, 17, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (5, 19, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (6, 15, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (7, 14, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (8, 13, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (9, 1, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (10, 2, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (11, 3, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (12, 4, '曹博', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (13, 5, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (14, 6, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (15, 7, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (16, 8, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (17, 9, '曹博', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (18, 10, '何琳', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (19, 11, '曹博', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_reviewer_assignments" VALUES (20, 12, 'system.auto', 'reviewer', 'assigned', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_role_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_role_permissions";
CREATE TABLE "public"."dtlms_role_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_role_permissions_id_seq'::regclass),
  "role_id" int8 NOT NULL,
  "permission_id" int8 NOT NULL,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_role_permissions
-- ----------------------------
INSERT INTO "public"."dtlms_role_permissions" VALUES (1, 1, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (2, 2, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (3, 3, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (4, 4, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5, 5, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (6, 6, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (7, 8, 1, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (8, 1, 2, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (9, 4, 2, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (10, 5, 2, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (11, 1, 3, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (12, 1, 4, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (13, 3, 4, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (14, 6, 4, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (15, 8, 4, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (16, 1, 5, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (17, 1, 6, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (18, 3, 6, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (19, 6, 6, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (20, 1, 7, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (21, 1, 8, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (22, 3, 8, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (23, 1, 9, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (24, 1, 10, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (25, 8, 10, '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5433, 1740, 1, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5438, 5, 3, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5448, 3, 7, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5451, 1740, 8, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5453, 1740, 9, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5456, 1, 2181, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5457, 1, 2182, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5458, 1740, 2182, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5459, 1, 2183, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5460, 1, 2184, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5461, 3, 2184, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5462, 4, 2184, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5463, 5, 2184, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5464, 1740, 2184, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5465, 1, 2185, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5466, 3, 2185, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');
INSERT INTO "public"."dtlms_role_permissions" VALUES (5467, 1740, 2185, '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');

-- ----------------------------
-- Table structure for dtlms_roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_roles";
CREATE TABLE "public"."dtlms_roles" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_roles_id_seq'::regclass),
  "role_code" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "role_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_roles
-- ----------------------------
INSERT INTO "public"."dtlms_roles" VALUES (1, 'platform_admin', '平台管理员', '系统级配置与全链路治理', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (2, 'student', '博士生', '个人学习、培养与学位办理', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (3, 'advisor', '导师', '培养方案制定、报告审阅、答辩指导', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (4, 'recruit_reviewer', '评分人', '招生材料评审与推荐', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (5, 'interview_officer', '面试官', '面试分组、评分与校算', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (6, 'hrbp', '中心HRBP', '实习状态确认与过程监督', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (7, 'dormitory_guard', '公寓保障', '住宿与在离校状态配合', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (8, 'party_affairs', '党群负责人', '思政考核与资助资格审查', 'f', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_roles" VALUES (1740, 'secretary', '学位秘书', '学位流程复核、送审与归档管理', 'f', '2026-04-07 10:05:52.301911+08', '2026-04-07 10:05:52.301911+08');

-- ----------------------------
-- Table structure for dtlms_runtime_audit_policies
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_audit_policies";
CREATE TABLE "public"."dtlms_runtime_audit_policies" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_audit_policies
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_audit_policies" VALUES (1, '{"id": 1, "item": "登录与鉴权审计", "policy": "记录登录成功、失败、退出与令牌刷新。", "status": "启用"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_audit_policies" VALUES (2, '{"id": 2, "item": "流程审批留痕", "policy": "所有流程动作、意见、节点变更必须留痕。", "status": "启用"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_audit_policies" VALUES (3, '{"id": 3, "item": "主数据变更审计", "policy": "学生、团队、角色与字典变更需记录操作日志。", "status": "启用"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_audit_policies" VALUES (4, '{"id": 4, "item": "敏感数据导出控制", "policy": "导出包含联系方式与身份信息时需保留审计记录。", "status": "启用"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_counters
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_counters";
CREATE TABLE "public"."dtlms_runtime_counters" (
  "counter_name" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "counter_value" int8 NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_counters
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('outbound_studies', 4, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('theses', 6, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('sync_logs', 3, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('teams', 6, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('students', 20, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('roles', 8, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('system_users', 11, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('recruitment_applications', 27, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('workflow_tasks', 47, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('recruitment_plans', 6, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('training_plans', 19, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('thesis_reviews', 5, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('portal_students', 21, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('scientific_reports', 9, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('audit_policies', 5, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('integrations', 4, '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_counters" VALUES ('operation_logs', 193, '2026-04-23 13:15:06.120155+08');

-- ----------------------------
-- Table structure for dtlms_runtime_integrations
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_integrations";
CREATE TABLE "public"."dtlms_runtime_integrations" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_integrations
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_integrations" VALUES (1, '{"id": 1, "name": "招生系统主数据同步", "owner": "系统管理员", "status": "正常", "cadence": "实时 + 每日对账", "direction": "主数据导入 / 录取回传"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_integrations" VALUES (2, '{"id": 2, "name": "实验室 OA 事件同步", "owner": "杨琴", "status": "正常", "cadence": "实时事件 + 定时补偿", "direction": "考勤 / 门禁 / 请假同步"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_integrations" VALUES (3, '{"id": 3, "name": "飞书待办推送", "owner": "周晴", "status": "告警", "cadence": "实时", "direction": "待办通知 / 审批提醒 / 回执"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_operation_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_operation_logs";
CREATE TABLE "public"."dtlms_runtime_operation_logs" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_operation_logs
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (179, '{"id": 179, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:03:34", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (178, '{"id": 178, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:02:58", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (177, '{"id": 177, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:01:59", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (176, '{"id": 176, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 12:09:15", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (175, '{"id": 175, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 12:02:07", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (174, '{"id": 174, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 12:01:46", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (173, '{"id": 173, "action": "新增", "result": "success", "summary": "新增报名申请 罗凯", "entity_id": "27", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 12:01:25", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (172, '{"id": 172, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 12:01:03", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (171, '{"id": 171, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 12:01:02", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (170, '{"id": 170, "action": "提交报名", "result": "success", "summary": "学生 李小玉 提交报名申请", "entity_id": "20", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 11:51:21", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (169, '{"id": 169, "action": "提交报名", "result": "success", "summary": "学生 李小玉 提交报名申请", "entity_id": "20", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 11:50:46", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (168, '{"id": 168, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:50:46", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (167, '{"id": 167, "action": "提交报名", "result": "success", "summary": "学生 李小玉 提交报名申请", "entity_id": "20", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 11:50:26", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (166, '{"id": 166, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:50:26", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (165, '{"id": 165, "action": "提交报名", "result": "success", "summary": "学生 李小玉 提交报名申请", "entity_id": "20", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 11:50:06", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (164, '{"id": 164, "action": "提交报名", "result": "success", "summary": "学生 李小玉 提交报名申请", "entity_id": "20", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 11:49:45", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (163, '{"id": 163, "action": "新增", "result": "success", "summary": "新增报名申请 李小玉", "entity_id": "26", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 11:49:20", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (162, '{"id": 162, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:49:14", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (161, '{"id": 161, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:49:04", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (160, '{"id": 160, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:47:35", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (159, '{"id": 159, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:45:18", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (158, '{"id": 158, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 11:44:41", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (52, '{"id": 52, "action": "重置密码", "result": "success", "summary": "学生 罗凯 重置门户密码", "entity_id": "1", "entity_name": "找回密码", "module_name": "学生门户", "operated_at": "2026-04-22 01:55:10", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (51, '{"id": 51, "action": "重置密码", "result": "success", "summary": "学生 罗凯 重置门户密码", "entity_id": "1", "entity_name": "找回密码", "module_name": "学生门户", "operated_at": "2026-04-22 01:53:19", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (48, '{"id": 48, "action": "编辑", "result": "success", "summary": "更新个人资料 系统管理员", "entity_id": "admin", "entity_name": "个人资料", "module_name": "个人空间", "operated_at": "2026-04-21 16:20:42", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (47, '{"id": 47, "action": "编辑", "result": "success", "summary": "更新个人资料 系统管理员", "entity_id": "admin", "entity_name": "个人资料", "module_name": "个人空间", "operated_at": "2026-04-21 16:19:49", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (45, '{"id": 45, "action": "注册", "result": "success", "summary": "学生 王珊 完成门户注册", "entity_id": "16", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 11:39:49", "operator_username": "15908833765"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (37, '{"id": 37, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:25:16", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (36, '{"id": 36, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:16:01", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (35, '{"id": 35, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:15:32", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (34, '{"id": 34, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:12:40", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (33, '{"id": 33, "action": "新增研究中心", "result": "success", "summary": "新增研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:12:12", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (32, '{"id": 32, "action": "新增", "result": "success", "summary": "新增报名申请 门户联调考生", "entity_id": "19", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-21 02:06:20", "operator_username": "132786107897"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (31, '{"id": 31, "action": "注册", "result": "success", "summary": "学生 门户联调考生 完成门户注册", "entity_id": "15", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 02:06:08", "operator_username": "132786107897"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (30, '{"id": 30, "action": "注册", "result": "success", "summary": "学生 中文考生 完成门户注册", "entity_id": "14", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 02:05:20", "operator_username": "13100000001"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (29, '{"id": 29, "action": "注册", "result": "success", "summary": "学生 门户联调考生 完成门户注册", "entity_id": "13", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 02:03:50", "operator_username": "131300757986"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (28, '{"id": 28, "action": "新增", "result": "success", "summary": "新增报名申请 ??????", "entity_id": "18", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-21 02:02:08", "operator_username": "139836871113"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (27, '{"id": 27, "action": "注册", "result": "success", "summary": "学生 ?????? 完成门户注册", "entity_id": "12", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 02:01:55", "operator_username": "139836871113"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (26, '{"id": 26, "action": "新增", "result": "success", "summary": "新增报名申请 Portal Smoke User", "entity_id": "17", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-21 01:58:19", "operator_username": "138610893902"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (25, '{"id": 25, "action": "注册", "result": "success", "summary": "学生 Portal Smoke User 完成门户注册", "entity_id": "11", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:58:09", "operator_username": "138610893902"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (24, '{"id": 24, "action": "注册", "result": "success", "summary": "学生 Portal Smoke User 完成门户注册", "entity_id": "10", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:57:43", "operator_username": "139602805956"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (23, '{"id": 23, "action": "新增", "result": "success", "summary": "新增报名申请 联调考生", "entity_id": "16", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-21 01:53:57", "operator_username": "136449765890"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (22, '{"id": 22, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "9", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:53:47", "operator_username": "136449765890"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (21, '{"id": 21, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "8", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:52:04", "operator_username": "131406454328"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (20, '{"id": 20, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "7", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:51:00", "operator_username": "138363035504"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (19, '{"id": 19, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "6", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:44:32", "operator_username": "135988852152"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (18, '{"id": 18, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "5", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:37:03", "operator_username": "135759274417"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (17, '{"id": 17, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "4", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 01:36:26", "operator_username": "133972320247"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (16, '{"id": 16, "action": "注册", "result": "success", "summary": "学生 联调考生 完成门户注册", "entity_id": "3", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-21 00:11:54", "operator_username": "13920260421"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (15, '{"id": 15, "action": "注册", "result": "success", "summary": "学生 张三 完成门户注册", "entity_id": "2", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-20 14:13:07", "operator_username": "18615768208"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (14, '{"id": 14, "action": "注册", "result": "success", "summary": "学生 罗凯 完成门户注册", "entity_id": "1", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-13 23:55:00", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (13, '{"id": 13, "action": "导入", "result": "success", "summary": "导入报名申请 在线联调0410132736", "entity_id": "15", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-10 13:27:37", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (12, '{"id": 12, "action": "导入", "result": "success", "summary": "导入报名申请 联调考生0410132613", "entity_id": "14", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-10 13:26:14", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (11, '{"id": 11, "action": "导入", "result": "success", "summary": "导入报名申请 联调考生0410131457", "entity_id": "13", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-10 13:14:58", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (10, '{"id": 10, "action": "复核通过", "result": "success", "summary": "周晴 执行 学位申请审批 - 复核通过", "entity_id": "SWSQSP202604090002", "entity_name": "论文主档", "module_name": "流程中心", "operated_at": "2026-04-09 20:15:26", "operator_username": "zhou.qing"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (9, '{"id": 9, "action": "提交送审", "result": "success", "summary": "徐素天 执行 学位申请审批 - 提交送审", "entity_id": "SWSQSP202604090002", "entity_name": "论文主档", "module_name": "流程中心", "operated_at": "2026-04-09 20:15:15", "operator_username": "xu.sutian"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (8, '{"id": 8, "action": "新增", "result": "success", "summary": "新增论文 沈知遥", "entity_id": "6", "entity_name": "论文主档", "module_name": "学位管理", "operated_at": "2026-04-09 20:15:05", "operator_username": "xu.sutian"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (7, '{"id": 7, "action": "复核通过", "result": "success", "summary": "周晴 执行 学位申请审批 - 复核通过", "entity_id": "SWSQSP202604090001", "entity_name": "论文主档", "module_name": "流程中心", "operated_at": "2026-04-09 20:14:35", "operator_username": "zhou.qing"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (6, '{"id": 6, "action": "提交送审", "result": "success", "summary": "徐素天 执行 学位申请审批 - 提交送审", "entity_id": "SWSQSP202604090001", "entity_name": "论文主档", "module_name": "流程中心", "operated_at": "2026-04-09 20:14:25", "operator_username": "xu.sutian"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (5, '{"id": 5, "action": "新增", "result": "success", "summary": "新增论文 沈知遥", "entity_id": "5", "entity_name": "论文主档", "module_name": "学位管理", "operated_at": "2026-04-09 20:14:15", "operator_username": "xu.sutian"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (4, '{"id": 4, "action": "新增", "result": "success", "summary": "新增招生计划 2027 春季招生计划", "entity_id": "5", "entity_name": "招生计划", "module_name": "招生管理", "operated_at": "2026-04-09 19:48:48", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (1, '{"id": 1, "action": "授权", "result": "success", "summary": "为导师角色补充流程处理权限。", "entity_id": "role-2", "entity_name": "角色权限", "module_name": "系统治理", "operated_at": "2026-04-06 09:00:00", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (2, '{"id": 2, "action": "审阅通过", "result": "success", "summary": "导师完成陈一鸣科研报告审阅。", "entity_id": "KYBGSY202604070001", "entity_name": "科研报告", "module_name": "培养管理", "operated_at": "2026-04-06 23:00:00", "operator_username": "liu.ya"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (3, '{"id": 3, "action": "复核", "result": "success", "summary": "学位秘书推进论文送审流程。", "entity_id": "SWSQSP202604070002", "entity_name": "论文主档", "module_name": "学位管理", "operated_at": "2026-04-07 03:00:00", "operator_username": "zhou.qing"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (38, '{"id": 38, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:27:49", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (39, '{"id": 39, "action": "新增研究中心", "result": "success", "summary": "新增研究中心 联调研究中心-1776709847", "entity_id": "7", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:30:47", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (40, '{"id": 40, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 联调研究中心-1776709847-更新", "entity_id": "7", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:30:48", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (41, '{"id": 41, "action": "删除研究中心", "result": "success", "summary": "删除研究中心 联调研究中心-1776709847-更新", "entity_id": "7", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:30:48", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (42, '{"id": 42, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:32:22", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (43, '{"id": 43, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:32:29", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (44, '{"id": 44, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 02:32:33", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (46, '{"id": 46, "action": "编辑研究中心", "result": "success", "summary": "更新研究中心 人工智能安全研究中心", "entity_id": "6", "entity_name": "研究中心主数据", "module_name": "学生管理", "operated_at": "2026-04-21 15:40:04", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (49, '{"id": 49, "action": "编辑", "result": "success", "summary": "更新个人资料 系统管理员", "entity_id": "admin", "entity_name": "个人资料", "module_name": "个人空间", "operated_at": "2026-04-21 16:25:28", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (50, '{"id": 50, "action": "编辑", "result": "success", "summary": "更新个人资料 系统管理员", "entity_id": "admin", "entity_name": "个人资料", "module_name": "个人空间", "operated_at": "2026-04-21 16:29:39", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (53, '{"id": 53, "action": "重置密码", "result": "success", "summary": "学生 罗凯 重置门户密码", "entity_id": "1", "entity_name": "找回密码", "module_name": "学生门户", "operated_at": "2026-04-22 02:03:56", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (54, '{"id": 54, "action": "新建账号", "result": "success", "summary": "新建系统账号 性能测试账号", "entity_id": "10", "entity_name": "系统用户", "module_name": "系统治理", "operated_at": "2026-04-22 02:22:27", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (55, '{"id": 55, "action": "重置密码", "result": "success", "summary": "更新账号 perf.tmp.1776795747 的登录密码", "entity_id": "perf.tmp.1776795747", "entity_name": "系统用户", "module_name": "系统治理", "operated_at": "2026-04-22 02:22:28", "operator_username": "perf.tmp.1776795747"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (56, '{"id": 56, "action": "删除账号", "result": "success", "summary": "删除系统账号 性能测试账号", "entity_id": "10", "entity_name": "系统用户", "module_name": "系统治理", "operated_at": "2026-04-22 02:22:28", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (57, '{"id": 57, "action": "停用账号", "result": "success", "summary": "停用注册学生账号 王珊", "entity_id": "16", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 02:23:44", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (58, '{"id": 58, "action": "启用账号", "result": "success", "summary": "启用注册学生账号 王珊", "entity_id": "16", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 02:23:44", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (59, '{"id": 59, "action": "重置密码", "result": "success", "summary": "重置注册学生密码 王珊", "entity_id": "16", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 02:23:44", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (60, '{"id": 60, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 王珊", "entity_id": "16", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 02:23:44", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (61, '{"id": 61, "action": "新建角色", "result": "success", "summary": "新建角色 性能测试角色", "entity_id": "8", "entity_name": "角色", "module_name": "系统治理", "operated_at": "2026-04-22 02:26:51", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (62, '{"id": 62, "action": "新建账号", "result": "success", "summary": "新建系统账号 角色联动测试用户", "entity_id": "11", "entity_name": "系统用户", "module_name": "系统治理", "operated_at": "2026-04-22 02:26:51", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (63, '{"id": 63, "action": "调整权限", "result": "success", "summary": "更新角色 性能测试角色V2 的权限配置", "entity_id": "8", "entity_name": "角色", "module_name": "系统治理", "operated_at": "2026-04-22 02:26:51", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (64, '{"id": 64, "action": "删除账号", "result": "success", "summary": "删除系统账号 角色联动测试用户", "entity_id": "11", "entity_name": "系统用户", "module_name": "系统治理", "operated_at": "2026-04-22 02:26:52", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (65, '{"id": 65, "action": "删除角色", "result": "success", "summary": "删除角色 性能测试角色V2", "entity_id": "8", "entity_name": "角色", "module_name": "系统治理", "operated_at": "2026-04-22 02:26:52", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (66, '{"id": 66, "action": "新增", "result": "success", "summary": "新增审批任务 性能验证手工任务", "entity_id": "38", "entity_name": "审批任务", "module_name": "审批中心", "operated_at": "2026-04-22 02:28:10", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (67, '{"id": 67, "action": "编辑", "result": "success", "summary": "更新审批任务 性能验证手工任务-更新", "entity_id": "38", "entity_name": "审批任务", "module_name": "审批中心", "operated_at": "2026-04-22 02:28:10", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (68, '{"id": 68, "action": "删除", "result": "success", "summary": "删除审批任务 性能验证手工任务-更新", "entity_id": "38", "entity_name": "审批任务", "module_name": "审批中心", "operated_at": "2026-04-22 02:28:11", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (69, '{"id": 69, "action": "新增", "result": "success", "summary": "新增招生计划 性能验证计划1776796165", "entity_id": "6", "entity_name": "招生计划", "module_name": "招生管理", "operated_at": "2026-04-22 02:29:25", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (70, '{"id": 70, "action": "编辑", "result": "success", "summary": "更新招生计划 性能验证计划1776796165-更新", "entity_id": "6", "entity_name": "招生计划", "module_name": "招生管理", "operated_at": "2026-04-22 02:29:26", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (71, '{"id": 71, "action": "登记方案", "result": "success", "summary": "登记培养方案 性能培养方案", "entity_id": "19", "entity_name": "培养方案", "module_name": "培养管理", "operated_at": "2026-04-22 02:51:49", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (72, '{"id": 72, "action": "维护方案", "result": "success", "summary": "维护培养方案 性能培养方案", "entity_id": "19", "entity_name": "培养方案", "module_name": "培养管理", "operated_at": "2026-04-22 02:51:49", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (73, '{"id": 73, "action": "删除方案", "result": "success", "summary": "删除培养方案 性能培养方案", "entity_id": "19", "entity_name": "培养方案", "module_name": "培养管理", "operated_at": "2026-04-22 02:51:50", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (74, '{"id": 74, "action": "新增", "result": "success", "summary": "新增盲审意见 评审专家A", "entity_id": "5", "entity_name": "盲审意见", "module_name": "学位管理", "operated_at": "2026-04-22 02:51:50", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (75, '{"id": 75, "action": "编辑", "result": "success", "summary": "更新盲审意见 评审专家A", "entity_id": "5", "entity_name": "盲审意见", "module_name": "学位管理", "operated_at": "2026-04-22 02:51:50", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (76, '{"id": 76, "action": "维护报告", "result": "success", "summary": "维护科研报告 江若溪", "entity_id": "8", "entity_name": "科研报告", "module_name": "培养管理", "operated_at": "2026-04-22 02:54:20", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (77, '{"id": 77, "action": "维护研修", "result": "success", "summary": "维护外出研修 孟书恒", "entity_id": "4", "entity_name": "外出研修", "module_name": "培养管理", "operated_at": "2026-04-22 02:54:20", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (78, '{"id": 78, "action": "编辑", "result": "success", "summary": "更新论文 沈知遥", "entity_id": "6", "entity_name": "论文主档", "module_name": "学位管理", "operated_at": "2026-04-22 02:54:21", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (79, '{"id": 79, "action": "登记报告", "result": "success", "summary": "登记科研报告 流程性能验证", "entity_id": "9", "entity_name": "科研报告", "module_name": "培养管理", "operated_at": "2026-04-22 02:57:36", "operator_username": "perf.creator"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (80, '{"id": 80, "action": "审阅通过", "result": "success", "summary": "perf.advisor 执行 科研报告审阅 - 审阅通过", "entity_id": "KYBGSY202604220001", "entity_name": "科研报告", "module_name": "流程中心", "operated_at": "2026-04-22 02:57:37", "operator_username": "perf.advisor"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (81, '{"id": 81, "action": "新建策略", "result": "success", "summary": "新建审计策略 性能策略1776797939", "entity_id": "5", "entity_name": "审计策略", "module_name": "系统治理", "operated_at": "2026-04-22 02:58:59", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (82, '{"id": 82, "action": "维护策略", "result": "success", "summary": "更新审计策略 性能策略1776797939", "entity_id": "5", "entity_name": "审计策略", "module_name": "系统治理", "operated_at": "2026-04-22 02:58:59", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (83, '{"id": 83, "action": "删除策略", "result": "success", "summary": "删除审计策略 性能策略1776797939", "entity_id": "5", "entity_name": "审计策略", "module_name": "系统治理", "operated_at": "2026-04-22 02:59:00", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (84, '{"id": 84, "action": "新建链路", "result": "success", "summary": "新建集成链路 性能链路1776797939", "entity_id": "4", "entity_name": "集成链路", "module_name": "系统治理", "operated_at": "2026-04-22 02:59:00", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (85, '{"id": 85, "action": "维护链路", "result": "success", "summary": "更新集成链路 性能链路1776797939", "entity_id": "4", "entity_name": "集成链路", "module_name": "系统治理", "operated_at": "2026-04-22 02:59:00", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (86, '{"id": 86, "action": "删除链路", "result": "success", "summary": "删除集成链路 性能链路1776797939", "entity_id": "4", "entity_name": "集成链路", "module_name": "系统治理", "operated_at": "2026-04-22 02:59:01", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (87, '{"id": 87, "action": "注册", "result": "success", "summary": "学生 性能回归be009f7d 完成门户注册", "entity_id": "17", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-22 09:24:01", "operator_username": "139be009f7d"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (88, '{"id": 88, "action": "保存草稿", "result": "success", "summary": "学生 性能回归be009f7d 保存报名草稿", "entity_id": "17", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 09:24:01", "operator_username": "139be009f7d"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (89, '{"id": 89, "action": "新增", "result": "success", "summary": "新增报名申请 性能回归be009f7d", "entity_id": "20", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:02", "operator_username": "139be009f7d"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (90, '{"id": 90, "action": "提交报名", "result": "success", "summary": "学生 性能回归be009f7d 提交报名申请", "entity_id": "17", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-22 09:24:02", "operator_username": "139be009f7d"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (91, '{"id": 91, "action": "新增", "result": "success", "summary": "新增报名申请 直建be009f7d", "entity_id": "21", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:03", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (92, '{"id": 92, "action": "编辑", "result": "success", "summary": "更新报名申请 直建更新be009f7d", "entity_id": "21", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:03", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (93, '{"id": 93, "action": "导入", "result": "success", "summary": "导入报名申请 导入be009f7d", "entity_id": "22", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:04", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (94, '{"id": 94, "action": "删除", "result": "success", "summary": "删除报名申请 直建更新be009f7d", "entity_id": "21", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:04", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (95, '{"id": 95, "action": "删除", "result": "success", "summary": "删除报名申请 导入be009f7d", "entity_id": "22", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:04", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (96, '{"id": 96, "action": "删除", "result": "success", "summary": "删除报名申请 性能回归be009f7d", "entity_id": "20", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:24:05", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (97, '{"id": 97, "action": "注册", "result": "success", "summary": "学生 性能回归52d69275 完成门户注册", "entity_id": "18", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-22 09:25:27", "operator_username": "13952d69275"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (98, '{"id": 98, "action": "保存草稿", "result": "success", "summary": "学生 性能回归52d69275 保存报名草稿", "entity_id": "18", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 09:25:27", "operator_username": "13952d69275"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (99, '{"id": 99, "action": "新增", "result": "success", "summary": "新增报名申请 性能回归52d69275", "entity_id": "23", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:28", "operator_username": "13952d69275"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (100, '{"id": 100, "action": "提交报名", "result": "success", "summary": "学生 性能回归52d69275 提交报名申请", "entity_id": "18", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-22 09:25:28", "operator_username": "13952d69275"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (101, '{"id": 101, "action": "新增", "result": "success", "summary": "新增报名申请 直建52d69275", "entity_id": "24", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:29", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (102, '{"id": 102, "action": "编辑", "result": "success", "summary": "更新报名申请 直建更新52d69275", "entity_id": "24", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:29", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (103, '{"id": 103, "action": "导入", "result": "success", "summary": "导入报名申请 导入52d69275", "entity_id": "25", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:30", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (104, '{"id": 104, "action": "删除", "result": "success", "summary": "删除报名申请 直建更新52d69275", "entity_id": "24", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:30", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (105, '{"id": 105, "action": "删除", "result": "success", "summary": "删除报名申请 导入52d69275", "entity_id": "25", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:31", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (106, '{"id": 106, "action": "删除", "result": "success", "summary": "删除报名申请 性能回归52d69275", "entity_id": "23", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-22 09:25:31", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (107, '{"id": 107, "action": "新增", "result": "success", "summary": "新增学生 性能验证学生", "entity_id": "19", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:32:33", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (108, '{"id": 108, "action": "编辑", "result": "success", "summary": "更新学生 性能验证学生-更新", "entity_id": "19", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:32:33", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (109, '{"id": 109, "action": "删除", "result": "success", "summary": "删除学生 性能验证学生-更新", "entity_id": "19", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:32:33", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (110, '{"id": 110, "action": "新增", "result": "success", "summary": "新增学生 性能验证学生8952d6ab", "entity_id": "20", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:33:31", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (111, '{"id": 111, "action": "编辑", "result": "success", "summary": "更新学生 性能验证学生更新8952d6ab", "entity_id": "20", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:33:32", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (112, '{"id": 112, "action": "删除", "result": "success", "summary": "删除学生 性能验证学生更新8952d6ab", "entity_id": "20", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 09:33:32", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (113, '{"id": 113, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 10:06:30", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (114, '{"id": 114, "action": "编辑", "result": "success", "summary": "更新个人资料 系统管理员", "entity_id": "admin", "entity_name": "个人资料", "module_name": "个人空间", "operated_at": "2026-04-22 13:12:05", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (115, '{"id": 115, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 13:34:31", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (116, '{"id": 116, "action": "编辑", "result": "success", "summary": "更新学生 陆承泽", "entity_id": "18", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 13:47:00", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (117, '{"id": 117, "action": "编辑", "result": "success", "summary": "更新学生 陆承泽", "entity_id": "18", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-22 13:47:06", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (118, '{"id": 118, "action": "注册", "result": "success", "summary": "学生 罗凯 完成门户注册", "entity_id": "19", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-22 15:16:42", "operator_username": "13908237925"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (119, '{"id": 119, "action": "重置密码", "result": "success", "summary": "重置注册学生密码 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 15:39:34", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (120, '{"id": 120, "action": "重置密码", "result": "success", "summary": "重置注册学生密码 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-22 16:29:37", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (121, '{"id": 121, "action": "重置密码", "result": "success", "summary": "学生 罗凯 重置门户密码", "entity_id": "1", "entity_name": "找回密码", "module_name": "学生门户", "operated_at": "2026-04-22 18:05:59", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (122, '{"id": 122, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 18:32:49", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (123, '{"id": 123, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 18:37:05", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (124, '{"id": 124, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 19:20:03", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (125, '{"id": 125, "action": "保存草稿", "result": "success", "summary": "学生 门户联调考生 保存报名草稿", "entity_id": "15", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 19:32:02", "operator_username": "132786107897"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (126, '{"id": 126, "action": "保存草稿", "result": "success", "summary": "学生 中文考生 保存报名草稿", "entity_id": "14", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 19:32:54", "operator_username": "13100000001"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (127, '{"id": 127, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 19:34:17", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (128, '{"id": 128, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-22 19:54:29", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (129, '{"id": 129, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 01:33:31", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (130, '{"id": 130, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 01:34:09", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (131, '{"id": 131, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 01:43:21", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (132, '{"id": 132, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 01:43:46", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (133, '{"id": 133, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 01:49:04", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (134, '{"id": 134, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 01:52:29", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (135, '{"id": 135, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 01:53:11", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (136, '{"id": 136, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 01:55:42", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (137, '{"id": 137, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 01:56:23", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (138, '{"id": 138, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 02:00:38", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (139, '{"id": 139, "action": "重置密码", "result": "success", "summary": "重置注册学生密码 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 02:00:48", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (140, '{"id": 140, "action": "修改密码", "result": "success", "summary": "学生 罗凯 在个人空间修改密码", "entity_id": "1", "entity_name": "个人空间", "module_name": "学生门户", "operated_at": "2026-04-23 02:01:21", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (141, '{"id": 141, "action": "发送邮件", "result": "success", "summary": "向注册学生发送邮件 罗凯", "entity_id": "1", "entity_name": "注册学生", "module_name": "学生管理", "operated_at": "2026-04-23 02:07:10", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (142, '{"id": 142, "action": "编辑", "result": "success", "summary": "更新学生 江若溪", "entity_id": "14", "entity_name": "学生主档", "module_name": "学生管理", "operated_at": "2026-04-23 02:07:38", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (143, '{"id": 143, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 02:11:11", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (144, '{"id": 144, "action": "删除", "result": "success", "summary": "删除报名申请 ??????", "entity_id": "18", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:12:12", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (145, '{"id": 145, "action": "删除", "result": "success", "summary": "删除报名申请 ??????", "entity_id": "18", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:18:15", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (146, '{"id": 146, "action": "编辑", "result": "success", "summary": "更新报名申请 门户联调考生", "entity_id": "19", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:18:36", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (147, '{"id": 147, "action": "编辑", "result": "success", "summary": "更新报名申请 门户联调考生", "entity_id": "19", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:19:23", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (148, '{"id": 148, "action": "编辑", "result": "success", "summary": "更新报名申请 Portal Smoke User", "entity_id": "17", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:52:45", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (149, '{"id": 149, "action": "编辑", "result": "success", "summary": "更新报名申请 测试管理保存", "entity_id": "19", "entity_name": "报名申请", "module_name": "招生管理", "operated_at": "2026-04-23 02:53:39", "operator_username": "admin"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (150, '{"id": 150, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 03:40:25", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (151, '{"id": 151, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 03:40:28", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (152, '{"id": 152, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 03:40:33", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (153, '{"id": 153, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 03:40:46", "operator_username": "18615768209"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (154, '{"id": 154, "action": "注册", "result": "success", "summary": "学生 李小玉 完成门户注册", "entity_id": "20", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-23 09:20:19", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (155, '{"id": 155, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 09:28:16", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (156, '{"id": 156, "action": "保存草稿", "result": "success", "summary": "学生 李小玉 保存报名草稿", "entity_id": "20", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 09:28:46", "operator_username": "13521297322"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (157, '{"id": 157, "action": "注册", "result": "success", "summary": "学生 牟沿霖 完成门户注册", "entity_id": "21", "entity_name": "门户注册", "module_name": "学生门户", "operated_at": "2026-04-23 10:28:25", "operator_username": "18918001537"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (180, '{"id": 180, "action": "提交报名", "result": "success", "summary": "学生提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:06:49", "operator_username": "18615768209"}', '2026-04-23 13:06:50.053496+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (181, '{"id": 181, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:07:02", "operator_username": "18615768209"}', '2026-04-23 13:07:03.281223+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (182, '{"id": 182, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:08:00", "operator_username": "18615768209"}', '2026-04-23 13:08:01.465552+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (183, '{"id": 183, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:13:24", "operator_username": "18615768209"}', '2026-04-23 13:13:25.966137+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (184, '{"id": 184, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:13:34", "operator_username": "18615768209"}', '2026-04-23 13:13:35.732518+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (185, '{"id": 185, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:13:44", "operator_username": "18615768209"}', '2026-04-23 13:13:45.765328+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (186, '{"id": 186, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:13:47", "operator_username": "18615768209"}', '2026-04-23 13:13:48.280537+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (187, '{"id": 187, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:14:38", "operator_username": "18615768209"}', '2026-04-23 13:14:39.504406+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (188, '{"id": 188, "action": "保存草稿", "result": "success", "summary": "学生 罗凯 保存报名草稿", "entity_id": "1", "entity_name": "申请草稿", "module_name": "学生门户", "operated_at": "2026-04-23 13:15:05", "operator_username": "18615768209"}', '2026-04-23 13:15:06.20893+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (189, '{"id": 189, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:15:08", "operator_username": "18615768209"}', '2026-04-23 13:15:09.107542+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (190, '{"id": 190, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:15:26", "operator_username": "18615768209"}', '2026-04-23 13:15:26.995468+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (191, '{"id": 191, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:15:37", "operator_username": "18615768209"}', '2026-04-23 13:15:38.260579+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (192, '{"id": 192, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:37:54", "operator_username": "18615768209"}', '2026-04-23 13:37:55.791601+08');
INSERT INTO "public"."dtlms_runtime_operation_logs" VALUES (193, '{"id": 193, "action": "提交报名", "result": "success", "summary": "学生 罗凯 提交报名申请", "entity_id": "1", "entity_name": "报名提交", "module_name": "学生门户", "operated_at": "2026-04-23 13:43:22", "operator_username": "18615768209"}', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_runtime_outbound_studies
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_outbound_studies";
CREATE TABLE "public"."dtlms_runtime_outbound_studies" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_outbound_studies
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_outbound_studies" VALUES (1, '{"id": 1, "end_date": "2026-08-31", "start_date": "2026-03-01", "student_no": "D20230007", "study_type": "联合培养", "destination": "新加坡国立大学", "advisor_name": "刘亚", "business_key": "WCYXSP202604070001", "student_name": "王书宁", "approval_status": "已批准", "expected_outcome": "完成联合培养课题与月度交流汇报。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_outbound_studies" VALUES (2, '{"id": 2, "end_date": "2026-07-30", "start_date": "2026-02-15", "student_no": "D20230008", "study_type": "访学交流", "destination": "香港科技大学", "advisor_name": "徐素天", "business_key": "WCYXSP202604070002", "student_name": "贺景川", "approval_status": "审批中", "expected_outcome": "完成知识图谱跨语种研究。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_outbound_studies" VALUES (3, '{"id": 3, "end_date": "2026-07-31", "start_date": "2026-05-01", "student_no": "D20240003", "study_type": "企业研修", "destination": "中控技术研究院", "advisor_name": "袁野", "business_key": "WCYXSP202604070003", "student_name": "周启航", "approval_status": "已驳回", "expected_outcome": "研修目标与阶段任务需进一步明确。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_outbound_studies" VALUES (4, '{"id": 4, "end_date": "2026-05-22", "start_date": "2026-05-18", "student_no": "D20250015", "study_type": "学术会议", "destination": "深圳", "advisor_name": "袁野", "business_key": "WCYXSP202604070004", "student_name": "孟书恒", "approval_status": "审批中", "expected_outcome": "参加流程治理与数字教育论坛。"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_portal_students
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_portal_students";
CREATE TABLE "public"."dtlms_runtime_portal_students" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_portal_students
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (13, '{"id": 13, "email": "portal.254277869@example.com", "gender": null, "id_type": "居民身份证", "full_name": "门户联调考生", "id_number": "32000019998800027", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "131300757986", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$/R8DYEzJ2TtHCAFA6P3fuw$7zcNBFXV.xuARaL1fU9gJ.Hj66GRNbzirLdAjwi1TAg", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (12, '{"id": 12, "email": "portal.338335439@example.com", "gender": "?", "id_type": null, "profile": {"gender": "?", "id_type": null, "birth_date": "1999-01-01", "ethnic_group": null, "native_place": "????", "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": "????", "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "??????", "id_number": "32000019993682138", "birth_date": "1999-01-01", "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": "[{\"member_name\": \"??\", \"relation_type\": \"??\"}, {\"member_name\": \"??\", \"relation_type\": \"??\"}]", "ethnic_group": null, "native_place": "????", "phone_number": "139836871113", "submitted_at": "2026-04-21 02:02:08", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$eq81RsgZA4BQak3JuRdibA$JZbIHUI5.W6kCwIodPwH96wu0z5u8eHGPACZu1b6zx0", "account_status": "启用", "highest_degree": "??", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": "????", "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"declaration_text": "????????????????", "has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-21 02:02:08", "family_members": [{"job_title": null, "member_name": "??", "contact_phone": null, "employer_name": null, "relation_type": "??"}, {"job_title": null, "member_name": "??", "contact_phone": null, "employer_name": null, "relation_type": "??"}], "source_channel": "?????", "selected_plan_id": 5, "personal_statement": {"resume_attachment_url": "/portal-attachments/uploads/student-12/resume/resume-079c71237fff479faf62c7d76eaa36b7.pdf", "personal_statement_text": "??????"}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [{"gpa": null, "ranking": null, "end_month": null, "major_name": null, "sort_order": 1, "school_name": "????", "start_month": null, "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "??", "transcript_attachment_url": null, "degree_certificate_attachment_url": null}], "english_proficiencies": []}, "graduation_school": "????", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"??\", \"school_name\": \"????\"}]", "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": "??????"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (5, '{"id": 5, "email": "portal.271598992@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "32000019998353673", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "135759274417", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$4tw75/wf47z33lvrHQMAYA$xHlSDvoay8SUxvyoX9jlj435woefjRCN6RJxQqSizLA", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (14, '{"id": 14, "email": "portal.test@example.com", "gender": null, "id_type": null, "profile": {"gender": null, "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": null, "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": null, "religious_belief": null, "profile_photo_url": "/portal-attachments/uploads/student-test/profile_photo/test.png", "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "中文考生", "id_number": "3200001999123456", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-22 19:32:54", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "13100000001", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$nBOidE7J2Vvr3bs3phSiNA$cG.wdf10RyfuzTRKRVLVJ9V9IsnKYOtPZQATe6jSz6Y", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": 1, "signed_agreement": false, "application_draft": {"declaration": {"has_read_declaration": false}, "preferences": [], "submitted_at": null, "family_members": [], "source_channel": null, "selected_plan_id": 1, "personal_statement": {}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [], "english_proficiencies": []}, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (11, '{"id": 11, "email": "portal.520532517@example.com", "gender": "Male", "id_type": null, "profile": {"gender": "Male", "id_type": null, "birth_date": "1999-01-01", "ethnic_group": null, "native_place": "Wuxi Jiangsu", "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": "PartyMember", "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "Portal Smoke User", "id_number": "32000019994456783", "birth_date": "1999-01-01", "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": "[{\"member_name\": \"Parent A\", \"relation_type\": \"Father\"}, {\"member_name\": \"Parent B\", \"relation_type\": \"Mother\"}]", "ethnic_group": null, "native_place": "Wuxi Jiangsu", "phone_number": "138610893902", "submitted_at": "2026-04-21 01:58:19", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$gJCyFqL0vnfundOaU4rReg$9242ot2pOB2niZjGxe0wgu6HWQe6m4PQN9QJpU9oQJg", "account_status": "启用", "highest_degree": "Master", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": "PartyMember", "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"declaration_text": "I confirm all submitted information is true.", "has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-21 01:58:19", "family_members": [{"job_title": null, "member_name": "Parent A", "contact_phone": null, "employer_name": null, "relation_type": "Father"}, {"job_title": null, "member_name": "Parent B", "contact_phone": null, "employer_name": null, "relation_type": "Mother"}], "source_channel": "LabSite", "selected_plan_id": 5, "personal_statement": {"resume_attachment_url": "/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf", "personal_statement_text": "Portal smoke submission"}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [{"gpa": null, "ranking": null, "end_month": null, "major_name": null, "sort_order": 1, "school_name": "Jiangnan University", "start_month": null, "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "Master", "transcript_attachment_url": null, "degree_certificate_attachment_url": null}], "english_proficiencies": []}, "graduation_school": "Jiangnan University", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"Master\", \"school_name\": \"Jiangnan University\"}]", "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": "Portal smoke submission"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (10, '{"id": 10, "email": "portal.651275151@example.com", "gender": null, "id_type": "居民身份证", "full_name": "Portal Smoke User", "id_number": "32000019993427012", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "139602805956", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$R8g5xxjjfI.xdo6xFmLsPQ$upSLPB/2rlwNk8bPOJue8vLZ.vgl3bwy2K.s1dtae/w", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (9, '{"id": 9, "email": "portal.550629792@example.com", "gender": "男", "id_type": null, "profile": {"gender": "男", "id_type": null, "birth_date": "1999-01-01", "ethnic_group": null, "native_place": "江苏无锡", "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": "中共党员", "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "联调考生", "id_number": "32000019999145401", "birth_date": "1999-01-01", "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": "[{\"member_name\": \"张父\", \"relation_type\": \"父亲\"}, {\"member_name\": \"张母\", \"relation_type\": \"母亲\"}]", "ethnic_group": null, "native_place": "江苏无锡", "phone_number": "136449765890", "submitted_at": "2026-04-21 01:53:57", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$41wrhTBmjNHam7N27j2nlA$p1REy2Vark0YRzS4UkTsNsMD2dkKNU.Nm6lEZLpghk4", "account_status": "启用", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": "中共党员", "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"declaration_text": "本人承诺以上填写内容真实、准确。", "has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-21 01:53:57", "family_members": [{"job_title": null, "member_name": "张父", "contact_phone": null, "employer_name": null, "relation_type": "父亲"}, {"job_title": null, "member_name": "张母", "contact_phone": null, "employer_name": null, "relation_type": "母亲"}], "source_channel": "实验室官网", "selected_plan_id": 5, "personal_statement": {"resume_attachment_url": "/portal-attachments/uploads/student-9/resume/resume-5221465b8e7d4c1693dd1274df5b6fac.pdf", "personal_statement_text": "真实联调提交"}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [{"gpa": null, "ranking": null, "end_month": null, "major_name": null, "sort_order": 1, "school_name": "江南大学", "start_month": null, "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "硕士", "transcript_attachment_url": null, "degree_certificate_attachment_url": null}], "english_proficiencies": []}, "graduation_school": "江南大学", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"school_name\": \"江南大学\"}]", "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": "真实联调提交"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (8, '{"id": 8, "email": "portal.157628501@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "32000019995416599", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "131406454328", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$kFKK8T4HAICQEoKQslbqPQ$NycXdbcknLzgPWzhsmQsSJX22.Ehwi4jIQbCrzX9STc", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (7, '{"id": 7, "email": "portal.150206797@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "32000019998271744", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "138363035504", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$H2MsJaSUshbiPEfoXet9Lw$UG4rZF2TosmON0mAFlp7ndThngQGzlCr8i81RzghvA0", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (6, '{"id": 6, "email": "portal.863164580@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "32000019991480547", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "135988852152", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$fw9BaM2ZU8r5H2Psvfdeiw$dsEp8UNs94xpEFCkzl5417oqMgZMHFMPT9exfEXTtQQ", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (4, '{"id": 4, "email": "portal.916429449@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "32000019992615150", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "133972320247", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$EoLQOufcm5PSmjPmfE8phQ$XB3Jc/u2Gg5MTPsanc.nCaxclr0ano.3EATmOet3HS4", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (3, '{"id": 3, "email": "portal.20260421001153@example.com", "gender": null, "id_type": "居民身份证", "full_name": "联调考生", "id_number": "320000199901011234", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "13920260421", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$aE3pHQNAiPFe632vNUZISQ$dVvded79NYS4Epe0LAGPTEloO6DRvJdFR/RWC6.9YJs", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (2, '{"id": 2, "email": "zsan@cotong.com", "gender": null, "id_type": "居民身份证", "full_name": "张三", "id_number": "510104197911301878", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-21 16:14:01", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "18615768208", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$5jznXItRau39vxcCwDhnLA$eSpx40C9plY2DUDXlffwWdwXJUQTLrcoEPZutNidauQ", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (16, '{"id": 16, "email": "wss@126.com", "gender": null, "id_type": "居民身份证", "full_name": "王珊", "id_number": "510104197910111000", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-22 02:23:44", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "15908833765", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$sJbSupeyFqLUGoMwRuhd6w$y1xzbm2tUcLMg.mbBw.ASOFAp.3Cy.0lEYbAVEYMZbo", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (17, '{"id": 17, "email": "perf_be009f7d@example.com", "gender": null, "id_type": null, "profile": {"gender": null, "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": null, "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": null, "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "性能回归be009f7d", "id_number": "32010119900101be00", "birth_date": null, "created_at": "2026-04-22 09:24:01", "updated_at": "2026-04-22 09:24:02", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "139be009f7d", "submitted_at": "2026-04-22 09:24:02", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$lFKqda7VWusdY6yV8v7/vw$V5umOb8mauV1s.1V5FW3B33h7cSZSpl05IhRK55L49Y", "account_status": "启用", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-22 09:24:02", "family_members": [], "source_channel": null, "selected_plan_id": 5, "personal_statement": {}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [], "english_proficiencies": []}, "graduation_school": "回归测试大学", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (18, '{"id": 18, "email": "perf_52d69275@example.com", "gender": null, "id_type": null, "profile": {"gender": null, "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": null, "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": null, "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "性能回归52d69275", "id_number": "3201011990010152d6", "birth_date": null, "created_at": "2026-04-22 09:25:27", "updated_at": "2026-04-22 09:25:28", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "13952d69275", "submitted_at": "2026-04-22 09:25:28", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$bU3Jea8VgtB6L2XsfS9lbA$JCrgIBI4zU8kjU5M5V/G0rj821L9mF8mTyg98yxyzjw", "account_status": "启用", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-22 09:25:28", "family_members": [], "source_channel": null, "selected_plan_id": 5, "personal_statement": {}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [], "english_proficiencies": []}, "graduation_school": "回归测试大学", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (19, '{"id": 19, "email": "lkai@cotong.com", "gender": null, "id_type": "居民身份证", "full_name": "罗凯", "id_number": "510104197911301877", "birth_date": null, "created_at": "2026-04-22 15:16:42", "updated_at": "2026-04-22 15:16:42", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "13908237925", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$qFXqnVNqjfE.p5RSilHqPQ$Mc26MBjuEeppBozWF8V5muhTxMs9zAU4Q7/5Vm0g4.Q", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (15, '{"id": 15, "email": "portal.606885427@example.com", "gender": null, "id_type": null, "profile": {"gender": null, "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": null, "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": null, "religious_belief": null, "profile_photo_url": "/portal-attachments/uploads/student-test/profile_photo/test.png", "emergency_contact_name": null, "emergency_contact_phone": null}, "full_name": "门户联调考生", "id_number": "32000019997301982", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-22 19:32:02", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "132786107897", "submitted_at": "2026-04-21 02:06:20", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$xxiDcE6JEUIoJcR4T8n5vw$1N0V1KgpQscHVLGlATKfVhnrowrjsb2/wYNKbjOBHm4", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": 5, "signed_agreement": false, "application_draft": {"declaration": {"has_read_declaration": false}, "preferences": [], "submitted_at": "2026-04-21 02:06:20", "family_members": [], "source_channel": null, "selected_plan_id": 5, "personal_statement": {}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [], "english_proficiencies": []}, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (20, '{"id": 20, "email": "annieleexy@hotmail.com", "gender": "女", "id_type": "居民身份证", "profile": {"gender": "女", "id_type": "居民身份证", "birth_date": null, "ethnic_group": "汉族", "native_place": null, "marital_status": null, "mailing_address": "1", "full_name_pinyin": "li xiaoyu", "political_status": "中共党员", "religious_belief": null, "profile_photo_url": "/portal-attachments/uploads/student-20/profile_photo/profile_photo-7a069d5d7f0f487e85b05482baf7438e.jpg", "emergency_contact_name": "1", "emergency_contact_phone": "1"}, "full_name": "李小玉", "id_number": "371326199602240040", "birth_date": null, "created_at": "2026-04-23 09:20:19", "updated_at": "2026-04-23 12:01:02", "family_info": "[{\"member_name\": \"1\", \"relation_type\": \"父亲\", \"employer_name\": \"1\", \"contact_phone\": \"1\"}, {\"member_name\": \"1\", \"relation_type\": \"母亲\", \"employer_name\": \"1\", \"contact_phone\": \"1\"}]", "ethnic_group": "汉族", "native_place": null, "phone_number": "13521297322", "submitted_at": "2026-04-23 11:51:21", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$aM35P.ecs5ZSqtWacw7BeA$QpFPFNFwLR3mX2SuNAoNh4k3ckVQEeEwNUMuf3xG1CY", "account_status": "启用", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": "1", "self_evaluation": null, "personal_profile": null, "political_status": "中共党员", "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"declaration_text": "我已同意并仔细阅读使用条款和隐私政策。", "progress_snapshot": {"family_count": 2, "english_count": 0, "practice_count": 0, "education_count": 1, "preference_count": 2, "achievement_count": 0}, "has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}, {"is_optional": true, "advisor_name": "刘亚", "preference_order": 2, "research_center_name": "机器人应用团队"}], "submitted_at": "2026-04-23 11:51:21", "family_members": [{"job_title": null, "member_name": "1", "contact_phone": "1", "employer_name": "1", "relation_type": "父亲"}, {"job_title": null, "member_name": "1", "contact_phone": "1", "employer_name": "1", "relation_type": "母亲"}], "source_channel": "实验室官网", "selected_plan_id": 5, "personal_statement": {"personal_statement_text": "11"}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [{"gpa": "1", "ranking": "1", "end_month": "2020-07", "major_name": "1", "sort_order": 1, "school_name": "北京大学", "start_month": "2017-09", "average_score": "1", "verifier_name": "1", "verifier_phone": "1", "education_stage": "硕士", "transcript_attachment_url": null, "transcript_attachment_name": null, "degree_certificate_attachment_url": null, "degree_certificate_attachment_name": null}], "english_proficiencies": []}, "graduation_school": "北京大学", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"start_month\": \"2017-09\", \"end_month\": \"2020-07\", \"school_name\": \"北京大学\", \"major_name\": \"1\", \"average_score\": \"1\", \"gpa\": \"1\", \"ranking\": \"1\", \"verifier_name\": \"1\", \"verifier_phone\": \"1\"}]", "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": "11"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (21, '{"id": 21, "email": "moupengfei11@163.com", "gender": null, "id_type": "居民身份证", "full_name": "牟沿霖", "id_number": "310105201403193216", "birth_date": null, "created_at": "2026-04-23 10:28:25", "updated_at": "2026-04-23 10:28:25", "family_info": null, "ethnic_group": null, "native_place": null, "phone_number": "18918001537", "submitted_at": null, "english_level": null, "password_hash": "$pbkdf2-sha256$29000$2huDcE4JofQ.xzgHQAhBCA$COELNy02aDiro5y.abl.5dq.9qXf0OQ/g2TU12rPOkg", "account_status": "启用", "highest_degree": null, "intended_field": null, "marital_status": null, "mailing_address": null, "self_evaluation": null, "personal_profile": null, "political_status": null, "religious_belief": null, "selected_plan_id": null, "signed_agreement": false, "graduation_school": null, "selected_team_name": null, "practice_experience": null, "education_experience": null, "recommendation_notes": null, "selected_advisor_name": null, "personal_statement_text": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_portal_students" VALUES (1, '{"id": 1, "email": "lk139@126.com", "gender": "男", "id_type": "居民身份证", "profile": {"gender": "男", "id_type": "居民身份证", "birth_date": null, "ethnic_group": "汉族", "native_place": null, "marital_status": null, "mailing_address": "上海市浦东新区惠南镇听达路185弄5号304室", "full_name_pinyin": "LUOKAI", "political_status": "群众", "religious_belief": null, "profile_photo_url": "/portal-attachments/uploads/student-1/profile_photo/profile_photo-525a6aaea02a4d0b83bb1b518df91983.png", "emergency_contact_name": "张丛秀", "emergency_contact_phone": "13682137095"}, "full_name": "罗凯", "id_number": "510104197911301879", "birth_date": null, "created_at": "2026-04-21 16:14:01", "updated_at": "2026-04-23 13:43:22", "family_info": "[{\"member_name\": \"罗道全\", \"relation_type\": \"父亲\"}, {\"member_name\": \"张丛秀\", \"relation_type\": \"母亲\"}]", "ethnic_group": "汉族", "native_place": null, "phone_number": "18615768209", "submitted_at": "2026-04-23 13:43:22", "english_level": null, "password_hash": "$pbkdf2-sha256$29000$iRECIOT8vzdGKAWA0Pqfsw$J0FkSN9r6D/JuwE/6LEObp07ar48ImHf1oIFozh3vxc", "account_status": "启用", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "mailing_address": "上海市浦东新区惠南镇听达路185弄5号304室", "self_evaluation": "测试", "personal_profile": null, "political_status": "群众", "religious_belief": null, "selected_plan_id": 5, "signed_agreement": true, "application_draft": {"declaration": {"declaration_text": "我已同意并仔细阅读使用条款和隐私政策。", "progress_snapshot": {"family_count": 2, "english_count": 0, "practice_count": 0, "education_count": 1, "preference_count": 1, "achievement_count": 0}, "has_read_declaration": true}, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "submitted_at": "2026-04-23 13:43:22", "family_members": [{"job_title": null, "member_name": "罗道全", "contact_phone": null, "employer_name": null, "relation_type": "父亲"}, {"job_title": null, "member_name": "张丛秀", "contact_phone": null, "employer_name": null, "relation_type": "母亲"}], "source_channel": "实验室官网", "selected_plan_id": 5, "personal_statement": {"ai_industry_opinion": "测试", "ai_problem_statement": "测试", "personal_statement_text": "测试"}, "achievement_records": [], "practice_experiences": [], "source_channel_other": null, "education_experiences": [{"gpa": null, "ranking": null, "end_month": "2022-09", "major_name": null, "sort_order": 1, "school_name": "电子科技大学", "start_month": "2018-07", "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "硕士", "transcript_attachment_url": null, "transcript_attachment_name": null, "degree_certificate_attachment_url": null, "degree_certificate_attachment_name": null}], "english_proficiencies": []}, "graduation_school": "电子科技大学", "selected_team_name": "智能制造团队", "practice_experience": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"start_month\": \"2018-07\", \"end_month\": \"2022-09\", \"school_name\": \"电子科技大学\"}]", "recommendation_notes": null, "selected_advisor_name": "刘亚", "personal_statement_text": "测试"}', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_runtime_profiles
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_profiles";
CREATE TABLE "public"."dtlms_runtime_profiles" (
  "username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_profiles
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('liu.ya', '{"email": "liu.ya@dtlms.local", "username": "liu.ya", "full_name": "刘亚", "role_name": "导师", "theme_color": "#13795b", "phone_number": "13800000021", "department_name": "智能制造学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('yuan.ye', '{"email": "yuan.ye@dtlms.local", "username": "yuan.ye", "full_name": "袁野", "role_name": "导师", "theme_color": "#13795b", "phone_number": "13800000022", "department_name": "工业软件学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('xu.sutian', '{"email": "xu.sutian@dtlms.local", "username": "xu.sutian", "full_name": "徐素天", "role_name": "导师", "theme_color": "#13795b", "phone_number": "13800000023", "department_name": "数据智能学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('zhou.qing', '{"email": "zhou.qing@dtlms.local", "username": "zhou.qing", "full_name": "周晴", "role_name": "学位秘书", "theme_color": "#0f4cbd", "phone_number": "13800000024", "department_name": "学位办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('he.lin', '{"email": "he.lin@dtlms.local", "username": "he.lin", "full_name": "何琳", "role_name": "评分人", "theme_color": "#0f4cbd", "phone_number": "13800000025", "department_name": "招生办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('cao.bo', '{"email": "cao.bo@dtlms.local", "username": "cao.bo", "full_name": "曹博", "role_name": "面试官", "theme_color": "#0f4cbd", "phone_number": "13800000026", "department_name": "招生办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('yang.qin', '{"email": "yang.qin@dtlms.local", "username": "yang.qin", "full_name": "杨琴", "role_name": "中心HRBP", "theme_color": "#0f4cbd", "phone_number": "13800000027", "department_name": "人力资源部"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('sun.wei', '{"email": "sun.wei@dtlms.local", "username": "sun.wei", "full_name": "孙伟", "role_name": "党群负责人", "theme_color": "#0f4cbd", "phone_number": "13800000028", "department_name": "党群工作部"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_profiles" VALUES ('admin', '{"email": "admin@dtlms.local", "username": "admin", "full_name": "系统管理员", "role_name": "平台管理员", "theme_color": "#409eff", "phone_number": "13800000000", "department_name": "学科与研究生管理处"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_recruitment_applications
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_recruitment_applications";
CREATE TABLE "public"."dtlms_runtime_recruitment_applications" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_recruitment_applications
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (26, '{"id": 26, "email": "annieleexy@hotmail.com", "gender": "女", "id_type": "居民身份证", "plan_id": 5, "profile": null, "id_number": "371326199602240040", "applied_at": "2026-04-23 11:51:21", "declaration": null, "family_info": "[{\"member_name\": \"1\", \"relation_type\": \"父亲\", \"employer_name\": \"1\", \"contact_phone\": \"1\"}, {\"member_name\": \"1\", \"relation_type\": \"母亲\", \"employer_name\": \"1\", \"contact_phone\": \"1\"}]", "final_score": null, "preferences": [], "business_key": "ZSLQSP202604230009", "candidate_no": "ZSLQSP202604230009", "first_choice": "智能制造团队", "graduate_gpa": null, "native_place": null, "phone_number": "13521297322", "review_round": null, "student_name": "李小玉", "graduate_rank": null, "reviewer_name": null, "second_choice": "机器人应用团队", "family_members": [], "graduate_major": null, "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "source_channel": "实验室官网", "dissenting_view": null, "graduate_school": null, "mailing_address": "1", "material_status": "待审核", "research_impact": null, "self_evaluation": null, "political_status": "中共党员", "religious_belief": null, "research_problem": null, "accept_adjustment": null, "ai_society_impact": null, "discovery_channel": "实验室官网", "graduation_school": "北京大学", "portal_student_id": 20, "undergraduate_gpa": null, "application_status": "报名已提交", "personal_statement": null, "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"start_month\": \"2017-09\", \"end_month\": \"2020-07\", \"school_name\": \"北京大学\", \"major_name\": \"1\", \"average_score\": \"1\", \"gpa\": \"1\", \"ranking\": \"1\", \"verifier_name\": \"1\", \"verifier_phone\": \"1\"}]", "practice_experiences": [], "source_channel_other": null, "undergraduate_school": null, "education_experiences": [], "intended_advisor_name": "刘亚", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": "11", "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (16, '{"id": 16, "email": "portal.550629792@example.com", "gender": "男", "id_type": null, "plan_id": 5, "id_number": "32000019999145401", "applied_at": "2026-04-21 01:53:57", "family_info": "[{\"member_name\": \"张父\", \"relation_type\": \"父亲\"}, {\"member_name\": \"张母\", \"relation_type\": \"母亲\"}]", "final_score": null, "business_key": "ZSLQSP202604210004", "candidate_no": "ZSLQSP202604210004", "first_choice": "智能制造团队", "graduate_gpa": null, "native_place": "江苏无锡", "phone_number": "136449765890", "review_round": null, "student_name": "联调考生", "graduate_rank": null, "reviewer_name": null, "second_choice": null, "graduate_major": null, "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "source_channel": "实验室官网", "dissenting_view": null, "graduate_school": null, "mailing_address": null, "material_status": "待审核", "research_impact": null, "self_evaluation": null, "political_status": "中共党员", "religious_belief": null, "research_problem": null, "accept_adjustment": null, "ai_society_impact": null, "discovery_channel": "实验室官网", "graduation_school": "江南大学", "portal_student_id": 9, "undergraduate_gpa": null, "application_status": "报名已提交", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"school_name\": \"江南大学\"}]", "source_channel_other": null, "undergraduate_school": null, "intended_advisor_name": "刘亚", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": "真实联调提交", "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": "/portal-attachments/uploads/student-9/resume/resume-5221465b8e7d4c1693dd1274df5b6fac.pdf", "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (17, '{"id": 17, "email": "portal.520532517@example.com", "gender": "Male", "id_type": "居民身份证", "plan_id": 5, "profile": {"gender": "Male", "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": "Wuxi Jiangsu", "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": "PartyMember", "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "id_number": "32000019994456783", "applied_at": "2026-04-21 01:58:19", "declaration": {"declaration_text": "I confirm all submitted information is true.", "progress_snapshot": null, "has_read_declaration": true}, "family_info": "[{\"member_name\": \"Parent A\", \"relation_type\": \"Father\"}, {\"member_name\": \"Parent B\", \"relation_type\": \"Mother\"}]", "final_score": null, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "business_key": "ZSLQSP202604210005", "candidate_no": "ZSLQSP202604210005", "first_choice": "智能制造团队", "graduate_gpa": "", "native_place": "Wuxi Jiangsu", "phone_number": "138610893902", "review_round": "", "student_name": "Portal Smoke User", "graduate_rank": "", "reviewer_name": "system.auto", "second_choice": "", "family_members": [{"job_title": null, "member_name": "Parent A", "contact_phone": null, "employer_name": null, "relation_type": "Father"}, {"job_title": null, "member_name": "Parent B", "contact_phone": null, "employer_name": null, "relation_type": "Mother"}], "graduate_major": "", "highest_degree": "Master", "intended_field": "智能制造团队", "marital_status": "未婚", "source_channel": "LabSite", "dissenting_view": null, "graduate_school": "", "mailing_address": null, "material_status": "待补材料", "research_impact": "", "self_evaluation": "", "political_status": "PartyMember", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": "", "discovery_channel": "LabSite", "graduation_school": "Jiangnan University", "portal_student_id": null, "undergraduate_gpa": null, "application_status": "报名已提交", "personal_statement": {"ai_industry_opinion": null, "ai_problem_statement": null, "resume_attachment_url": "/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf", "resume_attachment_name": "resume-75163dc510e24a04b6c90c0eaf77f253.pdf", "personal_statement_text": "Portal smoke submission"}, "undergraduate_rank": null, "practice_experience": "", "undergraduate_major": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"Master\", \"school_name\": \"Jiangnan University\"}]", "practice_experiences": [], "source_channel_other": null, "undergraduate_school": "", "education_experiences": [{"gpa": null, "ranking": null, "end_month": null, "major_name": null, "sort_order": 1, "school_name": "Jiangnan University", "start_month": null, "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "Master", "transcript_attachment_url": null, "transcript_attachment_name": null, "degree_certificate_attachment_url": null, "degree_certificate_attachment_name": null}], "intended_advisor_name": "刘亚", "supplementary_profile": "", "graduate_average_score": "", "personal_statement_text": "Portal smoke submission", "material_list_attachment": "", "overseas_university_name": "", "research_status_analysis": "", "student_activity_experience": "", "undergraduate_average_score": null, "personal_statement_attachment": "/portal-attachments/uploads/student-11/resume/resume-75163dc510e24a04b6c90c0eaf77f253.pdf", "overseas_master_university_name": ""}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (19, '{"id": 19, "email": "portal.606885427@example.com", "gender": "男", "id_type": "居民身份证", "plan_id": 5, "profile": {"gender": "男", "id_type": null, "birth_date": null, "ethnic_group": null, "native_place": "江苏无锡", "marital_status": null, "mailing_address": null, "full_name_pinyin": null, "political_status": "中共党员", "religious_belief": null, "profile_photo_url": null, "emergency_contact_name": null, "emergency_contact_phone": null}, "id_number": "32000019997301982", "applied_at": "2026-04-21 02:06:20", "declaration": {"declaration_text": "本人承诺以上填写内容真实、准确。", "progress_snapshot": null, "has_read_declaration": true}, "family_info": "[{\"member_name\": \"张父\", \"relation_type\": \"父亲\"}, {\"member_name\": \"张母\", \"relation_type\": \"母亲\"}]", "final_score": null, "preferences": [{"is_optional": false, "advisor_name": "刘亚", "preference_order": 1, "research_center_name": "智能制造团队"}], "business_key": "ZSLQSP202604210007", "candidate_no": "ZSLQSP202604210007", "first_choice": "智能制造团队", "graduate_gpa": "", "native_place": "江苏无锡", "phone_number": "132786107897", "review_round": "", "student_name": "测试管理保存", "graduate_rank": "", "reviewer_name": "system.auto", "second_choice": "", "family_members": [{"job_title": null, "member_name": "张父", "contact_phone": null, "employer_name": null, "relation_type": "父亲"}, {"job_title": null, "member_name": "张母", "contact_phone": null, "employer_name": null, "relation_type": "母亲"}], "graduate_major": "", "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": "未婚", "source_channel": "实验室官网", "dissenting_view": null, "graduate_school": "", "mailing_address": null, "material_status": "待补材料", "research_impact": "", "self_evaluation": "", "political_status": "中共党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": "", "discovery_channel": "实验室官网", "graduation_school": "江南大学", "portal_student_id": null, "undergraduate_gpa": null, "application_status": "报名已提交", "personal_statement": {"ai_industry_opinion": null, "ai_problem_statement": null, "resume_attachment_url": "/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf", "resume_attachment_name": "resume-1361bf8942e240b6afa9af9eb42236c5.pdf", "personal_statement_text": "门户联调提交"}, "undergraduate_rank": null, "practice_experience": "", "undergraduate_major": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"school_name\": \"江南大学\"}]", "practice_experiences": [], "source_channel_other": null, "undergraduate_school": "", "education_experiences": [{"gpa": null, "ranking": null, "end_month": null, "major_name": null, "sort_order": 1, "school_name": "江南大学", "start_month": null, "average_score": null, "verifier_name": null, "verifier_phone": null, "education_stage": "硕士", "transcript_attachment_url": null, "transcript_attachment_name": null, "degree_certificate_attachment_url": null, "degree_certificate_attachment_name": null}], "intended_advisor_name": "刘亚", "supplementary_profile": "", "graduate_average_score": "", "personal_statement_text": "门户联调提交", "material_list_attachment": "", "overseas_university_name": "", "research_status_analysis": "", "student_activity_experience": "", "undergraduate_average_score": null, "personal_statement_attachment": "/portal-attachments/uploads/student-15/resume/resume-1361bf8942e240b6afa9af9eb42236c5.pdf", "overseas_master_university_name": ""}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (15, '{"id": 15, "email": "web_0410132736@example.com", "gender": "男", "id_type": "居民身份证", "plan_id": 5, "id_number": "310115199901012736", "applied_at": "2026-04-10 15:00:00", "family_info": "家庭支持继续深造。", "final_score": null, "business_key": "ZSLQSP202604100004", "candidate_no": "ZSLQSP202604100004", "first_choice": "智能科学", "graduate_gpa": "3.95", "native_place": "上海", "phone_number": "13710132736", "review_round": "第11轮", "student_name": "在线联调0410132736", "graduate_rank": "3/80", "reviewer_name": null, "second_choice": "模式识别", "graduate_major": "人工智能", "highest_degree": "硕士", "intended_field": "智能科学", "marital_status": "未婚", "dissenting_view": "我不同意仅凭更大规模数据就能解决全部泛化问题。", "graduate_school": "复旦大学", "mailing_address": "上海市徐汇区联调路11号", "material_status": "材料齐全", "research_impact": "将提升高风险行业的智能辅助可靠性。", "self_evaluation": "具备扎实的研究训练基础。", "political_status": "中共党员", "religious_belief": "无", "research_problem": "复杂场景下的模型可信推理。", "accept_adjustment": "是", "ai_society_impact": "AI 会深刻改变知识工作与流程自动化。", "discovery_channel": "官网报名", "graduation_school": "浙江大学", "undergraduate_gpa": "3.88", "application_status": "报名已提交", "undergraduate_rank": "8/200", "practice_experience": "参与过科研项目与工程落地。", "undergraduate_major": "计算机科学与技术", "education_experience": "本科浙江大学，硕士复旦大学。", "undergraduate_school": "浙江大学", "intended_advisor_name": "刘亚", "supplementary_profile": "个人简介第二段。", "graduate_average_score": "92.3", "personal_statement_text": "个人简介第一段。", "material_list_attachment": "checklist.zip", "overseas_university_name": null, "research_status_analysis": "当前多集中于离线评测，真实世界泛化不足。", "student_activity_experience": "组织过多次学术活动。", "undergraduate_average_score": "90.1", "personal_statement_attachment": "ps.pdf", "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (14, '{"id": 14, "email": "online_0410132613@example.com", "gender": "男", "id_type": "居民身份证", "plan_id": 5, "id_number": "310115199901012613", "applied_at": "2026-04-10 15:00:00", "family_info": "家庭支持继续深造。", "final_score": null, "business_key": "ZSLQSP202604100003", "candidate_no": "ZSLQSP202604100003", "first_choice": "智能科学", "graduate_gpa": "3.95", "native_place": "上海", "phone_number": "13810132613", "review_round": "第10轮", "student_name": "联调考生0410132613", "graduate_rank": "3/80", "reviewer_name": null, "second_choice": "模式识别", "graduate_major": "人工智能", "highest_degree": "硕士", "intended_field": "智能科学", "marital_status": "未婚", "dissenting_view": "我不同意仅凭更大规模数据就能解决全部泛化问题。", "graduate_school": "复旦大学", "mailing_address": "上海市浦东新区联调路10号", "material_status": "材料齐全", "research_impact": "将提升高风险行业的智能辅助可靠性。", "self_evaluation": "具备扎实的研究训练基础。", "political_status": "中共党员", "religious_belief": "无", "research_problem": "复杂场景下的模型可信推理。", "accept_adjustment": "是", "ai_society_impact": "AI 会深刻改变知识工作与流程自动化。", "discovery_channel": "官网报名", "graduation_school": "浙江大学", "undergraduate_gpa": "3.88", "application_status": "报名已提交", "undergraduate_rank": "8/200", "practice_experience": "参与过科研项目与工程落地。", "undergraduate_major": "计算机科学与技术", "education_experience": "本科浙江大学，硕士复旦大学。", "undergraduate_school": "浙江大学", "intended_advisor_name": "刘亚", "supplementary_profile": "个人简介第二段。", "graduate_average_score": "92.3", "personal_statement_text": "个人简介第一段。", "material_list_attachment": "checklist.zip", "overseas_university_name": null, "research_status_analysis": "当前多集中于离线评测，真实世界泛化不足。", "student_activity_experience": "组织过多次学术活动。", "undergraduate_average_score": "90.1", "personal_statement_attachment": "ps.pdf", "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (13, '{"id": 13, "email": "jointest_0410131457@example.com", "gender": "女", "id_type": "居民身份证", "plan_id": 5, "id_number": "320211199901011457", "applied_at": "2026-04-10 14:00:00", "family_info": "家庭稳定，支持继续攻读博士。", "final_score": null, "business_key": "ZSLQSP202604100001", "candidate_no": "ZSLQSP202604100001", "first_choice": "人工智能", "graduate_gpa": "3.91", "native_place": "江苏无锡", "phone_number": "13910131457", "review_round": "第9轮", "student_name": "联调考生0410131457", "graduate_rank": "5/60", "reviewer_name": null, "second_choice": "计算机视觉", "graduate_major": "人工智能", "highest_degree": "硕士", "intended_field": "人工智能", "marital_status": "未婚", "dissenting_view": "我不同意只要扩大参数规模就必然提升系统可靠性的行业共识。", "graduate_school": "上海交通大学", "mailing_address": "江苏省无锡市滨湖区测试路9号", "material_status": "材料齐全", "research_impact": "若能解决，将提升智能系统在教育与工业领域的可信应用水平。", "self_evaluation": "具备较强科研潜力与工程落地能力。", "political_status": "共青团员", "religious_belief": "无", "research_problem": "面向复杂场景的多模态推理可靠性问题。", "accept_adjustment": "是", "ai_society_impact": "AI 将持续影响高风险决策支持与知识生产流程。", "discovery_channel": "导师推荐", "graduation_school": "东南大学", "undergraduate_gpa": "3.82", "application_status": "报名已提交", "undergraduate_rank": "12/180", "practice_experience": "曾参与科研项目、企业联合课题与开源社区维护。", "undergraduate_major": "软件工程", "education_experience": "2018-2022 东南大学 软件工程 本科；2022-2025 上海交通大学 人工智能 硕士。", "undergraduate_school": "东南大学", "intended_advisor_name": "刘亚", "supplementary_profile": "个人简介第二段。", "graduate_average_score": "91.2", "personal_statement_text": "个人简介第一段。", "material_list_attachment": "materials.zip", "overseas_university_name": null, "research_status_analysis": "当前研究已覆盖通用基准，但在真实场景稳健性方面仍有明显短板。", "student_activity_experience": "担任研究生会学术部负责人，组织多场学术活动。", "undergraduate_average_score": "89.5", "personal_statement_attachment": "statement.pdf", "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (1, '{"id": 1, "email": "candidate01@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": 91.0, "business_key": "ZSLQSP202604070001", "candidate_no": "ZSLQSP202604070001", "first_choice": "智能制造", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020001", "review_round": "1轮次", "student_name": "吴启程", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "机器学习", "graduate_major": "智能制造", "highest_degree": "硕士", "intended_field": "智能制造", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "中共党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "东南大学", "undergraduate_gpa": null, "application_status": "同意录取", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "智能制造", "education_experience": null, "undergraduate_school": "东南大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (2, '{"id": 2, "email": "candidate02@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": 88.5, "business_key": "ZSLQSP202604070002", "candidate_no": "ZSLQSP202604070002", "first_choice": "机器人控制", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020002", "review_round": "1轮次", "student_name": "沈清禾", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "工业互联网", "graduate_major": "机器人控制", "highest_degree": "硕士", "intended_field": "机器人控制", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "共青团员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "同济大学", "undergraduate_gpa": null, "application_status": "预录取", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "机器人控制", "education_experience": null, "undergraduate_school": "同济大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (3, '{"id": 3, "email": "candidate03@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": 85.0, "business_key": "ZSLQSP202604070003", "candidate_no": "ZSLQSP202604070003", "first_choice": "工业互联网", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020003", "review_round": "1轮次", "student_name": "顾明睿", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "知识图谱", "graduate_major": "工业互联网", "highest_degree": "硕士", "intended_field": "工业互联网", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "群众", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "华中科技大学", "undergraduate_gpa": null, "application_status": "面试完成", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "工业互联网", "education_experience": null, "undergraduate_school": "华中科技大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (4, '{"id": 4, "email": "candidate04@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": null, "business_key": "ZSLQSP202604070004", "candidate_no": "ZSLQSP202604070004", "first_choice": "视觉检测", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020004", "review_round": "1轮次", "student_name": "周亦凡", "graduate_rank": null, "reviewer_name": "曹博", "second_choice": "数据智能", "graduate_major": "视觉检测", "highest_degree": "硕士", "intended_field": "视觉检测", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "中共预备党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "哈尔滨工业大学", "undergraduate_gpa": null, "application_status": "面试待安排", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "视觉检测", "education_experience": null, "undergraduate_school": "哈尔滨工业大学", "intended_advisor_name": "曹博", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (5, '{"id": 5, "email": "candidate05@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": 82.0, "business_key": "ZSLQSP202604070005", "candidate_no": "ZSLQSP202604070005", "first_choice": "数据智能", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020005", "review_round": "1轮次", "student_name": "李静姝", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "数字孪生", "graduate_major": "数据智能", "highest_degree": "硕士", "intended_field": "数据智能", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "中共党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "浙江大学", "undergraduate_gpa": null, "application_status": "材料评分中", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "数据智能", "education_experience": null, "undergraduate_school": "浙江大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (6, '{"id": 6, "email": "candidate06@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 1, "id_number": null, "applied_at": null, "family_info": null, "final_score": null, "business_key": "ZSLQSP202604070006", "candidate_no": "ZSLQSP202604070006", "first_choice": "数字孪生", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020006", "review_round": "1轮次", "student_name": "陈思远", "graduate_rank": null, "reviewer_name": null, "second_choice": "软件工程", "graduate_major": "数字孪生", "highest_degree": "硕士", "intended_field": "数字孪生", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "待补材料", "research_impact": null, "self_evaluation": null, "political_status": "共青团员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "北京航空航天大学", "undergraduate_gpa": null, "application_status": "报名已提交", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "数字孪生", "education_experience": null, "undergraduate_school": "北京航空航天大学", "intended_advisor_name": null, "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (7, '{"id": 7, "email": "candidate07@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 2, "id_number": null, "applied_at": null, "family_info": null, "final_score": null, "business_key": "ZSLQSP202604070007", "candidate_no": "ZSLQSP202604070007", "first_choice": "工业软件", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020007", "review_round": "2轮次", "student_name": "赵安歌", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "机器学习", "graduate_major": "工业软件", "highest_degree": "硕士", "intended_field": "工业软件", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "群众", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "南京大学", "undergraduate_gpa": null, "application_status": "资格审核通过", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "工业软件", "education_experience": null, "undergraduate_school": "南京大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (8, '{"id": 8, "email": "candidate08@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 2, "id_number": null, "applied_at": null, "family_info": null, "final_score": 93.0, "business_key": "ZSLQSP202604070008", "candidate_no": "ZSLQSP202604070008", "first_choice": "软件工程", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020008", "review_round": "2轮次", "student_name": "林知夏", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "工业互联网", "graduate_major": "软件工程", "highest_degree": "硕士", "intended_field": "软件工程", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "中共预备党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "上海交通大学", "undergraduate_gpa": null, "application_status": "同意录取", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "软件工程", "education_experience": null, "undergraduate_school": "上海交通大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (9, '{"id": 9, "email": "candidate09@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 2, "id_number": null, "applied_at": null, "family_info": null, "final_score": 73.0, "business_key": "ZSLQSP202604070009", "candidate_no": "ZSLQSP202604070009", "first_choice": "模型驱动开发", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020009", "review_round": "2轮次", "student_name": "钱北辰", "graduate_rank": null, "reviewer_name": "曹博", "second_choice": "知识图谱", "graduate_major": "模型驱动开发", "highest_degree": "硕士", "intended_field": "模型驱动开发", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "中共党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "西安交通大学", "undergraduate_gpa": null, "application_status": "不录取", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "模型驱动开发", "education_experience": null, "undergraduate_school": "西安交通大学", "intended_advisor_name": "曹博", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (10, '{"id": 10, "email": "candidate10@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 2, "id_number": null, "applied_at": null, "family_info": null, "final_score": 86.0, "business_key": "ZSLQSP202604070010", "candidate_no": "ZSLQSP202604070010", "first_choice": "工业数据治理", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020010", "review_round": "2轮次", "student_name": "韩知遇", "graduate_rank": null, "reviewer_name": "何琳", "second_choice": "数据智能", "graduate_major": "工业数据治理", "highest_degree": "硕士", "intended_field": "工业数据治理", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "共青团员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "天津大学", "undergraduate_gpa": null, "application_status": "预录取", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "工业数据治理", "education_experience": null, "undergraduate_school": "天津大学", "intended_advisor_name": "何琳", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (11, '{"id": 11, "email": "candidate11@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 3, "id_number": null, "applied_at": null, "family_info": null, "final_score": null, "business_key": "ZSLQSP202604070011", "candidate_no": "ZSLQSP202604070011", "first_choice": "知识图谱", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020011", "review_round": "3轮次", "student_name": "朱安宁", "graduate_rank": null, "reviewer_name": "曹博", "second_choice": "数字孪生", "graduate_major": "知识图谱", "highest_degree": "硕士", "intended_field": "知识图谱", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "材料齐全", "research_impact": null, "self_evaluation": null, "political_status": "群众", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "武汉大学", "undergraduate_gpa": null, "application_status": "面试待安排", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "知识图谱", "education_experience": null, "undergraduate_school": "武汉大学", "intended_advisor_name": "曹博", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (12, '{"id": 12, "email": "candidate12@mail.example.com", "gender": "未知", "id_type": "居民身份证", "plan_id": 3, "id_number": null, "applied_at": null, "family_info": null, "final_score": null, "business_key": "ZSLQSP202604070012", "candidate_no": "ZSLQSP202604070012", "first_choice": "机器学习", "graduate_gpa": null, "native_place": "待补充", "phone_number": "13900020012", "review_round": "3轮次", "student_name": "谢明远", "graduate_rank": null, "reviewer_name": null, "second_choice": "软件工程", "graduate_major": "机器学习", "highest_degree": "硕士", "intended_field": "机器学习", "marital_status": "未婚", "dissenting_view": null, "graduate_school": null, "mailing_address": "待补充", "material_status": "已退回修改", "research_impact": null, "self_evaluation": null, "political_status": "中共预备党员", "religious_belief": "无", "research_problem": null, "accept_adjustment": "是", "ai_society_impact": null, "discovery_channel": null, "graduation_school": "北京理工大学", "undergraduate_gpa": null, "application_status": "报名已提交", "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": "机器学习", "education_experience": null, "undergraduate_school": "北京理工大学", "intended_advisor_name": null, "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": null, "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_applications" VALUES (27, '{"id": 27, "email": "lk139@126.com", "gender": "男", "id_type": "居民身份证", "plan_id": 5, "profile": null, "id_number": "510104197911301879", "applied_at": "2026-04-23 13:43:22", "declaration": null, "family_info": "[{\"member_name\": \"罗道全\", \"relation_type\": \"父亲\"}, {\"member_name\": \"张丛秀\", \"relation_type\": \"母亲\"}]", "final_score": null, "preferences": [], "business_key": "ZSLQSP202604230010", "candidate_no": "ZSLQSP202604230010", "first_choice": "智能制造团队", "graduate_gpa": null, "native_place": null, "phone_number": "18615768209", "review_round": null, "student_name": "罗凯", "graduate_rank": null, "reviewer_name": null, "second_choice": null, "family_members": [], "graduate_major": null, "highest_degree": "硕士", "intended_field": "智能制造团队", "marital_status": null, "source_channel": "实验室官网", "dissenting_view": null, "graduate_school": null, "mailing_address": "上海市浦东新区惠南镇听达路185弄5号304室", "material_status": "待审核", "research_impact": null, "self_evaluation": "测试", "political_status": "群众", "religious_belief": null, "research_problem": null, "accept_adjustment": null, "ai_society_impact": null, "discovery_channel": "实验室官网", "graduation_school": "电子科技大学", "portal_student_id": 1, "undergraduate_gpa": null, "application_status": "报名已提交", "personal_statement": null, "undergraduate_rank": null, "practice_experience": null, "undergraduate_major": null, "education_experience": "[{\"sort_order\": 1, \"education_stage\": \"硕士\", \"start_month\": \"2018-07\", \"end_month\": \"2022-09\", \"school_name\": \"电子科技大学\"}]", "practice_experiences": [], "source_channel_other": null, "undergraduate_school": null, "education_experiences": [], "intended_advisor_name": "刘亚", "supplementary_profile": null, "graduate_average_score": null, "personal_statement_text": "测试", "material_list_attachment": null, "overseas_university_name": null, "research_status_analysis": null, "student_activity_experience": null, "undergraduate_average_score": null, "personal_statement_attachment": null, "overseas_master_university_name": null}', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_runtime_recruitment_plans
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_recruitment_plans";
CREATE TABLE "public"."dtlms_runtime_recruitment_plans" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_recruitment_plans
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (5, '{"id": 5, "is_open": true, "semester": "春", "plan_name": "2027 春季招生计划", "target_quota": 30, "academic_year": "2027", "current_stage": "报名配置", "plan_description": null, "brochure_image_url": null, "interview_group_count": 3}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (1, '{"id": 1, "is_open": true, "semester": "秋", "plan_name": "2026 秋季博士招生", "target_quota": 36, "academic_year": "2026", "current_stage": "资格审核", "plan_description": null, "brochure_image_url": null, "interview_group_count": 4}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (2, '{"id": 2, "is_open": true, "semester": "秋", "plan_name": "2026 工程博士专项", "target_quota": 28, "academic_year": "2026", "current_stage": "评分推荐", "plan_description": null, "brochure_image_url": null, "interview_group_count": 3}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (3, '{"id": 3, "is_open": true, "semester": "秋", "plan_name": "2026 智能制造联合培养", "target_quota": 18, "academic_year": "2026", "current_stage": "面试执行", "plan_description": null, "brochure_image_url": null, "interview_group_count": 2}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (4, '{"id": 4, "is_open": false, "semester": "春", "plan_name": "2025 春季补录", "target_quota": 8, "academic_year": "2025", "current_stage": "预录取", "plan_description": null, "brochure_image_url": null, "interview_group_count": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_recruitment_plans" VALUES (6, '{"id": 6, "is_open": true, "semester": "秋季学期", "plan_name": "性能验证计划1776796165-更新", "target_quota": 0, "academic_year": "2026-2027", "current_stage": "报名配置", "plan_description": "仅验证增量持久化-更新", "brochure_image_url": null, "interview_group_count": 0}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_roles";
CREATE TABLE "public"."dtlms_runtime_roles" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_roles
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_roles" VALUES (1, '{"id": 1, "role_code": "platform_admin", "role_name": "平台管理员", "scope_name": "系统治理", "permissions": ["*"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (2, '{"id": 2, "role_code": "advisor", "role_name": "导师", "scope_name": "培养与学位", "permissions": ["dashboard:read", "students:read", "training:read", "training:write", "degree:read", "workflow:read", "workflow:write"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (3, '{"id": 3, "role_code": "secretary", "role_name": "学位秘书", "scope_name": "学位管理", "permissions": ["dashboard:read", "degree:read", "degree:write", "workflow:read", "workflow:write"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (4, '{"id": 4, "role_code": "recruit_reviewer", "role_name": "评分人", "scope_name": "招生管理", "permissions": ["dashboard:read", "recruitment:read"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (5, '{"id": 5, "role_code": "interview_officer", "role_name": "面试官", "scope_name": "招生管理", "permissions": ["dashboard:read", "recruitment:read", "recruitment:write"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (6, '{"id": 6, "role_code": "hrbp", "role_name": "中心HRBP", "scope_name": "跨部门协同", "permissions": ["dashboard:read", "students:read", "training:read"]}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_roles" VALUES (7, '{"id": 7, "role_code": "party_affairs", "role_name": "党群负责人", "scope_name": "学生管理", "permissions": ["dashboard:read", "students:read", "audit:read"]}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_scientific_reports
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_scientific_reports";
CREATE TABLE "public"."dtlms_runtime_scientific_reports" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_scientific_reports
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (1, '{"id": 1, "summary": "完成产线调度算法优化与仿真验证。", "student_no": "D20240001", "business_key": "KYBGSY202604070001", "period_label": "2026Q1", "review_score": 92.0, "student_name": "陈一鸣", "report_status": "已通过", "reviewer_name": "刘亚"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (2, '{"id": 2, "summary": "完成机器人视觉检测数据采集。", "student_no": "D20240002", "business_key": "KYBGSY202604070002", "period_label": "2026Q1", "review_score": null, "student_name": "林书雅", "report_status": "待导师审阅", "reviewer_name": "刘亚"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (3, '{"id": 3, "summary": "完成工业软件模块设计与接口联调。", "student_no": "D20240003", "business_key": "KYBGSY202604070003", "period_label": "2026Q1", "review_score": 88.0, "student_name": "周启航", "report_status": "已通过", "reviewer_name": "袁野"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (4, '{"id": 4, "summary": "实验结果不足，需要补充对比分析。", "student_no": "D20240004", "business_key": "KYBGSY202604070004", "period_label": "2026Q1", "review_score": 76.0, "student_name": "顾南乔", "report_status": "退回修改", "reviewer_name": "徐素天"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (5, '{"id": 5, "summary": "完成企业实习阶段需求分析与文档输出。", "student_no": "D20230005", "business_key": "KYBGSY202604070005", "period_label": "2026Q1", "review_score": 90.0, "student_name": "赵嘉霖", "report_status": "已通过", "reviewer_name": "袁野"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (6, '{"id": 6, "summary": "完成知识图谱抽取规则验证。", "student_no": "D20230006", "business_key": "KYBGSY202604070006", "period_label": "2026Q1", "review_score": null, "student_name": "沈知遥", "report_status": "待导师审阅", "reviewer_name": "徐素天"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (7, '{"id": 7, "summary": "完成入组初期课题调研和综述整理。", "student_no": "D20250013", "business_key": "KYBGSY202604070007", "period_label": "2026Q1", "review_score": null, "student_name": "宋知行", "report_status": "待导师审阅", "reviewer_name": "刘亚"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_scientific_reports" VALUES (8, '{"id": 8, "summary": "完成大模型辅助标注流程验证。", "student_no": "D20250014", "business_key": "KYBGSY202604070008", "period_label": "2026Q1", "review_score": 89.0, "student_name": "江若溪", "report_status": "已通过", "reviewer_name": "徐素天"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_students
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_students";
CREATE TABLE "public"."dtlms_runtime_students" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_students
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_students" VALUES (1, '{"id": 1, "status": "在校", "full_name": "陈一鸣", "team_name": "智能制造团队", "student_no": "D20240001", "degree_type": "工程博士", "advisor_name": "刘亚", "phone_number": "13800010001", "enrollment_year": 2024, "political_status": "中共党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (2, '{"id": 2, "status": "在校", "full_name": "林书雅", "team_name": "机器人应用团队", "student_no": "D20240002", "degree_type": "学术博士", "advisor_name": "刘亚", "phone_number": "13800010002", "enrollment_year": 2024, "political_status": "共青团员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (3, '{"id": 3, "status": "在校", "full_name": "周启航", "team_name": "工业软件团队", "student_no": "D20240003", "degree_type": "工程博士", "advisor_name": "袁野", "phone_number": "13800010003", "enrollment_year": 2024, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (4, '{"id": 4, "status": "在校", "full_name": "顾南乔", "team_name": "数据智能团队", "student_no": "D20240004", "degree_type": "学术博士", "advisor_name": "徐素天", "phone_number": "13800010004", "enrollment_year": 2024, "political_status": "中共预备党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (5, '{"id": 5, "status": "实习中", "full_name": "赵嘉霖", "team_name": "工业软件团队", "student_no": "D20230005", "degree_type": "工程博士", "advisor_name": "袁野", "phone_number": "13800010005", "enrollment_year": 2023, "political_status": "中共党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (6, '{"id": 6, "status": "实习中", "full_name": "沈知遥", "team_name": "数据智能团队", "student_no": "D20230006", "degree_type": "工程博士", "advisor_name": "徐素天", "phone_number": "13800010006", "enrollment_year": 2023, "political_status": "共青团员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (7, '{"id": 7, "status": "外出研修", "full_name": "王书宁", "team_name": "智能制造团队", "student_no": "D20230007", "degree_type": "学术博士", "advisor_name": "刘亚", "phone_number": "13800010007", "enrollment_year": 2023, "political_status": "共青团员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (8, '{"id": 8, "status": "外出研修", "full_name": "贺景川", "team_name": "数据智能团队", "student_no": "D20230008", "degree_type": "工程博士", "advisor_name": "徐素天", "phone_number": "13800010008", "enrollment_year": 2023, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (9, '{"id": 9, "status": "请假中", "full_name": "许安然", "team_name": "工业软件团队", "student_no": "D20230009", "degree_type": "学术博士", "advisor_name": "袁野", "phone_number": "13800010009", "enrollment_year": 2023, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (10, '{"id": 10, "status": "学位论文阶段", "full_name": "张乐之", "team_name": "工业软件团队", "student_no": "D20220010", "degree_type": "工程博士", "advisor_name": "袁野", "phone_number": "13800010010", "enrollment_year": 2022, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (11, '{"id": 11, "status": "学位论文阶段", "full_name": "赵嘉禾", "team_name": "数据智能团队", "student_no": "D20220011", "degree_type": "工程博士", "advisor_name": "徐素天", "phone_number": "13800010011", "enrollment_year": 2022, "political_status": "中共党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (12, '{"id": 12, "status": "学位论文阶段", "full_name": "顾清越", "team_name": "机器人应用团队", "student_no": "D20220012", "degree_type": "学术博士", "advisor_name": "刘亚", "phone_number": "13800010012", "enrollment_year": 2022, "political_status": "中共预备党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (13, '{"id": 13, "status": "在校", "full_name": "宋知行", "team_name": "智能制造团队", "student_no": "D20250013", "degree_type": "工程博士", "advisor_name": "刘亚", "phone_number": "13800010013", "enrollment_year": 2025, "political_status": "共青团员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (15, '{"id": 15, "status": "在校", "full_name": "孟书恒", "team_name": "平台治理团队", "student_no": "D20250015", "degree_type": "工程博士", "advisor_name": "袁野", "phone_number": "13800010015", "enrollment_year": 2025, "political_status": "中共党员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (16, '{"id": 16, "status": "在校", "full_name": "魏知远", "team_name": "机器人应用团队", "student_no": "D20250016", "degree_type": "学术博士", "advisor_name": "刘亚", "phone_number": "13800010016", "enrollment_year": 2025, "political_status": "共青团员"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (17, '{"id": 17, "status": "在校", "full_name": "韩嘉宁", "team_name": "工业软件团队", "student_no": "D20240017", "degree_type": "学术博士", "advisor_name": "袁野", "phone_number": "13800010017", "enrollment_year": 2024, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (14, '{"id": 14, "status": "在校", "full_name": "江若溪", "team_name": "数据智能团队", "student_no": "D20250014", "degree_type": "学术博士", "advisor_name": "徐素天", "phone_number": "13800010014", "enrollment_year": 2025, "political_status": "群众"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_students" VALUES (18, '{"id": 18, "status": "在校", "full_name": "陆承泽", "team_name": "数据智能团队", "student_no": "D20240018", "degree_type": "工程博士", "advisor_name": "徐素天", "phone_number": "13800010018", "enrollment_year": 2024, "political_status": "中共党员"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_sync_logs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_sync_logs";
CREATE TABLE "public"."dtlms_runtime_sync_logs" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_sync_logs
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_sync_logs" VALUES (1, '{"id": 1, "executed_at": "2026-04-07 05:00:00", "sync_status": "success", "record_count": 36, "source_system": "招生系统", "target_system": "DTLMS", "failure_reason": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_sync_logs" VALUES (2, '{"id": 2, "executed_at": "2026-04-07 06:00:00", "sync_status": "failed", "record_count": 4, "source_system": "飞书", "target_system": "DTLMS", "failure_reason": "回执接口超时，等待补偿重试。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_sync_logs" VALUES (3, '{"id": 3, "executed_at": "2026-04-07 07:00:00", "sync_status": "success", "record_count": 58, "source_system": "实验室OA", "target_system": "DTLMS", "failure_reason": null}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_system_users
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_system_users";
CREATE TABLE "public"."dtlms_runtime_system_users" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_system_users
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (3, '{"id": 3, "username": "yuan.ye", "full_name": "袁野", "role_code": "advisor", "phone_number": "13800000022", "last_login_at": "2026-04-06 06:00:00", "password_hash": "$pbkdf2-sha256$29000$yhnjPKfUei.F8H6PMWas1Q$qDDfghaS3TOjM/CZolO0gs7OheOG6MEO/VKfIUFRUzk", "account_status": "启用", "department_name": "工业软件学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (4, '{"id": 4, "username": "xu.sutian", "full_name": "徐素天", "role_code": "advisor", "phone_number": "13800000023", "last_login_at": "2026-04-05 09:00:00", "password_hash": "$pbkdf2-sha256$29000$orRW6l3rHWOMMeb8X8vZ2w$yBt8uqmPKhrdu7Kg9iItn5Id.06rttpMqgt15Oup/.E", "account_status": "启用", "department_name": "数据智能学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (6, '{"id": 6, "username": "he.lin", "full_name": "何琳", "role_code": "recruit_reviewer", "phone_number": "13800000025", "last_login_at": "2026-04-07 20:31:56", "password_hash": "$pbkdf2-sha256$29000$15oTAqB0bm2t1fo/x/i/tw$bBZXnpGNS4a3YF2Y/LK4X9MxeVpdLosUbXvnERPBKsI", "account_status": "启用", "department_name": "招生办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (7, '{"id": 7, "username": "cao.bo", "full_name": "曹博", "role_code": "interview_officer", "phone_number": "13800000026", "last_login_at": "2026-04-07 20:32:14", "password_hash": "$pbkdf2-sha256$29000$zdk7p7QWIiSEsJYyJgTgPA$7B79vX6lx71L6Bikm8eKkMTHB4Sd7nubfIHHr2hudTA", "account_status": "启用", "department_name": "招生办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (8, '{"id": 8, "username": "yang.qin", "full_name": "杨琴", "role_code": "hrbp", "phone_number": "13800000027", "last_login_at": "2026-04-07 20:32:40", "password_hash": "$pbkdf2-sha256$29000$0VpLyRmDEELoPYdQau29Vw$IKJK2kwKHjqV0NL3UtAXkttAmtLD24GDtYjuEL5iFzQ", "account_status": "启用", "department_name": "人力资源部"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (5, '{"id": 5, "username": "zhou.qing", "full_name": "周晴", "role_code": "secretary", "phone_number": "13800000024", "last_login_at": "2026-04-07 20:31:38", "password_hash": "$pbkdf2-sha256$29000$Rghh7B2jdK4VotTamxNizA$i2aBMIQoAYWLICfB2wLjqv5yr6NhpWr3kP8I2yeWWsI", "account_status": "启用", "department_name": "学位办公室"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (9, '{"id": 9, "username": "sun.wei", "full_name": "孙伟", "role_code": "party_affairs", "phone_number": "13800000028", "last_login_at": "2026-04-07 20:33:06", "password_hash": "$pbkdf2-sha256$29000$6X0vxfif8z5HKAVgjDEmxA$i.jQ93csIVlg6dbr1sqrfBowKaMZCwDisbWaF2EMZWs", "account_status": "启用", "department_name": "党群工作部"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (2, '{"id": 2, "username": "liu.ya", "full_name": "刘亚", "role_code": "advisor", "phone_number": "13800000021", "last_login_at": "2026-04-09 20:26:20", "password_hash": "$pbkdf2-sha256$29000$gHBuzZmTUmqNsbYWgrA2Bg$uIZuS.dgkFHpKWkrfYEWSvlN82b/6ga8RsuxazZCHh4", "account_status": "启用", "department_name": "智能制造学院"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_system_users" VALUES (1, '{"id": 1, "username": "admin", "full_name": "系统管理员", "role_code": "platform_admin", "phone_number": "13800000000", "last_login_at": "2026-04-23 13:45:39", "password_hash": "$pbkdf2-sha256$29000$l1LqXQvB.L93TomRMobQOg$9aLo8Vfx6V8DE0ppHrG5RnWCfTIBy6dt8Y.Y0.DAuTM", "account_status": "启用", "department_name": "学科与研究生管理处"}', '2026-04-23 13:45:40.482775+08');

-- ----------------------------
-- Table structure for dtlms_runtime_teams
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_teams";
CREATE TABLE "public"."dtlms_runtime_teams" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_teams
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_teams" VALUES (1, '{"id": 1, "status": "启用", "team_code": "TEAM-AUTO-001", "team_name": "智能制造团队", "created_on": "2026-04-21", "description": "由历史学生主档自动生成的团队记录。", "advisor_names": ["刘亚"], "established_on": "2026-04-21", "department_name": "未分配院系", "discipline_name": "未分配学科", "lead_advisor_name": "刘亚", "research_directions": []}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_teams" VALUES (2, '{"id": 2, "status": "启用", "team_code": "TEAM-AUTO-002", "team_name": "机器人应用团队", "created_on": "2026-04-21", "description": "由历史学生主档自动生成的团队记录。", "advisor_names": ["刘亚"], "established_on": "2026-04-21", "department_name": "未分配院系", "discipline_name": "未分配学科", "lead_advisor_name": "刘亚", "research_directions": []}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_teams" VALUES (3, '{"id": 3, "status": "启用", "team_code": "TEAM-AUTO-003", "team_name": "工业软件团队", "created_on": "2026-04-21", "description": "由历史学生主档自动生成的团队记录。", "advisor_names": ["袁野"], "established_on": "2026-04-21", "department_name": "未分配院系", "discipline_name": "未分配学科", "lead_advisor_name": "袁野", "research_directions": []}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_teams" VALUES (4, '{"id": 4, "status": "启用", "team_code": "TEAM-AUTO-004", "team_name": "数据智能团队", "created_on": "2026-04-21", "description": "由历史学生主档自动生成的团队记录。", "advisor_names": ["徐素天"], "established_on": "2026-04-21", "department_name": "未分配院系", "discipline_name": "未分配学科", "lead_advisor_name": "徐素天", "research_directions": []}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_teams" VALUES (5, '{"id": 5, "status": "启用", "team_code": "TEAM-AUTO-005", "team_name": "平台治理团队", "created_on": "2026-04-21", "description": "由历史学生主档自动生成的团队记录。", "advisor_names": ["袁野"], "established_on": "2026-04-21", "department_name": "未分配院系", "discipline_name": "未分配学科", "lead_advisor_name": "袁野", "research_directions": []}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_teams" VALUES (6, '{"id": 6, "status": "启用", "team_code": "CENTER-006", "team_name": "人工智能安全研究中心", "created_on": "2026-04-21", "description": null, "advisor_names": ["刘亚", "徐素天", "袁野"], "established_on": "2026-04-20", "department_name": "未分配院系", "discipline_name": "", "lead_advisor_name": "刘亚", "research_directions": []}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_theses
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_theses";
CREATE TABLE "public"."dtlms_runtime_theses" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_theses
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_theses" VALUES (1, '{"id": 1, "title": "面向工业软件的流程协同引擎设计与实现", "student_no": "D20220010", "advisor_name": "袁野", "business_key": "SWSQSP202604070001", "student_name": "张乐之", "degree_status": "待正式答辩", "thesis_status": "盲审通过", "defense_status": "正式答辩完成", "plagiarism_rate": 12.5, "blind_review_status": "已通过"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_theses" VALUES (2, '{"id": 2, "title": "知识图谱驱动的科研过程智能分析方法研究", "student_no": "D20220011", "advisor_name": "徐素天", "business_key": "SWSQSP202604070002", "student_name": "赵嘉禾", "degree_status": "授位审批中", "thesis_status": "查重通过", "defense_status": "待安排", "plagiarism_rate": 15.2, "blind_review_status": "进行中"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_theses" VALUES (3, '{"id": 3, "title": "机器人视觉检测中的多模态融合方法研究", "student_no": "D20220012", "advisor_name": "刘亚", "business_key": "SWSQSP202604070003", "student_name": "顾清越", "degree_status": "未授位", "thesis_status": "退回修改", "defense_status": "未进入", "plagiarism_rate": 18.0, "blind_review_status": "未通过"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_theses" VALUES (4, '{"id": 4, "title": "面向教育场景的大模型知识对齐与应用研究", "student_no": "D20230006", "advisor_name": "徐素天", "business_key": "SWSQSP202604070004", "student_name": "沈知遥", "degree_status": "待申请", "thesis_status": "待查重", "defense_status": "未进入", "plagiarism_rate": 9.8, "blind_review_status": "未送审"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_theses" VALUES (6, '{"id": 6, "title": "沈知遥学位申请闭环模拟-20260409201505", "student_no": "D20230006", "advisor_name": "徐素天", "business_key": "SWSQSP202604090002", "student_name": "沈知遥", "degree_status": "待正式答辩", "thesis_status": "盲审通过", "defense_status": "待安排", "plagiarism_rate": 7.8, "blind_review_status": "已通过"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_thesis_reviews
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_thesis_reviews";
CREATE TABLE "public"."dtlms_runtime_thesis_reviews" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_thesis_reviews
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_thesis_reviews" VALUES (1, '{"id": 1, "thesis_id": 1, "expert_name": "何振华", "review_score": 86.0, "thesis_title": "面向工业软件的流程协同引擎设计与实现", "review_status": "已通过", "review_comment": "研究目标明确，工程实现完整。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_thesis_reviews" VALUES (2, '{"id": 2, "thesis_id": 1, "expert_name": "潘雪松", "review_score": 88.0, "thesis_title": "面向工业软件的流程协同引擎设计与实现", "review_status": "已通过", "review_comment": "实验设计充分，建议补充性能对比。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_thesis_reviews" VALUES (3, '{"id": 3, "thesis_id": 2, "expert_name": "杨知行", "review_score": null, "thesis_title": "知识图谱驱动的科研过程智能分析方法研究", "review_status": "待反馈", "review_comment": null}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_thesis_reviews" VALUES (4, '{"id": 4, "thesis_id": 3, "expert_name": "陈明哲", "review_score": 70.0, "thesis_title": "机器人视觉检测中的多模态融合方法研究", "review_status": "需修改", "review_comment": "理论分析不充分，需要补强实验结果。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_thesis_reviews" VALUES (5, '{"id": 5, "thesis_id": 1, "expert_name": "评审专家A", "review_score": 90.0, "thesis_title": "性能验证论文", "review_status": "已完成", "review_comment": "仅验证增量持久化-更新"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_training_plans
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_training_plans";
CREATE TABLE "public"."dtlms_runtime_training_plans" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_training_plans
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (1, '{"id": 1, "student_no": "D20240001", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "月度", "student_name": "陈一鸣", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕智能制造团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (2, '{"id": 2, "student_no": "D20240002", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "月度", "student_name": "林书雅", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕机器人应用团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (3, '{"id": 3, "student_no": "D20240003", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "袁野", "report_cycle": "月度", "student_name": "周启航", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕工业软件团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (4, '{"id": 4, "student_no": "D20240004", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "月度", "student_name": "顾南乔", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (5, '{"id": 5, "student_no": "D20230005", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "袁野", "report_cycle": "季度", "student_name": "赵嘉霖", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕工业软件团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (6, '{"id": 6, "student_no": "D20230006", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "季度", "student_name": "沈知遥", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (7, '{"id": 7, "student_no": "D20230007", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "季度", "student_name": "王书宁", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕智能制造团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (8, '{"id": 8, "student_no": "D20230008", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "季度", "student_name": "贺景川", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (9, '{"id": 9, "student_no": "D20230009", "version_no": "v2.0", "plan_status": "待学生确认", "advisor_name": "袁野", "report_cycle": "季度", "student_name": "许安然", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕工业软件团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (10, '{"id": 10, "student_no": "D20220010", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "袁野", "report_cycle": "季度", "student_name": "张乐之", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕工业软件团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (11, '{"id": 11, "student_no": "D20220011", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "季度", "student_name": "赵嘉禾", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (12, '{"id": 12, "student_no": "D20220012", "version_no": "v2.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "季度", "student_name": "顾清越", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕机器人应用团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (13, '{"id": 13, "student_no": "D20250013", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "月度", "student_name": "宋知行", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕智能制造团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (14, '{"id": 14, "student_no": "D20250014", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "月度", "student_name": "江若溪", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (15, '{"id": 15, "student_no": "D20250015", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "袁野", "report_cycle": "月度", "student_name": "孟书恒", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕平台治理团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (16, '{"id": 16, "student_no": "D20250016", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "刘亚", "report_cycle": "月度", "student_name": "魏知远", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕机器人应用团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (17, '{"id": 17, "student_no": "D20240017", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "袁野", "report_cycle": "月度", "student_name": "韩嘉宁", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕工业软件团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_training_plans" VALUES (18, '{"id": 18, "student_no": "D20240018", "version_no": "v1.0", "plan_status": "执行中", "advisor_name": "徐素天", "report_cycle": "月度", "student_name": "陆承泽", "assessment_rule": "按周期提交科研报告，完成阶段汇报与论文节点考核。", "scientific_goal": "围绕数据智能团队承担课题，形成阶段性论文与系统原型。"}', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_runtime_workflow_tasks
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_runtime_workflow_tasks";
CREATE TABLE "public"."dtlms_runtime_workflow_tasks" (
  "id" int8 NOT NULL,
  "payload" jsonb NOT NULL,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_runtime_workflow_tasks
-- ----------------------------
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (46, '{"id": 46, "title": "李小玉报名审核", "due_at": "2026-04-24 11:49:20", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-23 11:49:20", "action_label": "发起流程", "result_status": "待处理", "operator_username": "13521297322", "operator_full_name": "13521297322"}], "node_key": "qualification_review", "priority": "中", "entity_id": 26, "flow_code": "recruitment_application", "created_at": "2026-04-23 11:49:20", "business_key": "ZSLQSP202604230009", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-eede6d1dd9", "form_summary": "业务编号：ZSLQSP202604230009；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "李小玉", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (36, '{"id": 36, "title": "??????报名审核", "due_at": "2026-04-22 02:02:08", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-21 02:02:08", "action_label": "发起流程", "result_status": "待处理", "operator_username": "139836871113", "operator_full_name": "139836871113"}], "node_key": "qualification_review", "priority": "中", "entity_id": 18, "flow_code": "recruitment_application", "created_at": "2026-04-21 02:02:08", "business_key": "ZSLQSP202604210006", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-5df923986a", "form_summary": "业务编号：ZSLQSP202604210006；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "??????", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604210006-034d0beb2e", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (34, '{"id": 34, "title": "联调考生报名审核", "due_at": "2026-04-22 01:53:57", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-21 01:53:57", "action_label": "发起流程", "result_status": "待处理", "operator_username": "136449765890", "operator_full_name": "136449765890"}], "node_key": "qualification_review", "priority": "中", "entity_id": 16, "flow_code": "recruitment_application", "created_at": "2026-04-21 01:53:57", "business_key": "ZSLQSP202604210004", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-f9b4e63f9c", "form_summary": "业务编号：ZSLQSP202604210004；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "联调考生", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604210004-198915ce91", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (33, '{"id": 33, "title": "在线联调0410132736报名审核", "due_at": "2026-04-11 13:27:37", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-10 13:27:37", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 15, "flow_code": "recruitment_application", "created_at": "2026-04-10 13:27:37", "business_key": "ZSLQSP202604100004", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-7d07ba753a", "form_summary": "业务编号：ZSLQSP202604100004；研究方向：智能科学；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "在线联调0410132736", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604100004-58be9b522d", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (35, '{"id": 35, "title": "Portal Smoke User报名审核", "due_at": "2026-04-22 01:58:19", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-21 01:58:19", "action_label": "发起流程", "result_status": "待处理", "operator_username": "138610893902", "operator_full_name": "138610893902"}], "node_key": "qualification_review", "priority": "中", "entity_id": 17, "flow_code": "recruitment_application", "created_at": "2026-04-21 01:58:19", "business_key": "ZSLQSP202604210005", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-887e01a071", "form_summary": "业务编号：ZSLQSP202604210005；研究方向：智能制造团队；材料状态：待补材料", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "Portal Smoke User", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (32, '{"id": 32, "title": "联调考生0410132613报名审核", "due_at": "2026-04-11 13:26:14", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-10 13:26:14", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 14, "flow_code": "recruitment_application", "created_at": "2026-04-10 13:26:14", "business_key": "ZSLQSP202604100003", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-18c95ca2f8", "form_summary": "业务编号：ZSLQSP202604100003；研究方向：智能科学；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "联调考生0410132613", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (31, '{"id": 31, "title": "联调考生0410131457报名审核", "due_at": "2026-04-11 13:14:58", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-10 13:14:58", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 13, "flow_code": "recruitment_application", "created_at": "2026-04-10 13:14:58", "business_key": "ZSLQSP202604100001", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-44869f7eed", "form_summary": "业务编号：ZSLQSP202604100001；研究方向：人工智能；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "联调考生0410131457", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604100001-7a103518ab", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (28, '{"id": 28, "title": "沈知遥授位审批", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_precheck", "priority": "中", "entity_id": 4, "flow_code": "thesis", "created_at": "2026-04-07 18:50:41", "business_key": "SWSQSP202604070004", "current_node": "导师预审", "execution_id": "exec-advisorprecheck-19a4d28b0a", "form_summary": "论文题目：面向教育场景的大模型知识对齐与应用研究；盲审状态：未送审", "deployment_id": "dep-thesis-d4b0719b", "workflow_name": "学位申请审批", "applicant_name": "沈知遥", "business_module": "学位管理", "current_handler": "徐素天", "business_dataset": "theses", "candidate_groups": ["advisor"], "process_instance_id": "procinst-thesis-swsqsp202604070004-e14f35b86f", "task_definition_key": "advisor_precheck", "process_definition_id": "procdef-thesis-v1-065eef39", "process_definition_key": "thesis", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (27, '{"id": 27, "title": "顾清越授位审批", "due_at": "2026-04-07 18:50:41", "status": "已驳回", "history": [], "priority": "中", "entity_id": 3, "flow_code": "thesis", "created_at": "2026-04-07 18:50:41", "business_key": "SWSQSP202604070003", "current_node": "流程结束", "execution_id": "exec-流程结束-7011ec3729", "form_summary": "论文题目：机器人视觉检测中的多模态融合方法研究；盲审状态：未通过", "deployment_id": "dep-thesis-d4b0719b", "workflow_name": "学位申请审批", "applicant_name": "顾清越", "business_module": "学位管理", "current_handler": "流程结束", "business_dataset": "theses", "candidate_groups": [], "process_instance_id": "procinst-thesis-swsqsp202604070003-559b20e292", "task_definition_key": "流程结束", "process_definition_id": "procdef-thesis-v1-065eef39", "process_definition_key": "thesis", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (26, '{"id": 26, "title": "赵嘉禾授位审批", "due_at": "2026-04-09 18:50:41", "status": "处理中", "history": [], "node_key": "secretary_review", "priority": "中", "entity_id": 2, "flow_code": "thesis", "created_at": "2026-04-07 18:50:41", "business_key": "SWSQSP202604070002", "current_node": "材料复核", "execution_id": "exec-secretaryreview-02832ea26f", "form_summary": "论文题目：知识图谱驱动的科研过程智能分析方法研究；盲审状态：进行中", "deployment_id": "dep-thesis-d4b0719b", "workflow_name": "学位申请审批", "applicant_name": "赵嘉禾", "business_module": "学位管理", "current_handler": "学位秘书", "business_dataset": "theses", "candidate_groups": ["secretary"], "process_instance_id": "procinst-thesis-swsqsp202604070002-1fdcd41689", "task_definition_key": "secretary_review", "process_definition_id": "procdef-thesis-v1-065eef39", "process_definition_key": "thesis", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (25, '{"id": 25, "title": "张乐之授位审批", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 1, "flow_code": "thesis", "created_at": "2026-04-07 18:50:41", "business_key": "SWSQSP202604070001", "current_node": "流程结束", "execution_id": "exec-流程结束-fa6064ddba", "form_summary": "论文题目：面向工业软件的流程协同引擎设计与实现；盲审状态：已通过", "deployment_id": "dep-thesis-d4b0719b", "workflow_name": "学位申请审批", "applicant_name": "张乐之", "business_module": "学位管理", "current_handler": "流程结束", "business_dataset": "theses", "candidate_groups": [], "process_instance_id": "procinst-thesis-swsqsp202604070001-206582850c", "task_definition_key": "流程结束", "process_definition_id": "procdef-thesis-v1-065eef39", "process_definition_key": "thesis", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (23, '{"id": 23, "title": "周启航外出研修申请", "due_at": "2026-04-07 18:50:41", "status": "已驳回", "history": [], "priority": "中", "entity_id": 3, "flow_code": "outbound_study", "created_at": "2026-04-07 18:50:41", "business_key": "WCYXSP202604070003", "current_node": "流程结束", "execution_id": "exec-流程结束-35415dcddd", "form_summary": "研修地点：中控技术研究院；起止：2026-05-01 至 2026-07-31", "deployment_id": "dep-outboundstudy-6d8e1576", "workflow_name": "外出研修审批", "applicant_name": "周启航", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "outbound_studies", "candidate_groups": [], "process_instance_id": "procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9", "task_definition_key": "流程结束", "process_definition_id": "procdef-outboundstudy-v1-aadfc5bd", "process_definition_key": "outbound_study", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (22, '{"id": 22, "title": "贺景川外出研修申请", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_review", "priority": "中", "entity_id": 2, "flow_code": "outbound_study", "created_at": "2026-04-07 18:50:41", "business_key": "WCYXSP202604070002", "current_node": "导师审核", "execution_id": "exec-advisorreview-d65a8149b8", "form_summary": "研修地点：香港科技大学；起止：2026-02-15 至 2026-07-30", "deployment_id": "dep-outboundstudy-6d8e1576", "workflow_name": "外出研修审批", "applicant_name": "贺景川", "business_module": "培养管理", "current_handler": "徐素天", "business_dataset": "outbound_studies", "candidate_groups": ["advisor"], "process_instance_id": "procinst-outboundstudy-wcyxsp202604070002-4d16cbba15", "task_definition_key": "advisor_review", "process_definition_id": "procdef-outboundstudy-v1-aadfc5bd", "process_definition_key": "outbound_study", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (21, '{"id": 21, "title": "王书宁外出研修申请", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 1, "flow_code": "outbound_study", "created_at": "2026-04-07 18:50:41", "business_key": "WCYXSP202604070001", "current_node": "流程结束", "execution_id": "exec-流程结束-d4614c71c7", "form_summary": "研修地点：新加坡国立大学；起止：2026-03-01 至 2026-08-31", "deployment_id": "dep-outboundstudy-6d8e1576", "workflow_name": "外出研修审批", "applicant_name": "王书宁", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "outbound_studies", "candidate_groups": [], "process_instance_id": "procinst-outboundstudy-wcyxsp202604070001-305be95a20", "task_definition_key": "流程结束", "process_definition_id": "procdef-outboundstudy-v1-aadfc5bd", "process_definition_key": "outbound_study", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (24, '{"id": 24, "title": "孟书恒外出研修申请", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_review", "priority": "中", "entity_id": 4, "flow_code": "outbound_study", "created_at": "2026-04-07 18:50:41", "business_key": "WCYXSP202604070004", "current_node": "导师审核", "execution_id": "exec-advisorreview-b5efa6424c", "form_summary": "研修地点：深圳；起止：2026-05-18 至 2026-05-22", "deployment_id": "dep-outboundstudy-6d8e1576", "workflow_name": "外出研修审批", "applicant_name": "孟书恒", "business_module": "培养管理", "current_handler": "袁野", "business_dataset": "outbound_studies", "candidate_groups": ["advisor"], "process_instance_id": "procinst-outboundstudy-wcyxsp202604070004-d049327905", "task_definition_key": "advisor_review", "process_definition_id": "procdef-outboundstudy-v1-aadfc5bd", "process_definition_key": "outbound_study", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (19, '{"id": 19, "title": "宋知行科研报告审阅", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_review", "priority": "中", "entity_id": 7, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070007", "current_node": "导师审阅", "execution_id": "exec-advisorreview-5dfab64a31", "form_summary": "周期：2026Q1；审阅人：刘亚", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "宋知行", "business_module": "培养管理", "current_handler": "导师", "business_dataset": "scientific_reports", "candidate_groups": ["advisor"], "process_instance_id": "procinst-scientificreport-kybgsy202604070007-3c62b8afbd", "task_definition_key": "advisor_review", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (18, '{"id": 18, "title": "沈知遥科研报告审阅", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_review", "priority": "中", "entity_id": 6, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070006", "current_node": "导师审阅", "execution_id": "exec-advisorreview-b7c77ef380", "form_summary": "周期：2026Q1；审阅人：徐素天", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "沈知遥", "business_module": "培养管理", "current_handler": "导师", "business_dataset": "scientific_reports", "candidate_groups": ["advisor"], "process_instance_id": "procinst-scientificreport-kybgsy202604070006-a75676b582", "task_definition_key": "advisor_review", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (17, '{"id": 17, "title": "赵嘉霖科研报告审阅", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 5, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070005", "current_node": "流程结束", "execution_id": "exec-流程结束-db12ceaa3d", "form_summary": "周期：2026Q1；审阅人：袁野", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "赵嘉霖", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "scientific_reports", "candidate_groups": [], "process_instance_id": "procinst-scientificreport-kybgsy202604070005-aede151d38", "task_definition_key": "流程结束", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (16, '{"id": 16, "title": "顾南乔科研报告审阅", "due_at": "2026-04-07 18:50:41", "status": "已驳回", "history": [], "priority": "中", "entity_id": 4, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070004", "current_node": "流程结束", "execution_id": "exec-流程结束-6535188ef7", "form_summary": "周期：2026Q1；审阅人：徐素天", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "顾南乔", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "scientific_reports", "candidate_groups": [], "process_instance_id": "procinst-scientificreport-kybgsy202604070004-d492085f3f", "task_definition_key": "流程结束", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (15, '{"id": 15, "title": "周启航科研报告审阅", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 3, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070003", "current_node": "流程结束", "execution_id": "exec-流程结束-7a9deb4a07", "form_summary": "周期：2026Q1；审阅人：袁野", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "周启航", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "scientific_reports", "candidate_groups": [], "process_instance_id": "procinst-scientificreport-kybgsy202604070003-6a150f25a3", "task_definition_key": "流程结束", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (14, '{"id": 14, "title": "林书雅科研报告审阅", "due_at": "2026-04-09 18:50:41", "status": "待处理", "history": [], "node_key": "advisor_review", "priority": "中", "entity_id": 2, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070002", "current_node": "导师审阅", "execution_id": "exec-advisorreview-4b9b967c7f", "form_summary": "周期：2026Q1；审阅人：刘亚", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "林书雅", "business_module": "培养管理", "current_handler": "导师", "business_dataset": "scientific_reports", "candidate_groups": ["advisor"], "process_instance_id": "procinst-scientificreport-kybgsy202604070002-56f9d14cb3", "task_definition_key": "advisor_review", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (13, '{"id": 13, "title": "陈一鸣科研报告审阅", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 1, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070001", "current_node": "流程结束", "execution_id": "exec-流程结束-f7640479cc", "form_summary": "周期：2026Q1；审阅人：刘亚", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "陈一鸣", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "scientific_reports", "candidate_groups": [], "process_instance_id": "procinst-scientificreport-kybgsy202604070001-ac313f254d", "task_definition_key": "流程结束", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (12, '{"id": 12, "title": "谢明远报名审核", "due_at": "2026-04-08 18:50:41", "status": "待处理", "history": [], "node_key": "qualification_review", "priority": "中", "entity_id": 12, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070012", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-edf7c6e87f", "form_summary": "业务编号：ZSLQSP202604070012；研究方向：机器学习；材料状态：已退回修改", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "谢明远", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070012-31b22e411a", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (11, '{"id": 11, "title": "朱安宁报名审核", "due_at": "2026-04-09 18:50:41", "status": "处理中", "history": [], "node_key": "admission_decision", "priority": "中", "entity_id": 11, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070011", "current_node": "录取决策", "execution_id": "exec-admissiondecision-aaede43f43", "form_summary": "业务编号：ZSLQSP202604070011；研究方向：知识图谱；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "朱安宁", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070011-48934cba0b", "task_definition_key": "admission_decision", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (10, '{"id": 10, "title": "韩知遇报名审核", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 10, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070010", "current_node": "流程结束", "execution_id": "exec-流程结束-65775a0795", "form_summary": "业务编号：ZSLQSP202604070010；研究方向：工业数据治理；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "韩知遇", "business_module": "招生管理", "current_handler": "流程结束", "business_dataset": "recruitment_applications", "candidate_groups": [], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070010-beee23a649", "task_definition_key": "流程结束", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (9, '{"id": 9, "title": "钱北辰报名审核", "due_at": "2026-04-07 18:50:41", "status": "已驳回", "history": [], "priority": "中", "entity_id": 9, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070009", "current_node": "流程结束", "execution_id": "exec-流程结束-e3bb67368b", "form_summary": "业务编号：ZSLQSP202604070009；研究方向：模型驱动开发；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "钱北辰", "business_module": "招生管理", "current_handler": "流程结束", "business_dataset": "recruitment_applications", "candidate_groups": [], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070009-01cf086f21", "task_definition_key": "流程结束", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (8, '{"id": 8, "title": "林知夏报名审核", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 8, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070008", "current_node": "流程结束", "execution_id": "exec-流程结束-446886c26d", "form_summary": "业务编号：ZSLQSP202604070008；研究方向：软件工程；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "林知夏", "business_module": "招生管理", "current_handler": "流程结束", "business_dataset": "recruitment_applications", "candidate_groups": [], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070008-23605124be", "task_definition_key": "流程结束", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (7, '{"id": 7, "title": "赵安歌报名审核", "due_at": "2026-04-08 18:50:41", "status": "处理中", "history": [], "node_key": "qualification_passed", "priority": "中", "entity_id": 7, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070007", "current_node": "评分准备", "execution_id": "exec-qualificationpasse-be93ae536d", "form_summary": "业务编号：ZSLQSP202604070007；研究方向：工业软件；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "赵安歌", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070007-b6a620fd62", "task_definition_key": "qualification_passed", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (6, '{"id": 6, "title": "陈思远报名审核", "due_at": "2026-04-08 18:50:41", "status": "待处理", "history": [], "node_key": "qualification_review", "priority": "中", "entity_id": 6, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070006", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-1fb9c8f469", "form_summary": "业务编号：ZSLQSP202604070006；研究方向：数字孪生；材料状态：待补材料", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "陈思远", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070006-ab47be6465", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (5, '{"id": 5, "title": "李静姝报名审核", "due_at": "2026-04-09 18:50:41", "status": "处理中", "history": [], "node_key": "interview_arrangement", "priority": "中", "entity_id": 5, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070005", "current_node": "面试安排", "execution_id": "exec-interviewarrangeme-7f0810d43d", "form_summary": "业务编号：ZSLQSP202604070005；研究方向：数据智能；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "李静姝", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070005-2131f46425", "task_definition_key": "interview_arrangement", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (4, '{"id": 4, "title": "周亦凡报名审核", "due_at": "2026-04-09 18:50:41", "status": "处理中", "history": [], "node_key": "admission_decision", "priority": "中", "entity_id": 4, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070004", "current_node": "录取决策", "execution_id": "exec-admissiondecision-fcaa129de5", "form_summary": "业务编号：ZSLQSP202604070004；研究方向：视觉检测；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "周亦凡", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070004-716ef62d39", "task_definition_key": "admission_decision", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (3, '{"id": 3, "title": "顾明睿报名审核", "due_at": "2026-04-09 18:50:41", "status": "处理中", "history": [], "node_key": "admission_confirmation", "priority": "中", "entity_id": 3, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070003", "current_node": "录取确认", "execution_id": "exec-admissionconfirmat-165e308f11", "form_summary": "业务编号：ZSLQSP202604070003；研究方向：工业互联网；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "顾明睿", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070003-15d97c12b2", "task_definition_key": "admission_confirmation", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (2, '{"id": 2, "title": "沈清禾报名审核", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 2, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070002", "current_node": "流程结束", "execution_id": "exec-流程结束-c2af43da3a", "form_summary": "业务编号：ZSLQSP202604070002；研究方向：机器人控制；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "沈清禾", "business_module": "招生管理", "current_handler": "流程结束", "business_dataset": "recruitment_applications", "candidate_groups": [], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070002-5625e6238f", "task_definition_key": "流程结束", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (1, '{"id": 1, "title": "吴启程报名审核", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 1, "flow_code": "recruitment_application", "created_at": "2026-04-07 18:50:41", "business_key": "ZSLQSP202604070001", "current_node": "流程结束", "execution_id": "exec-流程结束-d27bde8440", "form_summary": "业务编号：ZSLQSP202604070001；研究方向：智能制造；材料状态：材料齐全", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "吴启程", "business_module": "招生管理", "current_handler": "流程结束", "business_dataset": "recruitment_applications", "candidate_groups": [], "process_instance_id": "procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04", "task_definition_key": "流程结束", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (20, '{"id": 20, "title": "江若溪科研报告审阅", "due_at": "2026-04-07 18:50:41", "status": "已通过", "history": [], "priority": "中", "entity_id": 8, "flow_code": "scientific_report", "created_at": "2026-04-07 18:50:41", "business_key": "KYBGSY202604070008", "current_node": "流程结束", "execution_id": "exec-流程结束-7e005951a7", "form_summary": "周期：2026Q1；审阅人：徐素天", "deployment_id": "dep-scientificreport-9069a4b1", "workflow_name": "科研报告审阅", "applicant_name": "江若溪", "business_module": "培养管理", "current_handler": "流程结束", "business_dataset": "scientific_reports", "candidate_groups": [], "process_instance_id": "procinst-scientificreport-kybgsy202604070008-f6ee0b043e", "task_definition_key": "流程结束", "process_definition_id": "procdef-scientificreport-v1-60dc0211", "process_definition_key": "scientific_report", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (30, '{"id": 30, "title": "沈知遥授位审批", "due_at": "2026-04-11 20:15:15", "status": "已通过", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "导师预审", "from_node": "开始", "operated_at": "2026-04-09 20:15:05", "action_label": "发起流程", "result_status": "待处理", "operator_username": "xu.sutian", "operator_full_name": "xu.sutian"}, {"action": "submit_review", "comment": "导师完成预审并提交送审", "to_node": "材料复核", "from_node": "导师预审", "operated_at": "2026-04-09 20:15:15", "action_label": "提交送审", "result_status": "处理中", "operator_username": "xu.sutian", "operator_full_name": "徐素天"}, {"action": "approve", "comment": "学位秘书复核通过", "to_node": "流程结束", "from_node": "材料复核", "operated_at": "2026-04-09 20:15:26", "action_label": "复核通过", "result_status": "已通过", "operator_username": "zhou.qing", "operator_full_name": "周晴"}], "node_key": null, "priority": "中", "entity_id": 6, "flow_code": "thesis", "created_at": "2026-04-09 20:15:05", "business_key": "SWSQSP202604090002", "current_node": "流程结束", "execution_id": "exec-流程结束-387b35c278", "form_summary": "论文题目：沈知遥学位申请闭环模拟-20260409201505；盲审状态：已通过", "deployment_id": "dep-thesis-d4b0719b", "workflow_name": "学位申请审批", "applicant_name": "沈知遥", "latest_comment": "学位秘书复核通过", "business_module": "学位管理", "current_handler": "流程结束", "business_dataset": "theses", "candidate_groups": [], "process_instance_id": "procinst-thesis-swsqsp202604090002-a0b74461b9", "task_definition_key": "流程结束", "process_definition_id": "procdef-thesis-v1-065eef39", "process_definition_key": "thesis", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (40, '{"id": 40, "title": "性能回归be009f7d报名审核", "due_at": "2026-04-23 09:24:02", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:24:02", "action_label": "发起流程", "result_status": "待处理", "operator_username": "139be009f7d", "operator_full_name": "139be009f7d"}], "node_key": "qualification_review", "priority": "中", "entity_id": 20, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:24:02", "business_key": "ZSLQSP202604220001", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-8e43da6197", "form_summary": "业务编号：ZSLQSP202604220001；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "性能回归be009f7d", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220001-241ea95845", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (41, '{"id": 41, "title": "直建更新be009f7d报名审核", "due_at": "2026-04-23 09:24:03", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:24:03", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 21, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:24:03", "business_key": "ZSLQSP202604220002", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-d7d537306f", "form_summary": "业务编号：ZSLQSP202604220002；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "直建更新be009f7d", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220002-296d571cdb", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (42, '{"id": 42, "title": "导入be009f7d报名审核", "due_at": "2026-04-23 09:24:04", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:24:04", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 22, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:24:04", "business_key": "ZSLQSP202604220003", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-a7d2ad7040", "form_summary": "业务编号：ZSLQSP202604220003；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "导入be009f7d", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220003-29575e36a6", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (43, '{"id": 43, "title": "性能回归52d69275报名审核", "due_at": "2026-04-23 09:25:28", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:25:28", "action_label": "发起流程", "result_status": "待处理", "operator_username": "13952d69275", "operator_full_name": "13952d69275"}], "node_key": "qualification_review", "priority": "中", "entity_id": 23, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:25:28", "business_key": "ZSLQSP202604220004", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-1ddc0baae8", "form_summary": "业务编号：ZSLQSP202604220004；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "性能回归52d69275", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220004-324dcc7038", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (44, '{"id": 44, "title": "直建更新52d69275报名审核", "due_at": "2026-04-23 09:25:29", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:25:29", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 24, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:25:29", "business_key": "ZSLQSP202604220005", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-5263e586fb", "form_summary": "业务编号：ZSLQSP202604220005；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "直建更新52d69275", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (45, '{"id": 45, "title": "导入52d69275报名审核", "due_at": "2026-04-23 09:25:30", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-22 09:25:30", "action_label": "发起流程", "result_status": "待处理", "operator_username": "admin", "operator_full_name": "admin"}], "node_key": "qualification_review", "priority": "中", "entity_id": 25, "flow_code": "recruitment_application", "created_at": "2026-04-22 09:25:30", "business_key": "ZSLQSP202604220006", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-355ccf5e2d", "form_summary": "业务编号：ZSLQSP202604220006；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "导入52d69275", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604220006-a2ef59760e", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (37, '{"id": 37, "title": "测试管理保存报名审核", "due_at": "2026-04-22 02:06:20", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-21 02:06:20", "action_label": "发起流程", "result_status": "待处理", "operator_username": "132786107897", "operator_full_name": "132786107897"}], "node_key": "qualification_review", "priority": "中", "entity_id": 19, "flow_code": "recruitment_application", "created_at": "2026-04-21 02:06:20", "business_key": "ZSLQSP202604210007", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-59a9b3ebba", "form_summary": "业务编号：ZSLQSP202604210007；研究方向：智能制造团队；材料状态：待补材料", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "测试管理保存", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_runtime_workflow_tasks" VALUES (47, '{"id": 47, "title": "罗凯报名审核", "due_at": "2026-04-24 12:01:25", "status": "待处理", "history": [{"action": "start", "comment": "流程已发起，等待节点处理。", "to_node": "资格审核", "from_node": "开始", "operated_at": "2026-04-23 12:01:25", "action_label": "发起流程", "result_status": "待处理", "operator_username": "18615768209", "operator_full_name": "18615768209"}], "node_key": "qualification_review", "priority": "中", "entity_id": 27, "flow_code": "recruitment_application", "created_at": "2026-04-23 12:01:25", "business_key": "ZSLQSP202604230010", "current_node": "资格审核", "execution_id": "exec-qualificationrevie-d9ac1235d8", "form_summary": "业务编号：ZSLQSP202604230010；研究方向：智能制造团队；材料状态：待审核", "deployment_id": "dep-recruitmentapplication-4588d501", "workflow_name": "招生录取审批", "applicant_name": "罗凯", "latest_comment": "流程已发起，等待节点处理。", "business_module": "招生管理", "current_handler": "学合管理员", "business_dataset": "recruitment_applications", "candidate_groups": ["platform_admin"], "process_instance_id": "procinst-recruitmentappli-zslqsp202604230010-4e7a27718a", "task_definition_key": "qualification_review", "process_definition_id": "procdef-recruitmentapplicati-v1-52a2d0f8", "process_definition_key": "recruitment_application", "process_definition_version": 1}', '2026-04-23 13:43:23.07594+08');

-- ----------------------------
-- Table structure for dtlms_scientific_reports
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_scientific_reports";
CREATE TABLE "public"."dtlms_scientific_reports" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_scientific_reports_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "training_plan_id" int8 NOT NULL,
  "period_label" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "report_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "summary" text COLLATE "pg_catalog"."default" NOT NULL,
  "attachment_url" varchar(255) COLLATE "pg_catalog"."default",
  "reviewer_advisor_id" int8,
  "review_score" numeric(5,2),
  "review_comment" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "business_key" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of dtlms_scientific_reports
-- ----------------------------
INSERT INTO "public"."dtlms_scientific_reports" VALUES (1, 1, 1, '2026Q1', 'reviewed', '完成产线调度算法优化与仿真验证。', '/reports/D20240001/2026Q1.pdf', 1, 92.00, '导入状态：已通过', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070001');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (2, 2, 2, '2026Q1', 'reviewing', '完成机器人视觉检测数据采集。', '/reports/D20240002/2026Q1.pdf', 1, NULL, '导入状态：待导师审阅', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070002');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (3, 3, 3, '2026Q1', 'reviewed', '完成工业软件模块设计与接口联调。', '/reports/D20240003/2026Q1.pdf', 2, 88.00, '导入状态：已通过', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070003');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (4, 4, 4, '2026Q1', 'rework', '实验结果不足，需要补充对比分析。', '/reports/D20240004/2026Q1.pdf', 3, 76.00, '导入状态：退回修改', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070004');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (5, 5, 5, '2026Q1', 'reviewed', '完成企业实习阶段需求分析与文档输出。', '/reports/D20230005/2026Q1.pdf', 2, 90.00, '导入状态：已通过', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070005');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (6, 6, 6, '2026Q1', 'reviewing', '完成知识图谱抽取规则验证。', '/reports/D20230006/2026Q1.pdf', 3, NULL, '导入状态：待导师审阅', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070006');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (7, 13, 13, '2026Q1', 'reviewing', '完成入组初期课题调研和综述整理。', '/reports/D20250013/2026Q1.pdf', 1, NULL, '导入状态：待导师审阅', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070007');
INSERT INTO "public"."dtlms_scientific_reports" VALUES (8, 14, 14, '2026Q1', 'reviewed', '完成大模型辅助标注流程验证。', '/reports/D20250014/2026Q1.pdf', 3, 89.00, '导入状态：已通过', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'KYBGSY202604070008');

-- ----------------------------
-- Table structure for dtlms_student_advisor_history
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_student_advisor_history";
CREATE TABLE "public"."dtlms_student_advisor_history" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_student_advisor_history_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "advisor_id" int8 NOT NULL,
  "relation_type" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'primary'::character varying,
  "start_date" date NOT NULL,
  "end_date" date,
  "change_reason" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_student_advisor_history
-- ----------------------------
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (1, 1, 1, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (2, 2, 1, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (3, 3, 2, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (4, 4, 3, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (5, 5, 2, 'primary', '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (6, 6, 3, 'primary', '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (7, 7, 1, 'primary', '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (8, 8, 3, 'primary', '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (9, 9, 2, 'primary', '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (10, 10, 2, 'primary', '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (11, 11, 3, 'primary', '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (12, 12, 1, 'primary', '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (13, 13, 1, 'primary', '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (14, 15, 2, 'primary', '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (15, 16, 1, 'primary', '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (16, 17, 2, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (17, 14, 3, 'primary', '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_advisor_history" VALUES (18, 18, 3, 'primary', '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_student_team_history
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_student_team_history";
CREATE TABLE "public"."dtlms_student_team_history" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_student_team_history_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "team_id" int8 NOT NULL,
  "start_date" date NOT NULL,
  "end_date" date,
  "change_reason" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_student_team_history
-- ----------------------------
INSERT INTO "public"."dtlms_student_team_history" VALUES (1, 1, 1, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (2, 2, 2, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (3, 3, 3, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (4, 4, 4, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (5, 5, 3, '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (6, 6, 4, '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (7, 7, 1, '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (8, 8, 4, '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (9, 9, 3, '2023-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (10, 10, 3, '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (11, 11, 4, '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (12, 12, 2, '2022-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (13, 13, 1, '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (14, 15, 5, '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (15, 16, 2, '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (16, 17, 3, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (17, 14, 4, '2025-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_student_team_history" VALUES (18, 18, 4, '2024-09-01', NULL, '初始化导入', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_students
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_students";
CREATE TABLE "public"."dtlms_students" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_students_id_seq'::regclass),
  "student_no" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "full_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "gender" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "political_status" varchar(32) COLLATE "pg_catalog"."default",
  "phone_number" varchar(32) COLLATE "pg_catalog"."default",
  "identity_no" varchar(64) COLLATE "pg_catalog"."default",
  "enrollment_year" int4 NOT NULL,
  "degree_type" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "team_name" varchar(128) COLLATE "pg_catalog"."default",
  "current_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'enrolled'::character varying,
  "primary_advisor_id" int8,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "team_id" int8
)
;

-- ----------------------------
-- Records of dtlms_students
-- ----------------------------
INSERT INTO "public"."dtlms_students" VALUES (1, 'D20240001', '陈一鸣', '未知', '中共党员', '13800010001', 'ID-D20240001', 2024, '工程博士', NULL, 'enrolled', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 1);
INSERT INTO "public"."dtlms_students" VALUES (2, 'D20240002', '林书雅', '未知', '共青团员', '13800010002', 'ID-D20240002', 2024, '学术博士', NULL, 'enrolled', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 2);
INSERT INTO "public"."dtlms_students" VALUES (3, 'D20240003', '周启航', '未知', '群众', '13800010003', 'ID-D20240003', 2024, '工程博士', NULL, 'enrolled', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 3);
INSERT INTO "public"."dtlms_students" VALUES (4, 'D20240004', '顾南乔', '未知', '中共预备党员', '13800010004', 'ID-D20240004', 2024, '学术博士', NULL, 'enrolled', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);
INSERT INTO "public"."dtlms_students" VALUES (5, 'D20230005', '赵嘉霖', '未知', '中共党员', '13800010005', 'ID-D20230005', 2023, '工程博士', NULL, 'internship', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 3);
INSERT INTO "public"."dtlms_students" VALUES (6, 'D20230006', '沈知遥', '未知', '共青团员', '13800010006', 'ID-D20230006', 2023, '工程博士', NULL, 'internship', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);
INSERT INTO "public"."dtlms_students" VALUES (7, 'D20230007', '王书宁', '未知', '共青团员', '13800010007', 'ID-D20230007', 2023, '学术博士', NULL, 'outbound', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 1);
INSERT INTO "public"."dtlms_students" VALUES (8, 'D20230008', '贺景川', '未知', '群众', '13800010008', 'ID-D20230008', 2023, '工程博士', NULL, 'outbound', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);
INSERT INTO "public"."dtlms_students" VALUES (9, 'D20230009', '许安然', '未知', '群众', '13800010009', 'ID-D20230009', 2023, '学术博士', NULL, 'enrolled', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 3);
INSERT INTO "public"."dtlms_students" VALUES (10, 'D20220010', '张乐之', '未知', '群众', '13800010010', 'ID-D20220010', 2022, '工程博士', NULL, 'thesis', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 3);
INSERT INTO "public"."dtlms_students" VALUES (11, 'D20220011', '赵嘉禾', '未知', '中共党员', '13800010011', 'ID-D20220011', 2022, '工程博士', NULL, 'thesis', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);
INSERT INTO "public"."dtlms_students" VALUES (12, 'D20220012', '顾清越', '未知', '中共预备党员', '13800010012', 'ID-D20220012', 2022, '学术博士', NULL, 'thesis', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 2);
INSERT INTO "public"."dtlms_students" VALUES (13, 'D20250013', '宋知行', '未知', '共青团员', '13800010013', 'ID-D20250013', 2025, '工程博士', NULL, 'enrolled', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 1);
INSERT INTO "public"."dtlms_students" VALUES (15, 'D20250015', '孟书恒', '未知', '中共党员', '13800010015', 'ID-D20250015', 2025, '工程博士', NULL, 'enrolled', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 5);
INSERT INTO "public"."dtlms_students" VALUES (16, 'D20250016', '魏知远', '未知', '共青团员', '13800010016', 'ID-D20250016', 2025, '学术博士', NULL, 'enrolled', 1, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 2);
INSERT INTO "public"."dtlms_students" VALUES (17, 'D20240017', '韩嘉宁', '未知', '群众', '13800010017', 'ID-D20240017', 2024, '学术博士', NULL, 'enrolled', 2, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 3);
INSERT INTO "public"."dtlms_students" VALUES (14, 'D20250014', '江若溪', '未知', '群众', '13800010014', 'ID-D20250014', 2025, '学术博士', NULL, 'enrolled', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);
INSERT INTO "public"."dtlms_students" VALUES (18, 'D20240018', '陆承泽', '未知', '中共党员', '13800010018', 'ID-D20240018', 2024, '工程博士', NULL, 'enrolled', 3, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 4);

-- ----------------------------
-- Table structure for dtlms_system_configs
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_system_configs";
CREATE TABLE "public"."dtlms_system_configs" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_system_configs_id_seq'::regclass),
  "config_key" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "config_value" text COLLATE "pg_catalog"."default" NOT NULL,
  "description" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_system_configs
-- ----------------------------
INSERT INTO "public"."dtlms_system_configs" VALUES (1, 'report_overdue_days', '7', '科研报告逾期提醒阈值', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (2, 'report_escalation_days', '14', '科研报告升级提醒阈值', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (3, 'training_plan_edit_limit', '3', '培养方案每学年最大修改次数', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (4, 'thesis_plagiarism_threshold', '20', '学位论文查重率阈值', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (5, 'blind_review_pass_score', '75', '盲审平均通过分', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (6, 'redis_key_prefix', 'CTDTLMS_', 'Redis 统一前缀', '2026-04-01 19:09:38.298588+08', '2026-04-01 19:09:38.298588+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (85, 'audit.policy.1', '记录登录成功、失败、退出与令牌刷新。', '登录与鉴权审计', '2026-04-01 19:10:50.394906+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (86, 'audit.policy.2', '所有流程动作、意见、节点变更必须留痕。', '流程审批留痕', '2026-04-01 19:10:50.394906+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (87, 'audit.policy.3', '学生、团队、角色与字典变更需记录操作日志。', '主数据变更审计', '2026-04-01 19:10:50.394906+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (88, 'audit.policy.4', '导出包含联系方式与身份信息时需保留审计记录。', '敏感数据导出控制', '2026-04-01 19:10:50.394906+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (3126, 'integration.1.招生系统主数据同步', '主数据导入 / 录取回传|实时 + 每日对账|正常|系统管理员', '外部集成概览', '2026-04-07 10:05:53.326081+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (3127, 'integration.2.实验室 OA 事件同步', '考勤 / 门禁 / 请假同步|实时事件 + 定时补偿|正常|杨琴', '外部集成概览', '2026-04-07 10:05:53.326081+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (3128, 'integration.3.飞书待办推送', '待办通知 / 审批提醒 / 回执|实时|告警|周晴', '外部集成概览', '2026-04-07 10:05:53.326081+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (91, 'integration.3.飞书', '待办通知 / 审批提醒 / 回执|实时|告警|学合管理员', '外部集成概览', '2026-04-01 19:10:50.394906+08', '2026-04-07 09:41:57.031437+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (90, 'integration.2.实验室 OA', '考勤 / 门禁 / 请假同步|实时事件 + 定时补偿|正常|学院办公室', '外部集成概览', '2026-04-01 19:10:50.394906+08', '2026-04-07 09:41:57.031437+08');
INSERT INTO "public"."dtlms_system_configs" VALUES (89, 'integration.1.招生系统', '主数据导入 / 录取回传|实时 + 每日对账|正常|招生办公室', '外部集成概览', '2026-04-01 19:10:50.394906+08', '2026-04-07 09:41:57.031437+08');

-- ----------------------------
-- Table structure for dtlms_team_advisors
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_team_advisors";
CREATE TABLE "public"."dtlms_team_advisors" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_team_advisors_id_seq'::regclass),
  "team_id" int8 NOT NULL,
  "advisor_id" int8 NOT NULL,
  "advisor_role" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'member'::character varying,
  "joined_on" date,
  "left_on" date,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_team_advisors
-- ----------------------------
INSERT INTO "public"."dtlms_team_advisors" VALUES (1, 1, 1, 'lead', '2026-04-21', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (2, 2, 1, 'lead', '2026-04-21', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (3, 3, 2, 'lead', '2026-04-21', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (4, 4, 3, 'lead', '2026-04-21', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (5, 5, 2, 'lead', '2026-04-21', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (6, 6, 1, 'lead', '2026-04-20', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (7, 6, 3, 'member', '2026-04-20', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_team_advisors" VALUES (8, 6, 2, 'member', '2026-04-20', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_teams
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_teams";
CREATE TABLE "public"."dtlms_teams" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_teams_id_seq'::regclass),
  "team_code" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "team_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "department_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "discipline_name" varchar(128) COLLATE "pg_catalog"."default",
  "lead_advisor_id" int8,
  "research_directions" text COLLATE "pg_catalog"."default",
  "team_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'active'::character varying,
  "established_on" date,
  "description" text COLLATE "pg_catalog"."default",
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_teams
-- ----------------------------
INSERT INTO "public"."dtlms_teams" VALUES (1, 'TEAM-AUTO-001', '智能制造团队', '未分配院系', '未分配学科', 1, NULL, 'active', '2026-04-21', '由历史学生主档自动生成的团队记录。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_teams" VALUES (2, 'TEAM-AUTO-002', '机器人应用团队', '未分配院系', '未分配学科', 1, NULL, 'active', '2026-04-21', '由历史学生主档自动生成的团队记录。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_teams" VALUES (3, 'TEAM-AUTO-003', '工业软件团队', '未分配院系', '未分配学科', 2, NULL, 'active', '2026-04-21', '由历史学生主档自动生成的团队记录。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_teams" VALUES (4, 'TEAM-AUTO-004', '数据智能团队', '未分配院系', '未分配学科', 3, NULL, 'active', '2026-04-21', '由历史学生主档自动生成的团队记录。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_teams" VALUES (5, 'TEAM-AUTO-005', '平台治理团队', '未分配院系', '未分配学科', 2, NULL, 'active', '2026-04-21', '由历史学生主档自动生成的团队记录。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_teams" VALUES (6, 'CENTER-006', '人工智能安全研究中心', '未分配院系', '', 1, NULL, 'active', '2026-04-20', NULL, 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_theses
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_theses";
CREATE TABLE "public"."dtlms_theses" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_theses_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "advisor_id" int8 NOT NULL,
  "title" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "plagiarism_rate" numeric(5,2),
  "thesis_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'draft'::character varying,
  "blind_review_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "defense_date" date,
  "degree_granted" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "business_key" varchar(64) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of dtlms_theses
-- ----------------------------
INSERT INTO "public"."dtlms_theses" VALUES (1, 10, 2, '面向工业软件的流程协同引擎设计与实现', 12.50, 'review_passed', 'passed', NULL, 'pending', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'SWSQSP202604070001');
INSERT INTO "public"."dtlms_theses" VALUES (2, 11, 3, '知识图谱驱动的科研过程智能分析方法研究', 15.20, 'plagiarism_passed', 'reviewing', '2026-06-18', 'reviewing', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'SWSQSP202604070002');
INSERT INTO "public"."dtlms_theses" VALUES (3, 12, 1, '机器人视觉检测中的多模态融合方法研究', 18.00, 'rework', 'pending', NULL, 'pending', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'SWSQSP202604070003');
INSERT INTO "public"."dtlms_theses" VALUES (4, 6, 3, '面向教育场景的大模型知识对齐与应用研究', 9.80, 'draft', 'pending', NULL, 'pending', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'SWSQSP202604070004');
INSERT INTO "public"."dtlms_theses" VALUES (6, 6, 3, '沈知遥学位申请闭环模拟-20260409201505', 7.80, 'review_passed', 'passed', '2026-06-18', 'pending', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08', 'SWSQSP202604090002');

-- ----------------------------
-- Table structure for dtlms_thesis_reviews
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_thesis_reviews";
CREATE TABLE "public"."dtlms_thesis_reviews" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_thesis_reviews_id_seq'::regclass),
  "thesis_id" int8 NOT NULL,
  "expert_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "review_score" numeric(5,2),
  "review_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'pending'::character varying,
  "review_comment" text COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_thesis_reviews
-- ----------------------------
INSERT INTO "public"."dtlms_thesis_reviews" VALUES (1, 1, '何振华', 86.00, 'passed', '研究目标明确，工程实现完整。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_thesis_reviews" VALUES (2, 1, '潘雪松', 88.00, 'passed', '实验设计充分，建议补充性能对比。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_thesis_reviews" VALUES (3, 2, '杨知行', NULL, 'pending', NULL, '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_thesis_reviews" VALUES (4, 3, '陈明哲', 70.00, 'pending', '理论分析不充分，需要补强实验结果。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_thesis_reviews" VALUES (5, 1, '评审专家A', 90.00, 'pending', '仅验证增量持久化-更新', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_training_plan_versions
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_training_plan_versions";
CREATE TABLE "public"."dtlms_training_plan_versions" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_training_plan_versions_id_seq'::regclass),
  "training_plan_id" int8 NOT NULL,
  "version_no" varchar(16) COLLATE "pg_catalog"."default" NOT NULL,
  "change_reason" text COLLATE "pg_catalog"."default",
  "plan_snapshot" text COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_training_plan_versions
-- ----------------------------
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (1, 1, 'v1.0', '初始化导入', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (2, 2, 'v1.0', '初始化导入', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (3, 3, 'v1.0', '初始化导入', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (4, 4, 'v1.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (5, 5, 'v2.0', '初始化导入', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (6, 6, 'v2.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (7, 7, 'v2.0', '初始化导入', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (8, 8, 'v2.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (9, 9, 'v2.0', '初始化导入', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (10, 10, 'v2.0', '初始化导入', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (11, 11, 'v2.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (12, 12, 'v2.0', '初始化导入', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (13, 13, 'v1.0', '初始化导入', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (14, 14, 'v1.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (15, 15, 'v1.0', '初始化导入', '围绕平台治理团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (16, 16, 'v1.0', '初始化导入', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (17, 17, 'v1.0', '初始化导入', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plan_versions" VALUES (18, 18, 'v1.0', '初始化导入', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_training_plans
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_training_plans";
CREATE TABLE "public"."dtlms_training_plans" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_training_plans_id_seq'::regclass),
  "student_id" int8 NOT NULL,
  "advisor_id" int8 NOT NULL,
  "version_no" varchar(16) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'v1.0'::character varying,
  "report_cycle" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "plan_status" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'draft'::character varying,
  "scientific_goal" text COLLATE "pg_catalog"."default" NOT NULL,
  "assessment_rule" text COLLATE "pg_catalog"."default" NOT NULL,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_training_plans
-- ----------------------------
INSERT INTO "public"."dtlms_training_plans" VALUES (1, 1, 1, 'v1.0', '月度', 'effective', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (2, 2, 1, 'v1.0', '月度', 'effective', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (3, 3, 2, 'v1.0', '月度', 'effective', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (4, 4, 3, 'v1.0', '月度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (5, 5, 2, 'v2.0', '季度', 'effective', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (6, 6, 3, 'v2.0', '季度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (7, 7, 1, 'v2.0', '季度', 'effective', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (8, 8, 3, 'v2.0', '季度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (9, 9, 2, 'v2.0', '季度', 'pending_confirm', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (10, 10, 2, 'v2.0', '季度', 'effective', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (11, 11, 3, 'v2.0', '季度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (12, 12, 1, 'v2.0', '季度', 'effective', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (13, 13, 1, 'v1.0', '月度', 'effective', '围绕智能制造团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (14, 14, 3, 'v1.0', '月度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (15, 15, 2, 'v1.0', '月度', 'effective', '围绕平台治理团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (16, 16, 1, 'v1.0', '月度', 'effective', '围绕机器人应用团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (17, 17, 2, 'v1.0', '月度', 'effective', '围绕工业软件团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_training_plans" VALUES (18, 18, 3, 'v1.0', '月度', 'effective', '围绕数据智能团队承担课题，形成阶段性论文与系统原型。', '按周期提交科研报告，完成阶段汇报与论文节点考核。', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_user_roles
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_user_roles";
CREATE TABLE "public"."dtlms_user_roles" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_user_roles_id_seq'::regclass),
  "user_id" int8 NOT NULL,
  "role_id" int8 NOT NULL,
  "grant_source" varchar(64) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'bootstrap'::character varying,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_user_roles
-- ----------------------------
INSERT INTO "public"."dtlms_user_roles" VALUES (1, 3, 3, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (2, 4, 3, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (3, 6, 4, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (4, 7, 5, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (5, 8, 6, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (6, 5, 1740, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (7, 9, 8, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (8, 2, 3, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_user_roles" VALUES (9, 1, 1, 'runtime_seed', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_users
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_users";
CREATE TABLE "public"."dtlms_users" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_users_id_seq'::regclass),
  "username" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "full_name" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(128) COLLATE "pg_catalog"."default",
  "password_hash" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "is_active" bool NOT NULL DEFAULT true,
  "is_deleted" bool NOT NULL DEFAULT false,
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_users
-- ----------------------------
INSERT INTO "public"."dtlms_users" VALUES (3, 'yuan.ye', '袁野', 'yuan.ye@dtlms.local', '$pbkdf2-sha256$29000$yhnjPKfUei.F8H6PMWas1Q$qDDfghaS3TOjM/CZolO0gs7OheOG6MEO/VKfIUFRUzk', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (4, 'xu.sutian', '徐素天', 'xu.sutian@dtlms.local', '$pbkdf2-sha256$29000$orRW6l3rHWOMMeb8X8vZ2w$yBt8uqmPKhrdu7Kg9iItn5Id.06rttpMqgt15Oup/.E', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (6, 'he.lin', '何琳', 'he.lin@dtlms.local', '$pbkdf2-sha256$29000$15oTAqB0bm2t1fo/x/i/tw$bBZXnpGNS4a3YF2Y/LK4X9MxeVpdLosUbXvnERPBKsI', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (7, 'cao.bo', '曹博', 'cao.bo@dtlms.local', '$pbkdf2-sha256$29000$zdk7p7QWIiSEsJYyJgTgPA$7B79vX6lx71L6Bikm8eKkMTHB4Sd7nubfIHHr2hudTA', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (8, 'yang.qin', '杨琴', 'yang.qin@dtlms.local', '$pbkdf2-sha256$29000$0VpLyRmDEELoPYdQau29Vw$IKJK2kwKHjqV0NL3UtAXkttAmtLD24GDtYjuEL5iFzQ', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (5, 'zhou.qing', '周晴', 'zhou.qing@dtlms.local', '$pbkdf2-sha256$29000$Rghh7B2jdK4VotTamxNizA$i2aBMIQoAYWLICfB2wLjqv5yr6NhpWr3kP8I2yeWWsI', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (9, 'sun.wei', '孙伟', 'sun.wei@dtlms.local', '$pbkdf2-sha256$29000$6X0vxfif8z5HKAVgjDEmxA$i.jQ93csIVlg6dbr1sqrfBowKaMZCwDisbWaF2EMZWs', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (2, 'liu.ya', '刘亚', 'liu.ya@dtlms.local', '$pbkdf2-sha256$29000$gHBuzZmTUmqNsbYWgrA2Bg$uIZuS.dgkFHpKWkrfYEWSvlN82b/6ga8RsuxazZCHh4', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_users" VALUES (1, 'admin', '系统管理员', 'admin@dtlms.local', '$pbkdf2-sha256$29000$l1LqXQvB.L93TomRMobQOg$9aLo8Vfx6V8DE0ppHrG5RnWCfTIBy6dt8Y.Y0.DAuTM', 't', 'f', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_wf_de_model
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_de_model";
CREATE TABLE "public"."dtlms_wf_de_model" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "name_" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "key_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "category_" varchar(128) COLLATE "pg_catalog"."default",
  "version_" int4 NOT NULL DEFAULT 1,
  "model_type_" int4 NOT NULL DEFAULT 0,
  "description_" text COLLATE "pg_catalog"."default",
  "meta_info_" jsonb,
  "created_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "last_updated_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "tenant_id_" varchar(64) COLLATE "pg_catalog"."default",
  "deployment_id_" varchar(64) COLLATE "pg_catalog"."default",
  "resource_name_" varchar(255) COLLATE "pg_catalog"."default",
  "editor_source_value_" text COLLATE "pg_catalog"."default",
  "editor_source_extra_value_" jsonb
)
;

-- ----------------------------
-- Records of dtlms_wf_de_model
-- ----------------------------
INSERT INTO "public"."dtlms_wf_de_model" VALUES ('MODEL-recruitment_application', '招生录取审批', 'recruitment_application', '招生管理', 1, 0, '招生录取审批 流程模型', '{"source": "runtime_seed", "workflow_name": "招生录取审批"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08', NULL, 'dep-recruitmentapplication-4588d501', 'recruitment_application.bpmn20.xml', NULL, '{"flow_code": "recruitment_application", "business_module": "招生管理"}');
INSERT INTO "public"."dtlms_wf_de_model" VALUES ('MODEL-thesis', '学位申请审批', 'thesis', '学位管理', 1, 0, '学位申请审批 流程模型', '{"source": "runtime_seed", "workflow_name": "学位申请审批"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08', NULL, 'dep-thesis-d4b0719b', 'thesis.bpmn20.xml', NULL, '{"flow_code": "thesis", "business_module": "学位管理"}');
INSERT INTO "public"."dtlms_wf_de_model" VALUES ('MODEL-outbound_study', '外出研修审批', 'outbound_study', '培养管理', 1, 0, '外出研修审批 流程模型', '{"source": "runtime_seed", "workflow_name": "外出研修审批"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08', NULL, 'dep-outboundstudy-6d8e1576', 'outbound_study.bpmn20.xml', NULL, '{"flow_code": "outbound_study", "business_module": "培养管理"}');
INSERT INTO "public"."dtlms_wf_de_model" VALUES ('MODEL-scientific_report', '科研报告审阅', 'scientific_report', '培养管理', 1, 0, '科研报告审阅 流程模型', '{"source": "runtime_seed", "workflow_name": "科研报告审阅"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08', NULL, 'dep-scientificreport-9069a4b1', 'scientific_report.bpmn20.xml', NULL, '{"flow_code": "scientific_report", "business_module": "培养管理"}');

-- ----------------------------
-- Table structure for dtlms_wf_hi_actinst
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_hi_actinst";
CREATE TABLE "public"."dtlms_wf_hi_actinst" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_def_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "exec_id_" varchar(64) COLLATE "pg_catalog"."default",
  "act_id_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "act_name_" varchar(255) COLLATE "pg_catalog"."default",
  "act_type_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "assignee_" varchar(64) COLLATE "pg_catalog"."default",
  "start_time_" timestamptz(6) NOT NULL,
  "end_time_" timestamptz(6),
  "duration_ms_" int8,
  "business_key_" varchar(64) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_hi_actinst
-- ----------------------------
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-47-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', 'start', '发起流程', 'userTask', '18615768209', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08', 0, 'ZSLQSP202604230010');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-46-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', 'start', '发起流程', 'userTask', '13521297322', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08', 0, 'ZSLQSP202604230009');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-36-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', 'start', '发起流程', 'userTask', '139836871113', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08', 0, 'ZSLQSP202604210006');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-34-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', 'start', '发起流程', 'userTask', '136449765890', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08', 0, 'ZSLQSP202604210004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-33-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', 'start', '发起流程', 'userTask', 'admin', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08', 0, 'ZSLQSP202604100004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-35-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', 'start', '发起流程', 'userTask', '138610893902', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08', 0, 'ZSLQSP202604210005');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-32-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', 'start', '发起流程', 'userTask', 'admin', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08', 0, 'ZSLQSP202604100003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-31-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', 'start', '发起流程', 'userTask', 'admin', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08', 0, 'ZSLQSP202604100001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-28-0', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', 'advisor_precheck', '导师预审', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'SWSQSP202604070004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-27-0', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'SWSQSP202604070003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-26-0', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', 'secretary_review', '材料复核', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'SWSQSP202604070002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-25-0', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'SWSQSP202604070001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-23-0', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'WCYXSP202604070003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-22-0', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', 'advisor_review', '导师审核', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'WCYXSP202604070002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-21-0', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'WCYXSP202604070001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-24-0', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', 'advisor_review', '导师审核', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'WCYXSP202604070004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-19-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', 'advisor_review', '导师审阅', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070007');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-18-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', 'advisor_review', '导师审阅', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070006');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-17-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070005');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-16-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-15-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-14-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', 'advisor_review', '导师审阅', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-13-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-12-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', 'qualification_review', '资格审核', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070012');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-11-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', 'admission_decision', '录取决策', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070011');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-10-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070010');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-9-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070009');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-8-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070008');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-7-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', 'qualification_passed', '评分准备', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070007');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-6-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', 'qualification_review', '资格审核', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070006');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-5-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', 'interview_arrangement', '面试安排', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070005');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-4-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', 'admission_decision', '录取决策', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-3-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', 'admission_confirmation', '录取确认', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-2-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-1-0', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'ZSLQSP202604070001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-20-0', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', '流程结束', '流程结束', 'userTask', NULL, '2026-04-07 18:50:41+08', NULL, NULL, 'KYBGSY202604070008');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-30-1', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', 'start', '发起流程', 'userTask', 'xu.sutian', '2026-04-09 20:15:05+08', '2026-04-09 20:15:05+08', 0, 'SWSQSP202604090002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-30-2', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', 'submit_review', '提交送审', 'userTask', 'xu.sutian', '2026-04-09 20:15:15+08', '2026-04-09 20:15:15+08', 0, 'SWSQSP202604090002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-30-3', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', 'approve', '复核通过', 'userTask', 'zhou.qing', '2026-04-09 20:15:26+08', '2026-04-09 20:15:26+08', 0, 'SWSQSP202604090002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-40-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', 'start', '发起流程', 'userTask', '139be009f7d', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08', 0, 'ZSLQSP202604220001');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-41-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', 'start', '发起流程', 'userTask', 'admin', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08', 0, 'ZSLQSP202604220002');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-42-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', 'start', '发起流程', 'userTask', 'admin', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08', 0, 'ZSLQSP202604220003');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-43-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', 'start', '发起流程', 'userTask', '13952d69275', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08', 0, 'ZSLQSP202604220004');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-44-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', 'start', '发起流程', 'userTask', 'admin', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08', 0, 'ZSLQSP202604220005');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-45-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', 'start', '发起流程', 'userTask', 'admin', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08', 0, 'ZSLQSP202604220006');
INSERT INTO "public"."dtlms_wf_hi_actinst" VALUES ('ACT-37-1', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', 'start', '发起流程', 'userTask', '132786107897', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08', 0, 'ZSLQSP202604210007');

-- ----------------------------
-- Table structure for dtlms_wf_hi_procinst
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_hi_procinst";
CREATE TABLE "public"."dtlms_wf_hi_procinst" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "business_key_" varchar(64) COLLATE "pg_catalog"."default",
  "proc_def_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "start_time_" timestamptz(6) NOT NULL,
  "end_time_" timestamptz(6),
  "duration_ms_" int8,
  "start_user_id_" varchar(64) COLLATE "pg_catalog"."default",
  "end_act_id_" varchar(128) COLLATE "pg_catalog"."default",
  "delete_reason_" varchar(255) COLLATE "pg_catalog"."default",
  "start_act_id_" varchar(128) COLLATE "pg_catalog"."default",
  "state_" varchar(32) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'ACTIVE'::character varying
)
;

-- ----------------------------
-- Records of dtlms_wf_hi_procinst
-- ----------------------------
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'ZSLQSP202604230010', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-23 12:01:25+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'ZSLQSP202604230009', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-23 11:49:20+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'ZSLQSP202604210006', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-21 02:02:08+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'ZSLQSP202604210004', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-21 01:53:57+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'ZSLQSP202604100004', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-10 13:27:37+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'ZSLQSP202604210005', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-21 01:58:19+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'ZSLQSP202604100003', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-10 13:26:14+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'ZSLQSP202604100001', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-10 13:14:58+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-thesis-swsqsp202604070004-e14f35b86f', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'SWSQSP202604070004', 'procdef-thesis-v1-065eef39', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-thesis-swsqsp202604070003-559b20e292', 'procinst-thesis-swsqsp202604070003-559b20e292', 'SWSQSP202604070003', 'procdef-thesis-v1-065eef39', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', 'rejected', 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-thesis-swsqsp202604070002-1fdcd41689', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'SWSQSP202604070002', 'procdef-thesis-v1-065eef39', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-thesis-swsqsp202604070001-206582850c', 'procinst-thesis-swsqsp202604070001-206582850c', 'SWSQSP202604070001', 'procdef-thesis-v1-065eef39', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'WCYXSP202604070003', 'procdef-outboundstudy-v1-aadfc5bd', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', 'rejected', 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'WCYXSP202604070002', 'procdef-outboundstudy-v1-aadfc5bd', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'WCYXSP202604070001', 'procdef-outboundstudy-v1-aadfc5bd', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-outboundstudy-wcyxsp202604070004-d049327905', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'WCYXSP202604070004', 'procdef-outboundstudy-v1-aadfc5bd', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'KYBGSY202604070007', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070006-a75676b582', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'KYBGSY202604070006', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070005-aede151d38', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'KYBGSY202604070005', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070004-d492085f3f', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'KYBGSY202604070004', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', 'rejected', 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'KYBGSY202604070003', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'KYBGSY202604070002', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070001-ac313f254d', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'KYBGSY202604070001', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'ZSLQSP202604070012', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'ZSLQSP202604070011', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'ZSLQSP202604070010', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'ZSLQSP202604070009', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', 'rejected', 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070008-23605124be', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'ZSLQSP202604070008', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'ZSLQSP202604070007', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'ZSLQSP202604070006', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'ZSLQSP202604070005', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'ZSLQSP202604070004', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'ZSLQSP202604070003', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'ZSLQSP202604070002', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'ZSLQSP202604070001', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'KYBGSY202604070008', 'procdef-scientificreport-v1-60dc0211', '2026-04-07 18:50:41+08', NULL, NULL, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-thesis-swsqsp202604090002-a0b74461b9', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'SWSQSP202604090002', 'procdef-thesis-v1-065eef39', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08', 21000, NULL, '流程结束', NULL, 'startEvent', 'COMPLETED');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'ZSLQSP202604220001', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:24:02+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'ZSLQSP202604220002', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:24:03+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'ZSLQSP202604220003', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:24:04+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'ZSLQSP202604220004', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:25:28+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'ZSLQSP202604220005', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:25:29+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'ZSLQSP202604220006', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-22 09:25:30+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');
INSERT INTO "public"."dtlms_wf_hi_procinst" VALUES ('procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'ZSLQSP202604210007', 'procdef-recruitmentapplicati-v1-52a2d0f8', '2026-04-21 02:06:20+08', NULL, NULL, NULL, NULL, NULL, 'startEvent', 'ACTIVE');

-- ----------------------------
-- Table structure for dtlms_wf_hi_taskinst
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_hi_taskinst";
CREATE TABLE "public"."dtlms_wf_hi_taskinst" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "task_def_key_" varchar(128) COLLATE "pg_catalog"."default",
  "proc_def_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "exec_id_" varchar(64) COLLATE "pg_catalog"."default",
  "name_" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "business_key_" varchar(64) COLLATE "pg_catalog"."default",
  "assignee_" varchar(64) COLLATE "pg_catalog"."default",
  "owner_" varchar(64) COLLATE "pg_catalog"."default",
  "start_time_" timestamptz(6) NOT NULL,
  "claim_time_" timestamptz(6),
  "end_time_" timestamptz(6),
  "duration_ms_" int8,
  "due_date_" timestamptz(6),
  "delete_reason_" varchar(255) COLLATE "pg_catalog"."default",
  "priority_" int4 NOT NULL DEFAULT 50,
  "category_" varchar(128) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_hi_taskinst
-- ----------------------------
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-47', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', '罗凯报名审核', 'ZSLQSP202604230010', NULL, NULL, '2026-04-23 12:01:25+08', NULL, NULL, NULL, '2026-04-24 12:01:25+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-46', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', '李小玉报名审核', 'ZSLQSP202604230009', NULL, NULL, '2026-04-23 11:49:20+08', NULL, NULL, NULL, '2026-04-24 11:49:20+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-36', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', '??????报名审核', 'ZSLQSP202604210006', NULL, NULL, '2026-04-21 02:02:08+08', NULL, NULL, NULL, '2026-04-22 02:02:08+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-34', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', '联调考生报名审核', 'ZSLQSP202604210004', NULL, NULL, '2026-04-21 01:53:57+08', NULL, NULL, NULL, '2026-04-22 01:53:57+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-33', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', '在线联调0410132736报名审核', 'ZSLQSP202604100004', NULL, NULL, '2026-04-10 13:27:37+08', NULL, NULL, NULL, '2026-04-11 13:27:37+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-35', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', 'Portal Smoke User报名审核', 'ZSLQSP202604210005', NULL, NULL, '2026-04-21 01:58:19+08', NULL, NULL, NULL, '2026-04-22 01:58:19+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-32', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', '联调考生0410132613报名审核', 'ZSLQSP202604100003', NULL, NULL, '2026-04-10 13:26:14+08', NULL, NULL, NULL, '2026-04-11 13:26:14+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-31', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', '联调考生0410131457报名审核', 'ZSLQSP202604100001', NULL, NULL, '2026-04-10 13:14:58+08', NULL, NULL, NULL, '2026-04-11 13:14:58+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-28', 'advisor_precheck', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', '沈知遥授位审批', 'SWSQSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '学位管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-27', '流程结束', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', '顾清越授位审批', 'SWSQSP202604070003', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', 'rejected', 50, '学位管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-26', 'secretary_review', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', '赵嘉禾授位审批', 'SWSQSP202604070002', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '学位管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-25', '流程结束', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', '张乐之授位审批', 'SWSQSP202604070001', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '学位管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-23', '流程结束', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', '周启航外出研修申请', 'WCYXSP202604070003', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', 'rejected', 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-22', 'advisor_review', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', '贺景川外出研修申请', 'WCYXSP202604070002', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-21', '流程结束', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', '王书宁外出研修申请', 'WCYXSP202604070001', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-24', 'advisor_review', 'procdef-outboundstudy-v1-aadfc5bd', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', '孟书恒外出研修申请', 'WCYXSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-19', 'advisor_review', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', '宋知行科研报告审阅', 'KYBGSY202604070007', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-18', 'advisor_review', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', '沈知遥科研报告审阅', 'KYBGSY202604070006', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-17', '流程结束', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', '赵嘉霖科研报告审阅', 'KYBGSY202604070005', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-16', '流程结束', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', '顾南乔科研报告审阅', 'KYBGSY202604070004', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', 'rejected', 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-15', '流程结束', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', '周启航科研报告审阅', 'KYBGSY202604070003', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-14', 'advisor_review', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', '林书雅科研报告审阅', 'KYBGSY202604070002', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-13', '流程结束', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', '陈一鸣科研报告审阅', 'KYBGSY202604070001', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-12', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', '谢明远报名审核', 'ZSLQSP202604070012', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-08 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-11', 'admission_decision', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', '朱安宁报名审核', 'ZSLQSP202604070011', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-10', '流程结束', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', '韩知遇报名审核', 'ZSLQSP202604070010', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-9', '流程结束', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', '钱北辰报名审核', 'ZSLQSP202604070009', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', 'rejected', 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-8', '流程结束', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', '林知夏报名审核', 'ZSLQSP202604070008', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-7', 'qualification_passed', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', '赵安歌报名审核', 'ZSLQSP202604070007', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-08 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-6', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', '陈思远报名审核', 'ZSLQSP202604070006', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-08 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-5', 'interview_arrangement', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', '李静姝报名审核', 'ZSLQSP202604070005', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-4', 'admission_decision', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', '周亦凡报名审核', 'ZSLQSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-3', 'admission_confirmation', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', '顾明睿报名审核', 'ZSLQSP202604070003', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-09 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-2', '流程结束', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', '沈清禾报名审核', 'ZSLQSP202604070002', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-1', '流程结束', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', '吴启程报名审核', 'ZSLQSP202604070001', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-20', '流程结束', 'procdef-scientificreport-v1-60dc0211', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', '江若溪科研报告审阅', 'KYBGSY202604070008', NULL, NULL, '2026-04-07 18:50:41+08', NULL, NULL, NULL, '2026-04-07 18:50:41+08', NULL, 50, '培养管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-30', '流程结束', 'procdef-thesis-v1-065eef39', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', '沈知遥授位审批', 'SWSQSP202604090002', NULL, NULL, '2026-04-09 20:15:05+08', NULL, '2026-04-09 20:15:26+08', 21000, '2026-04-11 20:15:15+08', NULL, 50, '学位管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-40', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', '性能回归be009f7d报名审核', 'ZSLQSP202604220001', NULL, NULL, '2026-04-22 09:24:02+08', NULL, NULL, NULL, '2026-04-23 09:24:02+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-41', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', '直建更新be009f7d报名审核', 'ZSLQSP202604220002', NULL, NULL, '2026-04-22 09:24:03+08', NULL, NULL, NULL, '2026-04-23 09:24:03+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-42', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', '导入be009f7d报名审核', 'ZSLQSP202604220003', NULL, NULL, '2026-04-22 09:24:04+08', NULL, NULL, NULL, '2026-04-23 09:24:04+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-43', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', '性能回归52d69275报名审核', 'ZSLQSP202604220004', NULL, NULL, '2026-04-22 09:25:28+08', NULL, NULL, NULL, '2026-04-23 09:25:28+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-44', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', '直建更新52d69275报名审核', 'ZSLQSP202604220005', NULL, NULL, '2026-04-22 09:25:29+08', NULL, NULL, NULL, '2026-04-23 09:25:29+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-45', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', '导入52d69275报名审核', 'ZSLQSP202604220006', NULL, NULL, '2026-04-22 09:25:30+08', NULL, NULL, NULL, '2026-04-23 09:25:30+08', NULL, 50, '招生管理');
INSERT INTO "public"."dtlms_wf_hi_taskinst" VALUES ('TASK-37', 'qualification_review', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', '测试管理保存报名审核', 'ZSLQSP202604210007', NULL, NULL, '2026-04-21 02:06:20+08', NULL, NULL, NULL, '2026-04-22 02:06:20+08', NULL, 50, '招生管理');

-- ----------------------------
-- Table structure for dtlms_wf_hi_varinst
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_hi_varinst";
CREATE TABLE "public"."dtlms_wf_hi_varinst" (
  "id_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "exec_id_" varchar(64) COLLATE "pg_catalog"."default",
  "task_id_" varchar(64) COLLATE "pg_catalog"."default",
  "name_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "var_type_" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "text_value_" text COLLATE "pg_catalog"."default",
  "number_value_" int8,
  "json_value_" jsonb,
  "create_time_" timestamptz(6) NOT NULL,
  "last_updated_time_" timestamptz(6) NOT NULL
)
;

-- ----------------------------
-- Records of dtlms_wf_hi_varinst
-- ----------------------------
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-businessKey', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'businessKey', 'string', 'ZSLQSP202604230010', NULL, '{"value": "ZSLQSP202604230010"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-businessModule', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-flowCode', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-entityId', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'entityId', 'number', NULL, 27, '{"value": 27}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-currentNode', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-taskStatus', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-candidateGroups', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'exec-qualificationrevie-d9ac1235d8', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-23 12:01:25+08', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-businessKey', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'businessKey', 'string', 'ZSLQSP202604230009', NULL, '{"value": "ZSLQSP202604230009"}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-businessModule', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-flowCode', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-entityId', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'entityId', 'number', NULL, 26, '{"value": 26}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-currentNode', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-taskStatus', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-candidateGroups', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'exec-qualificationrevie-eede6d1dd9', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-23 11:49:20+08', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-businessKey', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'businessKey', 'string', 'ZSLQSP202604210006', NULL, '{"value": "ZSLQSP202604210006"}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-businessModule', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-flowCode', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-entityId', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'entityId', 'number', NULL, 18, '{"value": 18}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-currentNode', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-taskStatus', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-candidateGroups', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'exec-qualificationrevie-5df923986a', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 02:02:08+08', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-businessKey', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'businessKey', 'string', 'ZSLQSP202604210004', NULL, '{"value": "ZSLQSP202604210004"}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-businessModule', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-flowCode', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-entityId', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'entityId', 'number', NULL, 16, '{"value": 16}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-currentNode', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-taskStatus', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-candidateGroups', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'exec-qualificationrevie-f9b4e63f9c', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 01:53:57+08', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-businessKey', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'businessKey', 'string', 'ZSLQSP202604100004', NULL, '{"value": "ZSLQSP202604100004"}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-businessModule', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-flowCode', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-entityId', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'entityId', 'number', NULL, 15, '{"value": 15}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-currentNode', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-taskStatus', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-candidateGroups', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'exec-qualificationrevie-7d07ba753a', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:27:37+08', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-businessKey', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'businessKey', 'string', 'ZSLQSP202604210005', NULL, '{"value": "ZSLQSP202604210005"}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-businessModule', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-flowCode', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-entityId', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'entityId', 'number', NULL, 17, '{"value": 17}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-currentNode', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-taskStatus', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-candidateGroups', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'exec-qualificationrevie-887e01a071', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 01:58:19+08', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-businessKey', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'businessKey', 'string', 'ZSLQSP202604100003', NULL, '{"value": "ZSLQSP202604100003"}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-businessModule', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-flowCode', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-entityId', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'entityId', 'number', NULL, 14, '{"value": 14}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-currentNode', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-taskStatus', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-candidateGroups', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'exec-qualificationrevie-18c95ca2f8', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:26:14+08', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-businessKey', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'businessKey', 'string', 'ZSLQSP202604100001', NULL, '{"value": "ZSLQSP202604100001"}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-businessModule', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-flowCode', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-entityId', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'entityId', 'number', NULL, 13, '{"value": 13}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-currentNode', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-taskStatus', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-candidateGroups', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'exec-qualificationrevie-44869f7eed', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:14:58+08', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-businessKey', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'businessKey', 'string', 'SWSQSP202604070004', NULL, '{"value": "SWSQSP202604070004"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-businessModule', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-flowCode', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-entityId', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-currentNode', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'currentNode', 'string', '导师预审', NULL, '{"value": "导师预审"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-taskStatus', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-candidateGroups', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'exec-advisorprecheck-19a4d28b0a', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-businessKey', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'businessKey', 'string', 'SWSQSP202604070003', NULL, '{"value": "SWSQSP202604070003"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-businessModule', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-flowCode', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-entityId', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'entityId', 'number', NULL, 3, '{"value": 3}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-currentNode', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-taskStatus', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'taskStatus', 'string', '已驳回', NULL, '{"value": "已驳回"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070003-559b20e292-candidateGroups', 'procinst-thesis-swsqsp202604070003-559b20e292', 'exec-流程结束-7011ec3729', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-businessKey', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'businessKey', 'string', 'SWSQSP202604070002', NULL, '{"value": "SWSQSP202604070002"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-businessModule', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-flowCode', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-entityId', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-currentNode', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'currentNode', 'string', '材料复核', NULL, '{"value": "材料复核"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-taskStatus', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-candidateGroups', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'exec-secretaryreview-02832ea26f', NULL, 'candidateGroups', 'json', NULL, NULL, '["secretary"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-businessKey', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'businessKey', 'string', 'SWSQSP202604070001', NULL, '{"value": "SWSQSP202604070001"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-businessModule', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-flowCode', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-entityId', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'entityId', 'number', NULL, 1, '{"value": 1}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-currentNode', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-taskStatus', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604070001-206582850c-candidateGroups', 'procinst-thesis-swsqsp202604070001-206582850c', 'exec-流程结束-fa6064ddba', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-businessKey', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'businessKey', 'string', 'WCYXSP202604070003', NULL, '{"value": "WCYXSP202604070003"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-businessModule', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-flowCode', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-entityId', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'entityId', 'number', NULL, 3, '{"value": 3}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-currentNode', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-taskStatus', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'taskStatus', 'string', '已驳回', NULL, '{"value": "已驳回"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9-candidateGroups', 'procinst-outboundstudy-wcyxsp202604070003-c1dcb06ad9', 'exec-流程结束-35415dcddd', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-businessKey', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'businessKey', 'string', 'WCYXSP202604070002', NULL, '{"value": "WCYXSP202604070002"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-businessModule', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-flowCode', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-entityId', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-currentNode', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'currentNode', 'string', '导师审核', NULL, '{"value": "导师审核"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-taskStatus', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-candidateGroups', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'exec-advisorreview-d65a8149b8', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-businessKey', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'businessKey', 'string', 'WCYXSP202604070001', NULL, '{"value": "WCYXSP202604070001"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-businessModule', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-flowCode', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-entityId', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'entityId', 'number', NULL, 1, '{"value": 1}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-currentNode', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-taskStatus', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070001-305be95a20-candidateGroups', 'procinst-outboundstudy-wcyxsp202604070001-305be95a20', 'exec-流程结束-d4614c71c7', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-businessKey', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'businessKey', 'string', 'WCYXSP202604070004', NULL, '{"value": "WCYXSP202604070004"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-businessModule', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-flowCode', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-entityId', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-currentNode', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'currentNode', 'string', '导师审核', NULL, '{"value": "导师审核"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-taskStatus', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-candidateGroups', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'exec-advisorreview-b5efa6424c', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-businessKey', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'businessKey', 'string', 'KYBGSY202604070007', NULL, '{"value": "KYBGSY202604070007"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-businessModule', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-flowCode', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-entityId', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'entityId', 'number', NULL, 7, '{"value": 7}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-currentNode', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-taskStatus', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-candidateGroups', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'exec-advisorreview-5dfab64a31', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-businessKey', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'businessKey', 'string', 'KYBGSY202604070006', NULL, '{"value": "KYBGSY202604070006"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-businessModule', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-flowCode', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-entityId', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'entityId', 'number', NULL, 6, '{"value": 6}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-currentNode', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-taskStatus', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-candidateGroups', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'exec-advisorreview-b7c77ef380', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-businessKey', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'businessKey', 'string', 'KYBGSY202604070005', NULL, '{"value": "KYBGSY202604070005"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-businessModule', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-flowCode', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-entityId', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'entityId', 'number', NULL, 5, '{"value": 5}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-currentNode', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-taskStatus', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070005-aede151d38-candidateGroups', 'procinst-scientificreport-kybgsy202604070005-aede151d38', 'exec-流程结束-db12ceaa3d', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-businessKey', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'businessKey', 'string', 'KYBGSY202604070004', NULL, '{"value": "KYBGSY202604070004"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-businessModule', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-flowCode', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-entityId', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-currentNode', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-taskStatus', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'taskStatus', 'string', '已驳回', NULL, '{"value": "已驳回"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070004-d492085f3f-candidateGroups', 'procinst-scientificreport-kybgsy202604070004-d492085f3f', 'exec-流程结束-6535188ef7', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-businessKey', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'businessKey', 'string', 'KYBGSY202604070003', NULL, '{"value": "KYBGSY202604070003"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-businessModule', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-flowCode', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-entityId', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'entityId', 'number', NULL, 3, '{"value": 3}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-currentNode', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-taskStatus', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070003-6a150f25a3-candidateGroups', 'procinst-scientificreport-kybgsy202604070003-6a150f25a3', 'exec-流程结束-7a9deb4a07', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-businessKey', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'businessKey', 'string', 'KYBGSY202604070002', NULL, '{"value": "KYBGSY202604070002"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-businessModule', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-flowCode', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-entityId', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-currentNode', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-taskStatus', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-candidateGroups', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'exec-advisorreview-4b9b967c7f', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-businessKey', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'businessKey', 'string', 'KYBGSY202604070001', NULL, '{"value": "KYBGSY202604070001"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-businessModule', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-flowCode', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-entityId', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'entityId', 'number', NULL, 1, '{"value": 1}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-currentNode', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-taskStatus', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070001-ac313f254d-candidateGroups', 'procinst-scientificreport-kybgsy202604070001-ac313f254d', 'exec-流程结束-f7640479cc', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-businessKey', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'businessKey', 'string', 'ZSLQSP202604070012', NULL, '{"value": "ZSLQSP202604070012"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-businessModule', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-flowCode', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-entityId', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'entityId', 'number', NULL, 12, '{"value": 12}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-currentNode', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-taskStatus', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'exec-qualificationrevie-edf7c6e87f', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-businessKey', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'businessKey', 'string', 'ZSLQSP202604070011', NULL, '{"value": "ZSLQSP202604070011"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-businessModule', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-flowCode', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-entityId', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'entityId', 'number', NULL, 11, '{"value": 11}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-currentNode', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'currentNode', 'string', '录取决策', NULL, '{"value": "录取决策"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-taskStatus', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'exec-admissiondecision-aaede43f43', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-businessKey', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'businessKey', 'string', 'ZSLQSP202604070010', NULL, '{"value": "ZSLQSP202604070010"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-businessModule', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-flowCode', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-entityId', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'entityId', 'number', NULL, 10, '{"value": 10}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-currentNode', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-taskStatus', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070010-beee23a649-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070010-beee23a649', 'exec-流程结束-65775a0795', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-businessKey', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'businessKey', 'string', 'ZSLQSP202604070009', NULL, '{"value": "ZSLQSP202604070009"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-businessModule', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-flowCode', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-entityId', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'entityId', 'number', NULL, 9, '{"value": 9}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-currentNode', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-taskStatus', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'taskStatus', 'string', '已驳回', NULL, '{"value": "已驳回"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070009-01cf086f21-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070009-01cf086f21', 'exec-流程结束-e3bb67368b', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-businessKey', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'businessKey', 'string', 'ZSLQSP202604070008', NULL, '{"value": "ZSLQSP202604070008"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-businessModule', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-flowCode', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-entityId', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'entityId', 'number', NULL, 8, '{"value": 8}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-currentNode', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-taskStatus', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070008-23605124be-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070008-23605124be', 'exec-流程结束-446886c26d', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-businessKey', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'businessKey', 'string', 'ZSLQSP202604070007', NULL, '{"value": "ZSLQSP202604070007"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-businessModule', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-flowCode', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-entityId', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'entityId', 'number', NULL, 7, '{"value": 7}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-currentNode', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'currentNode', 'string', '评分准备', NULL, '{"value": "评分准备"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-taskStatus', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'exec-qualificationpasse-be93ae536d', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-businessKey', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'businessKey', 'string', 'ZSLQSP202604070006', NULL, '{"value": "ZSLQSP202604070006"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-businessModule', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-flowCode', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-entityId', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'entityId', 'number', NULL, 6, '{"value": 6}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-currentNode', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-taskStatus', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'exec-qualificationrevie-1fb9c8f469', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-businessKey', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'businessKey', 'string', 'ZSLQSP202604070005', NULL, '{"value": "ZSLQSP202604070005"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-businessModule', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-flowCode', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-entityId', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'entityId', 'number', NULL, 5, '{"value": 5}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-currentNode', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'currentNode', 'string', '面试安排', NULL, '{"value": "面试安排"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-taskStatus', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'exec-interviewarrangeme-7f0810d43d', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-businessKey', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'businessKey', 'string', 'ZSLQSP202604070004', NULL, '{"value": "ZSLQSP202604070004"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-businessModule', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-flowCode', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-entityId', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-currentNode', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'currentNode', 'string', '录取决策', NULL, '{"value": "录取决策"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-taskStatus', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'exec-admissiondecision-fcaa129de5', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-businessKey', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'businessKey', 'string', 'ZSLQSP202604070003', NULL, '{"value": "ZSLQSP202604070003"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-businessModule', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-flowCode', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-entityId', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'entityId', 'number', NULL, 3, '{"value": 3}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-currentNode', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'currentNode', 'string', '录取确认', NULL, '{"value": "录取确认"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-taskStatus', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'exec-admissionconfirmat-165e308f11', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-businessKey', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'businessKey', 'string', 'ZSLQSP202604070002', NULL, '{"value": "ZSLQSP202604070002"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-businessModule', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-flowCode', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-entityId', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-currentNode', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-taskStatus', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070002-5625e6238f-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070002-5625e6238f', 'exec-流程结束-c2af43da3a', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-businessKey', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'businessKey', 'string', 'ZSLQSP202604070001', NULL, '{"value": "ZSLQSP202604070001"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-businessModule', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-flowCode', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-entityId', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'entityId', 'number', NULL, 1, '{"value": 1}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-currentNode', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-taskStatus', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04-candidateGroups', 'procinst-recruitmentappli-zslqsp202604070001-c7f7f73c04', 'exec-流程结束-d27bde8440', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-businessKey', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'businessKey', 'string', 'KYBGSY202604070008', NULL, '{"value": "KYBGSY202604070008"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-businessModule', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-flowCode', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-entityId', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'entityId', 'number', NULL, 8, '{"value": 8}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-currentNode', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-taskStatus', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-scientificreport-kybgsy202604070008-f6ee0b043e-candidateGroups', 'procinst-scientificreport-kybgsy202604070008-f6ee0b043e', 'exec-流程结束-7e005951a7', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-07 18:50:41+08', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-businessKey', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'businessKey', 'string', 'SWSQSP202604090002', NULL, '{"value": "SWSQSP202604090002"}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-businessModule', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-flowCode', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-entityId', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'entityId', 'number', NULL, 6, '{"value": 6}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-currentNode', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'currentNode', 'string', '流程结束', NULL, '{"value": "流程结束"}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-taskStatus', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'taskStatus', 'string', '已通过', NULL, '{"value": "已通过"}', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-thesis-swsqsp202604090002-a0b74461b9-candidateGroups', 'procinst-thesis-swsqsp202604090002-a0b74461b9', 'exec-流程结束-387b35c278', NULL, 'candidateGroups', 'json', NULL, NULL, '[]', '2026-04-09 20:15:05+08', '2026-04-09 20:15:26+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-businessKey', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'businessKey', 'string', 'ZSLQSP202604220001', NULL, '{"value": "ZSLQSP202604220001"}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-businessModule', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-flowCode', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-entityId', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'entityId', 'number', NULL, 20, '{"value": 20}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-currentNode', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-taskStatus', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'exec-qualificationrevie-8e43da6197', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:02+08', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-businessKey', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'businessKey', 'string', 'ZSLQSP202604220002', NULL, '{"value": "ZSLQSP202604220002"}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-businessModule', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-flowCode', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-entityId', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'entityId', 'number', NULL, 21, '{"value": 21}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-currentNode', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-taskStatus', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'exec-qualificationrevie-d7d537306f', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:03+08', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-businessKey', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'businessKey', 'string', 'ZSLQSP202604220003', NULL, '{"value": "ZSLQSP202604220003"}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-businessModule', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-flowCode', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-entityId', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'entityId', 'number', NULL, 22, '{"value": 22}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-currentNode', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-taskStatus', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'exec-qualificationrevie-a7d2ad7040', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:04+08', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-businessKey', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'businessKey', 'string', 'ZSLQSP202604220004', NULL, '{"value": "ZSLQSP202604220004"}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-businessModule', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-flowCode', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-entityId', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'entityId', 'number', NULL, 23, '{"value": 23}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-currentNode', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-taskStatus', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'exec-qualificationrevie-1ddc0baae8', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:28+08', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-businessKey', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'businessKey', 'string', 'ZSLQSP202604220005', NULL, '{"value": "ZSLQSP202604220005"}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-businessModule', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-flowCode', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-entityId', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'entityId', 'number', NULL, 24, '{"value": 24}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-currentNode', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-taskStatus', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'exec-qualificationrevie-5263e586fb', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:29+08', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-businessKey', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'businessKey', 'string', 'ZSLQSP202604220006', NULL, '{"value": "ZSLQSP202604220006"}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-businessModule', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-flowCode', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-entityId', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'entityId', 'number', NULL, 25, '{"value": 25}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-currentNode', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-taskStatus', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-candidateGroups', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'exec-qualificationrevie-355ccf5e2d', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:30+08', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-businessKey', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'businessKey', 'string', 'ZSLQSP202604210007', NULL, '{"value": "ZSLQSP202604210007"}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-businessModule', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-flowCode', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-entityId', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'entityId', 'number', NULL, 19, '{"value": 19}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-currentNode', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-taskStatus', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_hi_varinst" VALUES ('HVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-candidateGroups', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'exec-qualificationrevie-59a9b3ebba', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 02:06:20+08', '2026-04-21 02:06:20+08');

-- ----------------------------
-- Table structure for dtlms_wf_re_deployment
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_re_deployment";
CREATE TABLE "public"."dtlms_wf_re_deployment" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "name_" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "category_" varchar(128) COLLATE "pg_catalog"."default",
  "key_" varchar(128) COLLATE "pg_catalog"."default",
  "deploy_time_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "tenant_id_" varchar(64) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_re_deployment
-- ----------------------------
INSERT INTO "public"."dtlms_wf_re_deployment" VALUES ('dep-recruitmentapplication-4588d501', '招生录取审批', '招生管理', 'recruitment_application', '2026-04-23 12:01:25+08', NULL);
INSERT INTO "public"."dtlms_wf_re_deployment" VALUES ('dep-thesis-d4b0719b', '学位申请审批', '学位管理', 'thesis', '2026-04-07 18:50:41+08', NULL);
INSERT INTO "public"."dtlms_wf_re_deployment" VALUES ('dep-outboundstudy-6d8e1576', '外出研修审批', '培养管理', 'outbound_study', '2026-04-07 18:50:41+08', NULL);
INSERT INTO "public"."dtlms_wf_re_deployment" VALUES ('dep-scientificreport-9069a4b1', '科研报告审阅', '培养管理', 'scientific_report', '2026-04-07 18:50:41+08', NULL);

-- ----------------------------
-- Table structure for dtlms_wf_re_procdef
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_re_procdef";
CREATE TABLE "public"."dtlms_wf_re_procdef" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "key_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "version_" int4 NOT NULL DEFAULT 1,
  "deployment_id_" varchar(64) COLLATE "pg_catalog"."default",
  "resource_name_" varchar(255) COLLATE "pg_catalog"."default",
  "diagram_resource_name_" varchar(255) COLLATE "pg_catalog"."default",
  "name_" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "category_" varchar(128) COLLATE "pg_catalog"."default",
  "description_" text COLLATE "pg_catalog"."default",
  "suspension_state_" int4 NOT NULL DEFAULT 1,
  "tenant_id_" varchar(64) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_re_procdef
-- ----------------------------
INSERT INTO "public"."dtlms_wf_re_procdef" VALUES ('procdef-recruitmentapplicati-v1-52a2d0f8', 'recruitment_application', 1, 'dep-recruitmentapplication-4588d501', 'recruitment_application.bpmn20.xml', 'recruitment_application.png', '招生录取审批', '招生管理', '招生录取审批 定义', 1, NULL);
INSERT INTO "public"."dtlms_wf_re_procdef" VALUES ('procdef-thesis-v1-065eef39', 'thesis', 1, 'dep-thesis-d4b0719b', 'thesis.bpmn20.xml', 'thesis.png', '学位申请审批', '学位管理', '学位申请审批 定义', 1, NULL);
INSERT INTO "public"."dtlms_wf_re_procdef" VALUES ('procdef-outboundstudy-v1-aadfc5bd', 'outbound_study', 1, 'dep-outboundstudy-6d8e1576', 'outbound_study.bpmn20.xml', 'outbound_study.png', '外出研修审批', '培养管理', '外出研修审批 定义', 1, NULL);
INSERT INTO "public"."dtlms_wf_re_procdef" VALUES ('procdef-scientificreport-v1-60dc0211', 'scientific_report', 1, 'dep-scientificreport-9069a4b1', 'scientific_report.bpmn20.xml', 'scientific_report.png', '科研报告审阅', '培养管理', '科研报告审阅 定义', 1, NULL);

-- ----------------------------
-- Table structure for dtlms_wf_ru_execution
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_ru_execution";
CREATE TABLE "public"."dtlms_wf_ru_execution" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_def_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "business_key_" varchar(64) COLLATE "pg_catalog"."default",
  "parent_id_" varchar(64) COLLATE "pg_catalog"."default",
  "act_id_" varchar(128) COLLATE "pg_catalog"."default",
  "is_active_" bool NOT NULL DEFAULT true,
  "is_concurrent_" bool NOT NULL DEFAULT false,
  "is_scope_" bool NOT NULL DEFAULT true,
  "start_time_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "start_user_id_" varchar(64) COLLATE "pg_catalog"."default",
  "super_exec_" varchar(64) COLLATE "pg_catalog"."default",
  "tenant_id_" varchar(64) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_ru_execution
-- ----------------------------
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604230010', NULL, 'qualification_review', 't', 'f', 't', '2026-04-23 12:01:25+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604230009', NULL, 'qualification_review', 't', 'f', 't', '2026-04-23 11:49:20+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604210006', NULL, 'qualification_review', 't', 'f', 't', '2026-04-21 02:02:08+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604210004', NULL, 'qualification_review', 't', 'f', 't', '2026-04-21 01:53:57+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604100004', NULL, 'qualification_review', 't', 'f', 't', '2026-04-10 13:27:37+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604210005', NULL, 'qualification_review', 't', 'f', 't', '2026-04-21 01:58:19+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604100003', NULL, 'qualification_review', 't', 'f', 't', '2026-04-10 13:26:14+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604100001', NULL, 'qualification_review', 't', 'f', 't', '2026-04-10 13:14:58+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'procdef-thesis-v1-065eef39', 'SWSQSP202604070004', NULL, 'advisor_precheck', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'procdef-thesis-v1-065eef39', 'SWSQSP202604070002', NULL, 'secretary_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'procdef-outboundstudy-v1-aadfc5bd', 'WCYXSP202604070002', NULL, 'advisor_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'procdef-outboundstudy-v1-aadfc5bd', 'WCYXSP202604070004', NULL, 'advisor_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'procdef-scientificreport-v1-60dc0211', 'KYBGSY202604070007', NULL, 'advisor_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'procdef-scientificreport-v1-60dc0211', 'KYBGSY202604070006', NULL, 'advisor_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'procdef-scientificreport-v1-60dc0211', 'KYBGSY202604070002', NULL, 'advisor_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070012', NULL, 'qualification_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070011', NULL, 'admission_decision', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070007', NULL, 'qualification_passed', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070006', NULL, 'qualification_review', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070005', NULL, 'interview_arrangement', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070004', NULL, 'admission_decision', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604070003', NULL, 'admission_confirmation', 't', 'f', 't', '2026-04-07 18:50:41+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220001', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:24:02+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220002', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:24:03+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220003', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:24:04+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220004', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:25:28+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220005', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:25:29+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604220006', NULL, 'qualification_review', 't', 'f', 't', '2026-04-22 09:25:30+08', NULL, NULL, NULL);
INSERT INTO "public"."dtlms_wf_ru_execution" VALUES ('exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'ZSLQSP202604210007', NULL, 'qualification_review', 't', 'f', 't', '2026-04-21 02:06:20+08', NULL, NULL, NULL);

-- ----------------------------
-- Table structure for dtlms_wf_ru_identitylink
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_ru_identitylink";
CREATE TABLE "public"."dtlms_wf_ru_identitylink" (
  "id_" int8 NOT NULL DEFAULT nextval('dtlms_wf_ru_identitylink_id__seq'::regclass),
  "task_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default",
  "user_id_" varchar(64) COLLATE "pg_catalog"."default",
  "group_id_" varchar(64) COLLATE "pg_catalog"."default",
  "link_type_" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_wf_ru_identitylink
-- ----------------------------
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6377, 'TASK-47', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6378, 'TASK-46', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6379, 'TASK-36', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6380, 'TASK-34', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6381, 'TASK-33', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6382, 'TASK-35', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6383, 'TASK-32', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6384, 'TASK-31', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6385, 'TASK-28', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6386, 'TASK-26', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'secretary', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6387, 'TASK-22', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6388, 'TASK-24', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6389, 'TASK-19', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6390, 'TASK-18', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6391, 'TASK-14', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'advisor', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6392, 'TASK-12', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6393, 'TASK-11', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6394, 'TASK-7', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6395, 'TASK-6', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6396, 'TASK-5', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6397, 'TASK-4', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6398, 'TASK-3', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6399, 'TASK-40', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6400, 'TASK-41', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6401, 'TASK-42', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6402, 'TASK-43', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6403, 'TASK-44', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6404, 'TASK-45', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_wf_ru_identitylink" VALUES (6405, 'TASK-37', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'platform_admin', 'candidate', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- Table structure for dtlms_wf_ru_task
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_ru_task";
CREATE TABLE "public"."dtlms_wf_ru_task" (
  "id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "exec_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_def_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "task_def_key_" varchar(128) COLLATE "pg_catalog"."default",
  "name_" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "business_key_" varchar(64) COLLATE "pg_catalog"."default",
  "assignee_" varchar(64) COLLATE "pg_catalog"."default",
  "owner_" varchar(64) COLLATE "pg_catalog"."default",
  "create_time_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "due_date_" timestamptz(6),
  "claim_time_" timestamptz(6),
  "priority_" int4 NOT NULL DEFAULT 50,
  "suspension_state_" int4 NOT NULL DEFAULT 1,
  "tenant_id_" varchar(64) COLLATE "pg_catalog"."default",
  "form_key_" varchar(255) COLLATE "pg_catalog"."default",
  "description_" text COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Records of dtlms_wf_ru_task
-- ----------------------------
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-47', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '罗凯报名审核', 'ZSLQSP202604230010', NULL, NULL, '2026-04-23 12:01:25+08', '2026-04-24 12:01:25+08', NULL, 50, 1, NULL, 'ZSLQSP202604230010', '业务编号：ZSLQSP202604230010；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-46', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '李小玉报名审核', 'ZSLQSP202604230009', NULL, NULL, '2026-04-23 11:49:20+08', '2026-04-24 11:49:20+08', NULL, 50, 1, NULL, 'ZSLQSP202604230009', '业务编号：ZSLQSP202604230009；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-36', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '??????报名审核', 'ZSLQSP202604210006', NULL, NULL, '2026-04-21 02:02:08+08', '2026-04-22 02:02:08+08', NULL, 50, 1, NULL, 'ZSLQSP202604210006', '业务编号：ZSLQSP202604210006；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-34', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '联调考生报名审核', 'ZSLQSP202604210004', NULL, NULL, '2026-04-21 01:53:57+08', '2026-04-22 01:53:57+08', NULL, 50, 1, NULL, 'ZSLQSP202604210004', '业务编号：ZSLQSP202604210004；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-33', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '在线联调0410132736报名审核', 'ZSLQSP202604100004', NULL, NULL, '2026-04-10 13:27:37+08', '2026-04-11 13:27:37+08', NULL, 50, 1, NULL, 'ZSLQSP202604100004', '业务编号：ZSLQSP202604100004；研究方向：智能科学；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-35', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', 'Portal Smoke User报名审核', 'ZSLQSP202604210005', NULL, NULL, '2026-04-21 01:58:19+08', '2026-04-22 01:58:19+08', NULL, 50, 1, NULL, 'ZSLQSP202604210005', '业务编号：ZSLQSP202604210005；研究方向：智能制造团队；材料状态：待补材料');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-32', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '联调考生0410132613报名审核', 'ZSLQSP202604100003', NULL, NULL, '2026-04-10 13:26:14+08', '2026-04-11 13:26:14+08', NULL, 50, 1, NULL, 'ZSLQSP202604100003', '业务编号：ZSLQSP202604100003；研究方向：智能科学；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-31', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '联调考生0410131457报名审核', 'ZSLQSP202604100001', NULL, NULL, '2026-04-10 13:14:58+08', '2026-04-11 13:14:58+08', NULL, 50, 1, NULL, 'ZSLQSP202604100001', '业务编号：ZSLQSP202604100001；研究方向：人工智能；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-28', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', 'procdef-thesis-v1-065eef39', 'advisor_precheck', '沈知遥授位审批', 'SWSQSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'SWSQSP202604070004', '论文题目：面向教育场景的大模型知识对齐与应用研究；盲审状态：未送审');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-26', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', 'procdef-thesis-v1-065eef39', 'secretary_review', '赵嘉禾授位审批', 'SWSQSP202604070002', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'SWSQSP202604070002', '论文题目：知识图谱驱动的科研过程智能分析方法研究；盲审状态：进行中');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-22', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', 'procdef-outboundstudy-v1-aadfc5bd', 'advisor_review', '贺景川外出研修申请', 'WCYXSP202604070002', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'WCYXSP202604070002', '研修地点：香港科技大学；起止：2026-02-15 至 2026-07-30');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-24', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', 'procdef-outboundstudy-v1-aadfc5bd', 'advisor_review', '孟书恒外出研修申请', 'WCYXSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'WCYXSP202604070004', '研修地点：深圳；起止：2026-05-18 至 2026-05-22');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-19', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', 'procdef-scientificreport-v1-60dc0211', 'advisor_review', '宋知行科研报告审阅', 'KYBGSY202604070007', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'KYBGSY202604070007', '周期：2026Q1；审阅人：刘亚');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-18', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', 'procdef-scientificreport-v1-60dc0211', 'advisor_review', '沈知遥科研报告审阅', 'KYBGSY202604070006', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'KYBGSY202604070006', '周期：2026Q1；审阅人：徐素天');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-14', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', 'procdef-scientificreport-v1-60dc0211', 'advisor_review', '林书雅科研报告审阅', 'KYBGSY202604070002', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'KYBGSY202604070002', '周期：2026Q1；审阅人：刘亚');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-12', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '谢明远报名审核', 'ZSLQSP202604070012', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-08 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070012', '业务编号：ZSLQSP202604070012；研究方向：机器学习；材料状态：已退回修改');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-11', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'admission_decision', '朱安宁报名审核', 'ZSLQSP202604070011', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070011', '业务编号：ZSLQSP202604070011；研究方向：知识图谱；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-7', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_passed', '赵安歌报名审核', 'ZSLQSP202604070007', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-08 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070007', '业务编号：ZSLQSP202604070007；研究方向：工业软件；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-6', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '陈思远报名审核', 'ZSLQSP202604070006', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-08 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070006', '业务编号：ZSLQSP202604070006；研究方向：数字孪生；材料状态：待补材料');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-5', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'interview_arrangement', '李静姝报名审核', 'ZSLQSP202604070005', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070005', '业务编号：ZSLQSP202604070005；研究方向：数据智能；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-4', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'admission_decision', '周亦凡报名审核', 'ZSLQSP202604070004', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070004', '业务编号：ZSLQSP202604070004；研究方向：视觉检测；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-3', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'admission_confirmation', '顾明睿报名审核', 'ZSLQSP202604070003', NULL, NULL, '2026-04-07 18:50:41+08', '2026-04-09 18:50:41+08', NULL, 50, 1, NULL, 'ZSLQSP202604070003', '业务编号：ZSLQSP202604070003；研究方向：工业互联网；材料状态：材料齐全');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-40', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '性能回归be009f7d报名审核', 'ZSLQSP202604220001', NULL, NULL, '2026-04-22 09:24:02+08', '2026-04-23 09:24:02+08', NULL, 50, 1, NULL, 'ZSLQSP202604220001', '业务编号：ZSLQSP202604220001；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-41', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '直建更新be009f7d报名审核', 'ZSLQSP202604220002', NULL, NULL, '2026-04-22 09:24:03+08', '2026-04-23 09:24:03+08', NULL, 50, 1, NULL, 'ZSLQSP202604220002', '业务编号：ZSLQSP202604220002；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-42', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '导入be009f7d报名审核', 'ZSLQSP202604220003', NULL, NULL, '2026-04-22 09:24:04+08', '2026-04-23 09:24:04+08', NULL, 50, 1, NULL, 'ZSLQSP202604220003', '业务编号：ZSLQSP202604220003；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-43', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '性能回归52d69275报名审核', 'ZSLQSP202604220004', NULL, NULL, '2026-04-22 09:25:28+08', '2026-04-23 09:25:28+08', NULL, 50, 1, NULL, 'ZSLQSP202604220004', '业务编号：ZSLQSP202604220004；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-44', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '直建更新52d69275报名审核', 'ZSLQSP202604220005', NULL, NULL, '2026-04-22 09:25:29+08', '2026-04-23 09:25:29+08', NULL, 50, 1, NULL, 'ZSLQSP202604220005', '业务编号：ZSLQSP202604220005；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-45', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '导入52d69275报名审核', 'ZSLQSP202604220006', NULL, NULL, '2026-04-22 09:25:30+08', '2026-04-23 09:25:30+08', NULL, 50, 1, NULL, 'ZSLQSP202604220006', '业务编号：ZSLQSP202604220006；研究方向：智能制造团队；材料状态：待审核');
INSERT INTO "public"."dtlms_wf_ru_task" VALUES ('TASK-37', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', 'procdef-recruitmentapplicati-v1-52a2d0f8', 'qualification_review', '测试管理保存报名审核', 'ZSLQSP202604210007', NULL, NULL, '2026-04-21 02:06:20+08', '2026-04-22 02:06:20+08', NULL, 50, 1, NULL, 'ZSLQSP202604210007', '业务编号：ZSLQSP202604210007；研究方向：智能制造团队；材料状态：待补材料');

-- ----------------------------
-- Table structure for dtlms_wf_ru_variable
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_wf_ru_variable";
CREATE TABLE "public"."dtlms_wf_ru_variable" (
  "id_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "exec_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "proc_inst_id_" varchar(64) COLLATE "pg_catalog"."default" NOT NULL,
  "task_id_" varchar(64) COLLATE "pg_catalog"."default",
  "name_" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "var_type_" varchar(32) COLLATE "pg_catalog"."default" NOT NULL,
  "text_value_" text COLLATE "pg_catalog"."default",
  "number_value_" int8,
  "json_value_" jsonb,
  "create_time_" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_wf_ru_variable
-- ----------------------------
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-businessKey', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'businessKey', 'string', 'ZSLQSP202604230010', NULL, '{"value": "ZSLQSP202604230010"}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-businessModule', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-flowCode', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-entityId', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'entityId', 'number', NULL, 27, '{"value": 27}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-currentNode', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-taskStatus', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230010-4e7a27718a-candidateGroups', 'exec-qualificationrevie-d9ac1235d8', 'procinst-recruitmentappli-zslqsp202604230010-4e7a27718a', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-23 12:01:25+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-businessKey', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'businessKey', 'string', 'ZSLQSP202604230009', NULL, '{"value": "ZSLQSP202604230009"}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-businessModule', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-flowCode', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-entityId', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'entityId', 'number', NULL, 26, '{"value": 26}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-currentNode', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-taskStatus', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f-candidateGroups', 'exec-qualificationrevie-eede6d1dd9', 'procinst-recruitmentappli-zslqsp202604230009-d7fe2cf18f', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-23 11:49:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-businessKey', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'businessKey', 'string', 'ZSLQSP202604210006', NULL, '{"value": "ZSLQSP202604210006"}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-businessModule', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-flowCode', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-entityId', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'entityId', 'number', NULL, 18, '{"value": 18}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-currentNode', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-taskStatus', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210006-034d0beb2e-candidateGroups', 'exec-qualificationrevie-5df923986a', 'procinst-recruitmentappli-zslqsp202604210006-034d0beb2e', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 02:02:08+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-businessKey', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'businessKey', 'string', 'ZSLQSP202604210004', NULL, '{"value": "ZSLQSP202604210004"}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-businessModule', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-flowCode', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-entityId', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'entityId', 'number', NULL, 16, '{"value": 16}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-currentNode', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-taskStatus', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210004-198915ce91-candidateGroups', 'exec-qualificationrevie-f9b4e63f9c', 'procinst-recruitmentappli-zslqsp202604210004-198915ce91', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 01:53:57+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-businessKey', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'businessKey', 'string', 'ZSLQSP202604100004', NULL, '{"value": "ZSLQSP202604100004"}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-businessModule', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-flowCode', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-entityId', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'entityId', 'number', NULL, 15, '{"value": 15}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-currentNode', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-taskStatus', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100004-58be9b522d-candidateGroups', 'exec-qualificationrevie-7d07ba753a', 'procinst-recruitmentappli-zslqsp202604100004-58be9b522d', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:27:37+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-businessKey', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'businessKey', 'string', 'ZSLQSP202604210005', NULL, '{"value": "ZSLQSP202604210005"}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-businessModule', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-flowCode', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-entityId', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'entityId', 'number', NULL, 17, '{"value": 17}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-currentNode', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-taskStatus', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb-candidateGroups', 'exec-qualificationrevie-887e01a071', 'procinst-recruitmentappli-zslqsp202604210005-d5520cb9cb', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 01:58:19+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-businessKey', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'businessKey', 'string', 'ZSLQSP202604100003', NULL, '{"value": "ZSLQSP202604100003"}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-businessModule', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-flowCode', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-entityId', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'entityId', 'number', NULL, 14, '{"value": 14}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-currentNode', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-taskStatus', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2-candidateGroups', 'exec-qualificationrevie-18c95ca2f8', 'procinst-recruitmentappli-zslqsp202604100003-a5e6d7a1a2', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:26:14+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-businessKey', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'businessKey', 'string', 'ZSLQSP202604100001', NULL, '{"value": "ZSLQSP202604100001"}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-businessModule', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-flowCode', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-entityId', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'entityId', 'number', NULL, 13, '{"value": 13}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-currentNode', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-taskStatus', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604100001-7a103518ab-candidateGroups', 'exec-qualificationrevie-44869f7eed', 'procinst-recruitmentappli-zslqsp202604100001-7a103518ab', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-10 13:14:58+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-businessKey', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'businessKey', 'string', 'SWSQSP202604070004', NULL, '{"value": "SWSQSP202604070004"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-businessModule', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-flowCode', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-entityId', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-currentNode', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'currentNode', 'string', '导师预审', NULL, '{"value": "导师预审"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-taskStatus', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070004-e14f35b86f-candidateGroups', 'exec-advisorprecheck-19a4d28b0a', 'procinst-thesis-swsqsp202604070004-e14f35b86f', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-businessKey', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'businessKey', 'string', 'SWSQSP202604070002', NULL, '{"value": "SWSQSP202604070002"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-businessModule', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'businessModule', 'string', '学位管理', NULL, '{"value": "学位管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-flowCode', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'flowCode', 'string', 'thesis', NULL, '{"value": "thesis"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-entityId', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-currentNode', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'currentNode', 'string', '材料复核', NULL, '{"value": "材料复核"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-taskStatus', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-thesis-swsqsp202604070002-1fdcd41689-candidateGroups', 'exec-secretaryreview-02832ea26f', 'procinst-thesis-swsqsp202604070002-1fdcd41689', NULL, 'candidateGroups', 'json', NULL, NULL, '["secretary"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-businessKey', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'businessKey', 'string', 'WCYXSP202604070002', NULL, '{"value": "WCYXSP202604070002"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-businessModule', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-flowCode', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-entityId', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-currentNode', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'currentNode', 'string', '导师审核', NULL, '{"value": "导师审核"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-taskStatus', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070002-4d16cbba15-candidateGroups', 'exec-advisorreview-d65a8149b8', 'procinst-outboundstudy-wcyxsp202604070002-4d16cbba15', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-businessKey', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'businessKey', 'string', 'WCYXSP202604070004', NULL, '{"value": "WCYXSP202604070004"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-businessModule', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-flowCode', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'flowCode', 'string', 'outbound_study', NULL, '{"value": "outbound_study"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-entityId', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-currentNode', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'currentNode', 'string', '导师审核', NULL, '{"value": "导师审核"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-taskStatus', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-outboundstudy-wcyxsp202604070004-d049327905-candidateGroups', 'exec-advisorreview-b5efa6424c', 'procinst-outboundstudy-wcyxsp202604070004-d049327905', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-businessKey', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'businessKey', 'string', 'KYBGSY202604070007', NULL, '{"value": "KYBGSY202604070007"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-businessModule', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-flowCode', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-entityId', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'entityId', 'number', NULL, 7, '{"value": 7}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-currentNode', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-taskStatus', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070007-3c62b8afbd-candidateGroups', 'exec-advisorreview-5dfab64a31', 'procinst-scientificreport-kybgsy202604070007-3c62b8afbd', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-businessKey', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'businessKey', 'string', 'KYBGSY202604070006', NULL, '{"value": "KYBGSY202604070006"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-businessModule', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-flowCode', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-entityId', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'entityId', 'number', NULL, 6, '{"value": 6}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-currentNode', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-taskStatus', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070006-a75676b582-candidateGroups', 'exec-advisorreview-b7c77ef380', 'procinst-scientificreport-kybgsy202604070006-a75676b582', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-businessKey', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'businessKey', 'string', 'KYBGSY202604070002', NULL, '{"value": "KYBGSY202604070002"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-businessModule', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'businessModule', 'string', '培养管理', NULL, '{"value": "培养管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-flowCode', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'flowCode', 'string', 'scientific_report', NULL, '{"value": "scientific_report"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-entityId', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'entityId', 'number', NULL, 2, '{"value": 2}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-currentNode', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'currentNode', 'string', '导师审阅', NULL, '{"value": "导师审阅"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-taskStatus', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-scientificreport-kybgsy202604070002-56f9d14cb3-candidateGroups', 'exec-advisorreview-4b9b967c7f', 'procinst-scientificreport-kybgsy202604070002-56f9d14cb3', NULL, 'candidateGroups', 'json', NULL, NULL, '["advisor"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-businessKey', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'businessKey', 'string', 'ZSLQSP202604070012', NULL, '{"value": "ZSLQSP202604070012"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-businessModule', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-flowCode', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-entityId', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'entityId', 'number', NULL, 12, '{"value": 12}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-currentNode', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-taskStatus', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070012-31b22e411a-candidateGroups', 'exec-qualificationrevie-edf7c6e87f', 'procinst-recruitmentappli-zslqsp202604070012-31b22e411a', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-businessKey', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'businessKey', 'string', 'ZSLQSP202604070011', NULL, '{"value": "ZSLQSP202604070011"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-businessModule', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-flowCode', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-entityId', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'entityId', 'number', NULL, 11, '{"value": 11}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-currentNode', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'currentNode', 'string', '录取决策', NULL, '{"value": "录取决策"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-taskStatus', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070011-48934cba0b-candidateGroups', 'exec-admissiondecision-aaede43f43', 'procinst-recruitmentappli-zslqsp202604070011-48934cba0b', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-businessKey', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'businessKey', 'string', 'ZSLQSP202604070007', NULL, '{"value": "ZSLQSP202604070007"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-businessModule', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-flowCode', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-entityId', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'entityId', 'number', NULL, 7, '{"value": 7}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-currentNode', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'currentNode', 'string', '评分准备', NULL, '{"value": "评分准备"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-taskStatus', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070007-b6a620fd62-candidateGroups', 'exec-qualificationpasse-be93ae536d', 'procinst-recruitmentappli-zslqsp202604070007-b6a620fd62', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-businessKey', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'businessKey', 'string', 'ZSLQSP202604070006', NULL, '{"value": "ZSLQSP202604070006"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-businessModule', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-flowCode', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-entityId', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'entityId', 'number', NULL, 6, '{"value": 6}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-currentNode', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-taskStatus', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070006-ab47be6465-candidateGroups', 'exec-qualificationrevie-1fb9c8f469', 'procinst-recruitmentappli-zslqsp202604070006-ab47be6465', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-businessKey', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'businessKey', 'string', 'ZSLQSP202604070005', NULL, '{"value": "ZSLQSP202604070005"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-businessModule', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-flowCode', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-entityId', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'entityId', 'number', NULL, 5, '{"value": 5}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-currentNode', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'currentNode', 'string', '面试安排', NULL, '{"value": "面试安排"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-taskStatus', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070005-2131f46425-candidateGroups', 'exec-interviewarrangeme-7f0810d43d', 'procinst-recruitmentappli-zslqsp202604070005-2131f46425', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-businessKey', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'businessKey', 'string', 'ZSLQSP202604070004', NULL, '{"value": "ZSLQSP202604070004"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-businessModule', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-flowCode', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-entityId', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'entityId', 'number', NULL, 4, '{"value": 4}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-currentNode', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'currentNode', 'string', '录取决策', NULL, '{"value": "录取决策"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-taskStatus', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070004-716ef62d39-candidateGroups', 'exec-admissiondecision-fcaa129de5', 'procinst-recruitmentappli-zslqsp202604070004-716ef62d39', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-businessKey', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'businessKey', 'string', 'ZSLQSP202604070003', NULL, '{"value": "ZSLQSP202604070003"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-businessModule', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-flowCode', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-entityId', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'entityId', 'number', NULL, 3, '{"value": 3}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-currentNode', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'currentNode', 'string', '录取确认', NULL, '{"value": "录取确认"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-taskStatus', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'taskStatus', 'string', '处理中', NULL, '{"value": "处理中"}', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604070003-15d97c12b2-candidateGroups', 'exec-admissionconfirmat-165e308f11', 'procinst-recruitmentappli-zslqsp202604070003-15d97c12b2', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-07 18:50:41+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-businessKey', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'businessKey', 'string', 'ZSLQSP202604220001', NULL, '{"value": "ZSLQSP202604220001"}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-businessModule', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-flowCode', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-entityId', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'entityId', 'number', NULL, 20, '{"value": 20}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-currentNode', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-taskStatus', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220001-241ea95845-candidateGroups', 'exec-qualificationrevie-8e43da6197', 'procinst-recruitmentappli-zslqsp202604220001-241ea95845', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:02+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-businessKey', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'businessKey', 'string', 'ZSLQSP202604220002', NULL, '{"value": "ZSLQSP202604220002"}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-businessModule', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-flowCode', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-entityId', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'entityId', 'number', NULL, 21, '{"value": 21}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-currentNode', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-taskStatus', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220002-296d571cdb-candidateGroups', 'exec-qualificationrevie-d7d537306f', 'procinst-recruitmentappli-zslqsp202604220002-296d571cdb', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:03+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-businessKey', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'businessKey', 'string', 'ZSLQSP202604220003', NULL, '{"value": "ZSLQSP202604220003"}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-businessModule', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-flowCode', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-entityId', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'entityId', 'number', NULL, 22, '{"value": 22}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-currentNode', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-taskStatus', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220003-29575e36a6-candidateGroups', 'exec-qualificationrevie-a7d2ad7040', 'procinst-recruitmentappli-zslqsp202604220003-29575e36a6', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:24:04+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-businessKey', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'businessKey', 'string', 'ZSLQSP202604220004', NULL, '{"value": "ZSLQSP202604220004"}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-businessModule', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-flowCode', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-entityId', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'entityId', 'number', NULL, 23, '{"value": 23}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-currentNode', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-taskStatus', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220004-324dcc7038-candidateGroups', 'exec-qualificationrevie-1ddc0baae8', 'procinst-recruitmentappli-zslqsp202604220004-324dcc7038', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:28+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-businessKey', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'businessKey', 'string', 'ZSLQSP202604220005', NULL, '{"value": "ZSLQSP202604220005"}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-businessModule', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-flowCode', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-entityId', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'entityId', 'number', NULL, 24, '{"value": 24}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-currentNode', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-taskStatus', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c-candidateGroups', 'exec-qualificationrevie-5263e586fb', 'procinst-recruitmentappli-zslqsp202604220005-ca3a7e306c', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:29+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-businessKey', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'businessKey', 'string', 'ZSLQSP202604220006', NULL, '{"value": "ZSLQSP202604220006"}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-businessModule', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-flowCode', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-entityId', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'entityId', 'number', NULL, 25, '{"value": 25}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-currentNode', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-taskStatus', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604220006-a2ef59760e-candidateGroups', 'exec-qualificationrevie-355ccf5e2d', 'procinst-recruitmentappli-zslqsp202604220006-a2ef59760e', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-22 09:25:30+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-businessKey', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'businessKey', 'string', 'ZSLQSP202604210007', NULL, '{"value": "ZSLQSP202604210007"}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-businessModule', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'businessModule', 'string', '招生管理', NULL, '{"value": "招生管理"}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-flowCode', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'flowCode', 'string', 'recruitment_application', NULL, '{"value": "recruitment_application"}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-entityId', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'entityId', 'number', NULL, 19, '{"value": 19}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-currentNode', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'currentNode', 'string', '资格审核', NULL, '{"value": "资格审核"}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-taskStatus', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'taskStatus', 'string', '待处理', NULL, '{"value": "待处理"}', '2026-04-21 02:06:20+08');
INSERT INTO "public"."dtlms_wf_ru_variable" VALUES ('RVAR-procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464-candidateGroups', 'exec-qualificationrevie-59a9b3ebba', 'procinst-recruitmentappli-zslqsp202604210007-a7d3ed4464', NULL, 'candidateGroups', 'json', NULL, NULL, '["platform_admin"]', '2026-04-21 02:06:20+08');

-- ----------------------------
-- Table structure for dtlms_written_exam_scores
-- ----------------------------
DROP TABLE IF EXISTS "public"."dtlms_written_exam_scores";
CREATE TABLE "public"."dtlms_written_exam_scores" (
  "id" int8 NOT NULL DEFAULT nextval('dtlms_written_exam_scores_id_seq'::regclass),
  "application_id" int8 NOT NULL,
  "exam_date" date,
  "exam_score" numeric(5,2),
  "import_batch_no" varchar(64) COLLATE "pg_catalog"."default",
  "created_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;

-- ----------------------------
-- Records of dtlms_written_exam_scores
-- ----------------------------
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (1, 27, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (2, 26, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (3, 16, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (4, 17, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (5, 19, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (6, 15, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (7, 14, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (8, 13, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (9, 1, '2026-03-20', 91.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (10, 2, '2026-03-20', 88.50, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (11, 3, '2026-03-20', 85.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (12, 4, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (13, 5, '2026-03-20', 82.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (14, 6, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (15, 7, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (16, 8, '2026-03-20', 93.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (17, 9, '2026-03-20', 73.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (18, 10, '2026-03-20', 86.00, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (19, 11, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');
INSERT INTO "public"."dtlms_written_exam_scores" VALUES (20, 12, '2026-03-20', NULL, 'SIM-2026-01', '2026-04-23 13:03:35.578384+08', '2026-04-23 13:03:35.578384+08');

-- ----------------------------
-- View structure for dtlms_v_student_lifecycle_snapshot
-- ----------------------------
DROP VIEW IF EXISTS "public"."dtlms_v_student_lifecycle_snapshot";
CREATE VIEW "public"."dtlms_v_student_lifecycle_snapshot" AS  WITH latest_report AS (
         SELECT DISTINCT ON (dtlms_scientific_reports.student_id) dtlms_scientific_reports.student_id,
            dtlms_scientific_reports.period_label,
            dtlms_scientific_reports.report_status,
            dtlms_scientific_reports.review_score,
            dtlms_scientific_reports.updated_at
           FROM dtlms_scientific_reports
          WHERE dtlms_scientific_reports.is_deleted = false
          ORDER BY dtlms_scientific_reports.student_id, dtlms_scientific_reports.updated_at DESC
        ), latest_admission AS (
         SELECT DISTINCT ON (dtlms_admission_decisions.application_id) dtlms_admission_decisions.application_id,
            dtlms_admission_decisions.decision_status,
            dtlms_admission_decisions.final_score,
            dtlms_admission_decisions.updated_at
           FROM dtlms_admission_decisions
          ORDER BY dtlms_admission_decisions.application_id, dtlms_admission_decisions.updated_at DESC
        )
 SELECT s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    s.degree_type,
    s.team_name,
    a.full_name AS primary_advisor_name,
    tp.version_no AS training_plan_version,
    tp.plan_status,
    lr.period_label AS latest_report_period,
    lr.report_status AS latest_report_status,
    lr.review_score AS latest_report_score,
    t.title AS thesis_title,
    t.thesis_status,
    t.blind_review_status,
    t.degree_granted
   FROM dtlms_students s
     LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.version_no,
            dtlms_training_plans.plan_status
           FROM dtlms_training_plans
          WHERE dtlms_training_plans.student_id = s.id AND dtlms_training_plans.is_deleted = false
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON true
     LEFT JOIN latest_report lr ON lr.student_id = s.id
     LEFT JOIN LATERAL ( SELECT dtlms_theses.title,
            dtlms_theses.thesis_status,
            dtlms_theses.blind_review_status,
            dtlms_theses.degree_granted
           FROM dtlms_theses
          WHERE dtlms_theses.student_id = s.id AND dtlms_theses.is_deleted = false
          ORDER BY dtlms_theses.updated_at DESC
         LIMIT 1) t ON true
  WHERE s.is_deleted = false;

-- ----------------------------
-- View structure for dtlms_v_recruitment_dashboard
-- ----------------------------
DROP VIEW IF EXISTS "public"."dtlms_v_recruitment_dashboard";
CREATE VIEW "public"."dtlms_v_recruitment_dashboard" AS  SELECT rp.id AS plan_id,
    rp.plan_code,
    rp.plan_name,
    rp.academic_year,
    rp.semester,
    rp.plan_status,
    count(DISTINCT ra.id) AS application_total,
    count(DISTINCT
        CASE
            WHEN ra.application_status::text = 'qualified'::text THEN ra.id
            ELSE NULL::bigint
        END) AS qualified_total,
    count(DISTINCT
        CASE
            WHEN ra.application_status::text = 'interviewing'::text THEN ra.id
            ELSE NULL::bigint
        END) AS interviewing_total,
    count(DISTINCT
        CASE
            WHEN ad.decision_status::text = ANY (ARRAY['pre_admitted'::character varying, 'accepted'::character varying]::text[]) THEN ad.id
            ELSE NULL::bigint
        END) AS admitted_total,
    avg(ms.material_score) AS avg_material_score
   FROM dtlms_recruitment_plans rp
     LEFT JOIN dtlms_recruitment_applications ra ON ra.plan_id = rp.id AND ra.is_deleted = false
     LEFT JOIN dtlms_material_scores ms ON ms.application_id = ra.id
     LEFT JOIN dtlms_admission_decisions ad ON ad.application_id = ra.id
  WHERE rp.is_deleted = false
  GROUP BY rp.id, rp.plan_code, rp.plan_name, rp.academic_year, rp.semester, rp.plan_status;

-- ----------------------------
-- View structure for dtlms_v_training_compliance
-- ----------------------------
DROP VIEW IF EXISTS "public"."dtlms_v_training_compliance";
CREATE VIEW "public"."dtlms_v_training_compliance" AS  SELECT s.id AS student_id,
    s.student_no,
    s.full_name,
    s.current_status,
    a.full_name AS advisor_name,
    tp.plan_status,
    tp.report_cycle,
    count(sr.id) FILTER (WHERE sr.report_status::text = ANY (ARRAY['submitted'::character varying, 'reviewed'::character varying]::text[])) AS submitted_report_count,
    count(sr.id) FILTER (WHERE sr.report_status::text = 'pending'::text) AS pending_report_count,
    count(os.id) FILTER (WHERE os.approval_status::text = ANY (ARRAY['submitted'::character varying, 'approved'::character varying, 'ongoing'::character varying]::text[])) AS outbound_study_count
   FROM dtlms_students s
     LEFT JOIN dtlms_advisors a ON a.id = s.primary_advisor_id
     LEFT JOIN LATERAL ( SELECT dtlms_training_plans.plan_status,
            dtlms_training_plans.report_cycle
           FROM dtlms_training_plans
          WHERE dtlms_training_plans.student_id = s.id AND dtlms_training_plans.is_deleted = false
          ORDER BY dtlms_training_plans.updated_at DESC
         LIMIT 1) tp ON true
     LEFT JOIN dtlms_scientific_reports sr ON sr.student_id = s.id AND sr.is_deleted = false
     LEFT JOIN dtlms_outbound_studies os ON os.student_id = s.id AND os.is_deleted = false
  WHERE s.is_deleted = false
  GROUP BY s.id, s.student_no, s.full_name, s.current_status, a.full_name, tp.plan_status, tp.report_cycle;

-- ----------------------------
-- View structure for dtlms_v_degree_pipeline
-- ----------------------------
DROP VIEW IF EXISTS "public"."dtlms_v_degree_pipeline";
CREATE VIEW "public"."dtlms_v_degree_pipeline" AS  SELECT t.id AS thesis_id,
    s.student_no,
    s.full_name,
    a.full_name AS advisor_name,
    t.title,
    t.plagiarism_rate,
    t.thesis_status,
    t.blind_review_status,
    t.defense_date,
    t.degree_granted,
    count(tr.id) AS review_count,
    avg(tr.review_score) AS avg_review_score
   FROM dtlms_theses t
     JOIN dtlms_students s ON s.id = t.student_id
     JOIN dtlms_advisors a ON a.id = t.advisor_id
     LEFT JOIN dtlms_thesis_reviews tr ON tr.thesis_id = t.id
  WHERE t.is_deleted = false
  GROUP BY t.id, s.student_no, s.full_name, a.full_name, t.title, t.plagiarism_rate, t.thesis_status, t.blind_review_status, t.defense_date, t.degree_granted;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_achievements_id_seq"
OWNED BY "public"."dtlms_achievements"."id";
SELECT setval('"public"."dtlms_achievements_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_admission_decisions_id_seq"
OWNED BY "public"."dtlms_admission_decisions"."id";
SELECT setval('"public"."dtlms_admission_decisions_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_advisors_id_seq"
OWNED BY "public"."dtlms_advisors"."id";
SELECT setval('"public"."dtlms_advisors_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_application_materials_id_seq"
OWNED BY "public"."dtlms_application_materials"."id";
SELECT setval('"public"."dtlms_application_materials_id_seq"', 28, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_data_sync_logs_id_seq"
OWNED BY "public"."dtlms_data_sync_logs"."id";
SELECT setval('"public"."dtlms_data_sync_logs_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_dict_data_id_seq"
OWNED BY "public"."dtlms_dict_data"."id";
SELECT setval('"public"."dtlms_dict_data_id_seq"', 48454, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_dict_types_id_seq"
OWNED BY "public"."dtlms_dict_types"."id";
SELECT setval('"public"."dtlms_dict_types_id_seq"', 9272, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_interview_groups_id_seq"
OWNED BY "public"."dtlms_interview_groups"."id";
SELECT setval('"public"."dtlms_interview_groups_id_seq"', 13, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_interview_schedules_id_seq"
OWNED BY "public"."dtlms_interview_schedules"."id";
SELECT setval('"public"."dtlms_interview_schedules_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_interview_scores_id_seq"
OWNED BY "public"."dtlms_interview_scores"."id";
SELECT setval('"public"."dtlms_interview_scores_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_login_logs_id_seq"
OWNED BY "public"."dtlms_login_logs"."id";
SELECT setval('"public"."dtlms_login_logs_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_material_scores_id_seq"
OWNED BY "public"."dtlms_material_scores"."id";
SELECT setval('"public"."dtlms_material_scores_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_notification_templates_id_seq"
OWNED BY "public"."dtlms_notification_templates"."id";
SELECT setval('"public"."dtlms_notification_templates_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_operation_logs_id_seq"
OWNED BY "public"."dtlms_operation_logs"."id";
SELECT setval('"public"."dtlms_operation_logs_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_outbound_studies_id_seq"
OWNED BY "public"."dtlms_outbound_studies"."id";
SELECT setval('"public"."dtlms_outbound_studies_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_permissions_id_seq"
OWNED BY "public"."dtlms_permissions"."id";
SELECT setval('"public"."dtlms_permissions_id_seq"', 2545, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_achievement_records_id_seq"
OWNED BY "public"."dtlms_portal_application_achievement_records"."id";
SELECT setval('"public"."dtlms_portal_application_achievement_records_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_attachments_id_seq"
OWNED BY "public"."dtlms_portal_application_attachments"."id";
SELECT setval('"public"."dtlms_portal_application_attachments_id_seq"', 36, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_education_experiences_id_seq"
OWNED BY "public"."dtlms_portal_application_education_experiences"."id";
SELECT setval('"public"."dtlms_portal_application_education_experiences_id_seq"', 8, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_english_proficiencies_id_seq"
OWNED BY "public"."dtlms_portal_application_english_proficiencies"."id";
SELECT setval('"public"."dtlms_portal_application_english_proficiencies_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_family_members_id_seq"
OWNED BY "public"."dtlms_portal_application_family_members"."id";
SELECT setval('"public"."dtlms_portal_application_family_members_id_seq"', 16, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_practice_experiences_id_seq"
OWNED BY "public"."dtlms_portal_application_practice_experiences"."id";
SELECT setval('"public"."dtlms_portal_application_practice_experiences_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_application_preferences_id_seq"
OWNED BY "public"."dtlms_portal_application_preferences"."id";
SELECT setval('"public"."dtlms_portal_application_preferences_id_seq"', 411, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_portal_students_id_seq"
OWNED BY "public"."dtlms_portal_students"."id";
SELECT setval('"public"."dtlms_portal_students_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_qualification_reviews_id_seq"
OWNED BY "public"."dtlms_qualification_reviews"."id";
SELECT setval('"public"."dtlms_qualification_reviews_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_recruitment_applications_id_seq"
OWNED BY "public"."dtlms_recruitment_applications"."id";
SELECT setval('"public"."dtlms_recruitment_applications_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_recruitment_plans_id_seq"
OWNED BY "public"."dtlms_recruitment_plans"."id";
SELECT setval('"public"."dtlms_recruitment_plans_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_research_fields_id_seq"
OWNED BY "public"."dtlms_research_fields"."id";
SELECT setval('"public"."dtlms_research_fields_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_research_projects_id_seq"
OWNED BY "public"."dtlms_research_projects"."id";
SELECT setval('"public"."dtlms_research_projects_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_reviewer_assignments_id_seq"
OWNED BY "public"."dtlms_reviewer_assignments"."id";
SELECT setval('"public"."dtlms_reviewer_assignments_id_seq"', 20, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_role_permissions_id_seq"
OWNED BY "public"."dtlms_role_permissions"."id";
SELECT setval('"public"."dtlms_role_permissions_id_seq"', 6475, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_roles_id_seq"
OWNED BY "public"."dtlms_roles"."id";
SELECT setval('"public"."dtlms_roles_id_seq"', 1961, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_scientific_reports_id_seq"
OWNED BY "public"."dtlms_scientific_reports"."id";
SELECT setval('"public"."dtlms_scientific_reports_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_student_advisor_history_id_seq"
OWNED BY "public"."dtlms_student_advisor_history"."id";
SELECT setval('"public"."dtlms_student_advisor_history_id_seq"', 18, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_student_team_history_id_seq"
OWNED BY "public"."dtlms_student_team_history"."id";
SELECT setval('"public"."dtlms_student_team_history_id_seq"', 18, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_students_id_seq"
OWNED BY "public"."dtlms_students"."id";
SELECT setval('"public"."dtlms_students_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_system_configs_id_seq"
OWNED BY "public"."dtlms_system_configs"."id";
SELECT setval('"public"."dtlms_system_configs_id_seq"', 4266, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_team_advisors_id_seq"
OWNED BY "public"."dtlms_team_advisors"."id";
SELECT setval('"public"."dtlms_team_advisors_id_seq"', 8, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_teams_id_seq"
OWNED BY "public"."dtlms_teams"."id";
SELECT setval('"public"."dtlms_teams_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_theses_id_seq"
OWNED BY "public"."dtlms_theses"."id";
SELECT setval('"public"."dtlms_theses_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_thesis_reviews_id_seq"
OWNED BY "public"."dtlms_thesis_reviews"."id";
SELECT setval('"public"."dtlms_thesis_reviews_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_training_plan_versions_id_seq"
OWNED BY "public"."dtlms_training_plan_versions"."id";
SELECT setval('"public"."dtlms_training_plan_versions_id_seq"', 18, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_training_plans_id_seq"
OWNED BY "public"."dtlms_training_plans"."id";
SELECT setval('"public"."dtlms_training_plans_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_user_roles_id_seq"
OWNED BY "public"."dtlms_user_roles"."id";
SELECT setval('"public"."dtlms_user_roles_id_seq"', 9, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_users_id_seq"
OWNED BY "public"."dtlms_users"."id";
SELECT setval('"public"."dtlms_users_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_wf_ru_identitylink_id__seq"
OWNED BY "public"."dtlms_wf_ru_identitylink"."id_";
SELECT setval('"public"."dtlms_wf_ru_identitylink_id__seq"', 6405, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."dtlms_written_exam_scores_id_seq"
OWNED BY "public"."dtlms_written_exam_scores"."id";
SELECT setval('"public"."dtlms_written_exam_scores_id_seq"', 20, true);

-- ----------------------------
-- Primary Key structure for table dtlms_achievements
-- ----------------------------
ALTER TABLE "public"."dtlms_achievements" ADD CONSTRAINT "dtlms_achievements_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_admission_decisions
-- ----------------------------
CREATE INDEX "idx_admission_decision_status" ON "public"."dtlms_admission_decisions" USING btree (
  "decision_status" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_admission_decisions
-- ----------------------------
ALTER TABLE "public"."dtlms_admission_decisions" ADD CONSTRAINT "dtlms_admission_decisions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_advisors" ADD CONSTRAINT "dtlms_advisors_advisor_no_key" UNIQUE ("advisor_no");

-- ----------------------------
-- Primary Key structure for table dtlms_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_advisors" ADD CONSTRAINT "dtlms_advisors_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_application_materials
-- ----------------------------
ALTER TABLE "public"."dtlms_application_materials" ADD CONSTRAINT "dtlms_application_materials_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_data_sync_logs
-- ----------------------------
CREATE INDEX "idx_sync_logs_source_target" ON "public"."dtlms_data_sync_logs" USING btree (
  "source_system" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "target_system" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "created_at" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_data_sync_logs
-- ----------------------------
ALTER TABLE "public"."dtlms_data_sync_logs" ADD CONSTRAINT "dtlms_data_sync_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_dict_data
-- ----------------------------
CREATE INDEX "idx_dtlms_dict_data_type_sort" ON "public"."dtlms_dict_data" USING btree (
  "dict_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "sort_order" "pg_catalog"."int4_ops" ASC NULLS LAST,
  "id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_dict_data
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_data" ADD CONSTRAINT "dtlms_dict_data_dict_type_value_key" UNIQUE ("dict_type", "value");

-- ----------------------------
-- Checks structure for table dtlms_dict_data
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_data" ADD CONSTRAINT "dtlms_dict_data_status_check" CHECK (status::text = ANY (ARRAY['启用'::character varying, '停用'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table dtlms_dict_data
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_data" ADD CONSTRAINT "dtlms_dict_data_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_dict_types
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_types" ADD CONSTRAINT "dtlms_dict_types_dict_type_key" UNIQUE ("dict_type");

-- ----------------------------
-- Checks structure for table dtlms_dict_types
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_types" ADD CONSTRAINT "dtlms_dict_types_status_check" CHECK (status::text = ANY (ARRAY['启用'::character varying, '停用'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table dtlms_dict_types
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_types" ADD CONSTRAINT "dtlms_dict_types_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_interview_groups
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_groups" ADD CONSTRAINT "dtlms_interview_groups_plan_id_group_code_key" UNIQUE ("plan_id", "group_code");

-- ----------------------------
-- Primary Key structure for table dtlms_interview_groups
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_groups" ADD CONSTRAINT "dtlms_interview_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_interview_schedules
-- ----------------------------
CREATE INDEX "idx_interview_schedule_time" ON "public"."dtlms_interview_schedules" USING btree (
  "starts_at" "pg_catalog"."timestamptz_ops" ASC NULLS LAST,
  "ends_at" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_interview_schedules
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_schedules" ADD CONSTRAINT "dtlms_interview_schedules_admission_ticket_no_key" UNIQUE ("admission_ticket_no");

-- ----------------------------
-- Checks structure for table dtlms_interview_schedules
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_schedules" ADD CONSTRAINT "dtlms_interview_schedules_check" CHECK (ends_at >= starts_at);

-- ----------------------------
-- Primary Key structure for table dtlms_interview_schedules
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_schedules" ADD CONSTRAINT "dtlms_interview_schedules_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_interview_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_scores" ADD CONSTRAINT "dtlms_interview_scores_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_login_logs
-- ----------------------------
ALTER TABLE "public"."dtlms_login_logs" ADD CONSTRAINT "dtlms_login_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_material_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_material_scores" ADD CONSTRAINT "dtlms_material_scores_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_notification_templates
-- ----------------------------
ALTER TABLE "public"."dtlms_notification_templates" ADD CONSTRAINT "dtlms_notification_templates_template_code_key" UNIQUE ("template_code");

-- ----------------------------
-- Primary Key structure for table dtlms_notification_templates
-- ----------------------------
ALTER TABLE "public"."dtlms_notification_templates" ADD CONSTRAINT "dtlms_notification_templates_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_operation_logs
-- ----------------------------
CREATE INDEX "idx_operation_logs_entity" ON "public"."dtlms_operation_logs" USING btree (
  "entity_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "entity_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_operation_logs_module_time" ON "public"."dtlms_operation_logs" USING btree (
  "module_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "created_at" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_operation_logs
-- ----------------------------
ALTER TABLE "public"."dtlms_operation_logs" ADD CONSTRAINT "dtlms_operation_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_outbound_studies
-- ----------------------------
CREATE INDEX "idx_outbound_studies_status" ON "public"."dtlms_outbound_studies" USING btree (
  "approval_status" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ux_dtlms_outbound_studies_business_key" ON "public"."dtlms_outbound_studies" USING btree (
  "business_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table dtlms_outbound_studies
-- ----------------------------
ALTER TABLE "public"."dtlms_outbound_studies" ADD CONSTRAINT "dtlms_outbound_studies_check" CHECK (end_date >= start_date);

-- ----------------------------
-- Primary Key structure for table dtlms_outbound_studies
-- ----------------------------
ALTER TABLE "public"."dtlms_outbound_studies" ADD CONSTRAINT "dtlms_outbound_studies_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_permissions
-- ----------------------------
ALTER TABLE "public"."dtlms_permissions" ADD CONSTRAINT "dtlms_permissions_permission_code_key" UNIQUE ("permission_code");

-- ----------------------------
-- Primary Key structure for table dtlms_permissions
-- ----------------------------
ALTER TABLE "public"."dtlms_permissions" ADD CONSTRAINT "dtlms_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_achievement_records
-- ----------------------------
CREATE INDEX "idx_portal_application_achievement_application" ON "public"."dtlms_portal_application_achievement_records" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "achievement_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_achievement_records
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_achievement_records" ADD CONSTRAINT "dtlms_portal_application_achievement_records_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_attachments
-- ----------------------------
CREATE INDEX "idx_portal_application_attachment_owner" ON "public"."dtlms_portal_application_attachments" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "owner_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "owner_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_attachments
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_attachments" ADD CONSTRAINT "dtlms_portal_application_attachments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_declarations
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_declarations" ADD CONSTRAINT "dtlms_portal_application_declarations_pkey" PRIMARY KEY ("application_id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_education_experiences
-- ----------------------------
CREATE INDEX "idx_portal_application_education_application" ON "public"."dtlms_portal_application_education_experiences" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "sort_order" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table dtlms_portal_application_education_experiences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_education_experiences" ADD CONSTRAINT "chk_portal_application_education_sort_order" CHECK (sort_order > 0);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_education_experiences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_education_experiences" ADD CONSTRAINT "dtlms_portal_application_education_experiences_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_english_proficiencies
-- ----------------------------
CREATE INDEX "idx_portal_application_english_application" ON "public"."dtlms_portal_application_english_proficiencies" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_english_proficiencies
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_english_proficiencies" ADD CONSTRAINT "dtlms_portal_application_english_proficiencies_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_family_members
-- ----------------------------
CREATE INDEX "idx_portal_application_family_application" ON "public"."dtlms_portal_application_family_members" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ux_portal_application_family_parent_unique" ON "public"."dtlms_portal_application_family_members" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "relation_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
) WHERE relation_type::text = ANY (ARRAY['父亲'::character varying, '母亲'::character varying]::text[]);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_family_members
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_family_members" ADD CONSTRAINT "dtlms_portal_application_family_members_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_personal_statements
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_personal_statements" ADD CONSTRAINT "dtlms_portal_application_personal_statements_pkey" PRIMARY KEY ("application_id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_practice_experiences
-- ----------------------------
CREATE INDEX "idx_portal_application_practice_application" ON "public"."dtlms_portal_application_practice_experiences" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_practice_experiences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_practice_experiences" ADD CONSTRAINT "dtlms_portal_application_practice_experiences_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_portal_application_preferences
-- ----------------------------
CREATE INDEX "idx_portal_application_preferences_application" ON "public"."dtlms_portal_application_preferences" USING btree (
  "application_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "preference_order" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_portal_application_preferences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_preferences" ADD CONSTRAINT "uq_portal_application_preferences_order" UNIQUE ("application_id", "preference_order");

-- ----------------------------
-- Checks structure for table dtlms_portal_application_preferences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_preferences" ADD CONSTRAINT "chk_portal_application_preferences_order" CHECK (preference_order > 0);

-- ----------------------------
-- Primary Key structure for table dtlms_portal_application_preferences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_preferences" ADD CONSTRAINT "dtlms_portal_application_preferences_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_portal_student_profiles
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_student_profiles" ADD CONSTRAINT "dtlms_portal_student_profiles_pkey" PRIMARY KEY ("portal_student_id");

-- ----------------------------
-- Uniques structure for table dtlms_portal_students
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_students" ADD CONSTRAINT "dtlms_portal_students_phone_number_key" UNIQUE ("phone_number");
ALTER TABLE "public"."dtlms_portal_students" ADD CONSTRAINT "dtlms_portal_students_email_key" UNIQUE ("email");
ALTER TABLE "public"."dtlms_portal_students" ADD CONSTRAINT "dtlms_portal_students_id_number_key" UNIQUE ("id_number");

-- ----------------------------
-- Primary Key structure for table dtlms_portal_students
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_students" ADD CONSTRAINT "dtlms_portal_students_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_qualification_reviews
-- ----------------------------
ALTER TABLE "public"."dtlms_qualification_reviews" ADD CONSTRAINT "dtlms_qualification_reviews_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_recruitment_applications
-- ----------------------------
CREATE INDEX "idx_applications_plan_status" ON "public"."dtlms_recruitment_applications" USING btree (
  "plan_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "application_status" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_applications_portal_student" ON "public"."dtlms_recruitment_applications" USING btree (
  "portal_student_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_dtlms_recruitment_applications_email" ON "public"."dtlms_recruitment_applications" USING btree (
  "email" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_dtlms_recruitment_applications_phone_number" ON "public"."dtlms_recruitment_applications" USING btree (
  "phone_number" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ux_dtlms_recruitment_applications_business_key" ON "public"."dtlms_recruitment_applications" USING btree (
  "business_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_recruitment_applications
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_applications" ADD CONSTRAINT "dtlms_recruitment_applications_candidate_no_key" UNIQUE ("candidate_no");

-- ----------------------------
-- Primary Key structure for table dtlms_recruitment_applications
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_applications" ADD CONSTRAINT "dtlms_recruitment_applications_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_recruitment_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_plans" ADD CONSTRAINT "dtlms_recruitment_plans_plan_code_key" UNIQUE ("plan_code");

-- ----------------------------
-- Checks structure for table dtlms_recruitment_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_plans" ADD CONSTRAINT "dtlms_recruitment_plans_check" CHECK (end_date >= start_date);

-- ----------------------------
-- Primary Key structure for table dtlms_recruitment_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_plans" ADD CONSTRAINT "dtlms_recruitment_plans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_research_fields
-- ----------------------------
ALTER TABLE "public"."dtlms_research_fields" ADD CONSTRAINT "dtlms_research_fields_field_code_key" UNIQUE ("field_code");

-- ----------------------------
-- Primary Key structure for table dtlms_research_fields
-- ----------------------------
ALTER TABLE "public"."dtlms_research_fields" ADD CONSTRAINT "dtlms_research_fields_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_research_projects
-- ----------------------------
ALTER TABLE "public"."dtlms_research_projects" ADD CONSTRAINT "dtlms_research_projects_project_code_key" UNIQUE ("project_code");

-- ----------------------------
-- Primary Key structure for table dtlms_research_projects
-- ----------------------------
ALTER TABLE "public"."dtlms_research_projects" ADD CONSTRAINT "dtlms_research_projects_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_reviewer_assignments
-- ----------------------------
ALTER TABLE "public"."dtlms_reviewer_assignments" ADD CONSTRAINT "dtlms_reviewer_assignments_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_role_permissions
-- ----------------------------
ALTER TABLE "public"."dtlms_role_permissions" ADD CONSTRAINT "dtlms_role_permissions_role_id_permission_id_key" UNIQUE ("role_id", "permission_id");

-- ----------------------------
-- Primary Key structure for table dtlms_role_permissions
-- ----------------------------
ALTER TABLE "public"."dtlms_role_permissions" ADD CONSTRAINT "dtlms_role_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_roles" ADD CONSTRAINT "dtlms_roles_role_code_key" UNIQUE ("role_code");

-- ----------------------------
-- Primary Key structure for table dtlms_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_roles" ADD CONSTRAINT "dtlms_roles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_audit_policies
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_audit_policies" ADD CONSTRAINT "dtlms_runtime_audit_policies_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_counters
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_counters" ADD CONSTRAINT "dtlms_runtime_counters_pkey" PRIMARY KEY ("counter_name");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_integrations
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_integrations" ADD CONSTRAINT "dtlms_runtime_integrations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_operation_logs
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_operation_logs" ADD CONSTRAINT "dtlms_runtime_operation_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_outbound_studies
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_outbound_studies" ADD CONSTRAINT "dtlms_runtime_outbound_studies_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_portal_students
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_portal_students" ADD CONSTRAINT "dtlms_runtime_portal_students_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_profiles
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_profiles" ADD CONSTRAINT "dtlms_runtime_profiles_pkey" PRIMARY KEY ("username");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_recruitment_applications
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_recruitment_applications" ADD CONSTRAINT "dtlms_runtime_recruitment_applications_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_recruitment_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_recruitment_plans" ADD CONSTRAINT "dtlms_runtime_recruitment_plans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_roles" ADD CONSTRAINT "dtlms_runtime_roles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_scientific_reports
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_scientific_reports" ADD CONSTRAINT "dtlms_runtime_scientific_reports_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_students
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_students" ADD CONSTRAINT "dtlms_runtime_students_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_sync_logs
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_sync_logs" ADD CONSTRAINT "dtlms_runtime_sync_logs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_system_users
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_system_users" ADD CONSTRAINT "dtlms_runtime_system_users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_teams
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_teams" ADD CONSTRAINT "dtlms_runtime_teams_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_theses
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_theses" ADD CONSTRAINT "dtlms_runtime_theses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_thesis_reviews
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_thesis_reviews" ADD CONSTRAINT "dtlms_runtime_thesis_reviews_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_training_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_training_plans" ADD CONSTRAINT "dtlms_runtime_training_plans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_runtime_workflow_tasks
-- ----------------------------
ALTER TABLE "public"."dtlms_runtime_workflow_tasks" ADD CONSTRAINT "dtlms_runtime_workflow_tasks_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_scientific_reports
-- ----------------------------
CREATE INDEX "idx_reports_student_period" ON "public"."dtlms_scientific_reports" USING btree (
  "student_id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "period_label" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ux_dtlms_scientific_reports_business_key" ON "public"."dtlms_scientific_reports" USING btree (
  "business_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table dtlms_scientific_reports
-- ----------------------------
ALTER TABLE "public"."dtlms_scientific_reports" ADD CONSTRAINT "dtlms_scientific_reports_report_status_check" CHECK (report_status::text = ANY (ARRAY['pending'::character varying, 'submitted'::character varying, 'reviewing'::character varying, 'reviewed'::character varying, 'rework'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table dtlms_scientific_reports
-- ----------------------------
ALTER TABLE "public"."dtlms_scientific_reports" ADD CONSTRAINT "dtlms_scientific_reports_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_student_advisor_history
-- ----------------------------
ALTER TABLE "public"."dtlms_student_advisor_history" ADD CONSTRAINT "dtlms_student_advisor_history_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Checks structure for table dtlms_student_team_history
-- ----------------------------
ALTER TABLE "public"."dtlms_student_team_history" ADD CONSTRAINT "dtlms_student_team_history_check" CHECK (end_date IS NULL OR end_date >= start_date);

-- ----------------------------
-- Primary Key structure for table dtlms_student_team_history
-- ----------------------------
ALTER TABLE "public"."dtlms_student_team_history" ADD CONSTRAINT "dtlms_student_team_history_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_students
-- ----------------------------
CREATE INDEX "idx_students_primary_advisor" ON "public"."dtlms_students" USING btree (
  "primary_advisor_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);
CREATE INDEX "idx_students_status" ON "public"."dtlms_students" USING btree (
  "current_status" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_students
-- ----------------------------
ALTER TABLE "public"."dtlms_students" ADD CONSTRAINT "dtlms_students_student_no_key" UNIQUE ("student_no");

-- ----------------------------
-- Primary Key structure for table dtlms_students
-- ----------------------------
ALTER TABLE "public"."dtlms_students" ADD CONSTRAINT "dtlms_students_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_system_configs
-- ----------------------------
ALTER TABLE "public"."dtlms_system_configs" ADD CONSTRAINT "dtlms_system_configs_config_key_key" UNIQUE ("config_key");

-- ----------------------------
-- Primary Key structure for table dtlms_system_configs
-- ----------------------------
ALTER TABLE "public"."dtlms_system_configs" ADD CONSTRAINT "dtlms_system_configs_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_team_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_team_id_advisor_id_key" UNIQUE ("team_id", "advisor_id");

-- ----------------------------
-- Checks structure for table dtlms_team_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_advisor_role_check" CHECK (advisor_role::text = ANY (ARRAY['lead'::character varying, 'member'::character varying, 'co_advisor'::character varying]::text[]));
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_check" CHECK (left_on IS NULL OR joined_on IS NULL OR left_on >= joined_on);

-- ----------------------------
-- Primary Key structure for table dtlms_team_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_teams
-- ----------------------------
ALTER TABLE "public"."dtlms_teams" ADD CONSTRAINT "dtlms_teams_team_code_key" UNIQUE ("team_code");
ALTER TABLE "public"."dtlms_teams" ADD CONSTRAINT "dtlms_teams_team_name_key" UNIQUE ("team_name");

-- ----------------------------
-- Checks structure for table dtlms_teams
-- ----------------------------
ALTER TABLE "public"."dtlms_teams" ADD CONSTRAINT "dtlms_teams_team_status_check" CHECK (team_status::text = ANY (ARRAY['active'::character varying, 'inactive'::character varying, 'planning'::character varying, 'archived'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table dtlms_teams
-- ----------------------------
ALTER TABLE "public"."dtlms_teams" ADD CONSTRAINT "dtlms_teams_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_theses
-- ----------------------------
CREATE INDEX "idx_thesis_status" ON "public"."dtlms_theses" USING btree (
  "thesis_status" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "ux_dtlms_theses_business_key" ON "public"."dtlms_theses" USING btree (
  "business_key" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table dtlms_theses
-- ----------------------------
ALTER TABLE "public"."dtlms_theses" ADD CONSTRAINT "dtlms_theses_plagiarism_rate_check" CHECK (plagiarism_rate IS NULL OR plagiarism_rate <= 100::numeric);

-- ----------------------------
-- Primary Key structure for table dtlms_theses
-- ----------------------------
ALTER TABLE "public"."dtlms_theses" ADD CONSTRAINT "dtlms_theses_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_thesis_reviews
-- ----------------------------
ALTER TABLE "public"."dtlms_thesis_reviews" ADD CONSTRAINT "dtlms_thesis_reviews_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_training_plan_versions
-- ----------------------------
ALTER TABLE "public"."dtlms_training_plan_versions" ADD CONSTRAINT "dtlms_training_plan_versions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table dtlms_training_plans
-- ----------------------------
CREATE INDEX "idx_training_plan_student" ON "public"."dtlms_training_plans" USING btree (
  "student_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Checks structure for table dtlms_training_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_training_plans" ADD CONSTRAINT "dtlms_training_plans_version_no_check" CHECK (version_no::text <> ''::text);
ALTER TABLE "public"."dtlms_training_plans" ADD CONSTRAINT "dtlms_training_plans_plan_status_check" CHECK (plan_status::text = ANY (ARRAY['draft'::character varying, 'pending_confirm'::character varying, 'effective'::character varying, 'archived'::character varying]::text[]));

-- ----------------------------
-- Primary Key structure for table dtlms_training_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_training_plans" ADD CONSTRAINT "dtlms_training_plans_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_user_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_user_roles" ADD CONSTRAINT "dtlms_user_roles_user_id_role_id_key" UNIQUE ("user_id", "role_id");

-- ----------------------------
-- Primary Key structure for table dtlms_user_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_user_roles" ADD CONSTRAINT "dtlms_user_roles_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table dtlms_users
-- ----------------------------
ALTER TABLE "public"."dtlms_users" ADD CONSTRAINT "dtlms_users_username_key" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table dtlms_users
-- ----------------------------
ALTER TABLE "public"."dtlms_users" ADD CONSTRAINT "dtlms_users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table dtlms_wf_de_model
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_de_model" ADD CONSTRAINT "dtlms_wf_de_model_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_hi_actinst
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_hi_actinst_proc_inst" ON "public"."dtlms_wf_hi_actinst" USING btree (
  "proc_inst_id_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_hi_actinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_actinst" ADD CONSTRAINT "dtlms_wf_hi_actinst_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_hi_procinst
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_hi_procinst_business_key" ON "public"."dtlms_wf_hi_procinst" USING btree (
  "business_key_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table dtlms_wf_hi_procinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_procinst" ADD CONSTRAINT "dtlms_wf_hi_procinst_proc_inst_id__key" UNIQUE ("proc_inst_id_");

-- ----------------------------
-- Primary Key structure for table dtlms_wf_hi_procinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_procinst" ADD CONSTRAINT "dtlms_wf_hi_procinst_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_hi_taskinst
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_hi_taskinst_proc_inst" ON "public"."dtlms_wf_hi_taskinst" USING btree (
  "proc_inst_id_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_hi_taskinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_taskinst" ADD CONSTRAINT "dtlms_wf_hi_taskinst_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_hi_varinst
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_hi_varinst_proc_inst" ON "public"."dtlms_wf_hi_varinst" USING btree (
  "proc_inst_id_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_hi_varinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_varinst" ADD CONSTRAINT "dtlms_wf_hi_varinst_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Primary Key structure for table dtlms_wf_re_deployment
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_re_deployment" ADD CONSTRAINT "dtlms_wf_re_deployment_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_re_procdef
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_re_procdef_key" ON "public"."dtlms_wf_re_procdef" USING btree (
  "key_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_re_procdef
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_re_procdef" ADD CONSTRAINT "dtlms_wf_re_procdef_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_ru_execution
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_ru_execution_proc_inst" ON "public"."dtlms_wf_ru_execution" USING btree (
  "proc_inst_id_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_ru_execution
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_execution" ADD CONSTRAINT "dtlms_wf_ru_execution_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Primary Key structure for table dtlms_wf_ru_identitylink
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_identitylink" ADD CONSTRAINT "dtlms_wf_ru_identitylink_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Indexes structure for table dtlms_wf_ru_task
-- ----------------------------
CREATE INDEX "idx_dtlms_wf_ru_task_business_key" ON "public"."dtlms_wf_ru_task" USING btree (
  "business_key_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_dtlms_wf_ru_task_proc_inst" ON "public"."dtlms_wf_ru_task" USING btree (
  "proc_inst_id_" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table dtlms_wf_ru_task
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_task" ADD CONSTRAINT "dtlms_wf_ru_task_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Primary Key structure for table dtlms_wf_ru_variable
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_variable" ADD CONSTRAINT "dtlms_wf_ru_variable_pkey" PRIMARY KEY ("id_");

-- ----------------------------
-- Primary Key structure for table dtlms_written_exam_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_written_exam_scores" ADD CONSTRAINT "dtlms_written_exam_scores_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table dtlms_achievements
-- ----------------------------
ALTER TABLE "public"."dtlms_achievements" ADD CONSTRAINT "dtlms_achievements_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_admission_decisions
-- ----------------------------
ALTER TABLE "public"."dtlms_admission_decisions" ADD CONSTRAINT "dtlms_admission_decisions_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_application_materials
-- ----------------------------
ALTER TABLE "public"."dtlms_application_materials" ADD CONSTRAINT "dtlms_application_materials_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_dict_data
-- ----------------------------
ALTER TABLE "public"."dtlms_dict_data" ADD CONSTRAINT "dtlms_dict_data_dict_type_id_fkey" FOREIGN KEY ("dict_type_id") REFERENCES "public"."dtlms_dict_types" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_interview_groups
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_groups" ADD CONSTRAINT "dtlms_interview_groups_plan_id_fkey" FOREIGN KEY ("plan_id") REFERENCES "public"."dtlms_recruitment_plans" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_interview_schedules
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_schedules" ADD CONSTRAINT "dtlms_interview_schedules_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_interview_schedules" ADD CONSTRAINT "dtlms_interview_schedules_interview_group_id_fkey" FOREIGN KEY ("interview_group_id") REFERENCES "public"."dtlms_interview_groups" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_interview_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_interview_scores" ADD CONSTRAINT "dtlms_interview_scores_schedule_id_fkey" FOREIGN KEY ("schedule_id") REFERENCES "public"."dtlms_interview_schedules" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_material_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_material_scores" ADD CONSTRAINT "dtlms_material_scores_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_material_scores" ADD CONSTRAINT "dtlms_material_scores_reviewer_assignment_id_fkey" FOREIGN KEY ("reviewer_assignment_id") REFERENCES "public"."dtlms_reviewer_assignments" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_outbound_studies
-- ----------------------------
ALTER TABLE "public"."dtlms_outbound_studies" ADD CONSTRAINT "dtlms_outbound_studies_advisor_id_fkey" FOREIGN KEY ("advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_outbound_studies" ADD CONSTRAINT "dtlms_outbound_studies_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_achievement_records
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_achievement_records" ADD CONSTRAINT "dtlms_portal_application_achievement_record_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_attachments
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_attachments" ADD CONSTRAINT "dtlms_portal_application_attachments_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_portal_application_attachments" ADD CONSTRAINT "dtlms_portal_application_attachments_portal_student_id_fkey" FOREIGN KEY ("portal_student_id") REFERENCES "public"."dtlms_portal_students" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_declarations
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_declarations" ADD CONSTRAINT "dtlms_portal_application_declarations_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_education_experiences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_education_experiences" ADD CONSTRAINT "dtlms_portal_application_education_experien_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_english_proficiencies
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_english_proficiencies" ADD CONSTRAINT "dtlms_portal_application_english_proficienc_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_family_members
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_family_members" ADD CONSTRAINT "dtlms_portal_application_family_members_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_personal_statements
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_personal_statements" ADD CONSTRAINT "dtlms_portal_application_personal_statement_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_practice_experiences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_practice_experiences" ADD CONSTRAINT "dtlms_portal_application_practice_experienc_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_application_preferences
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_application_preferences" ADD CONSTRAINT "dtlms_portal_application_preferences_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_student_profiles
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_student_profiles" ADD CONSTRAINT "dtlms_portal_student_profiles_portal_student_id_fkey" FOREIGN KEY ("portal_student_id") REFERENCES "public"."dtlms_portal_students" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_portal_students
-- ----------------------------
ALTER TABLE "public"."dtlms_portal_students" ADD CONSTRAINT "dtlms_portal_students_selected_plan_id_fkey" FOREIGN KEY ("selected_plan_id") REFERENCES "public"."dtlms_recruitment_plans" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_qualification_reviews
-- ----------------------------
ALTER TABLE "public"."dtlms_qualification_reviews" ADD CONSTRAINT "dtlms_qualification_reviews_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_recruitment_applications
-- ----------------------------
ALTER TABLE "public"."dtlms_recruitment_applications" ADD CONSTRAINT "dtlms_recruitment_applications_intended_field_id_fkey" FOREIGN KEY ("intended_field_id") REFERENCES "public"."dtlms_research_fields" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_recruitment_applications" ADD CONSTRAINT "dtlms_recruitment_applications_plan_id_fkey" FOREIGN KEY ("plan_id") REFERENCES "public"."dtlms_recruitment_plans" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_recruitment_applications" ADD CONSTRAINT "dtlms_recruitment_applications_portal_student_id_fkey" FOREIGN KEY ("portal_student_id") REFERENCES "public"."dtlms_portal_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_research_projects
-- ----------------------------
ALTER TABLE "public"."dtlms_research_projects" ADD CONSTRAINT "dtlms_research_projects_principal_advisor_id_fkey" FOREIGN KEY ("principal_advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_reviewer_assignments
-- ----------------------------
ALTER TABLE "public"."dtlms_reviewer_assignments" ADD CONSTRAINT "dtlms_reviewer_assignments_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_role_permissions
-- ----------------------------
ALTER TABLE "public"."dtlms_role_permissions" ADD CONSTRAINT "dtlms_role_permissions_permission_id_fkey" FOREIGN KEY ("permission_id") REFERENCES "public"."dtlms_permissions" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_role_permissions" ADD CONSTRAINT "dtlms_role_permissions_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."dtlms_roles" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_scientific_reports
-- ----------------------------
ALTER TABLE "public"."dtlms_scientific_reports" ADD CONSTRAINT "dtlms_scientific_reports_reviewer_advisor_id_fkey" FOREIGN KEY ("reviewer_advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_scientific_reports" ADD CONSTRAINT "dtlms_scientific_reports_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_scientific_reports" ADD CONSTRAINT "dtlms_scientific_reports_training_plan_id_fkey" FOREIGN KEY ("training_plan_id") REFERENCES "public"."dtlms_training_plans" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_student_advisor_history
-- ----------------------------
ALTER TABLE "public"."dtlms_student_advisor_history" ADD CONSTRAINT "dtlms_student_advisor_history_advisor_id_fkey" FOREIGN KEY ("advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_student_advisor_history" ADD CONSTRAINT "dtlms_student_advisor_history_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_student_team_history
-- ----------------------------
ALTER TABLE "public"."dtlms_student_team_history" ADD CONSTRAINT "dtlms_student_team_history_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_student_team_history" ADD CONSTRAINT "dtlms_student_team_history_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."dtlms_teams" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_students
-- ----------------------------
ALTER TABLE "public"."dtlms_students" ADD CONSTRAINT "dtlms_students_primary_advisor_id_fkey" FOREIGN KEY ("primary_advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_students" ADD CONSTRAINT "dtlms_students_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."dtlms_teams" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_team_advisors
-- ----------------------------
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_advisor_id_fkey" FOREIGN KEY ("advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_team_advisors" ADD CONSTRAINT "dtlms_team_advisors_team_id_fkey" FOREIGN KEY ("team_id") REFERENCES "public"."dtlms_teams" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_teams
-- ----------------------------
ALTER TABLE "public"."dtlms_teams" ADD CONSTRAINT "dtlms_teams_lead_advisor_id_fkey" FOREIGN KEY ("lead_advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_theses
-- ----------------------------
ALTER TABLE "public"."dtlms_theses" ADD CONSTRAINT "dtlms_theses_advisor_id_fkey" FOREIGN KEY ("advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_theses" ADD CONSTRAINT "dtlms_theses_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_thesis_reviews
-- ----------------------------
ALTER TABLE "public"."dtlms_thesis_reviews" ADD CONSTRAINT "dtlms_thesis_reviews_thesis_id_fkey" FOREIGN KEY ("thesis_id") REFERENCES "public"."dtlms_theses" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_training_plan_versions
-- ----------------------------
ALTER TABLE "public"."dtlms_training_plan_versions" ADD CONSTRAINT "dtlms_training_plan_versions_training_plan_id_fkey" FOREIGN KEY ("training_plan_id") REFERENCES "public"."dtlms_training_plans" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_training_plans
-- ----------------------------
ALTER TABLE "public"."dtlms_training_plans" ADD CONSTRAINT "dtlms_training_plans_advisor_id_fkey" FOREIGN KEY ("advisor_id") REFERENCES "public"."dtlms_advisors" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_training_plans" ADD CONSTRAINT "dtlms_training_plans_student_id_fkey" FOREIGN KEY ("student_id") REFERENCES "public"."dtlms_students" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_user_roles
-- ----------------------------
ALTER TABLE "public"."dtlms_user_roles" ADD CONSTRAINT "dtlms_user_roles_role_id_fkey" FOREIGN KEY ("role_id") REFERENCES "public"."dtlms_roles" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_user_roles" ADD CONSTRAINT "dtlms_user_roles_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "public"."dtlms_users" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_hi_actinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_actinst" ADD CONSTRAINT "dtlms_wf_hi_actinst_proc_def_id__fkey" FOREIGN KEY ("proc_def_id_") REFERENCES "public"."dtlms_wf_re_procdef" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_hi_procinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_procinst" ADD CONSTRAINT "dtlms_wf_hi_procinst_proc_def_id__fkey" FOREIGN KEY ("proc_def_id_") REFERENCES "public"."dtlms_wf_re_procdef" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_hi_taskinst
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_hi_taskinst" ADD CONSTRAINT "dtlms_wf_hi_taskinst_proc_def_id__fkey" FOREIGN KEY ("proc_def_id_") REFERENCES "public"."dtlms_wf_re_procdef" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_re_procdef
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_re_procdef" ADD CONSTRAINT "dtlms_wf_re_procdef_deployment_id__fkey" FOREIGN KEY ("deployment_id_") REFERENCES "public"."dtlms_wf_re_deployment" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_ru_execution
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_execution" ADD CONSTRAINT "dtlms_wf_ru_execution_proc_def_id__fkey" FOREIGN KEY ("proc_def_id_") REFERENCES "public"."dtlms_wf_re_procdef" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_ru_task
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_task" ADD CONSTRAINT "dtlms_wf_ru_task_exec_id__fkey" FOREIGN KEY ("exec_id_") REFERENCES "public"."dtlms_wf_ru_execution" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE "public"."dtlms_wf_ru_task" ADD CONSTRAINT "dtlms_wf_ru_task_proc_def_id__fkey" FOREIGN KEY ("proc_def_id_") REFERENCES "public"."dtlms_wf_re_procdef" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_wf_ru_variable
-- ----------------------------
ALTER TABLE "public"."dtlms_wf_ru_variable" ADD CONSTRAINT "dtlms_wf_ru_variable_exec_id__fkey" FOREIGN KEY ("exec_id_") REFERENCES "public"."dtlms_wf_ru_execution" ("id_") ON DELETE NO ACTION ON UPDATE NO ACTION;

-- ----------------------------
-- Foreign Keys structure for table dtlms_written_exam_scores
-- ----------------------------
ALTER TABLE "public"."dtlms_written_exam_scores" ADD CONSTRAINT "dtlms_written_exam_scores_application_id_fkey" FOREIGN KEY ("application_id") REFERENCES "public"."dtlms_recruitment_applications" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION;
