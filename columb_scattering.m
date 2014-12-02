% Program to find the total scattering cross section
clc;
clear all;
%m =1.6e-27;    %mass
m=1;
velocity = 1;
 E = 0.5*m*velocity^2;   %Energy
% e= 1.6e-19;
% k= -(9e9)*e^2;
% alpha = -k/(2*E);

alpha =1;
k=-1;
count =1;
for s = 0:0.01:1
    
    l = sqrt(2*m*E)*s;
    
    r_m = alpha + sqrt( alpha^2 + s^2);
        u_m = r_m^-1;
    
%    
   f = @(x) s/( 1 + x.*(k/E)  -x.^2.*s^2 ).^0.5;
     %syms y;
     %mysol =  @(y) E*(1 - s^2.*y.^-2) -alpha*exp(-k.*y); 
  
    % choose only real elements...
%      r = fsolve(@(y)E*(1 - s^2.*y.^-2) -alpha*exp(-k.*y),5);
%     sel = r == real(r);
%     r_reals =r( sel );
%     
%     %Choosing non-negative no..
%     
%     sol = max(r);
%     
%     u_m = 1/sol;
    
   % f = @(x) s/( 1 - (alpha/E)*exp(-k./x)  -x.^2.*s^2 ).^0.5;
    
     n=100;
    


   [point,W] = lgwt(n,0,u_m);  %Finding the weights and points for quadrature
   
   sum = 0;
   
   for i=1:length(W)
       sum = sum + W(i)*f(point(i));   %Gauss Quadrature integration
   end
   
    theta(count) = pi- 2*sum;
  
    count = count+1;
end


s= 0:0.01:1;
a = length(s);
p = polyfit(theta,s,2);
inverse_fun = polyfit(theta,s,15);
fun_der  = polyder(inverse_fun);


sigma_new = abs(polyval(fun_der,theta)).*s./sin(theta);


plot(s,theta);
grid on;
        xlabel('s ','FontWeight','bold');
        ylabel('theta ','FontWeight','bold');
        title('Theta Vs. s ','FontWeight','bold');
figure;

plot(polyval(inverse_fun,theta),theta);
grid on;
figure;

% plot(s,sigma_new);
% grid on;
%       xlabel('s','FontWeight','bold');
%       ylabel('sigma ','FontWeight','bold');
%       title('Scattering cross sectionl Vs. s ','FontWeight','bold');
% hold on;


sigma_th = (k/(4*E))^2*sin(theta./2).^-4;


plot(s,sigma_th,'r',s,sigma_new,'b');
grid on;
        legend('Theoretical','Numerical');
        xlabel('s','FontWeight','bold');
        ylabel('sigma ','FontWeight','bold');
        title('Scattering cross sectionl Vs. s ','FontWeight','bold');



