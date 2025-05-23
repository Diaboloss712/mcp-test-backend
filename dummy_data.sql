INSERT INTO categories (id, name, parent_id) VALUES (1, 'Math', NULL);
INSERT INTO categories (id, name, parent_id) VALUES (2, 'Science', NULL);
INSERT INTO categories (id, name, parent_id) VALUES (3, 'History', NULL);
INSERT INTO categories (id, name, parent_id) VALUES (4, 'Algebra', 1);
INSERT INTO categories (id, name, parent_id) VALUES (5, 'Geometry', 1);
INSERT INTO categories (id, name, parent_id) VALUES (6, 'Calculus', 1);
INSERT INTO categories (id, name, parent_id) VALUES (7, 'Biology', 2);
INSERT INTO categories (id, name, parent_id) VALUES (8, 'Chemistry', 2);
INSERT INTO categories (id, name, parent_id) VALUES (9, 'Physics', 2);
INSERT INTO categories (id, name, parent_id) VALUES (10, 'Ancient', 3);
INSERT INTO categories (id, name, parent_id) VALUES (11, 'Medieval', 3);
INSERT INTO categories (id, name, parent_id) VALUES (12, 'Modern', 3);
INSERT INTO categories (id, name, parent_id) VALUES (13, 'Linear Equations', 4);
INSERT INTO categories (id, name, parent_id) VALUES (14, 'Quadratic Equations', 4);
INSERT INTO categories (id, name, parent_id) VALUES (15, 'Polynomials', 4);
INSERT INTO categories (id, name, parent_id) VALUES (16, 'Triangles', 5);
INSERT INTO categories (id, name, parent_id) VALUES (17, 'Circles', 5);
INSERT INTO categories (id, name, parent_id) VALUES (18, 'Angles', 5);
INSERT INTO categories (id, name, parent_id) VALUES (19, 'Limits', 6);
INSERT INTO categories (id, name, parent_id) VALUES (20, 'Derivatives', 6);
INSERT INTO categories (id, name, parent_id) VALUES (21, 'Integrals', 6);
INSERT INTO categories (id, name, parent_id) VALUES (22, 'Cell Structure', 7);
INSERT INTO categories (id, name, parent_id) VALUES (23, 'Genetics', 7);
INSERT INTO categories (id, name, parent_id) VALUES (24, 'Evolution', 7);
INSERT INTO categories (id, name, parent_id) VALUES (25, 'Atoms', 8);
INSERT INTO categories (id, name, parent_id) VALUES (26, 'Bonds', 8);
INSERT INTO categories (id, name, parent_id) VALUES (27, 'Reactions', 8);
INSERT INTO categories (id, name, parent_id) VALUES (28, 'Motion', 9);
INSERT INTO categories (id, name, parent_id) VALUES (29, 'Forces', 9);
INSERT INTO categories (id, name, parent_id) VALUES (30, 'Energy', 9);
INSERT INTO categories (id, name, parent_id) VALUES (31, 'Mesopotamia', 10);
INSERT INTO categories (id, name, parent_id) VALUES (32, 'Egypt', 10);
INSERT INTO categories (id, name, parent_id) VALUES (33, 'Greece', 10);
INSERT INTO categories (id, name, parent_id) VALUES (34, 'Feudalism', 11);
INSERT INTO categories (id, name, parent_id) VALUES (35, 'Crusades', 11);
INSERT INTO categories (id, name, parent_id) VALUES (36, 'Plague', 11);
INSERT INTO categories (id, name, parent_id) VALUES (37, 'Revolutions', 12);
INSERT INTO categories (id, name, parent_id) VALUES (38, 'World Wars', 12);
INSERT INTO categories (id, name, parent_id) VALUES (39, 'Cold War', 12);
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Linear Equations Q1', 'This is a sample question 1 about Linear Equations.', 'select', 'Answer 1', 13, '2025-05-08T07:12:47.812930');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Linear Equations Q2', 'This is a sample question 2 about Linear Equations.', 'select', 'Answer 2', 13, '2025-05-08T07:12:47.812942');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Linear Equations Q3', 'This is a sample question 3 about Linear Equations.', 'select', 'Answer 3', 13, '2025-05-08T07:12:47.812944');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Linear Equations Q4', 'This is a sample question 4 about Linear Equations.', 'select', 'Answer 4', 13, '2025-05-08T07:12:47.812947');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Linear Equations Q5', 'This is a sample question 5 about Linear Equations.', 'select', 'Answer 5', 13, '2025-05-08T07:12:47.812949');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Quadratic Equations Q1', 'This is a sample question 1 about Quadratic Equations.', 'select', 'Answer 1', 14, '2025-05-08T07:12:47.812952');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Quadratic Equations Q2', 'This is a sample question 2 about Quadratic Equations.', 'select', 'Answer 2', 14, '2025-05-08T07:12:47.812956');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Quadratic Equations Q3', 'This is a sample question 3 about Quadratic Equations.', 'select', 'Answer 3', 14, '2025-05-08T07:12:47.812959');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Quadratic Equations Q4', 'This is a sample question 4 about Quadratic Equations.', 'select', 'Answer 4', 14, '2025-05-08T07:12:47.812961');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Quadratic Equations Q5', 'This is a sample question 5 about Quadratic Equations.', 'select', 'Answer 5', 14, '2025-05-08T07:12:47.812964');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Polynomials Q1', 'This is a sample question 1 about Polynomials.', 'select', 'Answer 1', 15, '2025-05-08T07:12:47.812968');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Polynomials Q2', 'This is a sample question 2 about Polynomials.', 'select', 'Answer 2', 15, '2025-05-08T07:12:47.812970');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Polynomials Q3', 'This is a sample question 3 about Polynomials.', 'select', 'Answer 3', 15, '2025-05-08T07:12:47.812973');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Polynomials Q4', 'This is a sample question 4 about Polynomials.', 'select', 'Answer 4', 15, '2025-05-08T07:12:47.812975');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Polynomials Q5', 'This is a sample question 5 about Polynomials.', 'select', 'Answer 5', 15, '2025-05-08T07:12:47.812977');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Triangles Q1', 'This is a sample question 1 about Triangles.', 'select', 'Answer 1', 16, '2025-05-08T07:12:47.812981');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Triangles Q2', 'This is a sample question 2 about Triangles.', 'select', 'Answer 2', 16, '2025-05-08T07:12:47.812983');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Triangles Q3', 'This is a sample question 3 about Triangles.', 'select', 'Answer 3', 16, '2025-05-08T07:12:47.812986');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Triangles Q4', 'This is a sample question 4 about Triangles.', 'select', 'Answer 4', 16, '2025-05-08T07:12:47.812988');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Triangles Q5', 'This is a sample question 5 about Triangles.', 'select', 'Answer 5', 16, '2025-05-08T07:12:47.812990');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Circles Q1', 'This is a sample question 1 about Circles.', 'select', 'Answer 1', 17, '2025-05-08T07:12:47.812993');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Circles Q2', 'This is a sample question 2 about Circles.', 'select', 'Answer 2', 17, '2025-05-08T07:12:47.812995');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Circles Q3', 'This is a sample question 3 about Circles.', 'select', 'Answer 3', 17, '2025-05-08T07:12:47.812997');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Circles Q4', 'This is a sample question 4 about Circles.', 'select', 'Answer 4', 17, '2025-05-08T07:12:47.812999');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Circles Q5', 'This is a sample question 5 about Circles.', 'select', 'Answer 5', 17, '2025-05-08T07:12:47.813002');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Angles Q1', 'This is a sample question 1 about Angles.', 'select', 'Answer 1', 18, '2025-05-08T07:12:47.813005');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Angles Q2', 'This is a sample question 2 about Angles.', 'select', 'Answer 2', 18, '2025-05-08T07:12:47.813007');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Angles Q3', 'This is a sample question 3 about Angles.', 'select', 'Answer 3', 18, '2025-05-08T07:12:47.813009');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Angles Q4', 'This is a sample question 4 about Angles.', 'select', 'Answer 4', 18, '2025-05-08T07:12:47.813012');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Angles Q5', 'This is a sample question 5 about Angles.', 'select', 'Answer 5', 18, '2025-05-08T07:12:47.813014');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Limits Q1', 'This is a sample question 1 about Limits.', 'select', 'Answer 1', 19, '2025-05-08T07:12:47.813017');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Limits Q2', 'This is a sample question 2 about Limits.', 'select', 'Answer 2', 19, '2025-05-08T07:12:47.813019');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Limits Q3', 'This is a sample question 3 about Limits.', 'select', 'Answer 3', 19, '2025-05-08T07:12:47.813021');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Limits Q4', 'This is a sample question 4 about Limits.', 'select', 'Answer 4', 19, '2025-05-08T07:12:47.813024');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Limits Q5', 'This is a sample question 5 about Limits.', 'select', 'Answer 5', 19, '2025-05-08T07:12:47.813026');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Derivatives Q1', 'This is a sample question 1 about Derivatives.', 'select', 'Answer 1', 20, '2025-05-08T07:12:47.813029');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Derivatives Q2', 'This is a sample question 2 about Derivatives.', 'select', 'Answer 2', 20, '2025-05-08T07:12:47.813031');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Derivatives Q3', 'This is a sample question 3 about Derivatives.', 'select', 'Answer 3', 20, '2025-05-08T07:12:47.813033');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Derivatives Q4', 'This is a sample question 4 about Derivatives.', 'select', 'Answer 4', 20, '2025-05-08T07:12:47.813035');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Derivatives Q5', 'This is a sample question 5 about Derivatives.', 'select', 'Answer 5', 20, '2025-05-08T07:12:47.813038');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Integrals Q1', 'This is a sample question 1 about Integrals.', 'select', 'Answer 1', 21, '2025-05-08T07:12:47.813040');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Integrals Q2', 'This is a sample question 2 about Integrals.', 'select', 'Answer 2', 21, '2025-05-08T07:12:47.813043');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Integrals Q3', 'This is a sample question 3 about Integrals.', 'select', 'Answer 3', 21, '2025-05-08T07:12:47.813045');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Integrals Q4', 'This is a sample question 4 about Integrals.', 'select', 'Answer 4', 21, '2025-05-08T07:12:47.813047');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Integrals Q5', 'This is a sample question 5 about Integrals.', 'select', 'Answer 5', 21, '2025-05-08T07:12:47.813049');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cell Structure Q1', 'This is a sample question 1 about Cell Structure.', 'select', 'Answer 1', 22, '2025-05-08T07:12:47.813053');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cell Structure Q2', 'This is a sample question 2 about Cell Structure.', 'select', 'Answer 2', 22, '2025-05-08T07:12:47.813055');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cell Structure Q3', 'This is a sample question 3 about Cell Structure.', 'select', 'Answer 3', 22, '2025-05-08T07:12:47.813058');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cell Structure Q4', 'This is a sample question 4 about Cell Structure.', 'select', 'Answer 4', 22, '2025-05-08T07:12:47.813060');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cell Structure Q5', 'This is a sample question 5 about Cell Structure.', 'select', 'Answer 5', 22, '2025-05-08T07:12:47.813063');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Genetics Q1', 'This is a sample question 1 about Genetics.', 'select', 'Answer 1', 23, '2025-05-08T07:12:47.813066');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Genetics Q2', 'This is a sample question 2 about Genetics.', 'select', 'Answer 2', 23, '2025-05-08T07:12:47.813068');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Genetics Q3', 'This is a sample question 3 about Genetics.', 'select', 'Answer 3', 23, '2025-05-08T07:12:47.813070');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Genetics Q4', 'This is a sample question 4 about Genetics.', 'select', 'Answer 4', 23, '2025-05-08T07:12:47.813072');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Genetics Q5', 'This is a sample question 5 about Genetics.', 'select', 'Answer 5', 23, '2025-05-08T07:12:47.813074');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Evolution Q1', 'This is a sample question 1 about Evolution.', 'select', 'Answer 1', 24, '2025-05-08T07:12:47.813077');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Evolution Q2', 'This is a sample question 2 about Evolution.', 'select', 'Answer 2', 24, '2025-05-08T07:12:47.813081');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Evolution Q3', 'This is a sample question 3 about Evolution.', 'select', 'Answer 3', 24, '2025-05-08T07:12:47.813083');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Evolution Q4', 'This is a sample question 4 about Evolution.', 'select', 'Answer 4', 24, '2025-05-08T07:12:47.813086');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Evolution Q5', 'This is a sample question 5 about Evolution.', 'select', 'Answer 5', 24, '2025-05-08T07:12:47.813088');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Atoms Q1', 'This is a sample question 1 about Atoms.', 'select', 'Answer 1', 25, '2025-05-08T07:12:47.813091');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Atoms Q2', 'This is a sample question 2 about Atoms.', 'select', 'Answer 2', 25, '2025-05-08T07:12:47.813093');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Atoms Q3', 'This is a sample question 3 about Atoms.', 'select', 'Answer 3', 25, '2025-05-08T07:12:47.813096');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Atoms Q4', 'This is a sample question 4 about Atoms.', 'select', 'Answer 4', 25, '2025-05-08T07:12:47.813098');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Atoms Q5', 'This is a sample question 5 about Atoms.', 'select', 'Answer 5', 25, '2025-05-08T07:12:47.813100');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Bonds Q1', 'This is a sample question 1 about Bonds.', 'select', 'Answer 1', 26, '2025-05-08T07:12:47.813103');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Bonds Q2', 'This is a sample question 2 about Bonds.', 'select', 'Answer 2', 26, '2025-05-08T07:12:47.813106');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Bonds Q3', 'This is a sample question 3 about Bonds.', 'select', 'Answer 3', 26, '2025-05-08T07:12:47.813108');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Bonds Q4', 'This is a sample question 4 about Bonds.', 'select', 'Answer 4', 26, '2025-05-08T07:12:47.813110');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Bonds Q5', 'This is a sample question 5 about Bonds.', 'select', 'Answer 5', 26, '2025-05-08T07:12:47.813117');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Reactions Q1', 'This is a sample question 1 about Reactions.', 'select', 'Answer 1', 27, '2025-05-08T07:12:47.813120');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Reactions Q2', 'This is a sample question 2 about Reactions.', 'select', 'Answer 2', 27, '2025-05-08T07:12:47.813122');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Reactions Q3', 'This is a sample question 3 about Reactions.', 'select', 'Answer 3', 27, '2025-05-08T07:12:47.813124');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Reactions Q4', 'This is a sample question 4 about Reactions.', 'select', 'Answer 4', 27, '2025-05-08T07:12:47.813126');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Reactions Q5', 'This is a sample question 5 about Reactions.', 'select', 'Answer 5', 27, '2025-05-08T07:12:47.813129');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Motion Q1', 'This is a sample question 1 about Motion.', 'select', 'Answer 1', 28, '2025-05-08T07:12:47.813132');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Motion Q2', 'This is a sample question 2 about Motion.', 'select', 'Answer 2', 28, '2025-05-08T07:12:47.813134');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Motion Q3', 'This is a sample question 3 about Motion.', 'select', 'Answer 3', 28, '2025-05-08T07:12:47.813136');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Motion Q4', 'This is a sample question 4 about Motion.', 'select', 'Answer 4', 28, '2025-05-08T07:12:47.813138');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Motion Q5', 'This is a sample question 5 about Motion.', 'select', 'Answer 5', 28, '2025-05-08T07:12:47.813140');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Forces Q1', 'This is a sample question 1 about Forces.', 'select', 'Answer 1', 29, '2025-05-08T07:12:47.813143');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Forces Q2', 'This is a sample question 2 about Forces.', 'select', 'Answer 2', 29, '2025-05-08T07:12:47.813145');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Forces Q3', 'This is a sample question 3 about Forces.', 'select', 'Answer 3', 29, '2025-05-08T07:12:47.813148');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Forces Q4', 'This is a sample question 4 about Forces.', 'select', 'Answer 4', 29, '2025-05-08T07:12:47.813150');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Forces Q5', 'This is a sample question 5 about Forces.', 'select', 'Answer 5', 29, '2025-05-08T07:12:47.813152');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Energy Q1', 'This is a sample question 1 about Energy.', 'select', 'Answer 1', 30, '2025-05-08T07:12:47.813155');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Energy Q2', 'This is a sample question 2 about Energy.', 'select', 'Answer 2', 30, '2025-05-08T07:12:47.813157');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Energy Q3', 'This is a sample question 3 about Energy.', 'select', 'Answer 3', 30, '2025-05-08T07:12:47.813159');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Energy Q4', 'This is a sample question 4 about Energy.', 'select', 'Answer 4', 30, '2025-05-08T07:12:47.813161');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Energy Q5', 'This is a sample question 5 about Energy.', 'select', 'Answer 5', 30, '2025-05-08T07:12:47.813163');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Mesopotamia Q1', 'This is a sample question 1 about Mesopotamia.', 'select', 'Answer 1', 31, '2025-05-08T07:12:47.813167');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Mesopotamia Q2', 'This is a sample question 2 about Mesopotamia.', 'select', 'Answer 2', 31, '2025-05-08T07:12:47.813169');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Mesopotamia Q3', 'This is a sample question 3 about Mesopotamia.', 'select', 'Answer 3', 31, '2025-05-08T07:12:47.813171');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Mesopotamia Q4', 'This is a sample question 4 about Mesopotamia.', 'select', 'Answer 4', 31, '2025-05-08T07:12:47.813173');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Mesopotamia Q5', 'This is a sample question 5 about Mesopotamia.', 'select', 'Answer 5', 31, '2025-05-08T07:12:47.813175');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Egypt Q1', 'This is a sample question 1 about Egypt.', 'select', 'Answer 1', 32, '2025-05-08T07:12:47.813178');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Egypt Q2', 'This is a sample question 2 about Egypt.', 'select', 'Answer 2', 32, '2025-05-08T07:12:47.813180');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Egypt Q3', 'This is a sample question 3 about Egypt.', 'select', 'Answer 3', 32, '2025-05-08T07:12:47.813183');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Egypt Q4', 'This is a sample question 4 about Egypt.', 'select', 'Answer 4', 32, '2025-05-08T07:12:47.813185');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Egypt Q5', 'This is a sample question 5 about Egypt.', 'select', 'Answer 5', 32, '2025-05-08T07:12:47.813187');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Greece Q1', 'This is a sample question 1 about Greece.', 'select', 'Answer 1', 33, '2025-05-08T07:12:47.813190');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Greece Q2', 'This is a sample question 2 about Greece.', 'select', 'Answer 2', 33, '2025-05-08T07:12:47.813196');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Greece Q3', 'This is a sample question 3 about Greece.', 'select', 'Answer 3', 33, '2025-05-08T07:12:47.813198');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Greece Q4', 'This is a sample question 4 about Greece.', 'select', 'Answer 4', 33, '2025-05-08T07:12:47.813200');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Greece Q5', 'This is a sample question 5 about Greece.', 'select', 'Answer 5', 33, '2025-05-08T07:12:47.813202');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Feudalism Q1', 'This is a sample question 1 about Feudalism.', 'select', 'Answer 1', 34, '2025-05-08T07:12:47.813205');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Feudalism Q2', 'This is a sample question 2 about Feudalism.', 'select', 'Answer 2', 34, '2025-05-08T07:12:47.813208');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Feudalism Q3', 'This is a sample question 3 about Feudalism.', 'select', 'Answer 3', 34, '2025-05-08T07:12:47.813210');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Feudalism Q4', 'This is a sample question 4 about Feudalism.', 'select', 'Answer 4', 34, '2025-05-08T07:12:47.813213');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Feudalism Q5', 'This is a sample question 5 about Feudalism.', 'select', 'Answer 5', 34, '2025-05-08T07:12:47.813215');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Crusades Q1', 'This is a sample question 1 about Crusades.', 'select', 'Answer 1', 35, '2025-05-08T07:12:47.813218');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Crusades Q2', 'This is a sample question 2 about Crusades.', 'select', 'Answer 2', 35, '2025-05-08T07:12:47.813220');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Crusades Q3', 'This is a sample question 3 about Crusades.', 'select', 'Answer 3', 35, '2025-05-08T07:12:47.813222');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Crusades Q4', 'This is a sample question 4 about Crusades.', 'select', 'Answer 4', 35, '2025-05-08T07:12:47.813224');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Crusades Q5', 'This is a sample question 5 about Crusades.', 'select', 'Answer 5', 35, '2025-05-08T07:12:47.813226');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Plague Q1', 'This is a sample question 1 about Plague.', 'select', 'Answer 1', 36, '2025-05-08T07:12:47.813229');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Plague Q2', 'This is a sample question 2 about Plague.', 'select', 'Answer 2', 36, '2025-05-08T07:12:47.813231');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Plague Q3', 'This is a sample question 3 about Plague.', 'select', 'Answer 3', 36, '2025-05-08T07:12:47.813233');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Plague Q4', 'This is a sample question 4 about Plague.', 'select', 'Answer 4', 36, '2025-05-08T07:12:47.813235');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Plague Q5', 'This is a sample question 5 about Plague.', 'select', 'Answer 5', 36, '2025-05-08T07:12:47.813238');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Revolutions Q1', 'This is a sample question 1 about Revolutions.', 'select', 'Answer 1', 37, '2025-05-08T07:12:47.813241');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Revolutions Q2', 'This is a sample question 2 about Revolutions.', 'select', 'Answer 2', 37, '2025-05-08T07:12:47.813243');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Revolutions Q3', 'This is a sample question 3 about Revolutions.', 'select', 'Answer 3', 37, '2025-05-08T07:12:47.813245');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Revolutions Q4', 'This is a sample question 4 about Revolutions.', 'select', 'Answer 4', 37, '2025-05-08T07:12:47.813247');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Revolutions Q5', 'This is a sample question 5 about Revolutions.', 'select', 'Answer 5', 37, '2025-05-08T07:12:47.813249');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('World Wars Q1', 'This is a sample question 1 about World Wars.', 'select', 'Answer 1', 38, '2025-05-08T07:12:47.813252');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('World Wars Q2', 'This is a sample question 2 about World Wars.', 'select', 'Answer 2', 38, '2025-05-08T07:12:47.813254');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('World Wars Q3', 'This is a sample question 3 about World Wars.', 'select', 'Answer 3', 38, '2025-05-08T07:12:47.813256');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('World Wars Q4', 'This is a sample question 4 about World Wars.', 'select', 'Answer 4', 38, '2025-05-08T07:12:47.813258');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('World Wars Q5', 'This is a sample question 5 about World Wars.', 'select', 'Answer 5', 38, '2025-05-08T07:12:47.813261');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cold War Q1', 'This is a sample question 1 about Cold War.', 'select', 'Answer 1', 39, '2025-05-08T07:12:47.813264');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cold War Q2', 'This is a sample question 2 about Cold War.', 'select', 'Answer 2', 39, '2025-05-08T07:12:47.813267');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cold War Q3', 'This is a sample question 3 about Cold War.', 'select', 'Answer 3', 39, '2025-05-08T07:12:47.813269');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cold War Q4', 'This is a sample question 4 about Cold War.', 'select', 'Answer 4', 39, '2025-05-08T07:12:47.813272');
INSERT INTO problems (title, content, type, answer, category_id, created_at) VALUES ('Cold War Q5', 'This is a sample question 5 about Cold War.', 'select', 'Answer 5', 39, '2025-05-08T07:12:47.813274');