
WITH tb_rf AS(
SELECT 
    t1.customer_unique_id AS idCustomer,
    CAST(julianday('2018-10-31') - MAX(julianday(DATE(t2.order_approved_at))) AS INTEGER) AS recenciaDias,
    COUNT(DATE(t2.order_approved_at)) AS frequenciaCompras
FROM olist_customers_dataset AS t1
LEFT JOIN 
    olist_orders_dataset AS t2
    ON t1.customer_id = t2.customer_id
GROUP BY idCustomer),

tb_val AS(
SELECT 
    t3.customer_unique_id AS idCustomer,
    SUM(t1.payment_value) AS valorTotal,
    AVG(t1.payment_value) AS valorMedio

FROM olist_order_payments_dataset AS t1
LEFT JOIN olist_orders_dataset AS t2
ON t1.order_id = t2.order_id

LEFT JOIN olist_customers_dataset AS t3
ON t2.customer_id = t3.customer_id

GROUP BY idCustomer)

SELECT 
    '2018-10-31' AS dtRef,
    t1.*,
    t2.valorTotal,
    t2.valorMedio
FROM tb_rf AS t1
LEFT JOIN tb_val AS t2
ON t1.idCustomer = t2.idCustomer