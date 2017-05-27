
load('./CT_2012_03_01_LG_Chem_R3S8_45_deg_CD_CS_1_to_1_test_data.mat');

data = CT_2012_03_01_LG_Chem_R3S8_45_deg_CD_CS_1_to_1_test_data;

dt = 0.1;
capacity = 15;


% Compute SOC
soc = zeros(1, length(data.u(:,1)));
soc(1) = 0.5;
for i = 2:length(soc)
    soc(i) = soc(i-1) + (-data.u(i)/3600/capacity) * dt;
end

plot(soc)
