% PARAMETROS DEL SISTEMA
M = 0;            % El carrito no tiene masa
m = 1;            % Masa del péndulo
l = 1;            % Longitud del péndulo
g = 9.8;          % Gravedad
u = 0;            % Fuerza

% FUNCION DE TRANSFERENCIA
numtf = [m*l];                           % Numerador
dentf = [(M + m)*l^2, 0, -m*g*l];        % Denominador
G=tf(numtf, dentf);                      % Funcion de transferencia

% CONTROLADOR PID SIN SINTONIZAR
K_p = 100;     %Constante proporcional
K_i = 75;      %Constante integral
K_d = 10;       %Constante derivativa
C_no_sintonizado= pid (K_p, K_i, K_d);

%------------------------------------------------------------------------------------------------------%

% IMPRESION DE GRAFICAS
T_no_sintonizado= feedback(G,C_no_sintonizado)

% GRAFICA DE LAS RAICES DEL PID
figure(1)
rlocus(T_no_sintonizado)
title({'Raices del PID sin sintonizar'});

% GRAFICA DE LA RESPUESTA AL IMPULSO
figure(2)
t=0:0.01:5; % Tiempo de simulación a 10 segundos
impulse(T_no_sintonizado,t)
axis([0, 2, -0.2, 0.2]);  % Límites del gráfico
title({'Resultado respecto al Ángulo \theta'});

%------------------------------------------------------------------------------------------------------%

pidTuner (G, C_no_sintonizado);           %PIDTUNER SINTONIZA AUTOMATICAMENTE LAS CONSTANTES(K_d, K_i, K_d) DEL PID 

% CONTROLADOR PID SINTONIZADO
K_p = 256.7083;
K_i = 495.8264;
K_d = 33.2269;
C_sintonizado = pid (K_p, K_i, K_d);

% IMPRESION DE GRAFICAS
T_sintonizado= feedback(G,C_sintonizado);

% GRAFICA DE LAS RAICES DEL PID
figure(3)
rlocus(T_sintonizado)
title({'Lugar geometrico de las raices PID sintonizado'});

% GRAFICA DE LA RESPUESTA AL IMPULSO
figure(4)
t=0:0.01:5; % Tiempo de simulación a 10 segundos
impulse(T_sintonizado,t)
axis([0, 2, -0.2, 0.2]);  % Límites del gráfico
title({'Respuesta péndulo mejorado respecto al Ángulo \theta'});

%------------------------------------------------------------------------------------------------------%

% GRAFICA DE COMPARACION DE LA RESPUESTA DEL IMPULSO
figure(5);
impulse(T_no_sintonizado, 'b', T_sintonizado, 'r');
legend('PID no sintonizado', 'PID sintonizado');
title('Comparación de respuestas al impulso');


