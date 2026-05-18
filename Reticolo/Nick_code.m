format compact
%% Fixed Parameters
n_air = 1;
%% Grating Parameters
h = 440;
d = 280;
a = 600;
surround_spacing = a * 3;
%% Dispersion Parameters
incidence_angle = linspace(0,18,25);
k_vector_ratio = incidence_angle / 90;
lam =linspace((3/2.9)*10^3,(3/2.2)*10^3,30);
%% Physical Parameters
parm=res0(-1); % For TE param=res0(1). For TM : parm=res0(-1)
parm.res1.champ=1;% the electromagnetic field is calculated accurately
nn=60;% Fourier harmonics run from [-40,40]
parm.res3.sens = 1; % Grating illuminated from top
%parm.res1.trace = 1;
%% Spacing Between
offset = 0;
transmission_disp = zeros(length(lam),length(incidence_angle));
for i = 1:length(lam)
    for j = 1:length(incidence_angle)
        % Interpolate the index values for Si
        % The textures cell must be defined inside the forloop for parallel
        % computing
        n_silicon = 3.67;
        n_sio2 = 1.45;
        % Formulate textures
        textures=cell(1,4);
        textures{1} = n_air;
        textures{2} = n_sio2;
        textures{3} = {n_sio2, [0,0, d/2, d/2,n_silicon,20]};
        textures{4} = n_sio2;
        % Now perform the simulation
        k_parallel=n_air*sind(incidence_angle(j)); % This is an important parameter
        aa=res1(lam(i),a,textures,nn,k_parallel,parm);
        profile={[surround_spacing,h,surround_spacing],[2,3,4]};
        one_D_TM=res2(aa,profile);
        transmission_disp(i,j) = sum(one_D_TM.inc_top_transmitted.efficiency);

        %x=linspace(-a/2,a/2,51);% x coordinates(z-coordinates are determined by res3.m)
        %einc=1;
        %parm.res3.trace=1; % plotting automatically
        %parm.res3.npts=[50,50,50];
        %[e,z,index]=res3(x,aa,profile,einc,parm);
        %figure;
        %pcolor(x,z,real(squeeze(e(:,:,1)))); % user plotting
        %shading flat;xlabel('x');ylabel('y');axis equal;title('Real(Ey)');
    end
end
%% Plotting Spacing Between
figure(6)
ax = gca;
ax.FontSize = 16;
hold on
imagesc(incidence_angle, lam, transmission_disp)
xlabel("$\theta$",'FontSize',16,'Interpreter', 'latex')
ylabel("Wavelength (nm)",'FontSize',16)
hold off
%figure()
%hold on
%plot(incidence_angle, transmission_disp,'linewidth',1.5,'LineStyle','-')
%xlabel("$theta$",'FontSize',16,'Interpreter', 'latex')
%ylabel("Transmission",'FontSize',16)
%title(strcat("\lambda = ",num2str(lam)," nm"),'FontSize',16)
%axis tight
%%set(gca, 'XScale', 'log')
%grid on

n_silicon = 3.67;
        n_pmma = 1.45;
        n_sio2 = 1.45;
        % Formulate textures
        textures=cell(1,4);
        textures{1} = n_air;
        textures{2} = n_sio2;
        textures{3} = {n_sio2, [0,0, d/2, d/2,n_silicon,20]};
        textures{4} = n_sio2;
        % Now perform the simulation
        k_parallel=n_air*sind(incidence_angle(j)); % This is an important parameter
        aa=res1(lam(i),a,textures,nn,k_parallel,parm);
        profile={[surround_spacing,h,surround_spacing],[2,3,4]};
        one_D_TM=res2(aa,profile);
[e,z,o]=res3(x,y,aa,profile,einc,parm)
figure(7)
retsubplot(1,4,1);retcolor(x,y,real(o(:,:,1)));xlabel('Z');ylabel('X');axis equal;title(['objet coupe Y=',num2str(y)]);