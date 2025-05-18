CREATE SCHEMA pizza_runner;
SET search_path = pizza_runner;

DROP TABLE IF EXISTS runners;
CREATE TABLE runners (
  "runner_id" INTEGER,
  "registration_date" DATE
);
INSERT INTO runners
  ("runner_id", "registration_date")
VALUES
  (1, '2021-01-01'),
  (2, '2021-01-03'),
  (3, '2021-01-08'),
  (4, '2021-01-15');


DROP TABLE IF EXISTS customer_orders;
CREATE TABLE customer_orders (
  "order_id" INTEGER,
  "customer_id" INTEGER,
  "pizza_id" INTEGER,
  "exclusions" VARCHAR(4),
  "extras" VARCHAR(4),
  "order_time" TIMESTAMP
);

INSERT INTO customer_orders
  ("order_id", "customer_id", "pizza_id", "exclusions", "extras", "order_time")
VALUES
  ('1', '101', '1', '', '', '2020-01-01 18:05:02'),
  ('2', '101', '1', '', '', '2020-01-01 19:00:52'),
  ('3', '102', '1', '', '', '2020-01-02 23:51:23'),
  ('3', '102', '2', '', NULL, '2020-01-02 23:51:23'),
  ('4', '103', '1', '4', '', '2020-01-04 13:23:46'),
  ('4', '103', '1', '4', '', '2020-01-04 13:23:46'),
  ('4', '103', '2', '4', '', '2020-01-04 13:23:46'),
  ('5', '104', '1', 'null', '1', '2020-01-08 21:00:29'),
  ('6', '101', '2', 'null', 'null', '2020-01-08 21:03:13'),
  ('7', '105', '2', 'null', '1', '2020-01-08 21:20:29'),
  ('8', '102', '1', 'null', 'null', '2020-01-09 23:54:33'),
  ('9', '103', '1', '4', '1, 5', '2020-01-10 11:22:59'),
  ('10', '104', '1', 'null', 'null', '2020-01-11 18:34:49'),
  ('10', '104', '1', '2, 6', '1, 4', '2020-01-11 18:34:49');


DROP TABLE IF EXISTS runner_orders;
CREATE TABLE runner_orders (
  "order_id" INTEGER,
  "runner_id" INTEGER,
  "pickup_time" VARCHAR(19),
  "distance" VARCHAR(7),
  "duration" VARCHAR(10),
  "cancellation" VARCHAR(23)
);

INSERT INTO runner_orders
  ("order_id", "runner_id", "pickup_time", "distance", "duration", "cancellation")
VALUES
  ('1', '1', '2020-01-01 18:15:34', '20km', '32 minutes', ''),
  ('2', '1', '2020-01-01 19:10:54', '20km', '27 minutes', ''),
  ('3', '1', '2020-01-03 00:12:37', '13.4km', '20 mins', NULL),
  ('4', '2', '2020-01-04 13:53:03', '23.4', '40', NULL),
  ('5', '3', '2020-01-08 21:10:57', '10', '15', NULL),
  ('6', '3', 'null', 'null', 'null', 'Restaurant Cancellation'),
  ('7', '2', '2020-01-08 21:30:45', '25km', '25mins', 'null'),
  ('8', '2', '2020-01-10 00:15:02', '23.4 km', '15 minute', 'null'),
  ('9', '2', 'null', 'null', 'null', 'Customer Cancellation'),
  ('10', '1', '2020-01-11 18:50:20', '10km', '10minutes', 'null');


DROP TABLE IF EXISTS pizza_names;
CREATE TABLE pizza_names (
  "pizza_id" INTEGER,
  "pizza_name" TEXT
);
INSERT INTO pizza_names
  ("pizza_id", "pizza_name")
VALUES
  (1, 'Meatlovers'),
  (2, 'Vegetarian');


DROP TABLE IF EXISTS pizza_recipes;
CREATE TABLE pizza_recipes (
  "pizza_id" INTEGER,
  "toppings" TEXT
);
INSERT INTO pizza_recipes
  ("pizza_id", "toppings")
VALUES
  (1, '1, 2, 3, 4, 5, 6, 8, 10'),
  (2, '4, 6, 7, 9, 11, 12');


DROP TABLE IF EXISTS pizza_toppings;
CREATE TABLE pizza_toppings (
  "topping_id" INTEGER,
  "topping_name" TEXT
);
INSERT INTO pizza_toppings
  ("topping_id", "topping_name")
VALUES
  (1, 'Bacon'),
  (2, 'BBQ Sauce'),
  (3, 'Beef'),
  (4, 'Cheese'),
  (5, 'Chicken'),
  (6, 'Mushrooms'),
  (7, 'Onions'),
  (8, 'Pepperoni'),
  (9, 'Peppers'),
  (10, 'Salami'),
  (11, 'Tomatoes'),
  (12, 'Tomato Sauce');


 select count(*) from customer_orders;
    
    select count(DISTINCT order_id) as unique_customer from  customer_orders;
    
    
    -- How many successful orders were delivered by each runner?
    
    select count(order_id),runner_id from runner_orders where duration!='' group by runner_id;
    
    
    -- How many of each type of pizza was delivered?
    select  p.pizza_name, 
  COUNT(c.pizza_id) AS delivered_pizza_count
FROM customer_orders AS c
join runner_orders as r on c.order_id=r.order_id
JOIN pizza_names AS p
  ON c.pizza_id = p.pizza_id
WHERE r.distance != ''
GROUP BY p.pizza_name;



-- How many Vegetarian and Meatlovers were ordered by each customer?

select c.customer_id,p.pizza_name,count(c.pizza_id) from customer_orders as c join pizza_names as p on p.pizza_id=c.pizza_id group by c.customer_id, p.pizza_name order by c.customer_id;


-- What was the maximum number of pizzas delivered in a single order?

with pizza_count_cte as (
  select count(c.pizza_id) as max_pizza_per_order,c.order_id
  from customer_orders as c join runner_orders as r
  on r.order_id=c.order_id where r.distance!=''
  group by c.order_id
)
select max(max_pizza_per_order) as max_pizza from pizza_count_cte;


-- For each customer, how many delivered pizzas had at least 1 change and how many had no changes?
UPDATE customer_orders 
SET exclusions = '', extras = '' 
WHERE exclusions IS NULL OR extras IS NULL;

select c.customer_id,
sum(case 
    when c.exclusions!='' or c.extras!='' then 1
    else 0
    end)as has_change,
    sum( case when c.exclusions='' and c.extras='' then 1
    else 0
    end)no_Change
    from customer_orders as c join runner_orders as r
on c.order_id=r.order_id
group by c.customer_id
order by c.customer_id;



-- How many pizzas were delivered that had both exclusions and extras?

SELECT  
  SUM(
    CASE WHEN exclusions IS NOT NULL AND extras IS NOT NULL THEN 1
    ELSE 0
    END) AS pizza_count_w_exclusions_extras
    from customer_orders as c join runner_orders as r on r.order_id=c.order_id
  WHERE r.distance !='';
   
   -- What was the total volume of pizzas ordered for each hour of the day?
   
  
   SELECT 
    EXTRACT(HOUR FROM order_time) AS order_hour,
    COUNT(*) AS total_pizzas
FROM 
    customer_orders
GROUP BY 
    order_hour
ORDER BY 
    order_hour;
    
    
    -- What was the volume of orders for each day of the week?

   
   
   
   
   