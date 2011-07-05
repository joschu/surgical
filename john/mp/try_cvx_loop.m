cvx_begin
variable x(3)
expr = 0;
for i=1:4
    expr = expr + norm(x);
end
minimize(expr)
cvx_end