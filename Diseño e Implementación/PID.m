% PARAMETROS DEL SISTEMA
M = 0;            % El carrito no tiene masa
m = 1;            % Masa del péndulo
l = 1;            % Longitud del péndulo
g = 9.8;          % Gravedad
u = 0;            % Fuerza


% Funcion de transferencia
numtf = [m*l];                           % Numerador
dentf = [(M + m)*l^2, 0, -m*g*l];        % Denominador
G=tf(numtf, dentf);                      % Funcion de transferencia

% Controlador PID sin sintonizar
K_p = 100;     %Constante proporcional
K_i = 75;      %Constante integral
K_d = 10;       %Constante derivativa
C = pid (K_p, K_i, K_d);

% %Impresión de gráficas
T = feedback(G,C)

% Gráfica de las raíces del PID
figure(1)
rlocus(T)
title({'Raices del PID sin sintonizar'});

% Gráfica de la respuesta al impulso
figure(2)
t=0:0.01:10; % Tiempo de simulación a 10 segundos
impulse(T,t)
axis([0, 5, -0.5, 0.5]);  % Límites del gráfico
title({'Resultado respecto al Ángulo \ theta - PID: Kp=100, Ki=50, Kd=5'});