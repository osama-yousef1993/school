CREATE TABLE `User` (
  `id` varchar(36) PRIMARY KEY,
  `first_name` varchar(300),
  `last_name` varchar(300),
  `email` varchar(300) UNIQUE,
  `password` varchar(300),
  `type` varchar(300),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Teacher` (
  `id` varchar(36) PRIMARY KEY,
  `first_name` varchar(300),
  `last_name` varchar(300),
  `email` varchar(300) UNIQUE,
  `teacher_id` varchar(36) UNIQUE,
  `password` varchar(300),
  `type` varchar(300),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Student` (
  `id` varchar(36) PRIMARY KEY,
  `first_name` varchar(300),
  `last_name` varchar(300),
  `student_id` varchar(300) UNIQUE,
  `class_id` varchar(36),
  `subject_id` varchar(36),
  `teacher_id` varchar(36),
  `parent_id` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Class` (
  `id` varchar(36) PRIMARY KEY,
  `name` varchar(300),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Subject` (
  `id` varchar(36) PRIMARY KEY,
  `name` varchar(300),
  `class_id` varchar(36),
  `teacher_id` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Terms` (
  `id` varchar(36) PRIMARY KEY,
  `name` varchar(300),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Marks` (
  `id` varchar(36) PRIMARY KEY,
  `participation` float,
  `home_work` float,
  `class_work` float,
  `quiz` float,
  `mid_term` float,
  `final` float,
  `student_id` varchar(36),
  `teacher_id` varchar(36),
  `terms_id` varchar(36),
  `class_id` varchar(36),
  `subject_id` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `Comments` (
  `id` varchar(36) PRIMARY KEY,
  `teacher_id` varchar(36),
  `parent_id` varchar(36),
  `student_id` varchar(36),
  `subject_id` varchar(36),
  `comments` varchar(300),
  `date_added` timestamp,
  `from_who` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE TABLE `student_subjects` (
  `id` varchar(36) PRIMARY KEY,
  `student_id` varchar(36),
  `subject_id` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);
CREATE TABLE `term_marks` (
  `id` varchar(36) PRIMARY KEY,
  `term_id` varchar(36),
  `mark_id` varchar(36),
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `update_at` timestamp
);

CREATE INDEX `User_index_0` ON `User` (`id`);

CREATE INDEX `User_index_1` ON `User` (`first_name`);

CREATE INDEX `User_index_2` ON `User` (`last_name`);

CREATE INDEX `User_index_3` ON `User` (`email`);

CREATE INDEX `Teacher_index_4` ON `Teacher` (`id`);

CREATE INDEX `Teacher_index_5` ON `Teacher` (`first_name`);

CREATE INDEX `Teacher_index_6` ON `Teacher` (`last_name`);

CREATE INDEX `Teacher_index_7` ON `Teacher` (`email`);

CREATE INDEX `Teacher_index_8` ON `Teacher` (`teacher_id`);

CREATE INDEX `Student_index_9` ON `Student` (`id`);

CREATE INDEX `Student_index_10` ON `Student` (`teacher_id`);

CREATE INDEX `Student_index_11` ON `Student` (`class_id`);

CREATE INDEX `Student_index_12` ON `Student` (`first_name`);

CREATE INDEX `Student_index_13` ON `Student` (`last_name`);

CREATE INDEX `Student_index_14` ON `Student` (`student_id`);

CREATE INDEX `Student_index_15` ON `Student` (`parent_id`);

CREATE INDEX `Class_index_16` ON `Class` (`id`);

CREATE INDEX `Class_index_17` ON `Class` (`name`);

CREATE INDEX `Subject_index_18` ON `Subject` (`id`);

CREATE INDEX `Subject_index_19` ON `Subject` (`name`);

CREATE INDEX `Subject_index_20` ON `Subject` (`teacher_id`);

CREATE INDEX `Subject_index_21` ON `Subject` (`class_id`);

CREATE INDEX `Terms_index_22` ON `Terms` (`id`);

CREATE INDEX `Terms_index_23` ON `Terms` (`name`);

CREATE INDEX `Marks_index_24` ON `Marks` (`id`);

CREATE INDEX `Marks_index_25` ON `Marks` (`terms_id`);

CREATE INDEX `Marks_index_26` ON `Marks` (`teacher_id`);

CREATE INDEX `Marks_index_27` ON `Marks` (`student_id`);

CREATE INDEX `Marks_index_28` ON `Marks` (`class_id`);

CREATE INDEX `Marks_index_29` ON `Marks` (`subject_id`);

CREATE INDEX `Comments_index_30` ON `Comments` (`id`);

CREATE INDEX `Comments_index_31` ON `Comments` (`parent_id`);

CREATE INDEX `Comments_index_32` ON `Comments` (`teacher_id`);

CREATE INDEX `Comments_index_33` ON `Comments` (`student_id`);

ALTER TABLE `Student` ADD FOREIGN KEY (`class_id`) REFERENCES `Class` (`id`);

ALTER TABLE `Student` ADD FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`);

ALTER TABLE `Student` ADD FOREIGN KEY (`parent_id`) REFERENCES `User` (`id`);

ALTER TABLE `Subject` ADD FOREIGN KEY (`class_id`) REFERENCES `Class` (`id`);

ALTER TABLE `Subject` ADD FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`);

ALTER TABLE `Marks` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`);

ALTER TABLE `Marks` ADD FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`);

ALTER TABLE `Marks` ADD FOREIGN KEY (`terms_id`) REFERENCES `Terms` (`id`);

ALTER TABLE `Marks` ADD FOREIGN KEY (`class_id`) REFERENCES `Class` (`id`);

ALTER TABLE `Marks` ADD FOREIGN KEY (`subject_id`) REFERENCES `Subject` (`id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`teacher_id`) REFERENCES `Teacher` (`id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`parent_id`) REFERENCES `User` (`id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`);

ALTER TABLE `Comments` ADD FOREIGN KEY (`subject_id`) REFERENCES `Subject` (`id`);

ALTER TABLE `student_subjects` ADD FOREIGN KEY (`student_id`) REFERENCES `Student` (`id`);

ALTER TABLE `student_subjects` ADD FOREIGN KEY (`subject_id`) REFERENCES `Subject` (`id`);

ALTER TABLE `term_marks` ADD FOREIGN KEY (`term_id`) REFERENCES `Terms` (`id`);

ALTER TABLE `term_marks` ADD FOREIGN KEY (`mark_id`) REFERENCES `Marks` (`id`);
