function ds = frLinear2(diff_states,diff_jacs,states)

[T,N] = size(diff_states);
K = size(diff_jacs,3);

SCALE = [1,1,1,.25,.25,.25,1,1,1,.25,.25,.25];
SIZELIM = .1; % largest value in du
SPEEDLIM = .4; % largest change betwen timesteps

cvx_begin
variable ds(K,T-2)
expr = 0;
for t = 2:T-1
    expr = expr + sum_square(diff_states(t,:)' + squeeze(diff_jacs(t,:,:)) * ds(:,t-1));
end
minimize(expr)
subject to
    abs(ds) < repmat(SIZELIM*SCALE',1,T-2);
    abs(states(:,3:end-1) + ds(:,2:end) - states(:,2:end-2) - ds(:,1:end-1)) < repmat(SPEEDLIM*SCALE',1,T-3);
    abs(states(:,2) + ds(:,1) - states(:,1)) < SPEEDLIM*SCALE'
    abs(states(:,end) - states(:,end-1) - ds(:,end)) < SPEEDLIM*SCALE'
cvx_end

end
