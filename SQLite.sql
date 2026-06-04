SELECT 
    s.sale_id,
    c.first_name || ' ' || c.last_name AS client_name,
    p.product_name,
    s.quantity_sold,
    s.total_amount,
    s.sale_date
FROM sales s
JOIN clients c ON s.client_id = c.client_id
JOIN products p ON s.product_id = p.product_id;