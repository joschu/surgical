function du = frLinear(diff_states,fwd_jacs,rev_jacs)

[T,N] = size(diff_states);
K = size(fwd_jacs,3);


cvx_begin
variable du(K,T-1)
expr = 0;
for t = 2:T-1
    expr = expr + norm(diff_states(t,:)' + squeeze(fwd_jacs(t,:,:)) * du(:,t-1) + squeeze(rev_jacs(t,:,:))*du(:,t));
end
minimize(expr);
subject to
    abs(du) <= repmat([1,1,1,.25,.25,.25,1,1,1,.25,.25,.25]'*.1,1,T-1)
    sum(du,2) == 0
cvx_end

end