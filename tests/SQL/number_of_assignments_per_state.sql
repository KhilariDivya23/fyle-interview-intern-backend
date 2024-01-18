-- Write query to get number of assignments for each state
SELECT state, COUNT(state) FROM assignments GROUP BY state