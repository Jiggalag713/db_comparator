/*create databases*/

create database prod;
create database test;

/*
create metadata
---------------------------------------------------------------------------
create tables with differs metadata
---------------------------------------------------------------------------
create tables with same columns, but in test table third column is absent.*/

create table prod.different_columns (
    column1 varchar(10),
    column2 varchar(10),
    column3 varchar(10)
);
create table test.different_columns (
    column1 varchar(10),
    column2 varchar(10)
);

/*create tables with same amount of columns, but one column name in one table differs*/

create table prod.different_column_names (
    column1 varchar(10),
    column2 varchar(10),
    column3 varchar(10)
);
create table test.different_column_names (
    column1 varchar(10),
    column_two varchar(10),
    column3 varchar(10)
);

/*create tables with different data types in one column*/

create table prod.different_types (
    column1 varchar(10),
    column2 varchar(10),
    column3 varchar(10)
);
create table test.different_types (
    column1 int,
    column2 varchar(10),
    column3 varchar(10)
);

/*
create tables with same metadata
*/

create table prod.one_addition_record (
    first_column int,
    second_column varchar(20)
);
create table test.one_addition_record (
    first_column int,
    second_column varchar(20)
);

create table prod.one_differ_record (
    first_column int,
    second_column varchar(20)
);
create table test.one_differ_record (
    first_column int,
    second_column varchar(20)
);

/*
create data
 */

/*insert records into one_addition_record*/
insert into prod.one_addition_record
values
    (1, 'first_record'),
    (2, 'second_record'),
    (3, 'third_record');
insert into test.one_addition_record
values
    (1, 'first_record'),
    (2, 'second_record');

/*insert records into one_differ_record*/
insert into prod.one_differ_record
values
    (1, 'first_record'),
    (2, 'second_record'),
    (3, 'third_record');
insert into test.one_differ_record
values
    (1, 'first_record'),
    (2, 'not_second_record'),
    (3, 'third_record');