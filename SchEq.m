function SchEq

% initialise H and S matrices

N= 8;

H_matrix= zeros(N,N);
S_matrix= zeros(N,N);

for m=1:N
    
    for n=1:N
        if (mod((m+n),2)==0)
         H_matrix(m,n) = -8.0*(1.0-m-n-2*m*n) /((m+n+3)*(m+n+1)*(m+n-1));
         S_matrix(m,n) = 2.0/(n+m+5)- 4.0/(n+m+3)+2.0/(n+m+1);
        else
            H_matrix(m,n)= 0;
            S_matrix(m,n)= 0;
            
        end
    end
end

[U,s]= eig(S_matrix);

s_inv = inv(s);
s_sqroot_inv = sqrt(s_inv);

V= U*s_sqroot_inv;

H_dash = ctranspose(V)*H_matrix*V;

E = eig(H_dash)

[C_dash, Ediag] = eig(H_dash);

C = V*C_dash


end










