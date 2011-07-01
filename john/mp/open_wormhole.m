consts
unspace = @(s) s(s ~= ' ');
conn = tcpip('localhost',TCP_PORT,'timeout',inf,'OutputBufferSize',L_BUFFER,'InputBufferSize',L_BUFFER);
fopen(conn)
disp('waiting for connection')

while true
    disp 'waiting for message'
    cmd_class = unspace(char(fread(conn,L_CMD))');
    fprintf('cmd class: %s\n',cmd_class)
    if strcmp(cmd_class,'put')
        name = unspace(char(fread(conn,L_NAME))');
        fprintf('name: %s\n',name);
        shape_str = char(fread(conn,L_SHAPE))';
        shape = eval(shape_str);
        targ = zeros(shape);
        n_floats = prod(shape);
        n_read = 0;
        while n_read < n_floats
            n_toread = min(L_BUFFER/8,n_floats-n_read);
            targ(n_read+1:n_read+n_toread) = fread(conn,n_toread,'double');
            n_read = n_read + n_toread;
%             fprintf('%i/%i bytes read\n',n_read,n_floats);
        end
        eval(sprintf('%s = targ;',name))
    elseif strcmp(cmd_class,'exec')
        stmt = char(fread(conn,L_STMT))';
        eval(stmt)
        pause(.1) % to allow for plotting
    elseif strcmp(cmd_class,'get')
        name = unspace(char(fread(conn,L_NAME))');
        fprintf('getting %s\n',name)
        eval(sprintf('src = %s;',name))
        fwrite(conn,sprintf('%30s',num2str(size(src))))
        n_floats = numel(src);        
        n_sent = 0;
        while n_sent < n_floats
            n_tosend = min(L_BUFFER/8,n_floats-n_sent);
            fwrite(conn,src(n_sent+1:n_sent+n_tosend),'double')
            n_sent = n_sent + n_tosend;
%             fprintf('%i/%i floats sent\n',n_sent,n_floats);
        end
    else error('unrecognized message')
    end
        
    
end
